import subprocess
import sys
from io import StringIO

import pytest

from ghost_basic.errors import BasicError
from ghost_basic.program import Program
from ghost_basic.runtime import Runtime
from ghost_basic.shell import Shell


def execute(source, inputs="", limit=10000):
    out = StringIO()
    runtime = Runtime(output=out, input_stream=StringIO(inputs), max_steps=limit)
    runtime.run(Program.from_source(source))
    return out.getvalue(), runtime


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("2+3*4", "14"),
        ("-2^2", "-4"),
        ("2^3^2", "64"),
        ("7\\2", "3"),
        ("-7 MOD 3", "-1"),
        ("NOT 1=1", "0"),
        ("1<2", "-1"),
        ('LEN("abc")', "3"),
        ('MID$("abcd",2,2)', "bc"),
        ('"a"+"b"', "ab"),
        ("INT(-1.2)", "-2"),
        ("FIX(-1.2)", "-1"),
        ("&HFF", "255"),
        ("ABS(-4)", "4"),
        ("1 OR 2 AND 4", "1"),
    ],
)
def test_expressions(expression, expected):
    output, _ = execute(f"10 PRINT {expression}")
    assert output.strip() == expected


def test_loop_subroutine_and_inline_if():
    output, runtime = execute("""10 S=0
20 FOR I=1 TO 3
30 GOSUB 100
40 NEXT I
50 IF S=6 THEN PRINT "yes": PRINT S ELSE PRINT "no"
60 END
100 S=S+I: RETURN""")
    assert output == "yes\n 6 \n"
    assert runtime.variables["S"].data == 6


def test_if_false_skips_whole_then_branch():
    assert execute('10 IF 0 THEN PRINT "bad": PRINT "bad" ELSE PRINT "ok"')[0] == "ok\n"


def test_descending_and_empty_loops():
    assert execute("10 FOR I=3 TO 1 STEP -1: PRINT I;: NEXT I")[0] == " 3  2  1 "
    assert execute('10 FOR I=2 TO 1: PRINT "bad": NEXT I\n20 PRINT "ok"')[0] == "ok\n"


def test_nested_for_and_while():
    out, _ = execute("""10 FOR I=1 TO 2
20 FOR J=1 TO 2
30 PRINT I*J;
40 NEXT J: NEXT I
50 A=0
60 WHILE A<2
70 A=A+1
80 WEND
90 PRINT A""")
    assert out == " 1  2  2  4  2 \n"


def test_arrays_and_data_restore():
    out, _ = execute("""10 DIM A(2)
20 DATA 5,6,"hi"
30 READ A(0),A(2),S$
40 PRINT A(0)+A(2);S$
50 RESTORE
60 READ X
70 PRINT X""")
    assert out == " 11 hi\n 5 \n"


def test_input_and_suffixes():
    out, runtime = execute('10 INPUT "Name";N$\n20 INPUT A%\n30 PRINT N$;A%', "Ada\n2.6\n")
    assert out == "Name? ? Ada 3 \n"
    assert runtime.variables["A%"].data == 3


@pytest.mark.parametrize(
    "source, message",
    [
        ("10 PRINT 1/0", "Division by zero"),
        ("10 A$=1", "Type mismatch"),
        ("10 GOTO 99", "Undefined line"),
        ("10 RETURN", "RETURN without GOSUB"),
        ("10 NEXT", "NEXT without FOR"),
        ("10 READ A", "Out of DATA"),
        ("10 A%=40000", "Overflow"),
        ("10 DIM A(1): PRINT A(2)", "Subscript out of range"),
        ('10 PRINT "unterminated', "Syntax error"),
        ("10 PRINT 1 2", "Syntax error"),
    ],
)
def test_basic_errors(source, message):
    with pytest.raises(BasicError, match=message):
        execute(source)


def test_execution_budget():
    with pytest.raises(BasicError, match="Execution limit"):
        execute("10 GOTO 10", limit=20)


def test_program_editing():
    program = Program()
    program.edit('20 PRINT "b"')
    program.edit('10 PRINT "a"')
    program.edit('20 PRINT "c"')
    assert program.listing() == '10 PRINT "a"\n20 PRINT "c"\n'
    program.edit("10")
    assert program.listing() == '20 PRINT "c"\n'


def test_shell_persistence_and_run_reset(tmp_path):
    output = StringIO()
    shell = Shell(root=tmp_path, output=output, input_stream=StringIO())
    for command in ["10 A=A+1: PRINT A", 'SAVE "test.bas"', "NEW", 'LOAD "test.bas"', "RUN", "RUN"]:
        shell.submit(command)
    assert output.getvalue() == " 1 \n 1 \n"
    assert (tmp_path / "test.bas").read_text() == "10 A=A+1: PRINT A\n"


def test_disk_confinement(tmp_path):
    shell = Shell(root=tmp_path, output=StringIO())
    with pytest.raises(BasicError, match="Permission denied"):
        shell.submit('SAVE "../escape.bas"')
    outside = tmp_path.parent / "outside.bas"
    outside.write_text("10 END")
    (tmp_path / "link.bas").symlink_to(outside)
    with pytest.raises(BasicError, match="Permission denied"):
        shell.submit('LOAD "link.bas"')


def test_cli(tmp_path):
    path = tmp_path / "hello.bas"
    path.write_text('10 PRINT "Hello"\n')
    result = subprocess.run(
        [sys.executable, "-m", "ghost_basic", str(path)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == "Hello\n"


def test_step_api():
    runtime = Runtime(output=StringIO())
    runtime.prepare(Program.from_source("10 A=1\n20 A=A+1\n30 END"))
    assert runtime.step()
    assert runtime.variables["A"].data == 1
    assert runtime.instructions[runtime.pc].line == 20
    assert runtime.step()
    assert runtime.variables["A"].data == 2


@pytest.mark.parametrize(
    "source, expected",
    [
        ("10 PRINT 8/2*3", " 12 \n"),
        ("10 PRINT 10 MOD -3", " 1 \n"),
        ("10 PRINT 5.6\\2", " 3 \n"),
        ("10 PRINT NOT 0;1 EQV 1;0 IMP 0", "-1 -1 -1 \n"),
        ('10 PRINT "a:b";"c"', "a:bc\n"),
        ('10 PRINT "ok": REM " ignored : PRINT "bad"', "ok\n"),
        ('10 PRINT "ok" \' comment', "ok\n"),
        ('10 IF 1 THEN 30 ELSE 20\n20 PRINT "bad": END\n30 PRINT "ok"', "ok\n"),
        ('10 IF 1 THEN IF 0 THEN PRINT "bad" ELSE PRINT "ok"', "ok\n"),
        ("10 PRINT UNKNOWN;UNKNOWN$", " 0 \n"),
        ('10 PRINT CHR$(65);LEFT$("ABC",2);RIGHT$("ABC",0)', "AAB\n"),
        ("10 PRINT SPACE$(2);STRING$(3,65)", "  AAA\n"),
        ("10 DATA 1\n20 DATA 2\n30 RESTORE 20\n40 READ A\n50 PRINT A", " 2 \n"),
        ("10 FOR I=1 TO 2: FOR J=1 TO 2: PRINT I*J;: NEXT J,I", " 1  2  2  4 "),
        ('10 WHILE 0: PRINT "bad": WEND\n20 PRINT "ok"', "ok\n"),
        ("10 A(10)=3: PRINT A(10)", " 3 \n"),
        ('10 DIM A$(2,3): A$(1,2)="yes": PRINT A$(1,2)', "yes\n"),
    ],
)
def test_semantic_regressions(source, expected):
    assert execute(source)[0] == expected


@pytest.mark.parametrize(
    "source, message",
    [
        ("10 FOR I=1 TO 3", "FOR without NEXT"),
        ("10 WHILE 1", "WHILE without WEND"),
        ("10 WEND", "WEND without WHILE"),
        ("10 FOR I=1 TO 2 STEP 0: NEXT", "Illegal function call"),
        ("10 DIM A(2): DIM A(2)", "Duplicate definition"),
        ("10 DIM A(32767,32767)", "Out of memory"),
        ("10 PRINT SQR(-1)", "Illegal function call"),
        ("10 PRINT LEN(1)", "Type mismatch"),
        ('10 PRINT LEFT$("abc",-1)', "Illegal function call"),
        ("10 PRINT 2^10000", "Overflow"),
        ("10 PRINT 1 MOD 0", "Division by zero"),
        ("10 DATA 1+2", "Syntax error"),
    ],
)
def test_additional_errors(source, message):
    with pytest.raises(BasicError, match=message):
        execute(source)


def test_failed_load_does_not_destroy_program(tmp_path):
    shell = Shell(root=tmp_path, output=StringIO())
    shell.submit('10 PRINT "safe"')
    (tmp_path / "bad.bas").write_text("this is not numbered BASIC")
    with pytest.raises(BasicError):
        shell.submit('LOAD "bad.bas"')
    assert shell.program.listing() == '10 PRINT "safe"\n'


def test_immediate_variable_state():
    out = StringIO()
    shell = Shell(output=out)
    shell.submit("A=7")
    shell.submit("PRINT A")
    assert out.getvalue() == " 7 \n"


def test_program_error_has_line():
    with pytest.raises(BasicError) as caught:
        execute("10 A=1\n90 PRINT 1/0")
    assert str(caught.value) == "Division by zero in 90"


def test_oversized_hex_literal_is_basic_error():
    with pytest.raises(BasicError, match="Overflow"):
        execute("10 PRINT &H" + "F" * 10000)


def test_prompt_session():
    result = subprocess.run(
        [sys.executable, "-m", "ghost_basic"],
        input='10 PRINT "prompt works"\nRUN\nSYSTEM\n',
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "prompt works" in result.stdout
    assert "Traceback" not in result.stderr


def test_cli_error_exit(tmp_path):
    path = tmp_path / "broken.bas"
    path.write_text("10 PRINT 1/0")
    result = subprocess.run(
        [sys.executable, "-m", "ghost_basic", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert result.stderr.strip() == "Division by zero in 10"


@pytest.mark.parametrize(
    "name, args, expected",
    [
        ("ABS", "-3", "3"),
        ("SGN", "-3", "-1"),
        ("SQR", "9", "3"),
        ("SIN", "0", "0"),
        ("COS", "0", "1"),
        ("TAN", "0", "0"),
        ("ATN", "0", "0"),
        ("LOG", "1", "0"),
        ("EXP", "0", "1"),
        ("CINT", "2.5", "2"),
        ("CSNG", "2", "2"),
        ("CDBL", "2", "2"),
        ("ASC", '"A"', "65"),
        ("VAL", '" -12.5tail"', "-12.5"),
        ("STR$", "12", "12"),
        ("LEFT$", '"ABC",2', "AB"),
        ("RIGHT$", '"ABC",2', "BC"),
        ("MID$", '"ABC",2', "BC"),
        ("STRING$", '3,"x"', "xxx"),
    ],
)
def test_intrinsic_inventory(name, args, expected):
    assert execute(f"10 PRINT {name}({args})")[0].strip() == expected


def test_array_budget_is_cumulative():
    runtime = Runtime(max_cells=5, output=StringIO())
    with pytest.raises(BasicError, match="Out of memory"):
        runtime.run(Program.from_source("10 DIM A(2),B(2)"))


def test_load_source_limit(tmp_path):
    shell = Shell(root=tmp_path, output=StringIO())
    (tmp_path / "big.bas").write_text(" " * 1_000_001)
    with pytest.raises(BasicError, match="Program too large"):
        shell.submit('LOAD "big.bas"')


def test_oversized_line_number_is_basic_error():
    with pytest.raises(BasicError, match="Illegal function call"):
        Program.from_source("9" * 5000 + " PRINT 1")


def test_cyclic_symlink_is_file_error(tmp_path):
    (tmp_path / "a.bas").symlink_to(tmp_path / "b.bas")
    (tmp_path / "b.bas").symlink_to(tmp_path / "a.bas")
    shell = Shell(root=tmp_path, output=StringIO())
    with pytest.raises(BasicError, match="File error"):
        shell.submit('LOAD "a.bas"')


def test_deep_expression_is_basic_error():
    with pytest.raises(BasicError, match="Expression too complex"):
        execute("10 PRINT " + "(" * 2000 + "1" + ")" * 2000)


def test_literal_string_limit():
    with pytest.raises(BasicError, match="String too long"):
        execute('10 PRINT "' + "x" * 32768 + '"')


def test_shell_variable_with_command_prefix():
    output = StringIO()
    shell = Shell(output=output)
    shell.submit("SAVER=12")
    shell.submit("LOADER=3")
    shell.submit("PRINT SAVER+LOADER")
    assert output.getvalue() == " 15 \n"
