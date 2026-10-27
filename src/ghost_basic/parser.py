"""Recursive descent statements and Pratt expressions; no host language evaluation."""

from .errors import BasicError
from .lexer import Token, tokenize
from .syntax import Binary, Expr, Literal, Reference, Statement, Unary
from .values import Kind, Value, numeric

# GW-BASIC exponentiation associates left; sign binds below exponentiation.
_PRECEDENCE = {
    "IMP": 1,
    "EQV": 2,
    "XOR": 3,
    "OR": 4,
    "AND": 5,
    "=": 7,
    "<>": 7,
    "<": 7,
    ">": 7,
    "<=": 7,
    ">=": 7,
    "+": 8,
    "-": 8,
    "MOD": 9,
    "\\": 10,
    "*": 11,
    "/": 11,
    "^": 13,
}


class Parser:
    def __init__(self, source: str) -> None:
        self.tokens = tokenize(source)
        self.pos = 0

    @property
    def current(self) -> Token:
        return self.tokens[self.pos]

    def take(self) -> Token:
        token = self.current
        if token.kind != "EOF":
            self.pos += 1
        return token

    def accept(self, text: str) -> bool:
        if self.current.text == text:
            self.take()
            return True
        return False

    def expect(self, text: str) -> None:
        if not self.accept(text):
            self.fail(f"Expected {text}")

    def fail(self, detail: str = "") -> None:
        raise BasicError(f"Syntax error at column {self.current.column}: {detail}")

    def expression(self, minimum: int = 0) -> Expr:
        token = self.take()
        if token.text in ("+", "-", "NOT"):
            left: Expr = Unary(token.text, self.expression(6 if token.text == "NOT" else 12))
        elif token.text == "(":
            left = self.expression()
            self.expect(")")
        elif token.kind == "STRING":
            left = Literal(Value(Kind.STRING, token.text[1:-1]))
        elif token.kind == "NUMBER":
            text = token.text.upper()
            if text.startswith("&"):
                value = numeric(int(text[2:], 16 if text[1] == "H" else 8))
            else:
                suffix = text[-1] if text[-1] in "%!#" else ""
                kind = {"%": Kind.INTEGER, "!": Kind.SINGLE, "#": Kind.DOUBLE}.get(
                    suffix, Kind.DOUBLE
                )
                value = numeric(float((text[:-1] if suffix else text).replace("D", "E")), kind)
            left = Literal(value)
        elif token.kind == "NAME":
            left = self.reference(token.text)
        else:
            self.fail("Expected expression")
        while self.current.text in _PRECEDENCE:
            op = self.current.text
            precedence = _PRECEDENCE[op]
            if precedence < minimum:
                break
            self.take()
            left = Binary(op, left, self.expression(precedence + 1))
        return left

    def reference(self, name: str | None = None) -> Reference:
        if name is None:
            if self.current.kind != "NAME":
                self.fail("Expected variable")
            name = self.take().text
        args: list[Expr] = []
        if self.accept("("):
            args.append(self.expression())
            while self.accept(","):
                args.append(self.expression())
            self.expect(")")
        return Reference(name, tuple(args))

    def sequence(self) -> tuple[Statement, ...]:
        result = []
        while self.current.kind != "EOF" and self.current.text != "ELSE":
            if self.accept(":"):
                continue
            result.append(self.statement())
            if self.current.kind != "EOF" and self.current.text != "ELSE":
                self.expect(":")
        return tuple(result)

    def parse(self) -> tuple[Statement, ...]:
        statements = self.sequence()
        if self.current.kind != "EOF":
            self.fail("Unexpected token")
        return statements

    def statement(self) -> Statement:
        op = self.take().text
        expressions: list[Expr] = []
        if op in ("PRINT", "?"):
            separators = []
            while self.current.kind != "EOF" and self.current.text not in (":", "ELSE"):
                expressions.append(self.expression())
                separator = self.take().text if self.current.text in (";", ",") else ""
                separators.append(separator)
                if not separator:
                    break
            return Statement("PRINT", tuple(expressions), separators=tuple(separators))
        if op == "IF":
            condition = self.expression()
            self.expect("THEN")
            then = self.branch()
            otherwise = self.branch() if self.accept("ELSE") else ()
            return Statement(op, (condition,), then_body=then, else_body=otherwise)
        if op == "FOR":
            target = self.reference()
            if target.indices or target.name.endswith("$"):
                self.fail("Expected numeric scalar")
            self.expect("=")
            start = self.expression()
            self.expect("TO")
            end = self.expression()
            step = self.expression() if self.accept("STEP") else Literal(numeric(1))
            return Statement(op, (start, end, step), (target,))
        if op == "NEXT":
            targets = []
            if self.current.kind == "NAME" and self.current.text != "ELSE":
                targets.append(self.reference())
                while self.accept(","):
                    targets.append(self.reference())
            return Statement(op, targets=tuple(targets))
        if op in ("GOTO", "GOSUB", "WHILE"):
            return Statement(op, (self.expression(),))
        if op in ("END", "STOP", "RETURN", "WEND", "CLS", "BEEP"):
            return Statement(op)
        if op == "RESTORE":
            if self.current.kind != "EOF" and self.current.text not in (":", "ELSE"):
                expressions.append(self.expression())
            return Statement(op, tuple(expressions))
        if op == "DATA":
            while True:
                expressions.append(self.expression())
                if not self.accept(","):
                    break
            if not all(
                isinstance(e, Literal)
                or (isinstance(e, Unary) and e.op in ("+", "-") and isinstance(e.operand, Literal))
                for e in expressions
            ):
                self.fail("DATA requires quoted strings or numeric literals")
            return Statement(op, tuple(expressions))
        if op in ("DIM", "READ", "INPUT"):
            prompt = ""
            if op == "INPUT" and self.current.kind == "STRING":
                prompt = self.take().text[1:-1]
                self.expect(";")
            targets = [self.reference()]
            while self.accept(","):
                targets.append(self.reference())
            return Statement(op, targets=tuple(targets), text=prompt)
        if op != "LET":
            self.pos -= 1
        target = self.reference()
        self.expect("=")
        return Statement("LET", (self.expression(),), (target,))

    def branch(self) -> tuple[Statement, ...]:
        if self.current.kind == "NUMBER":
            return (Statement("GOTO", (self.expression(),)),)
        return self.sequence()
