"""A short, skippable ASCII ghost flight; independent of BASIC execution."""

import math
import time

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.events import Click, Key, Resize
from textual.screen import ModalScreen
from textual.timer import Timer
from textual.widgets import Static

_GHOST = (
    "    .-.    ",
    "   (o o)   ",
    "   | O \\   ",
    "  /     \\  ",
    " (       ) ",
    "  '~~~~~'  ",
)


def ghost_frame(width: int, elapsed: float) -> str:
    """Render a ghost that moves horizontally and gently bobs, using only ASCII."""
    width = max(1, width)
    travel = max(1, width - len(_GHOST[0]))
    position = int(elapsed * 22) % (travel * 2)
    x = min(position, travel * 2 - position)
    bob = 1 + round(math.sin(elapsed * 4))
    ghost = list(_GHOST)
    if int(elapsed * 6) % 2:
        ghost[-1] = "  '~^~^~'  "
    lines = [""] * bob + [" " * x + line for line in ghost]
    lines += [""] * (9 - len(lines))
    return "\n".join(line[:width] for line in lines)


class SplashScreen(ModalScreen[None]):
    """Dismiss after 5 seconds, or immediately on any key or mouse click."""

    DEFAULT_CSS = """
    SplashScreen { background: #000080; align: center middle; }
    #splash-card {
        width: 90%; max-width: 100; height: 19; max-height: 95%;
        border: ascii #55ffff; background: #000080; padding: 1 2;
    }
    #splash-title { height: 2; text-align: center; text-style: bold; color: #ffffff; }
    #splash-subtitle { height: 1; text-align: center; color: #55ffff; }
    #ghost-flight { height: 9; color: #ffffff; }
    #splash-skip { height: 1; text-align: center; color: #ffff55; }
    """

    def __init__(self) -> None:
        super().__init__()
        self.started = 0.0
        self.frame_text = ""
        self.finished = False
        self.animation_timer: Timer | None = None

    def compose(self) -> ComposeResult:
        with Vertical(id="splash-card"):
            yield Static("Ghost BASIC", id="splash-title", markup=False)
            yield Static("Your BASIC programming environment", id="splash-subtitle", markup=False)
            yield Static("", id="ghost-flight", markup=False)
            yield Static("Press any key or click to continue", id="splash-skip", markup=False)

    def on_mount(self) -> None:
        self.started = time.monotonic()
        self.call_after_refresh(self.animate_ghost)
        self.animation_timer = self.set_interval(0.08, self.animate_ghost)

    def animate_ghost(self) -> None:
        if self.finished:
            return
        elapsed = time.monotonic() - self.started
        if elapsed >= 5.0:
            self.finish()
            return
        flight = self.query_one("#ghost-flight", Static)
        self.frame_text = ghost_frame(flight.content_size.width, elapsed)
        flight.update(self.frame_text)

    def on_resize(self, event: Resize) -> None:
        if self.is_mounted:
            self.call_after_refresh(self.animate_ghost)

    def on_key(self, event: Key) -> None:
        event.stop()
        event.prevent_default()
        self.finish()

    def on_click(self, event: Click) -> None:
        event.stop()
        self.finish()

    def finish(self) -> None:
        if not self.finished:
            self.finished = True
            if self.animation_timer:
                self.animation_timer.stop()
            self.dismiss(None)

    def on_unmount(self) -> None:
        self.finished = True
        if self.animation_timer:
            self.animation_timer.stop()
