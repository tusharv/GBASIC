import subprocess
import sys


def test_explicit_shell_works_with_pipes():
    result = subprocess.run(
        [sys.executable, "-m", "ghost_basic", "--shell"],
        input='PRINT "classic"\nSYSTEM\n',
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "classic" in result.stdout


def test_forced_ide_requires_terminal():
    result = subprocess.run(
        [sys.executable, "-m", "ghost_basic", "--ide"],
        input="",
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 2
    assert "requires an interactive terminal" in result.stderr


def test_mode_flags_are_mutually_exclusive():
    result = subprocess.run(
        [sys.executable, "-m", "ghost_basic", "--ide", "--shell"],
        input="",
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 2


def test_no_splash_option_is_accepted():
    result = subprocess.run(
        [sys.executable, "-m", "ghost_basic", "--shell", "--no-splash"],
        input='PRINT "ready"\nSYSTEM\n',
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "ready" in result.stdout
    assert "Press any key" not in result.stdout


def test_keyword_help_from_terminal():
    result = subprocess.run(
        [sys.executable, "-m", "ghost_basic", "--help-keyword", "PRINT"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "Parameters" in result.stdout and "Examples" in result.stdout
    result = subprocess.run(
        [sys.executable, "-m", "ghost_basic", "--help-keyword", "badkeyword"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "No matching help" in result.stderr
