"""A read-only, downsampled snapshot of the stopped graphics framebuffer."""

from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Static

from .graphics import PALETTE, Graphics


class GraphicsScreen(ModalScreen[None]):
    BINDINGS = [("escape", "close", "Close"), ("f9", "close", "Close")]
    DEFAULT_CSS = """
    #graphics-dialog { width: 96%; height: 94%; border: ascii #55ffff;
        background: #000020; padding: 0 1; }
    #graphics-title { height: 2; }
    #graphics-preview { height: 1fr; overflow: hidden; }
    #graphics-close { height: 3; border: ascii #aaaaaa; }
    """

    def __init__(self, graphics: Graphics) -> None:
        super().__init__()
        self.width, self.height = graphics.width, graphics.height
        self.pixels = bytes(graphics.pixels)

    def compose(self) -> ComposeResult:
        with Vertical(id="graphics-dialog"):
            yield Static(
                f"Graphics {self.width}x{self.height} | scaled snapshot | Esc close",
                id="graphics-title",
            )
            yield Static(id="graphics-preview")
            yield Button("Close", id="graphics-close")

    def on_mount(self) -> None:
        self.call_after_refresh(self.draw)

    def on_resize(self) -> None:
        self.call_after_refresh(self.draw)

    def draw(self) -> None:
        if not self.is_mounted:
            return
        widget = self.query_one("#graphics-preview", Static)
        columns, rows = max(1, widget.size.width), max(1, widget.size.height)
        scale = min(columns / self.width, rows * 2 / self.height)
        columns = max(1, int(self.width * scale))
        rows = max(1, int(self.height * scale / 2))
        text = Text()
        for row in range(rows):
            for column in range(columns):
                x = column * self.width // columns
                top = self.pixels[(2 * row) * self.height // (2 * rows) * self.width + x]
                bottom = self.pixels[(2 * row + 1) * self.height // (2 * rows) * self.width + x]
                fg = "#%02x%02x%02x" % PALETTE[top]
                bg = "#%02x%02x%02x" % PALETTE[bottom]
                text.append("▀", style=f"{fg} on {bg}")
            if row < rows - 1:
                text.append("\n")
        widget.update(text)

    @on(Button.Pressed, "#graphics-close")
    def action_close(self) -> None:
        self.dismiss(None)
