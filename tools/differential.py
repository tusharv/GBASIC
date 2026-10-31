"""Opt-in black-box compatibility runner; no reference runtime is bundled."""

import argparse
import json
import math
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TypedDict

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "tests" / "compatibility" / "cases.json"


class Result(TypedDict):
    stdout: str
    stderr: str
    returncode: int | None
    error: str | None


def parse_command(value: str) -> list[str]:
    command = json.loads(value)
    if (
        not isinstance(command, list)
        or not command
        or not all(isinstance(arg, str) and arg and "\0" not in arg for arg in command)
        or not any("{program}" in arg for arg in command)
    ):
        raise ValueError("command must be a JSON string array containing {program}")
    return command


def run(command: list[str], source: str, inputs: str, timeout: float) -> Result:
    """Run a trusted adapter in a fresh workspace; preserve all output spacing."""
    with TemporaryDirectory(prefix="ghost differential ") as directory:
        program = Path(directory) / "program.bas"
        program.write_text(source, encoding="ascii")
        argv = [arg.replace("{program}", str(program)) for arg in command]
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "src")
        try:
            process = subprocess.run(
                argv,
                input=inputs,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="strict",
                cwd=directory,
                env=env,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return Result(stdout="", stderr="", returncode=None, error="timeout")
        except (OSError, UnicodeError) as error:
            return Result(stdout="", stderr="", returncode=None, error=str(error))
        return Result(
            stdout=process.stdout, stderr=process.stderr, returncode=process.returncode, error=None
        )


def matches(left: Result, right: Result) -> bool:
    return (
        left["error"] is None
        and right["error"] is None
        and left["returncode"] == right["returncode"] == 0
        and left["stdout"] == right["stdout"]
        and left["stderr"] == right["stderr"]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reference",
        default=os.getenv("GHOST_BASIC_REFERENCE_COMMAND"),
        help="JSON argv for a trusted reference adapter, with {program}",
    )
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--require-reference", action="store_true")
    args = parser.parse_args(argv)
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("--timeout must be finite and positive")
    if not args.reference:
        print("SKIP: no reference runtime configured (GHOST_BASIC_REFERENCE_COMMAND)")
        return 2 if args.require_reference else 0
    try:
        reference = parse_command(args.reference)
    except ValueError as error:
        parser.error(str(error))
    ghost = [sys.executable, "-m", "ghost_basic", "{program}"]
    failures = 0
    for case in json.loads(CORPUS.read_text(encoding="utf-8")):
        actual = run(ghost, case["source"], case["inputs"], args.timeout)
        expected = run(reference, case["source"], case["inputs"], args.timeout)
        passed = matches(actual, expected)
        failures += not passed
        print(f"{'PASS' if passed else 'FAIL'}: {case['id']}")
        if not passed:
            print(json.dumps({"ghost": actual, "reference": expected}, ensure_ascii=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
