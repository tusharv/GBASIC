"""Editable numbered source; compilation occurs at RUN, as in classic BASIC."""

import re
from dataclasses import dataclass, field

from .errors import BasicError


@dataclass
class Program:
    lines: dict[int, str] = field(default_factory=dict)

    def edit(self, source: str) -> None:
        match = re.fullmatch(r"\s*(\d+)\s*(.*)", source)
        if not match:
            raise BasicError("Syntax error: expected line number")
        digits = match[1].lstrip("0") or "0"
        if len(digits) > 5:
            raise BasicError("Illegal function call: line number")
        number = int(digits)
        if not 0 <= number <= 65529:
            raise BasicError("Illegal function call: line number")
        if match[2]:
            self.lines[number] = match[2]
        else:
            self.lines.pop(number, None)

    def listing(self) -> str:
        return "".join(f"{n} {text}\n" for n, text in sorted(self.lines.items()))

    @classmethod
    def from_source(cls, source: str) -> "Program":
        program = cls()
        for physical, line in enumerate(source.splitlines(), 1):
            if line.strip():
                if not re.match(r"\s*\d", line):
                    raise BasicError(
                        "Unnumbered QBasic execution is not supported yet; "
                        "open this file in the editor to view or edit it",
                        physical,
                    )
                try:
                    program.edit(line)
                except BasicError as error:
                    error.line = physical
                    raise
        return program
