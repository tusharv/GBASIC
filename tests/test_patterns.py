from io import StringIO
from pathlib import Path

import pytest

from ghost_basic import Program, Runtime
from ghost_basic.devices import Disk

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


@pytest.mark.parametrize(
    "name, expected",
    [
        ("triangle_01_left", "*\n**\n***\n****\n*****\n"),
        ("triangle_02_inverted", "*****\n****\n***\n**\n*\n"),
        ("triangle_03_right", "    *\n   **\n  ***\n ****\n*****\n"),
        ("triangle_04_pyramid", "    *\n   ***\n  *****\n *******\n*********\n"),
        ("triangle_05_inverted_pyramid", "*********\n *******\n  *****\n   ***\n    *\n"),
        ("triangle_06_hollow", "*\n**\n* *\n*  *\n*****\n"),
        ("triangle_07_numbers", "1\n12\n123\n1234\n12345\n"),
        ("triangle_08_floyd", "1 \n2 3 \n4 5 6 \n7 8 9 10 \n11 12 13 14 15 \n"),
        ("triangle_09_pascal", "    1 \n   1 1 \n  1 2 1 \n 1 3 3 1 \n1 4 6 4 1 \n"),
        (
            "triangle_10_diamond",
            "    *\n   ***\n  *****\n *******\n*********\n *******\n  *****\n   ***\n    *\n",
        ),
        ("logic_sum", "Sum = 55 \n"),
        ("logic_factorial", "5! = 120 \n"),
        ("logic_prime", "Prime\n"),
    ],
)
def test_learning_programs(name, expected):
    output = StringIO()
    runtime = Runtime(output=output, max_steps=10000)
    runtime.run(Program.from_source((EXAMPLES / f"{name}.bas").read_text()))
    assert output.getvalue() == expected
    assert f"examples/{name}.bas" in Disk(EXAMPLES.parent).example_programs()


@pytest.mark.parametrize(
    "name, expected",
    [
        ("triangle_01_left", "*\n"),
        ("triangle_02_inverted", "*\n"),
        ("triangle_03_right", "*\n"),
        ("triangle_04_pyramid", "*\n"),
        ("triangle_05_inverted_pyramid", "*\n"),
        ("triangle_06_hollow", "*\n"),
        ("triangle_07_numbers", "1\n"),
        ("triangle_08_floyd", "1 \n"),
        ("triangle_09_pascal", "1 \n"),
        ("triangle_10_diamond", "*\n"),
    ],
)
def test_single_row_patterns(name, expected):
    source = (EXAMPLES / f"{name}.bas").read_text().replace("N=5", "N=1")
    out = StringIO()
    Runtime(output=out).run(Program.from_source(source))
    assert out.getvalue() == expected


@pytest.mark.parametrize(
    "number, expected", [(1, "Not prime\n"), (2, "Prime\n"), (9, "Not prime\n")]
)
def test_prime_boundaries(number, expected):
    source = (EXAMPLES / "logic_prime.bas").read_text().replace("N=29", f"N={number}")
    out = StringIO()
    Runtime(output=out).run(Program.from_source(source))
    assert out.getvalue() == expected
