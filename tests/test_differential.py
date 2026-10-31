"""Exercise the comparison harness using real small subprocesses."""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parents[1] / "tools" / "differential.py"


def runner():
    assert TOOL.exists(), "The differential runner has not been implemented"
    spec = importlib.util.spec_from_file_location("differential", TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def command(code):
    return [sys.executable, "-c", code, "{program}"]


def test_comparison_preserves_spaces_and_normalizes_newlines():
    tool = runner()
    a = tool.run(command("print(' A ')"), "10 END", "", 2)
    b = tool.run(command("import sys; sys.stdout.buffer.write(b' A \\r\\n')"), "10 END", "", 2)
    assert tool.matches(a, b)
    c = tool.run(command("print('A')"), "10 END", "", 2)
    assert not tool.matches(a, c)


def test_input_source_and_isolated_working_directories():
    tool = runner()
    cmd = command(
        "import pathlib,sys; p=pathlib.Path(sys.argv[1]); "
        "assert p.name == 'program.bas'; assert p.read_text() == '10 END'; "
        "assert not pathlib.Path('marker').exists(); "
        "pathlib.Path('marker').touch(); print(sys.stdin.read(), end='')"
    )
    for _ in range(2):
        result = tool.run(cmd, "10 END", "Ada\n", 2)
        assert result == {"stdout": "Ada\n", "stderr": "", "returncode": 0, "error": None}


def test_failures_and_timeouts_never_match():
    tool = runner()
    bad = tool.run(command("raise SystemExit(1)"), "", "", 2)
    assert not tool.matches(bad, bad)
    timeout = tool.run(command("import time; time.sleep(5)"), "", "", 0.05)
    assert timeout["error"] == "timeout"
    assert not tool.matches(timeout, timeout)
    missing = tool.run(["/nonexistent/ghost-reference", "{program}"], "", "", 1)
    assert missing["error"]
    assert not tool.matches(missing, missing)


@pytest.mark.parametrize("value", ['"program"', "[]", "[1]", '["python"]'])
def test_invalid_reference_commands(value):
    with pytest.raises(ValueError):
        runner().parse_command(value)


def test_command_parsing_preserves_spaces():
    cmd = ["/path with spaces/reference", "--run", "{program}"]
    assert runner().parse_command(json.dumps(cmd)) == cmd


def test_unconfigured_reference_is_explicit_skip(monkeypatch, capsys):
    monkeypatch.delenv("GHOST_BASIC_REFERENCE_COMMAND", raising=False)
    assert runner().main([]) == 0
    assert "SKIP" in capsys.readouterr().out


def test_corpus_runs_against_ghost_basic():
    tool = runner()
    cases = json.loads(tool.CORPUS.read_text())
    assert len({case["id"] for case in cases}) == len(cases) > 0
    for case in cases:
        result = tool.run(
            [sys.executable, "-m", "ghost_basic", "{program}"], case["source"], case["inputs"], 5
        )
        assert result == {"stdout": case["output"], "stderr": "", "returncode": 0, "error": None}, (
            case["id"]
        )


def test_main_reports_real_mismatch_and_bad_configuration(capsys):
    tool = runner()
    assert tool.main(["--reference", json.dumps(command("print('wrong')"))]) == 1
    assert "FAIL: print-spacing" in capsys.readouterr().out
    with pytest.raises(SystemExit) as error:
        tool.main(["--reference", "invalid json"])
    assert error.value.code == 2


def test_required_reference_and_timeout_validation(monkeypatch):
    monkeypatch.delenv("GHOST_BASIC_REFERENCE_COMMAND", raising=False)
    tool = runner()
    assert tool.main(["--require-reference"]) == 2
    for value in ("0", "-1", "nan", "inf"):
        with pytest.raises(SystemExit):
            tool.main(["--timeout", value])


def test_optional_licensed_reference():
    import os

    configured = os.getenv("GHOST_BASIC_REFERENCE_COMMAND")
    if not configured:
        pytest.skip("No separately installed licensed reference runtime configured")
    assert runner().main(["--reference", configured, "--require-reference"]) == 0
