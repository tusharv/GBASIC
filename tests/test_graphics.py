import struct
import subprocess
import sys
import zlib
from io import StringIO

import pytest

from ghost_basic.errors import BasicError
from ghost_basic.program import Program
from ghost_basic.runtime import Runtime


def run(source):
    runtime = Runtime(output=StringIO())
    runtime.run(Program.from_source(source))
    return runtime


def test_pixels_colors_readback_and_clear():
    r = run(
        "10 SCREEN 7\n20 COLOR 14,1\n30 CLS\n40 PSET (2,3)\n"
        "50 PRESET (4,5)\n60 PRINT POINT(2,3);POINT(4,5);POINT(-1,0)"
    )
    assert r.output.getvalue() == " 14  1 -1 \n"
    assert r.graphics.point(2, 3) == 14
    assert r.graphics.point(0, 0) == 1


def test_lines_boxes_circles_and_clipping():
    r = run(
        "10 SCREEN 12\n20 LINE (-2,0)-(2,0),4\n"
        "30 LINE (10,10)-(14,14),2,B\n40 LINE (20,20)-(22,22),3,BF\n"
        "50 CIRCLE (40,40),5,5\n60 LINE (50,50)-(52,52),,BF"
    )
    g = r.graphics
    assert (g.width, g.height) == (640, 480)
    assert [g.point(x, 0) for x in range(4)] == [4, 4, 4, 0]
    assert g.point(10, 12) == 2 and g.point(12, 12) == 0
    assert g.point(21, 21) == 3 and g.point(51, 51) == 15
    assert [g.point(x, y) for x, y in [(35, 40), (45, 40), (40, 35), (40, 45)]] == [5] * 4
    assert g.point(40, 40) == 0


@pytest.mark.parametrize(
    "statement",
    [
        "SCREEN 99",
        "SCREEN 7,1",
        "PSET (1,2),16",
        "CIRCLE (1,2),-1",
        "CIRCLE (1,2),4,1,0,2",
        "LINE (1,2)-(3,4),1,BAD",
        "PSET STEP(1,2)",
        "COLOR 16",
        "PRINT POINT(1)",
        "PRINT POINT(1,2,3)",
    ],
)
def test_invalid_graphics_reports_basic_error_with_line(statement):
    with pytest.raises(BasicError) as error:
        run("10 SCREEN 7\n20 " + statement)
    assert error.value.line == 20


def test_graphics_requires_mode_and_run_resets():
    with pytest.raises(BasicError):
        run("10 PSET (1,1)")
    r = run("10 SCREEN 7\n20 PSET (1,1),2")
    r.run(Program.from_source('10 PRINT "text"'))
    assert r.graphics.mode == 0
    r.run(Program.from_source("10 SCREEN 9\n20 PSET (1,1),2"))
    r.run(Program({0: "PSET (2,2),3"}), reset=False)
    assert r.graphics.point(1, 1) == 2 and r.graphics.point(2, 2) == 3


def test_png_export_and_cli(tmp_path):
    source = tmp_path / "picture.bas"
    target = tmp_path / "picture.png"
    source.write_text("10 SCREEN 7\n20 PSET (0,0),4\n30 END")
    proc = subprocess.run(
        [sys.executable, "-m", "ghost_basic", str(source), "--graphics-output", str(target)],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    data = target.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    assert struct.unpack(">II", data[16:24]) == (320, 200)
    pos = 8
    compressed = b""
    while pos < len(data):
        size = int.from_bytes(data[pos : pos + 4], "big")
        kind = data[pos + 4 : pos + 8]
        chunk = data[pos + 8 : pos + 8 + size]
        assert zlib.crc32(kind + chunk) == int.from_bytes(
            data[pos + 8 + size : pos + 12 + size], "big"
        )
        if kind == b"IDAT":
            compressed += chunk
        pos += size + 12
    raw = zlib.decompress(compressed)
    assert len(raw) == 321 * 200 and raw[:3] == bytes([0, 4, 0])


def test_api_validates_before_mutation():
    r = run("10 SCREEN 7\n20 PSET (1,1),3")
    g = r.graphics
    before = bytes(g.pixels)
    for action in [
        lambda: g.screen(99),
        lambda: g.pset(1, 1, 16),
        lambda: g.line(0, 0, 99999999, 1, 2),
        lambda: g.circle(1, 1, -1, 2),
    ]:
        with pytest.raises(BasicError):
            action()
        assert bytes(g.pixels) == before


@pytest.mark.asyncio
@pytest.mark.parametrize("size", [(80, 24), (120, 40)])
async def test_editor_graphics_preview_and_close(tmp_path, size):
    from textual.widgets import TextArea

    from ghost_basic.tui import GhostBasicApp

    app = GhostBasicApp(root=tmp_path)
    async with app.run_test(size=size) as pilot:
        source = "10 SCREEN 7\n20 LINE (0,0)-(319,199),4,BF"
        app.query_one("#editor", TextArea).load_text(source)
        await pilot.press("f5")
        for _ in range(50):
            await pilot.pause(0.02)
            if not app.runner.running:
                break
        await pilot.press("f9")
        assert app.screen.query("#graphics-preview")
        assert app.screen.query_one("#graphics-close").region.bottom <= size[1]
        await pilot.press("escape")
        assert not app.screen.query("#graphics-preview")
        assert app.query_one("#editor", TextArea).text == source


@pytest.mark.parametrize(
    "name, xy, color",
    [
        ("graphics_shapes", (40, 40), 9),
        ("graphics_palette", (10, 10), 0),
        ("graphics_plot", (160, 100), 8),
    ],
)
def test_graphics_examples(name, xy, color):
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "examples" / (name + ".bas")
    assert path.exists()
    r = run(path.read_text())
    assert r.graphics.point(*xy) == color
    assert any(r.graphics.pixels)


def test_export_failure_keeps_existing_file(tmp_path):
    source = tmp_path / "text.bas"
    target = tmp_path / "keep.png"
    source.write_text('10 PRINT "text only"')
    target.write_bytes(b"keep")
    proc = subprocess.run(
        [sys.executable, "-m", "ghost_basic", str(source), "--graphics-output", str(target)],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 1 and "graphics SCREEN" in proc.stderr
    assert target.read_bytes() == b"keep"


def test_direct_api_bounded_fills_and_reset():
    from ghost_basic import Graphics

    g = Graphics()
    g.screen(7)
    g.line(-32768, -32768, 32767, 32767, 6, "BF")
    assert len(g.pixels) == 320 * 200 and set(g.pixels) == {6}
    g.screen(9)
    assert (g.width, g.height) == (640, 350) and not any(g.pixels)
    g.screen(0)
    assert not g.pixels
    with pytest.raises(BasicError):
        g.png()


@pytest.mark.asyncio
async def test_preview_without_graphics_and_while_running(tmp_path):
    from ghost_basic.tui import GhostBasicApp

    app = GhostBasicApp(root=tmp_path)
    async with app.run_test() as pilot:
        await pilot.press("f9")
        assert not app.screen.query("#graphics-preview")
        app.start_execution("10 SCREEN 7\n20 INPUT A$")
        await pilot.pause(0.1)
        await pilot.press("f9")
        assert not app.screen.query("#graphics-preview")
        app.runner.stop()
        await pilot.pause(0.1)


@pytest.mark.asyncio
async def test_preview_f9_toggles_and_blocks_editor_actions(tmp_path):
    from textual.widgets import TextArea

    from ghost_basic.tui import GhostBasicApp

    app = GhostBasicApp(root=tmp_path)
    async with app.run_test() as pilot:
        source = "10 SCREEN 7\n20 PSET (1,1),14"
        app.query_one("#editor", TextArea).load_text(source)
        app.runner.runtime = run(source)
        await pilot.press("f9")
        assert len(app.screen_stack) == 2
        for action in ("run", "new", "open", "save", "save_as", "command", "magic", "help"):
            assert app.check_action(action, ()) is False
        await pilot.press("f9")
        assert len(app.screen_stack) == 1
        assert app.query_one("#editor", TextArea).text == source
