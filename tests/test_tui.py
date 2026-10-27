import pytest
from textual.widgets import Input, TextArea

from ghost_basic.tui import GhostBasicApp


async def settle(pilot, app):
    for _ in range(100):
        await pilot.pause(0.02)
        if not app.runner.running:
            app.poll_execution()
            return
    raise AssertionError("Program did not finish")


@pytest.mark.asyncio
@pytest.mark.parametrize("size", [(80, 24), (120, 40)])
async def test_ascii_editor_and_run(tmp_path, size):
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test(size=size) as pilot:
        editor = app.query_one("#editor", TextArea)
        editor.load_text('10 PRINT "ASCII UI"\n')
        await pilot.press("f5")
        await settle(pilot, app)
        assert "ASCII UI" in app.output_text
        assert editor.region.height >= 5
        assert app.query_one("#output").region.height >= 3
        assert app.query_one("#shortcuts").region.bottom <= size[1]
        assert str(editor.styles.border_top[0]) == "ascii"


@pytest.mark.asyncio
async def test_open_and_save(tmp_path):
    (tmp_path / "hello.bas").write_text('10 PRINT "loaded"\n')
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test() as pilot:
        await pilot.press("f3")
        app.screen.query_one("#filename", Input).value = "hello.bas"
        await pilot.press("enter")
        await pilot.pause()
        editor = app.query_one("#editor", TextArea)
        assert "loaded" in editor.text
        editor.load_text('10 PRINT "saved"\n')
        await pilot.press("f2")
        await pilot.pause()
        assert (tmp_path / "hello.bas").read_text() == '10 PRINT "saved"\n'
        assert not app.dirty


@pytest.mark.asyncio
async def test_unsaved_new_cancel_and_discard(tmp_path):
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test() as pilot:
        app.query_one("#editor", TextArea).load_text('10 PRINT "keep"')
        await pilot.pause()
        await pilot.press("ctrl+n")
        await pilot.press("escape")
        assert "keep" in app.query_one("#editor", TextArea).text
        await pilot.press("ctrl+n")
        await pilot.click("#discard")
        assert app.query_one("#editor", TextArea).text == ""


@pytest.mark.asyncio
async def test_input_and_stop(tmp_path):
    app = GhostBasicApp(root=tmp_path, max_steps=100_000_000)
    async with app.run_test() as pilot:
        app.query_one("#editor", TextArea).load_text("10 INPUT N$\n20 PRINT N$")
        await pilot.press("f5")
        for _ in range(100):
            await pilot.pause(0.02)
            if app.waiting_input:
                break
        assert app.waiting_input
        field = app.query_one("#command", Input)
        field.value = "Ada"
        field.focus()
        await pilot.press("enter")
        await settle(pilot, app)
        assert "Ada" in app.output_text
        app.query_one("#editor", TextArea).load_text("10 GOTO 10")
        await pilot.press("f5")
        await pilot.press("f6")
        await settle(pilot, app)
        assert "Stopped" in app.output_text


@pytest.mark.asyncio
async def test_error_and_path_escape(tmp_path):
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test() as pilot:
        app.query_one("#editor", TextArea).load_text("10 PRINT 1/0")
        await pilot.press("f5")
        await settle(pilot, app)
        assert "Division by zero in 10" in app.output_text
        await pilot.press("f2")
        app.screen.query_one("#filename", Input).value = "../escape.bas"
        await pilot.press("enter")
        await pilot.pause()
        assert app.dirty
        assert "Permission denied" in app.status_text


@pytest.mark.asyncio
async def test_immediate_command(tmp_path):
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test() as pilot:
        command = app.query_one("#command", Input)
        command.value = "PRINT 2+3"
        command.focus()
        await pilot.press("enter")
        await settle(pilot, app)
        assert " 5 " in app.output_text


@pytest.mark.asyncio
async def test_overwrite_cancel_and_confirm(tmp_path):
    (tmp_path / "existing.bas").write_text('10 PRINT "original"')
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test() as pilot:
        app.query_one("#editor", TextArea).load_text('10 PRINT "replacement"')
        app.save_file("existing.bas")
        await pilot.pause()
        await pilot.press("escape")
        assert (tmp_path / "existing.bas").read_text() == '10 PRINT "original"'
        app.save_file("existing.bas")
        await pilot.pause()
        await pilot.click("#discard")
        assert (tmp_path / "existing.bas").read_text() == '10 PRINT "replacement"'
        assert not app.dirty


@pytest.mark.asyncio
async def test_help_and_resize(tmp_path):
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("f1")
        assert app.screen.query_one("#close").region.bottom <= 24
        await pilot.press("escape")
        await pilot.resize_terminal(100, 32)
        assert app.query_one("#shortcuts").region.bottom <= 32
        rendered = "\n".join(strip.text for strip in app.screen._compositor.render_strips())
        assert all(ord(char) < 128 for char in rendered)
        assert "+-" in rendered


@pytest.mark.asyncio
async def test_quoted_markup_output_is_plain(tmp_path):
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test() as pilot:
        app.query_one("#editor", TextArea).load_text('10 PRINT "[bold]literal[/bold]"')
        await pilot.press("f5")
        await settle(pilot, app)
        assert "[bold]literal[/bold]" in app.output_text


@pytest.mark.asyncio
async def test_quit_protects_unsaved_work(tmp_path):
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test() as pilot:
        app.query_one("#editor", TextArea).load_text('10 PRINT "keep"')
        await pilot.press("f10")
        assert app.screen.query_one("#discard")
        await pilot.press("escape")
        assert "keep" in app.query_one("#editor", TextArea).text


@pytest.mark.asyncio
async def test_open_failure_preserves_editor(tmp_path):
    (tmp_path / "broken.bas").write_bytes(b"\xff\x01\x02")
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test():
        before = app.query_one("#editor", TextArea).text
        app.open_file("broken.bas")
        assert app.query_one("#editor", TextArea).text == before
        assert "not supported" in app.status_text


@pytest.mark.asyncio
async def test_open_examples_dropdown_keyboard(tmp_path):
    from textual.widgets import Select

    examples = tmp_path / "examples"
    examples.mkdir()
    (examples / "zebra.bas").write_text('10 PRINT "Zebra"\n')
    (examples / "alpha.BAS").write_text('10 PRINT "Alpha"\n')
    (examples / "notes.txt").write_text("ignore")
    (examples / "folder.bas").mkdir()
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("f3")
        dropdown = app.screen.query_one("#examples", Select)
        assert dropdown.has_focus
        await pilot.press("enter", "down", "enter")
        await pilot.pause()
        assert app.screen.query_one("#filename", Input).value == "examples/alpha.BAS"
        rendered = "\n".join(strip.text for strip in app.screen._compositor.render_strips())
        assert all(ord(char) < 128 for char in rendered)
        await pilot.press("enter")
        await pilot.pause()
        assert "Alpha" in app.query_one("#editor", TextArea).text
        assert app.filename == "examples/alpha.BAS"


@pytest.mark.asyncio
async def test_open_empty_examples_allows_manual_filename(tmp_path):
    from textual.widgets import Select

    (tmp_path / "custom.bas").write_text("10 END\n")
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test() as pilot:
        await pilot.press("f3")
        assert app.screen.query_one("#examples", Select).disabled
        field = app.screen.query_one("#filename", Input)
        assert field.has_focus
        field.value = "custom.bas"
        await pilot.press("enter")
        await pilot.pause()
        assert app.filename == "custom.bas"


@pytest.mark.asyncio
@pytest.mark.parametrize("size, minimum_list_height", [((80, 24), 12), ((120, 40), 20)])
async def test_open_dialog_shows_more_files(tmp_path, size, minimum_list_height):

    folder = tmp_path / "examples"
    folder.mkdir()
    for number in range(30):
        (folder / f"example_{number:02}.bas").write_text("10 END\n")
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test(size=size) as pilot:
        await pilot.press("f3")
        dialog = app.screen.query_one("#dialog")
        assert dialog.region.width >= int(size[0] * 0.85)
        assert dialog.region.height >= int(size[1] * 0.85)
        assert app.screen.query_one("#accept").region.bottom <= size[1]
        await pilot.press("enter")
        overlay = app.screen.query_one("SelectOverlay")
        assert overlay.region.height >= minimum_list_height
        assert overlay.region.y >= 0
        assert overlay.region.bottom <= size[1]
        rendered = "\n".join(strip.text for strip in app.screen._compositor.render_strips())
        assert rendered.count("example_") >= minimum_list_height - 3
        await pilot.press("end", "enter")
        assert app.screen.query_one("#filename", Input).value == "examples/example_29.bas"
        await pilot.press("enter")
        await pilot.pause()
        assert app.filename == "examples/example_29.bas"


@pytest.mark.asyncio
async def test_save_dialog_remains_compact(tmp_path):
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("f2")
        assert app.screen.query_one("#dialog").region.width == 66
        assert app.screen.query_one("#dialog").region.height < 20
