"""Explicit expression evaluation and a small, validated intrinsic inventory."""

import math
import operator
from collections.abc import Callable

from .errors import BasicError
from .syntax import Binary, Expr, Literal, Reference, Unary
from .values import Kind, Value, formatted, numeric

_MATH: dict[str, Callable[[float], float]] = {
    "ABS": abs,
    "INT": math.floor,
    "FIX": math.trunc,
    "SQR": math.sqrt,
    "SIN": math.sin,
    "COS": math.cos,
    "TAN": math.tan,
    "ATN": math.atan,
    "LOG": math.log,
    "EXP": math.exp,
}
_ARITH: dict[str, Callable[[float, float], float]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "^": math.pow,
}
_COMPARE: dict[str, Callable[[float | str, float | str], bool]] = {
    "=": operator.eq,
    "<>": operator.ne,
    "<": operator.lt,
    ">": operator.gt,
    "<=": operator.le,
    ">=": operator.ge,
}
FUNCTIONS = set(_MATH) | {
    "LEN",
    "ASC",
    "CHR$",
    "STR$",
    "VAL",
    "LEFT$",
    "RIGHT$",
    "MID$",
    "SPACE$",
    "STRING$",
    "SGN",
    "CINT",
    "CSNG",
    "CDBL",
}


def intrinsic(name: str, args: list[Value]) -> Value:
    arities = {"MID$": (2, 3), "LEFT$": (2,), "RIGHT$": (2,), "STRING$": (2,)}
    if len(args) not in arities.get(name, (1,)):
        raise BasicError("Illegal function call: argument count")
    a = args[0]
    if name in _MATH:
        return numeric(_MATH[name](a.number()))
    if name == "SGN":
        return numeric((a.number() > 0) - (a.number() < 0))
    if name in ("CINT", "CSNG", "CDBL"):
        return numeric(
            a.number(), {"CINT": Kind.INTEGER, "CSNG": Kind.SINGLE, "CDBL": Kind.DOUBLE}[name]
        )
    if name == "LEN":
        return numeric(len(a.string()))
    if name == "ASC":
        if not a.string():
            raise BasicError("Illegal function call")
        return numeric(ord(a.string()[0]))
    if name == "VAL":
        import re

        match = re.match(r"\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?)", a.string())
        return numeric(float(match[1]) if match else 0)
    if name == "STR$":
        return Value(Kind.STRING, formatted(a).rstrip())
    if name == "CHR$":
        n = a.integer()
        if not 0 <= n <= 255:
            raise BasicError("Illegal function call")
        return Value(Kind.STRING, chr(n))
    if name in ("SPACE$", "STRING$"):
        n = a.integer()
        if n < 0:
            raise BasicError("Illegal function call")
        char = " "
        if name == "STRING$":
            char = (
                intrinsic("CHR$", [args[1]]).string()
                if args[1].kind != Kind.STRING
                else args[1].string()[:1]
            )
            if not char:
                raise BasicError("Illegal function call")
        return Value(Kind.STRING, char * n)
    text = a.string()
    n = args[1].integer()
    if n < (1 if name == "MID$" else 0):
        raise BasicError("Illegal function call")
    if name == "LEFT$":
        text = text[:n]
    elif name == "RIGHT$":
        text = text[-n:] if n else ""
    else:
        length = args[2].integer() if len(args) == 3 else len(text)
        if length < 0:
            raise BasicError("Illegal function call")
        text = text[n - 1 : n - 1 + length]
    return Value(Kind.STRING, text)


def evaluate(expr: Expr, lookup: Callable[[Reference], Value]) -> Value:
    try:
        return _evaluate(expr, lookup)
    except ZeroDivisionError:
        raise BasicError("Division by zero") from None
    except OverflowError:
        raise BasicError("Overflow") from None
    except ValueError:
        raise BasicError("Illegal function call") from None
    except RecursionError:
        raise BasicError("Expression too complex") from None


def _evaluate(expr: Expr, lookup: Callable[[Reference], Value]) -> Value:
    if isinstance(expr, Literal):
        return expr.value
    if isinstance(expr, Reference):
        if expr.name in FUNCTIONS:
            return intrinsic(expr.name, [evaluate(a, lookup) for a in expr.indices])
        return lookup(expr)
    if isinstance(expr, Unary):
        value = evaluate(expr.operand, lookup)
        if expr.op == "NOT":
            return numeric(~value.integer(), Kind.INTEGER)
        return numeric(value.number() if expr.op == "+" else -value.number())
    assert isinstance(expr, Binary)
    left, right = evaluate(expr.left, lookup), evaluate(expr.right, lookup)
    op = expr.op
    if op in _COMPARE:
        if (left.kind == Kind.STRING) != (right.kind == Kind.STRING):
            raise BasicError("Type mismatch")
        a: float | str = left.string() if left.kind == Kind.STRING else left.number()
        b: float | str = right.string() if right.kind == Kind.STRING else right.number()
        return numeric(-int(_COMPARE[op](a, b)), Kind.INTEGER)
    if op == "+" and left.kind == Kind.STRING:
        text = left.string() + right.string()
        if len(text) > 32767:
            raise BasicError("String too long")
        return Value(Kind.STRING, text)
    if op in _ARITH:
        return numeric(_ARITH[op](left.number(), right.number()))
    x, y = left.integer(), right.integer()
    if op == "\\":
        return numeric(math.trunc(x / y))
    if op == "MOD":
        return numeric(x - math.trunc(x / y) * y)
    bits = {"AND": operator.and_, "OR": operator.or_, "XOR": operator.xor}
    if op in bits:
        return numeric(bits[op](x, y), Kind.INTEGER)
    if op == "EQV":
        return numeric(~(x ^ y), Kind.INTEGER)
    return numeric((~x) | y, Kind.INTEGER)
