import pytest
from textual.widgets import Input, OptionList, TextArea

from ghost_basic.keyword_help import KeywordHelpScreen
from ghost_basic.tui import GhostBasicApp


@pytest.mark.asyncio
@pytest.mark.parametrize("size", [(80, 24), (120, 40)])
async def test_searchable_keyword_help(tmp_path, size):
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test(size=size) as pilot:
        await pilot.press("f1")
        assert isinstance(app.screen, KeywordHelpScreen)
        app.screen.query_one("#help-search", Input).value = "MID$"
        await pilot.pause()
        assert app.screen.query_one("#help-topics", OptionList).option_count == 1
        detail = app.screen.query_one("#help-detail", TextArea).text
        assert "MID$" in detail and "Parameters" in detail and "Examples" in detail
        assert app.screen.query_one("#close").region.bottom <= size[1]
        await pilot.press("escape")
        assert not isinstance(app.screen, KeywordHelpScreen)
        assert app.query_one("#editor", TextArea).has_focus


@pytest.mark.asyncio
async def test_help_empty_search_and_planned_keyword(tmp_path):
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test() as pilot:
        await pilot.press("f1")
        field = app.screen.query_one("#help-search", Input)
        field.value = "nomatches987654"
        await pilot.pause()
        assert "No matching" in app.screen.query_one("#help-detail", TextArea).text
        field.value = "SUB"
        await pilot.pause()
        listing = app.screen.query_one("#help-topics", OptionList)
        listing.focus()
        # Exact matches are ranked before substring matches such as GOSUB.
        await pilot.press("home", "enter")
        assert "Not implemented" in app.screen.query_one("#help-detail", TextArea).text
        await pilot.press("f1")
        assert not isinstance(app.screen, KeywordHelpScreen)


@pytest.mark.asyncio
async def test_context_help_preserves_source(tmp_path):
    source = '10 PRINT "help me"\n'
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test() as pilot:
        editor = app.query_one("#editor", TextArea)
        editor.load_text(source)
        editor.move_cursor((0, 5))
        await pilot.press("f1")
        assert app.screen.current_topic.keyword == "PRINT"
        await pilot.press("f5")
        assert not app.runner.running
        await pilot.press("escape")
        assert editor.text == source
        assert app.dirty


@pytest.mark.asyncio
async def test_help_topic_pages_scroll_and_keyboard_navigation(tmp_path):
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("f1")
        app.screen.query_one("#help-search", Input).value = "PRINT"
        await pilot.pause()
        details = app.screen.query_one("#help-detail", TextArea)
        details.focus()
        await pilot.press("pagedown", "pagedown")
        assert details.scroll_y > 0
        assert "Notes" in details.text
        await pilot.press("escape")
        assert app.query_one("#editor", TextArea).has_focus


@pytest.mark.asyncio
async def test_help_from_command_field(tmp_path):
    app = GhostBasicApp(root=tmp_path)
    async with app.run_test() as pilot:
        command = app.query_one("#command", Input)
        command.value = "HELP INPUT"
        command.focus()
        await pilot.press("enter")
        assert isinstance(app.screen, KeywordHelpScreen)
        assert app.screen.current_topic.keyword == "INPUT"
