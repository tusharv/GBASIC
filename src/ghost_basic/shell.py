"""Interactive command session sharing runtime variables between immediate commands."""

import re
from pathlib import Path
from typing import TextIO

from .devices import Disk
from .errors import BasicError
from .help_topics import get_topic, help_index, render_text
from .program import Program
from .runtime import Runtime


class Shell:
    def __init__(
        self,
        *,
        root: Path | None = None,
        output: TextIO | None = None,
        input_stream: TextIO | None = None,
        max_steps: int = 100_000,
    ) -> None:
        self.program = Program()
        self.disk = Disk(root or Path.cwd())
        self.runtime = Runtime(output=output, input_stream=input_stream, max_steps=max_steps)

    def submit(self, source: str) -> bool:
        source = source.strip()
        if not source:
            return True
        if source[0].isdigit():
            self.program.edit(source)
            return True
        command = source.upper()
        if command in ("SYSTEM", "QUIT", "EXIT"):
            return False
        if command == "RUN":
            self.runtime.run(self.program)
        elif command == "LIST":
            self.runtime.emit(self.program.listing())
        elif command == "NEW":
            self.program = Program()
            self.runtime.variables.clear()
            self.runtime.arrays.clear()
        elif command == "CLEAR":
            self.runtime.variables.clear()
            self.runtime.arrays.clear()
        elif command == "HELP" or command.startswith("HELP "):
            keyword = source[4:].strip()
            if not keyword:
                self.runtime.emit(help_index())
            else:
                topic = get_topic(keyword)
                self.runtime.emit(
                    render_text(topic)
                    if topic
                    else f"No matching help for {keyword}. Try HELP for the index.\n"
                )
        elif re.match(r'(SAVE|LOAD)(?=\s|"|$)', source, re.IGNORECASE):
            match = re.fullmatch(r'(SAVE|LOAD)\s+"([^"\r\n]+)"', source, re.IGNORECASE)
            if not match:
                raise BasicError("Syntax error: expected quoted filename")
            if match[1].upper() == "LOAD":
                self.program = Program.from_source(self.disk.read(match[2]))
            else:
                self.disk.write(match[2], self.program.listing())
        else:
            self.runtime.run(Program({0: source}), reset=False)
        return True
