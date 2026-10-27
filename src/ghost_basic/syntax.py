"""Immutable AST; nodes contain syntax, never effects or evaluation behavior."""

from dataclasses import dataclass

from .values import Value


@dataclass(frozen=True)
class Literal:
    value: Value


@dataclass(frozen=True)
class Reference:
    name: str
    indices: tuple["Expr", ...] = ()


@dataclass(frozen=True)
class Unary:
    op: str
    operand: "Expr"


@dataclass(frozen=True)
class Binary:
    op: str
    left: "Expr"
    right: "Expr"


type Expr = Literal | Reference | Unary | Binary


@dataclass(frozen=True)
class Statement:
    op: str
    expressions: tuple[Expr, ...] = ()
    targets: tuple[Reference, ...] = ()
    separators: tuple[str, ...] = ()
    then_body: tuple["Statement", ...] = ()
    else_body: tuple["Statement", ...] = ()
    text: str = ""
