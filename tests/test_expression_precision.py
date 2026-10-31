from io import StringIO
from pathlib import Path

import pytest

from ghost_basic.errors import BasicError
from ghost_basic.evaluator import evaluate
from ghost_basic.parser import Parser
from ghost_basic.program import Program
from ghost_basic.runtime import Runtime
from ghost_basic.values import Kind


def value(source):
    return evaluate(Parser(source).expression(), lambda ref: pytest.fail("Unexpected variable"))


@pytest.mark.parametrize(
    "source, kind, expected",
    [
        ("2+3", Kind.INTEGER, 5),
        ("2-3", Kind.INTEGER, -1),
        ("2*3", Kind.INTEGER, 6),
        ("32767+1", Kind.SINGLE, 32768),
        ("&H8000-1", Kind.SINGLE, -32769),
        ("300*300", Kind.SINGLE, 90000),
        ("1!+2", Kind.SINGLE, 3),
        ("1+2!", Kind.SINGLE, 3),
        ("3!-1", Kind.SINGLE, 2),
        ("3!*2", Kind.SINGLE, 6),
        ("1!+2#", Kind.DOUBLE, 3),
        ("1#+2!", Kind.DOUBLE, 3),
        ("3#-1!", Kind.DOUBLE, 2),
        ("3!*2#", Kind.DOUBLE, 6),
        ("1/2", Kind.SINGLE, 0.5),
        ("1!/2", Kind.SINGLE, 0.5),
        ("1/2#", Kind.DOUBLE, 0.5),
        ("1#/2!", Kind.DOUBLE, 0.5),
        ("(16777216!+1!)-16777216!", Kind.SINGLE, 0),
        ("(16777216#+1!)-16777216!", Kind.DOUBLE, 1),
        ("ABS(-2!)", Kind.SINGLE, 2),
        ("ABS(&H8000)", Kind.SINGLE, 32768),
        ("INT(-1.5!)", Kind.SINGLE, -2),
        ("FIX(-1.5!)", Kind.SINGLE, -1),
        ("ABS(-2%)", Kind.INTEGER, 2),
        ("INT(2%)", Kind.INTEGER, 2),
        ("FIX(2%)", Kind.INTEGER, 2),
        ("INT(2.5#)", Kind.DOUBLE, 2),
    ],
)
def test_expression_result_precision(source, kind, expected):
    result = value(source)
    assert result.kind == kind
    assert result.number() == expected


def test_double_assignment_does_not_restore_single_precision():
    output = StringIO()
    Runtime(output=output).run(
        Program.from_source(
            "10 A#=(16777216!+1!)-16777216!\n20 PRINT A#\n"
            "30 B#=(16777216#+1!)-16777216!\n40 PRINT B#"
        )
    )
    assert output.getvalue() == " 0 \n 1 \n"


@pytest.mark.parametrize(
    "source, message",
    [
        ("1!/0", "Division by zero"),
        ("3E38*2!", "Overflow"),
        ('"text"+1', "Type mismatch"),
        ('1+"text"', "Type mismatch"),
    ],
)
def test_arithmetic_errors_remain_basic_errors(source, message):
    with pytest.raises(BasicError, match=message):
        value(source)


@pytest.mark.parametrize(
    "name, expected",
    [
        ("numeric_literals", "Hex: -1 \nOctal: -1 \nShort octal: -1 \nMask:  255 \n"),
        (
            "numeric_precision",
            "Single intermediate:  0 \nDouble intermediate:  1 \nLiteral rounded before CDBL\n",
        ),
        (
            "numeric_integers",
            "Promoted sum:  32768 \nPromoted product:  90000 \nDivision:  2.5 \nINT: -2 \nFIX: -1 \n",
        ),
    ],
)
def test_numeric_gallery(name, expected):
    path = Path(__file__).resolve().parents[1] / "examples" / f"{name}.bas"
    assert path.exists(), "New numeric example is missing"
    output = StringIO()
    Runtime(output=output).run(Program.from_source(path.read_text()))
    assert output.getvalue() == expected
