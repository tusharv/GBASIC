import pytest
from textual.widgets import TextArea

from ghost_basic.splash import SplashScreen, ghost_frame
from ghost_basic.tui import GhostBasicApp


def test_ghost_is_ascii_and_flies_within_bounds():
    first = ghost_frame(70, 0)
    later = ghost_frame(70, 0.5)
    assert first != later
    for width in (1, 8, 40, 70, 120):
        for elapsed in (0, 0.5, 2, 20):
            frame = ghost_frame(width, elapsed)
            assert all(len(line) <= width for line in frame.splitlines())
            assert all(ord(c) < 128 for c in frame)
    assert "o o" in first


@pytest.mark.asyncio
@pytest.mark.parametrize("size", [(80, 24), (120, 40)])
async def test_splash_title_animation_and_skip(tmp_path, size):
    app = GhostBasicApp(root=tmp_path, show_splash=True)
    async with app.run_test(size=size) as pilot:
        assert isinstance(app.screen, SplashScreen)
        initial = app.screen.frame_text
        await pilot.pause(0.15)
        assert app.screen.frame_text != initial
        rendered = "\n".join(strip.text for strip in app.screen._compositor.render_strips())
        assert "Ghost BASIC" in rendered
        assert "Program output" not in rendered
        assert "F1 Help" not in rendered
        assert "Press any key" in rendered
        assert all(ord(c) < 128 for c in rendered)
        await pilot.press("space")
        assert not isinstance(app.screen, SplashScreen)
        assert app.query_one("#editor", TextArea).has_focus
        assert not app.dirty
        assert not app.runner.running


@pytest.mark.asyncio
async def test_splash_auto_enters_editor(tmp_path):
    app = GhostBasicApp(root=tmp_path, show_splash=True)
    async with app.run_test() as pilot:
        await pilot.pause(3.0)
        assert isinstance(app.screen, SplashScreen)
        await pilot.pause(2.3)
        assert not isinstance(app.screen, SplashScreen)
        assert app.query_one("#editor", TextArea).has_focus


@pytest.mark.asyncio
async def test_splash_shortcut_does_not_open_hidden_dialog(tmp_path):
    app = GhostBasicApp(root=tmp_path, show_splash=True)
    async with app.run_test() as pilot:
        await pilot.press("f3")
        assert not isinstance(app.screen, SplashScreen)
        assert len(app.screen.query("#examples")) == 0
        await pilot.press("f3")
        assert len(app.screen.query("#examples")) == 1


@pytest.mark.asyncio
async def test_splash_click_to_skip(tmp_path):
    app = GhostBasicApp(root=tmp_path, show_splash=True)
    async with app.run_test() as pilot:
        await pilot.click("#splash-title")
        assert not isinstance(app.screen, SplashScreen)


@pytest.mark.asyncio
async def test_embedded_ui_can_skip_splash(tmp_path):
    app = GhostBasicApp(root=tmp_path, show_splash=False)
    async with app.run_test():
        assert not isinstance(app.screen, SplashScreen)


@pytest.mark.asyncio
async def test_splash_resizes_and_then_enters_editor(tmp_path):
    app = GhostBasicApp(root=tmp_path, show_splash=True)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.resize_terminal(80, 24)
        assert isinstance(app.screen, SplashScreen)
        card = app.screen.query_one("#splash-card")
        assert card.region.x >= 0 and card.region.right <= 80
        assert card.region.y >= 0 and card.region.bottom <= 24
        await pilot.press("escape")
        assert not isinstance(app.screen, SplashScreen)


@pytest.mark.asyncio
async def test_splash_preserves_startup_program(tmp_path):
    source = '10 PRINT "Loaded before splash"\n'
    (tmp_path / "start.bas").write_text(source)
    app = GhostBasicApp(root=tmp_path, filename="start.bas", show_splash=True)
    async with app.run_test() as pilot:
        assert isinstance(app.screen, SplashScreen)
        await pilot.press("enter")
        assert app.filename == "start.bas"
        assert app.query_one("#editor", TextArea).text == source
        assert not app.dirty
