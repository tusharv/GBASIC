"""Language errors are independent of the host Python exceptions."""


class BasicError(Exception):
    def __init__(self, message: str, line: int | None = None) -> None:
        self.message = message
        self.line = line
        super().__init__(message)

    def __str__(self) -> str:
        return self.message + (f" in {self.line}" if self.line is not None else "")
