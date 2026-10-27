"""Position-preserving tokenizer for one physical BASIC source line."""

import re
from dataclasses import dataclass

from .errors import BasicError

_PATTERN = re.compile(
    r'(?P<SPACE>[ \t]+)|(?P<STRING>"[^"\r\n]*")|'
    r"(?P<NUMBER>&[Hh][0-9A-Fa-f]+|&[Oo][0-7]+|"
    r"(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?[%!#]?)|"
    r"(?P<NAME>[A-Za-z][A-Za-z0-9.]*[$%!#]?)|"
    r"(?P<OP><=|>=|<>|[+*/\\^=<>(),;:?\-])"
)


@dataclass(frozen=True)
class Token:
    kind: str
    text: str
    column: int


def tokenize(source: str) -> list[Token]:
    result = []
    pos = 0
    while pos < len(source):
        if source[pos] == "'":
            break
        m = _PATTERN.match(source, pos)
        if not m:
            raise BasicError(f"Syntax error at column {pos + 1}")
        kind = m.lastgroup or ""
        text = m.group()
        if kind == "NAME":
            text = text.upper()
            if text == "REM":
                break
        if kind != "SPACE":
            result.append(Token(kind, text, pos + 1))
        pos = m.end()
    result.append(Token("EOF", "", len(source) + 1))
    return result
