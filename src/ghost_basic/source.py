"""Plain-text BASIC source loading, including DOS CP437 and trailing DOS EOF."""

from pathlib import Path

from .errors import BasicError

MAX_SOURCE_BYTES = 1_000_000


def decode_source(data: bytes) -> str:
    """Prefer UTF-8; fall back to CP437 only for BOM-less legacy text.

    This is a deterministic fallback, not general-purpose encoding detection.
    Tokenized/protected files need a separate decoder and must not be mistaken for text.
    """
    if data.startswith((b"\xff", b"\xfe")):
        raise BasicError(
            "Tokenized/protected or UTF-16 BASIC files are not supported; use plain text"
        )
    if b"\x00" in data:
        raise BasicError("Binary BASIC files are not supported; export as plain text")
    if b"\x1a" in data:
        before, after = data.split(b"\x1a", 1)
        if after.strip(b" \t\r\n\x1a"):
            raise BasicError("Embedded DOS EOF is not supported in source text")
        data = before
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        if data.startswith(b"\xef\xbb\xbf"):
            raise BasicError("File error: invalid UTF-8 after UTF-8 BOM") from None
        text = data.decode("cp437")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def read_source(path: Path, *, max_bytes: int = MAX_SOURCE_BYTES) -> str:
    try:
        with path.open("rb") as stream:
            data = stream.read(max_bytes + 1)
    except OSError as error:
        raise BasicError(f"File error: {error}") from None
    if len(data) > max_bytes:
        raise BasicError("Program too large")
    return decode_source(data)
