"""Tagged BASIC scalars and explicit conversion rules (IEEE, not legacy MBF)."""

import math
import struct
from dataclasses import dataclass
from enum import Enum

from .errors import BasicError


class Kind(Enum):
    INTEGER = "%"
    SINGLE = "!"
    DOUBLE = "#"
    STRING = "$"


@dataclass(frozen=True)
class Value:
    kind: Kind
    data: float | int | str

    def __post_init__(self) -> None:
        if isinstance(self.data, str) and len(self.data) > 32767:
            raise BasicError("String too long")

    def number(self) -> float:
        if isinstance(self.data, str):
            raise BasicError("Type mismatch")
        return float(self.data)

    def string(self) -> str:
        if not isinstance(self.data, str):
            raise BasicError("Type mismatch")
        return self.data

    def integer(self) -> int:
        n = round(self.number())
        if not -32768 <= n <= 32767:
            raise BasicError("Overflow")
        return n


def numeric(n: float, kind: Kind = Kind.DOUBLE) -> Value:
    try:
        finite = math.isfinite(n)
    except OverflowError:
        raise BasicError("Overflow") from None
    if not finite:
        raise BasicError("Overflow")
    if kind == Kind.INTEGER:
        n = round(n)
        if not -32768 <= n <= 32767:
            raise BasicError("Overflow")
    elif kind == Kind.SINGLE:
        try:
            n = struct.unpack("f", struct.pack("f", n))[0]
        except (OverflowError, struct.error):
            raise BasicError("Overflow") from None
        if not math.isfinite(n):
            raise BasicError("Overflow")
    return Value(kind, n)


def kind_for(name: str) -> Kind:
    return next((k for k in Kind if name.endswith(k.value)), Kind.SINGLE)


def coerce(name: str, value: Value) -> Value:
    kind = kind_for(name)
    if kind == Kind.STRING:
        text = value.string()
        if len(text) > 32767:
            raise BasicError("String too long")
        return Value(kind, text)
    return numeric(value.number(), kind)


def default(name: str) -> Value:
    return Value(Kind.STRING, "") if kind_for(name) == Kind.STRING else numeric(0, kind_for(name))


def formatted(value: Value) -> str:
    if value.kind == Kind.STRING:
        return value.string()
    n = value.number()
    text = format(n, ".7g" if value.kind == Kind.SINGLE else ".15g")
    return (" " if n >= 0 else "") + text + " "


def numeric_literal(text: str) -> Value:
    """Convert a lexer-validated literal, retaining its BASIC precision category."""
    text = text.upper()
    if text.startswith("&"):
        hexadecimal = text.startswith("&H")
        digits = text[2:] if text.startswith(("&H", "&O")) else text[1:]
        digits = digits.lstrip("0") or "0"
        # Reject huge literals before allocating a host arbitrary-precision integer.
        if len(digits) > (4 if hexadecimal else 6):
            raise BasicError("Overflow")
        radix_number = int(digits, 16 if hexadecimal else 8)
        if radix_number > 65535:
            raise BasicError("Overflow")
        return numeric(radix_number if radix_number < 32768 else radix_number - 65536, Kind.INTEGER)

    suffix = text[-1] if text[-1] in "%!#" else ""
    body = text[:-1] if suffix else text
    number = float(body.replace("D", "E"))
    if suffix:
        kind = {"%": Kind.INTEGER, "!": Kind.SINGLE, "#": Kind.DOUBLE}[suffix]
    elif "D" in body:
        kind = Kind.DOUBLE
    elif "E" in body:
        kind = Kind.SINGLE
    elif "." not in body and number <= 32767:
        kind = Kind.INTEGER
    else:
        significant = body.replace(".", "").lstrip("0")
        kind = Kind.SINGLE if len(significant) <= 7 else Kind.DOUBLE
    return numeric(number, kind)


def arithmetic_result(number: float, kind: Kind) -> Value:
    """Promote overflowing integer calculations; assignments still use strict coerce."""
    if kind == Kind.INTEGER and not -32768 <= number <= 32767:
        kind = Kind.SINGLE
    return numeric(number, kind)
