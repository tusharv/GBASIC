import asyncio

import pytest
from test_tui import settle
from textual.widgets import Button, Input, TextArea

from ghost_basic.ai import AIReply
from ghost_basic.magic import MagicSettingsScreen
from ghost_basic.tui import GhostBasicApp


class FakeAgent:
    def __init__(self, reply=None):
        self.reply = reply or AIReply("A fixed divisor.", "10 PRINT 10/2\n")
        self.calls = []
        self.started = asyncio.Event()
        self.cancelled = asyncio.Event()
        self.wait = False
        self.checks = 0

    async def check_key(self, settings):
        self.checks += 1

    async def ask(self, settings, context, mode, prompt, history=(), progress=None):
        self.calls.append((settings, context, mode, prompt, list(history)))
        self.started.set()
        if self.wait:
            try:
                await asyncio.Event().wait()
            finally:
                self.cancelled.set()
        return self.reply


async def configure(pilot, app):
    await pilot.click("#magic-settings")
    assert isinstance(app.screen, MagicSettingsScreen)
    app.screen.query_one("#magic-key", Input).value = "secret-test-key"
    await pilot.pause()
    rendered = "\n".join(strip.text for strip in app.screen._compositor.render_strips())
    assert "secret-test-key" not in rendered
    await pilot.click("#magic-settings-save")
    for _ in range(100):
        await pilot.pause(0.02)
        if not app.magic_panel.busy:
            break


async def send(pilot, app):
    if not app.ai_settings.api_key:
        await configure(pilot, app)
    await pilot.click("#magic-send")
    for _ in range(100):
        await pilot.pause(0.02)
        if not app.magic_panel.busy:
            return
    raise AssertionError("Magic did not finish")


@pytest.mark.asyncio
@pytest.mark.parametrize("size", [(80, 24), (120, 40)])
async def test_magic_review_apply_and_undo(tmp_path, size):
    agent = FakeAgent()
    app = GhostBasicApp(root=tmp_path, magic_agent=agent)
    async with app.run_test(size=size) as pilot:
        editor = app.query_one("#editor", TextArea)
        original = "10 PRINT 10/0\n"
        editor.load_text(original)
        await pilot.press("f5")
        await settle(pilot, app)
        await pilot.press("f8")
        assert app.magic_panel.display
        assert not agent.calls
        assert editor.region.right <= app.magic_panel.region.x
        assert editor.region.width >= size[0] // 2
        assert app.query_one("#output").region.width == editor.region.width
        await send(pilot, app)
        assert "Division by zero" in agent.calls[0][1].diagnostics
        assert editor.text == original
        assert app.magic_panel.query_one("#magic-apply", Button).disabled
        await pilot.click("#magic-diff")
        assert "+10 PRINT 10/2" in app.magic_panel.query_one("#magic-answer", TextArea).text
        assert app.magic_panel.query_one("#magic-close").region.bottom <= size[1]
        rendered = "\n".join(strip.text for strip in app.screen._compositor.render_strips())
        assert "secret-test-key" not in rendered
        assert all(ord(c) < 128 for c in rendered)
        await pilot.click("#magic-apply")
        await pilot.pause()
        assert editor.text == "10 PRINT 10/2\n"
        assert app.dirty
        assert not list(tmp_path.iterdir())
        assert not app.runner.running
        await pilot.press("ctrl+z")
        assert editor.text == original


@pytest.mark.asyncio
async def test_context_opt_out_and_editor_remains_usable(tmp_path):
    agent = FakeAgent()
    app = GhostBasicApp(root=tmp_path, magic_agent=agent)
    async with app.run_test() as pilot:
        await pilot.press("f8")
        await pilot.click("#magic-context")
        await send(pilot, app)
        assert agent.calls[0][1].source == ""
        editor = app.query_one("#editor", TextArea)
        editor.focus()
        before = editor.text
        await pilot.press("x")
        assert editor.text != before
        assert len(editor.text) == len(before) + 1
        assert app.magic_panel.display
        await pilot.press("f8")
        assert not app.magic_panel.display


@pytest.mark.asyncio
async def test_invalid_proposal_is_never_applicable(tmp_path):
    agent = FakeAgent(AIReply("Oops", "10 PRINT (", "Syntax error"))
    app = GhostBasicApp(root=tmp_path, magic_agent=agent)
    async with app.run_test() as pilot:
        original = app.query_one("#editor", TextArea).text
        await pilot.press("f8")
        await send(pilot, app)
        await pilot.click("#magic-diff")
        assert app.magic_panel.query_one("#magic-apply", Button).disabled
        await pilot.press("escape")
        assert app.query_one("#editor", TextArea).text == original


@pytest.mark.asyncio
async def test_close_cancels_network_and_preserves_source(tmp_path):
    agent = FakeAgent()
    agent.wait = True
    app = GhostBasicApp(root=tmp_path, magic_agent=agent)
    async with app.run_test() as pilot:
        original = app.query_one("#editor", TextArea).text
        await pilot.press("f8")
        await configure(pilot, app)
        await pilot.click("#magic-send")
        await asyncio.wait_for(agent.started.wait(), 1)
        await pilot.press("escape")
        await pilot.pause()
        assert agent.cancelled.is_set()
        assert app.query_one("#editor", TextArea).text == original


@pytest.mark.asyncio
async def test_stale_snapshot_is_not_applied(tmp_path):
    app = GhostBasicApp(root=tmp_path, magic_agent=FakeAgent())
    async with app.run_test() as pilot:
        editor = app.query_one("#editor", TextArea)
        await pilot.press("f8")
        await send(pilot, app)
        editor.load_text('10 PRINT "new edit"\n')
        await pilot.click("#magic-diff")
        await pilot.click("#magic-apply")
        assert "new edit" in editor.text
        assert "changed" in app.status_text.lower()


@pytest.mark.asyncio
async def test_missing_key_is_local_and_can_be_corrected(tmp_path, monkeypatch):
    monkeypatch.delenv("OLLAMA_API_KEY", raising=False)
    agent = FakeAgent()
    app = GhostBasicApp(root=tmp_path, magic_agent=agent)
    async with app.run_test() as pilot:
        await pilot.press("f8")
        await pilot.click("#magic-send")
        assert not agent.calls
        assert "API key" in app.magic_panel.status_text
        await pilot.pause(0.25)
        await send(pilot, app)
        assert len(agent.calls) == 1


@pytest.mark.asyncio
async def test_old_run_diagnostics_are_not_sent_for_new_source(tmp_path):
    agent = FakeAgent()
    app = GhostBasicApp(root=tmp_path, magic_agent=agent)
    async with app.run_test() as pilot:
        editor = app.query_one("#editor", TextArea)
        editor.load_text("10 PRINT 1/0")
        await pilot.press("f5")
        await settle(pilot, app)
        editor.load_text("10 PRINT 1")
        await pilot.press("f8")
        await send(pilot, app)
        assert not agent.calls[0][1].diagnostics


@pytest.mark.asyncio
async def test_cancel_then_send_again(tmp_path):
    agent = FakeAgent()
    agent.wait = True
    app = GhostBasicApp(root=tmp_path, magic_agent=agent)
    async with app.run_test() as pilot:
        await pilot.press("f8")
        await configure(pilot, app)
        await pilot.click("#magic-send")
        await asyncio.wait_for(agent.started.wait(), 1)
        assert app.magic_panel.query_one("#magic-send", Button).disabled
        await pilot.click("#magic-cancel")
        await pilot.pause(0.25)
        assert agent.cancelled.is_set()
        assert not app.magic_panel.busy
        agent.wait = False
        await send(pilot, app)
        assert len(agent.calls) == 2
        assert app.magic_panel.reply.proposal


@pytest.mark.asyncio
async def test_real_agent_http_contract_through_ui(tmp_path):
    import httpx

    from ghost_basic.ai import MagicAgent, OllamaCloudClient

    requests = []

    def handle(request):
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "done": True,
                "message": {"content": "Use a constant.\n```basic\n10 PRINT 5\n```"},
            },
        )

    app = GhostBasicApp(
        root=tmp_path,
        magic_agent=MagicAgent(OllamaCloudClient(transport=httpx.MockTransport(handle))),
    )
    async with app.run_test() as pilot:
        await pilot.press("f8")
        await pilot.click("#magic-write")
        app.magic_panel.query_one("#magic-prompt", Input).value = "Print five"
        await send(pilot, app)
        assert len(requests) == 2  # one key check, then the program request
        await pilot.click("#magic-diff")
        await pilot.click("#magic-apply")
        assert app.query_one("#editor", TextArea).text == "10 PRINT 5\n"


@pytest.mark.asyncio
async def test_network_error_keeps_dialog_usable(tmp_path):
    import httpx

    from ghost_basic.ai import MagicAgent, OllamaCloudClient

    app = GhostBasicApp(
        root=tmp_path,
        magic_agent=MagicAgent(
            OllamaCloudClient(transport=httpx.MockTransport(lambda r: httpx.Response(401)))
        ),
    )
    async with app.run_test() as pilot:
        await pilot.press("f8")
        await send(pilot, app)
        assert "API key" in app.magic_panel.query_one("#magic-answer", TextArea).text
        assert not app.magic_panel.query_one("#magic-send", Button).disabled
        assert app.magic_panel.query_one("#magic-apply", Button).disabled


@pytest.mark.asyncio
async def test_f8_closes_magic_and_running_program_blocks_open(tmp_path):
    app = GhostBasicApp(root=tmp_path, max_steps=100_000_000, magic_agent=FakeAgent())
    async with app.run_test() as pilot:
        await pilot.press("f8")
        assert app.magic_panel.display
        await pilot.press("f8")
        assert not app.magic_panel.display
        app.query_one("#editor", TextArea).load_text("10 GOTO 10")
        await pilot.press("f5", "f8")
        assert not app.magic_panel.display
        assert "F6" in app.status_text
        await pilot.press("f6")
        await settle(pilot, app)


@pytest.mark.asyncio
async def test_follow_up_uses_current_editor_and_settings_are_compact(tmp_path):
    agent = FakeAgent()
    app = GhostBasicApp(root=tmp_path, magic_agent=agent)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("f8")
        await pilot.click("#magic-settings")
        assert app.screen.query_one("#magic-settings-dialog").region.width < 80
        assert app.screen.query_one("#magic-settings-save").region.bottom <= 24
        await pilot.press("f5", "ctrl+n")
        assert isinstance(app.screen, MagicSettingsScreen)
        await pilot.press("escape")
        await send(pilot, app)
        editor = app.query_one("#editor", TextArea)
        editor.load_text('10 PRINT "latest"\n')
        await pilot.pause(0.25)
        await send(pilot, app)
        assert agent.calls[-1][1].source == editor.text
        assert len(agent.calls[-1][4]) == 2
        await pilot.press("f8")
        assert not app.magic_panel.display
        assert not app.magic_panel.history
        await pilot.press("f8")
        assert app.ai_settings.api_key == "secret-test-key"


@pytest.mark.asyncio
async def test_can_edit_while_magic_thinks_then_reject_stale_apply(tmp_path):
    agent = FakeAgent()
    agent.wait = True
    app = GhostBasicApp(root=tmp_path, magic_agent=agent)
    async with app.run_test() as pilot:
        await pilot.press("f8")
        await configure(pilot, app)
        await pilot.click("#magic-send")
        await asyncio.wait_for(agent.started.wait(), 1)
        editor = app.query_one("#editor", TextArea)
        editor.focus()
        before = editor.text
        await pilot.press("x")
        assert len(editor.text) == len(before) + 1
        assert app.magic_panel.busy
        await pilot.press("f8")
        await pilot.pause()
        assert agent.cancelled.is_set()
        assert not app.magic_panel.display


@pytest.mark.asyncio
async def test_saved_key_is_reused_across_app_restarts_without_prompt(tmp_path):
    first = GhostBasicApp(root=tmp_path, magic_agent=FakeAgent())
    async with first.run_test() as pilot:
        await pilot.press("f8")
        await configure(pilot, first)
        assert first.ai_settings.key_status == "Valid"
        assert first.ai_settings.storage == "Saved securely"
    agent = FakeAgent()
    second = GhostBasicApp(root=tmp_path, magic_agent=agent)
    async with second.run_test(size=(80, 24)) as pilot:
        await pilot.press("f8")
        await pilot.pause()
        assert second.ai_settings.api_key == "secret-test-key"
        assert second.ai_settings.key_status == "Valid"
        assert agent.checks == 1
        assert (
            "Use Settings for your Ollama key"
            not in second.magic_panel.query_one("#magic-answer", TextArea).text
        )
        await pilot.press("f8", "f8")
        assert agent.checks == 1
        await pilot.click("#magic-settings")
        assert not second.screen.query_one("#magic-key", Input).display
        assert second.screen.query_one("#magic-key", Input).value == ""
        assert second.screen.query_one("#magic-replace-key", Button).display
        assert second.screen.query_one("#magic-settings-save").region.bottom <= 24


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status,expected",
    [(401, "Invalid"), (403, "Access denied"), (429, "Not checked"), (503, "Not checked")],
)
async def test_key_status_distinguishes_authentication_from_service_failures(
    tmp_path, status, expected
):
    import httpx

    from ghost_basic.ai import MagicAgent, OllamaCloudClient

    app = GhostBasicApp(
        root=tmp_path,
        magic_agent=MagicAgent(
            OllamaCloudClient(transport=httpx.MockTransport(lambda r: httpx.Response(status)))
        ),
    )
    async with app.run_test() as pilot:
        await pilot.press("f8")
        await configure(pilot, app)
        assert app.ai_settings.key_status == expected
        assert app.magic_panel.query_one("#magic-close").region.bottom <= 24


@pytest.mark.asyncio
async def test_get_key_links_and_replace_saved_key(tmp_path):
    from textual.widgets import Link

    app = GhostBasicApp(root=tmp_path, magic_agent=FakeAgent())
    async with app.run_test() as pilot:
        await pilot.press("f8")
        assert (
            app.magic_panel.query_one("#magic-get-key", Link).url == "https://docs.ollama.com/cloud"
        )
        await configure(pilot, app)
        await pilot.click("#magic-settings")
        assert app.screen.query_one("#magic-key-guide", Link).url == "https://docs.ollama.com/cloud"
        await pilot.click("#magic-replace-key")
        app.screen.query_one("#magic-key", Input).value = "replacement-key"
        await pilot.click("#magic-settings-save")
        await pilot.pause()
        assert app.ai_settings.api_key == "replacement-key"
        assert app.credential_store.load().api_key == "replacement-key"


@pytest.mark.asyncio
async def test_open_file_context_defaults_on_includes_unsaved_edits_and_tracks_file_switch(
    tmp_path,
):
    from textual.widgets import Static

    (tmp_path / "first.bas").write_text("10 PRINT 1\n")
    (tmp_path / "second.bas").write_text("10 PRINT 2\n")
    agent = FakeAgent()
    app = GhostBasicApp(root=tmp_path, filename="first.bas", magic_agent=agent)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("f8")
        assert app.magic_panel.include_context
        assert "first.bas" in str(app.magic_panel.query_one("#magic-privacy", Static).render())
        app.query_one("#editor", TextArea).load_text("10 PRINT 3\n")
        await send(pilot, app)
        context = agent.calls[-1][1]
        assert context.filename == "first.bas"
        assert context.source == "10 PRINT 3\n"
        assert context.modified is True
        await pilot.click("#magic-context")
        await pilot.press("f8", "f8")
        assert app.magic_panel.include_context
        app.replace_source("second.bas", "10 PRINT 2\n")
        await pilot.pause(0.25)
        assert "second.bas" in str(app.magic_panel.query_one("#magic-privacy", Static).render())
        await send(pilot, app)
        assert agent.calls[-1][1].filename == "second.bas"
        assert agent.calls[-1][1].source == "10 PRINT 2\n"
        assert agent.calls[-1][1].modified is False
