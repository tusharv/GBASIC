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
