"""Literal behavior specified independently of the parser's conversion code."""

from io import StringIO

import pytest

from ghost_basic.errors import BasicError
from ghost_basic.evaluator import evaluate
from ghost_basic.parser import Parser
from ghost_basic.program import Program
from ghost_basic.runtime import Runtime
from ghost_basic.values import Kind


def value(source):
    parser = Parser(source)
    expr = parser.expression()
    assert parser.current.kind == "EOF"
    return evaluate(expr, lambda ref: pytest.fail("Unexpected variable"))


@pytest.mark.parametrize(
    "source, kind, expected",
    [
        ("0", Kind.INTEGER, 0),
        ("32767", Kind.INTEGER, 32767),
        ("32768", Kind.SINGLE, 32768),
        ("000000001", Kind.INTEGER, 1),
        ("1.5", Kind.SINGLE, 1.5),
        ("1234567.", Kind.SINGLE, 1234567),
        ("12345678", Kind.DOUBLE, 12345678),
        ("0.000000125", Kind.SINGLE, 0.000000125),
        ("1E0", Kind.SINGLE, 1),
        ("1D0", Kind.DOUBLE, 1),
        ("1!", Kind.SINGLE, 1),
        ("1#", Kind.DOUBLE, 1),
        ("1%", Kind.INTEGER, 1),
        ("12345678!", Kind.SINGLE, 12345678),
        ("&H7FFF", Kind.INTEGER, 32767),
        ("&H8000", Kind.INTEGER, -32768),
        ("&HFFFF", Kind.INTEGER, -1),
        ("&O177777", Kind.INTEGER, -1),
        ("&177777", Kind.INTEGER, -1),
        ("&hffff", Kind.INTEGER, -1),
        ("&o100000", Kind.INTEGER, -32768),
        ("&0", Kind.INTEGER, 0),
        ("-1!", Kind.SINGLE, -1),
        ("+1!", Kind.SINGLE, 1),
        ("-1%", Kind.INTEGER, -1),
        ("-&H8000", Kind.SINGLE, 32768),
    ],
)
def test_literal_classification_and_value(source, kind, expected):
    result = value(source)
    assert result.kind == kind
    assert result.number() == pytest.approx(expected)


@pytest.mark.parametrize(
    "source", ["&H10000", "&O200000", "&200000", "&H" + "F" * 5000, "1E9999", "32768%"]
)
def test_literal_overflow_is_basic_error(source):
    with pytest.raises(BasicError, match="Overflow"):
        value(source)


@pytest.mark.parametrize("source", ["&H", "&O", "&", "&8", "&O8"])
def test_incomplete_or_invalid_radix_is_basic_error(source):
    with pytest.raises(BasicError):
        value(source)


def test_radix_values_in_data_assignment_and_bitwise_expressions():
    output = StringIO()
    Runtime(output=output).run(
        Program.from_source(
            "10 DATA &HFFFF,&100000\n20 READ A%,B%\n30 PRINT A%;B%;(&HFFFF AND 255)\n40 END"
        )
    )
    assert output.getvalue() == "-1 -32768  255 \n"


def test_single_literal_rounds_before_conversion_to_double():
    assert value("CDBL(2.04)").number() == 2.0399999618530273
    assert value("2.04#").number() == 2.04
