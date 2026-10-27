from io import StringIO
from pathlib import Path

import pytest

from ghost_basic import Program, Runtime

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


@pytest.mark.parametrize(
    "name, inputs, expected",
    [
        ("hello", "", "Hello from Ghost BASIC!\n"),
        ("fibonacci", "", " 0  1  1  2  3  5  8  13  21  34 \n"),
        ("subroutines", "", "odd\neven\nodd\n"),
        ("data", "", "Ada:  10 \nGrace:  20 \nAlan:  30 \nFirst: Ada\n"),
        ("input", "Ada\n30\n", "Your name? Your age? Hello Ada, next year:  31 \n"),
        ("while", "", "5! = 120 \n"),
        ("types", "", " 3  1.25  10000000000 BASIC\nASI!\n-1 -2 -1 \n"),
    ],
)
def test_gallery(name, inputs, expected):
    output = StringIO()
    Runtime(output=output, input_stream=StringIO(inputs)).run(
        Program.from_source((EXAMPLES / f"{name}.bas").read_text())
    )
    assert output.getvalue() == expected
