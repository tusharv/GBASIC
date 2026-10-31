"""Deterministic 16-color raster API and dependency-free indexed PNG export."""

import struct
import zlib
from pathlib import Path

from .errors import BasicError

PALETTE = (
    (0, 0, 0),
    (0, 0, 170),
    (0, 170, 0),
    (0, 170, 170),
    (170, 0, 0),
    (170, 0, 170),
    (170, 85, 0),
    (170, 170, 170),
    (85, 85, 85),
    (85, 85, 255),
    (85, 255, 85),
    (85, 255, 255),
    (255, 85, 85),
    (255, 85, 255),
    (255, 255, 85),
    (255, 255, 255),
)
MODES = {0: (0, 0), 7: (320, 200), 9: (640, 350), 12: (640, 480)}


def checked(value: int, low: int, high: int) -> int:
    if not isinstance(value, int) or not low <= value <= high:
        raise BasicError("Illegal function call: graphics argument out of range")
    return value


class Graphics:
    """Pixel coordinates use top-left origin; drawing clips to the selected screen."""

    def __init__(self) -> None:
        self.mode = self.width = self.height = 0
        self.foreground, self.background = 15, 0
        self.pixels = bytearray()

    def screen(self, mode: int) -> None:
        if not isinstance(mode, int) or mode not in MODES:
            raise BasicError("Illegal function call: supported SCREEN modes are 0, 7, 9, 12")
        self.mode = mode
        self.width, self.height = MODES[mode]
        self.foreground, self.background = 15, 0
        self.pixels = bytearray(self.width * self.height)

    def require_screen(self) -> None:
        if not self.mode:
            raise BasicError("Illegal function call: select a graphics SCREEN first")

    def color(self, foreground: int, background: int | None = None) -> None:
        self.require_screen()
        checked(foreground, 0, 15)
        if background is not None:
            checked(background, 0, 15)
        self.foreground = foreground
        if background is not None:
            self.background = background

    def clear(self) -> None:
        self.require_screen()
        self.pixels[:] = bytes([self.background]) * len(self.pixels)

    def _arguments(self, color: int | None, *coordinates: int) -> int:
        self.require_screen()
        for coordinate in coordinates:
            checked(coordinate, -32768, 32767)
        return checked(self.foreground if color is None else color, 0, 15)

    def _plot(self, x: int, y: int, color: int) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y * self.width + x] = color

    def pset(self, x: int, y: int, color: int | None = None) -> None:
        color = self._arguments(color, x, y)
        self._plot(x, y, color)

    def preset(self, x: int, y: int, color: int | None = None) -> None:
        self.pset(x, y, self.background if color is None else color)

    def point(self, x: int, y: int) -> int:
        self._arguments(None, x, y)
        return (
            self.pixels[y * self.width + x]
            if (0 <= x < self.width and 0 <= y < self.height)
            else -1
        )

    def line(
        self, x1: int, y1: int, x2: int, y2: int, color: int | None = None, box: str = ""
    ) -> None:
        color = self._arguments(color, x1, y1, x2, y2)
        if box not in ("", "B", "BF"):
            raise BasicError("Illegal function call: box must be B or BF")
        if box:
            left, right = sorted((x1, x2))
            top, bottom = sorted((y1, y2))
            if box == "BF":
                left, right = max(0, left), min(self.width - 1, right)
                if left <= right:
                    row = bytes([color]) * (right - left + 1)
                    for y in range(max(0, top), min(self.height - 1, bottom) + 1):
                        start = y * self.width + left
                        self.pixels[start : start + len(row)] = row
            else:
                self.line(left, top, right, top, color)
                self.line(right, top, right, bottom, color)
                self.line(right, bottom, left, bottom, color)
                self.line(left, bottom, left, top, color)
            return
        dx, dy = abs(x2 - x1), -abs(y2 - y1)
        sx, sy = (1 if x1 < x2 else -1), (1 if y1 < y2 else -1)
        error = dx + dy
        while True:
            self._plot(x1, y1, color)
            if x1 == x2 and y1 == y2:
                break
            twice = 2 * error
            if twice >= dy:
                error += dy
                x1 += sx
            if twice <= dx:
                error += dx
                y1 += sy

    def circle(self, cx: int, cy: int, radius: int, color: int | None = None) -> None:
        color = self._arguments(color, cx, cy)
        checked(radius, 0, 32767)
        x, y, error = radius, 0, 1 - radius
        while x >= y:
            for dx, dy in ((x, y), (y, x), (-y, x), (-x, y), (-x, -y), (-y, -x), (y, -x), (x, -y)):
                self._plot(cx + dx, cy + dy, color)
            y += 1
            if error < 0:
                error += 2 * y + 1
            else:
                x -= 1
                error += 2 * (y - x) + 1

    def png(self) -> bytes:
        self.require_screen()

        def chunk(kind: bytes, data: bytes) -> bytes:
            return (
                struct.pack(">I", len(data))
                + kind
                + data
                + struct.pack(">I", zlib.crc32(kind + data))
            )

        rows = b"".join(
            b"\0" + self.pixels[y * self.width : (y + 1) * self.width] for y in range(self.height)
        )
        return (
            b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", self.width, self.height, 8, 3, 0, 0, 0))
            + chunk(b"PLTE", bytes(c for rgb in PALETTE for c in rgb))
            + chunk(b"IDAT", zlib.compress(rows))
            + chunk(b"IEND", b"")
        )

    def save_png(self, path: str | Path) -> None:
        Path(path).write_bytes(self.png())
