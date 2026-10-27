"""Capability-limited disk adapter; execution itself has no host filesystem access."""

from pathlib import Path
from typing import Protocol

from .errors import BasicError
from .source import read_source


class Disk:
    max_source_bytes = 1_000_000

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def path(self, name: str) -> Path:
        try:
            path = (self.root / name).resolve()
        except (OSError, RuntimeError) as error:
            raise BasicError(f"File error: {error}") from None
        if not path.is_relative_to(self.root):
            raise BasicError("Permission denied: outside workspace")
        return path

    def example_programs(self) -> tuple[str, ...]:
        """List only BASIC files in the workspace's examples directory."""
        try:
            folder = self.path("examples")
            if not folder.is_dir():
                return ()
            programs = []
            for entry in folder.iterdir():
                name = f"examples/{entry.name}"
                try:
                    if entry.suffix.lower() == ".bas" and self.path(name).is_file():
                        programs.append(name)
                except (BasicError, OSError):
                    continue
            return tuple(sorted(programs, key=str.casefold))
        except (BasicError, OSError):
            return ()

    def read(self, name: str) -> str:
        return read_source(self.path(name), max_bytes=self.max_source_bytes)

    def write(self, name: str, source: str) -> None:
        try:
            self.path(name).write_text(source, encoding="utf-8")
        except OSError as error:
            raise BasicError(f"File error: {error}") from None


class TextOutput(Protocol):
    """Minimal runtime output capability shared by terminal and UI adapters."""

    def write(self, text: str, /) -> int: ...


class TextInput(Protocol):
    """Minimal runtime keyboard capability; independent of host console APIs."""

    def readline(self) -> str: ...
