"""ASCII Code Magic workspace: ask, inspect an answer, review a diff, then apply."""

from collections.abc import Callable
from dataclasses import dataclass
from difflib import unified_diff

from rich.text import Text
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Link, Static, TextArea

from .ai import (
    AIAccessError,
    AIAuthenticationError,
    AIContext,
    AIError,
    AIReply,
    AISettings,
    MagicAgent,
    redact,
    validate_proposal,
)
from .credentials import CredentialStore

DEFAULT_REQUESTS = {
    "Debug": "Find the cause of the error or bug. Explain it and propose a corrected program.",
    "Explain": "Explain this program, its control flow, and the key BASIC concepts it uses.",
    "Write": "Write a numbered BASIC program that prints a triangle using nested FOR loops.",
    "Suggest": "Suggest a useful improvement or next feature. Explain why it helps before proposing code.",
}


class SecretInput(Input):
    """Textual's password behavior with ASCII asterisks instead of bullets."""

    @property
    def _value(self) -> Text:
        return Text("*" * len(self.value), no_wrap=True, overflow="ignore", end="")


@dataclass(frozen=True)
class MagicEdit:
    original: str
    replacement: str


class MagicSettingsScreen(ModalScreen[AISettings | None]):
    BINDINGS = [Binding("escape", "close", "Close", priority=True)]
    DEFAULT_CSS = """
    #magic-settings-dialog { width: 62; max-width: 95%; height: auto;
        border: ascii #55ffff; padding: 1 2; background: #000080; }
    #magic-settings-dialog Input { border: ascii #aaaaaa; background: #000020; color: white; }
    #magic-settings-error { height: auto; color: #ffff55; }
    #magic-replace-key { height: 1; border: none; }
    #magic-settings-dialog Link { height: 1; }
    #magic-settings-buttons { height: 3; }
    #magic-settings-buttons Button { border: ascii #aaaaaa; width: 1fr; min-width: 10; }
    """

    def __init__(self, settings: AISettings) -> None:
        super().__init__()
        self.settings = settings

    def compose(self) -> ComposeResult:
        with Vertical(id="magic-settings-dialog"):
            yield Static("Ollama Cloud / settings", classes="dialog-title")
            yield Link(
                "How to get an Ollama API key",
                url="https://docs.ollama.com/cloud",
                id="magic-key-guide",
            )
            yield Link(
                "Create a key at ollama.com/settings/keys", url="https://ollama.com/settings/keys"
            )
            yield Static(
                "Key: " + (self.settings.key_status if self.settings.api_key else "Not added"),
                id="magic-settings-key-status",
                markup=False,
            )
            yield Button("Replace key", id="magic-replace-key", compact=True)
            yield SecretInput(
                "",
                password=True,
                placeholder="API key",
                id="magic-key",
                max_length=1024,
            )
            yield Input(
                self.settings.model, placeholder="Cloud model", id="magic-model", max_length=128
            )
            yield Static(
                "Save remembers the key in your OS credential store and checks Cloud access. The check sends no program code.",
                markup=False,
            )
            yield Static("", id="magic-settings-error", markup=False)
            with Horizontal(id="magic-settings-buttons"):
                yield Button("Save & check", id="magic-settings-save")
                yield Button("Cancel", id="magic-settings-cancel")

    def on_mount(self) -> None:
        self.query_one("#magic-key", Input).border_title = " API key "
        self.query_one("#magic-model", Input).border_title = " Cloud model "
        self.query_one("#magic-key", Input).display = not bool(self.settings.api_key)
        self.query_one("#magic-replace-key", Button).display = bool(self.settings.api_key)
        self.query_one("#magic-model" if self.settings.api_key else "#magic-key", Input).focus()

    @on(Button.Pressed, "#magic-replace-key")
    def replace_key(self) -> None:
        field = self.query_one("#magic-key", Input)
        field.display = True
        field.placeholder = "New API key (blank keeps existing)"
        field.focus()

    @on(Button.Pressed, "#magic-settings-save")
    def save_settings(self) -> None:
        settings = AISettings(
            self.query_one("#magic-key", Input).value.strip() or self.settings.api_key,
            self.query_one("#magic-model", Input).value.strip(),
        )
        try:
            settings.validate()
        except AIError as error:
            self.query_one("#magic-settings-error", Static).update(str(error))
            return
        self.dismiss(settings)

    @on(Button.Pressed, "#magic-settings-cancel")
    def action_close(self) -> None:
        self.dismiss(None)


WELCOME = (
    "Your BASIC companion\n\n"
    "Debug an error, explain a loop, write a feature, or suggest an improvement.\n\n"
    "Choose an action and type a request. A blank request uses that action's example.\n\n"
    "Use Settings for your Ollama key and model. Then Send.\n\n"
    "Review Changes before Apply. Code goes directly into the editor on the left.\n"
    "Ctrl+Z undoes. F5 tests. F2 saves.\n"
)


class MagicPanel(Vertical):
    BINDINGS = [
        Binding("escape", "close", "Close", priority=True),
        Binding("ctrl+enter", "send", "Ask", priority=True),
    ]
    DEFAULT_CSS = """
    MagicPanel { display: none; width: 42%; min-width: 34; max-width: 52;
        height: 1fr; border: ascii #55ffff; background: #000080; padding: 0 1; }
    #magic-title { height: 1; color: #ffff55; text-style: bold; }
    #magic-key-row { height: 1; }
    #magic-key-status { width: 1fr; height: 1; }
    #magic-get-key { height: 1; color: #55ffff; }
    #magic-privacy { height: 2; color: #bbbbbb; }
    #magic-prompt { height: 3; border: ascii #aaaaaa; background: #000020; color: white; }
    .magic-bar { height: 1; }
    .magic-bar Button { height: 1; min-width: 6; width: auto; padding: 0 1;
        border: none; background: #bbbbbb; color: #000040; }
    #magic-modes Button { width: 1fr; padding: 0; min-width: 7; }
    .magic-bar Button.chosen { background: #00aaaa; }
    .magic-bar Button:focus { background: #ffff55; color: #000040; }
    MagicPanel Button:disabled { opacity: 45%; }
    #magic-answer { height: 1fr; min-height: 3; background: #000020; }
    #magic-status { height: 2; color: #55ffff; }
    #magic-bottom Button { width: 1fr; padding: 0; }
    """

    def __init__(
        self,
        settings: AISettings,
        agent: MagicAgent,
        *,
        credential_store: CredentialStore,
        get_context: Callable[[], AIContext],
        apply_edit: Callable[[MagicEdit], bool],
        close_panel: Callable[[], None],
    ) -> None:
        super().__init__(id="magic-panel")
        self.credential_store = credential_store
        self.initial_check_done = False
        self.context_filename = ""
        self.context = AIContext("")
        self.settings = settings
        self.agent = agent
        self.get_context = get_context
        self.apply_edit = apply_edit
        self.close_panel = close_panel
        self.mode = "Explain"
        self.include_context = True
        self.busy = False
        self.reply: AIReply | None = None
        self.reviewed = False
        self.applied = False
        self.history: list[dict[str, str]] = []
        self.status_text = (
            "Ready | Choose an action." if settings.api_key else "Ready | Settings for API key."
        )
        self.request_id = 0

    def compose(self) -> ComposeResult:
        yield Static("CODE MAGIC / Ollama Cloud", id="magic-title")
        yield Static(
            "Send shares request + context\nwith Ollama Cloud.", id="magic-privacy", markup=False
        )
        with Horizontal(classes="magic-bar", id="magic-key-row"):
            yield Static("", id="magic-key-status", markup=False)
            yield Button("Check", id="magic-check-key", compact=True)
        yield Link("Get an Ollama API key", url="https://docs.ollama.com/cloud", id="magic-get-key")
        with Horizontal(classes="magic-bar", id="magic-options"):
            yield Button("Settings", id="magic-settings", compact=True)
            yield Button("Context: ON", id="magic-context", compact=True)
        with Horizontal(classes="magic-bar", id="magic-modes"):
            for mode in DEFAULT_REQUESTS:
                yield Button(
                    mode,
                    id=f"magic-{mode.lower()}",
                    compact=True,
                    classes="chosen" if mode == self.mode else "",
                )
        yield Input(placeholder="Ask Magic...", id="magic-prompt", max_length=4000)
        with Horizontal(classes="magic-bar", id="magic-views"):
            yield Button("Answer", id="magic-explanation", compact=True, classes="chosen")
            yield Button("Code", id="magic-code", compact=True, disabled=True)
            yield Button("Changes", id="magic-diff", compact=True, disabled=True)
        yield TextArea(
            self.welcome_text(),
            id="magic-answer",
            read_only=True,
            soft_wrap=True,
            highlight_cursor_line=False,
        )
        yield Static(self.status_text, id="magic-status", markup=False)
        with Horizontal(classes="magic-bar", id="magic-bottom"):
            yield Button("Send", id="magic-send", compact=True)
            yield Button("Cancel", id="magic-cancel", compact=True, disabled=True)
            yield Button("Apply", id="magic-apply", compact=True, disabled=True)
            yield Button("Close", id="magic-close", compact=True)

    def on_mount(self) -> None:
        self.refresh_key_status()
        self.query_one("#magic-prompt", Input).border_title = " Request "
        self.query_one("#magic-answer", TextArea).border_title = " Answer | PgDn/PgUp "

    def open_panel(self, *, has_error: bool = False) -> None:
        self.display = True
        self.include_context = True
        self.query_one("#magic-context", Button).label = "Context: ON"
        self.refresh_context_label()
        self.select_mode("Debug" if has_error else "Explain")
        self.query_one("#magic-prompt", Input).focus()
        self.refresh_key_status()
        if self.settings.api_key and not self.initial_check_done:
            self.initial_check_done = True
            if self.settings.key_status == "Not checked":
                self.action_check_key()

    def refresh_context_label(self) -> None:
        context = self.get_context()
        if self.context_filename != context.filename:
            self.history.clear()
            self.context_filename = context.filename
        label = self.query_one("#magic-privacy", Static)
        if self.include_context:
            name = context.filename or "Untitled.bas"
            marker = " *" if context.modified else ""
            # Keep the filename readable even in the 80-column sidebar.
            width = max(18, self.content_size.width or 30)
            available = max(8, width - 6 - len(marker))
            short = name if len(name) <= available else name[: available - 3] + "..."
            label.update(f"Send shares file with Cloud.\nFile: {short}{marker}")
            label.tooltip = f"{name}{marker} - latest editor text, including unsaved changes"
        else:
            label.update("Send shares request only.\nFile context is OFF.")
            label.tooltip = "No program, filename or run diagnostics will be sent."

    def welcome_text(self) -> str:
        if self.settings.api_key:
            return WELCOME.replace(
                "Use Settings for your Ollama key and model. Then Send.",
                "Your key is loaded. Choose an action and Send.",
            )
        return WELCOME

    def refresh_key_status(self) -> None:
        state = self.settings.key_status if self.settings.api_key else "Not added"
        color = "#55ff55" if state == "Valid" else "#ff5555" if state == "Invalid" else "#ffff55"
        self.query_one("#magic-key-status", Static).update(Text(f"Key: {state}", style=color))

    @on(Button.Pressed, "#magic-check-key")
    def action_check_key(self) -> None:
        if self.busy:
            return
        if not self.settings.api_key:
            self.status("No API key yet. Use Settings or Get key.")
            return
        self.settings.key_status = "Checking..."
        self.status("Checking key with Ollama Cloud...")
        self.refresh_key_status()
        self.request_id += 1
        self.set_busy(True)
        self.check_key(self.request_id)

    @work(group="magic", exclusive=True)
    async def check_key(self, request_id: int) -> None:
        try:
            await self.agent.check_key(AISettings(self.settings.api_key, self.settings.model))
            if request_id == self.request_id:
                self.settings.key_status = "Valid"
                self.status("Key valid | " + self.settings.storage)
        except AIError as error:
            self.key_check_failed(error)
            self.status(str(error))
            self.query_one("#magic-answer", TextArea).load_text(str(error))
        finally:
            if self.is_mounted and request_id == self.request_id:
                if self.settings.key_status == "Checking...":
                    self.settings.key_status = "Not checked"
                self.refresh_key_status()
                self.set_busy(False)

    def key_check_failed(self, error: AIError) -> None:
        if isinstance(error, AIAuthenticationError):
            self.settings.key_status = "Invalid"
        elif isinstance(error, AIAccessError):
            self.settings.key_status = "Access denied"
        elif self.settings.key_status != "Valid":
            self.settings.key_status = "Not checked"
        self.refresh_key_status()

    @on(Button.Pressed, "#magic-settings")
    def open_settings(self) -> None:
        self.app.push_screen(MagicSettingsScreen(self.settings), self.settings_closed)

    def settings_closed(self, settings: AISettings | None) -> None:
        if settings is not None:
            if self.settings.api_key != settings.api_key:
                self.settings.key_status = "Not checked"
            self.settings.api_key, self.settings.model = settings.api_key, settings.model
            self.credential_store.save(self.settings)
            self.history.clear()
            self.query_one("#magic-answer", TextArea).load_text(self.welcome_text())
            self.initial_check_done = True
            self.action_check_key()
        self.query_one("#magic-prompt", Input).focus()

    def select_mode(self, mode: str) -> None:
        self.mode = mode
        for button in self.query("#magic-modes Button"):
            button.set_class(button.id == f"magic-{mode.lower()}", "chosen")
        self.query_one("#magic-prompt", Input).placeholder = f"{mode}: describe your request..."

    def status(self, text: str) -> None:
        self.status_text = text
        self.query_one("#magic-status", Static).update(text)

    def set_busy(self, busy: bool) -> None:
        self.busy = busy
        for selector in (
            "#magic-send",
            "#magic-check-key",
            "#magic-options Button",
            "#magic-prompt",
            "#magic-modes Button",
        ):
            for widget in self.query(selector):
                widget.disabled = busy
        self.query_one("#magic-cancel", Button).disabled = not busy
        self.query_one("#magic-apply", Button).disabled = (
            busy
            or self.applied
            or not self.reviewed
            or self.reply is None
            or self.reply.proposal is None
            or self.reply.validation_error is not None
        )

    @on(Button.Pressed, "#magic-context")
    def toggle_context(self) -> None:
        self.include_context = not self.include_context
        self.history.clear()
        self.query_one("#magic-context", Button).label = (
            "Context: ON" if self.include_context else "Context: OFF"
        )
        self.refresh_context_label()
        self.status("Context changed; conversation cleared. Next Send uses this setting.")

    @on(Button.Pressed)
    def choose_mode_or_view(self, event: Button.Pressed) -> None:
        name = event.button.id or ""
        for mode in DEFAULT_REQUESTS:
            if name == f"magic-{mode.lower()}":
                self.select_mode(mode)
                self.query_one("#magic-prompt", Input).focus()
                return
        if name in {"magic-explanation", "magic-code", "magic-diff"}:
            self.show_view(name)

    def show_view(self, name: str) -> None:
        if self.reply is None:
            return
        for button in self.query("#magic-views Button"):
            button.set_class(button.id == name, "chosen")
        text = self.reply.explanation or "See the proposed program and changes."
        if name == "magic-code":
            text = self.reply.proposal or "No code proposed."
        elif name == "magic-diff":
            # The exact editor snapshot is compared, even if cloud context was disabled.
            text = (
                "\n".join(
                    unified_diff(
                        self.context.source.splitlines(),
                        (self.reply.proposal or "").splitlines(),
                        fromfile="current.bas",
                        tofile="proposed.bas",
                        lineterm="",
                    )
                )
                or "No changes."
            )
            self.reviewed = True
            self.set_busy(self.busy)
        text = redact(text, self.settings.api_key)
        answer = self.query_one("#magic-answer", TextArea)
        answer.load_text(text)
        answer.scroll_home(animate=False)

    @on(Input.Submitted, "#magic-prompt")
    @on(Button.Pressed, "#magic-send")
    def action_send(self) -> None:
        if self.busy:
            return
        settings = AISettings(self.settings.api_key, self.settings.model)
        try:
            settings.validate()
        except AIError as error:
            self.status("Check the API key/model in Settings.")
            self.query_one("#magic-answer", TextArea).load_text(str(error))
            return
        self.refresh_context_label()
        self.context = self.get_context()
        self.applied = False
        prompt = self.query_one("#magic-prompt", Input).value.strip() or DEFAULT_REQUESTS[self.mode]
        context = self.context if self.include_context else AIContext("")
        self.reply = None
        self.reviewed = False
        self.query_one("#magic-code", Button).disabled = True
        self.query_one("#magic-diff", Button).disabled = True
        self.query_one("#magic-answer", TextArea).load_text(
            "Working on your request...\nYou can cancel or close at any time."
        )
        self.request_id += 1
        self.set_busy(True)
        self.status("Asking Ollama Cloud...")
        self.request(settings, context, self.mode, prompt, self.request_id)

    @work(group="magic", exclusive=True)
    async def request(
        self,
        settings: AISettings,
        context: AIContext,
        mode: str,
        prompt: str,
        request_id: int,
    ) -> None:
        try:
            reply = await self.agent.ask(settings, context, mode, prompt, self.history, self.status)
            if request_id != self.request_id:
                return
            self.settings.key_status = "Valid"
            self.refresh_key_status()
            self.reply = reply
            history_reply = reply.explanation + (
                "\n```basic\n" + reply.proposal + "```" if reply.proposal else ""
            )
            self.history.extend(
                [
                    {"role": "user", "content": redact(prompt, settings.api_key)},
                    {
                        "role": "assistant",
                        "content": redact(history_reply, settings.api_key)[:12_000],
                    },
                ]
            )
            self.history = self.history[-6:]
            self.query_one("#magic-code", Button).disabled = reply.proposal is None
            self.query_one("#magic-diff", Button).disabled = reply.proposal is None
            self.show_view("magic-explanation")
            if reply.validation_error:
                self.status("Cannot apply: " + reply.validation_error)
                self.query_one("#magic-answer", TextArea).load_text(
                    reply.explanation + "\n\nLOCAL CHECK FAILED:\n" + reply.validation_error
                )
            elif reply.proposal:
                self.status("Syntax checked, not run. Review Changes, then Apply.")
            else:
                self.status("Answer ready. Ask a follow-up or choose another action.")
        except AIError as error:
            self.key_check_failed(error)
            self.status(str(error))
            self.query_one("#magic-answer", TextArea).load_text(str(error))
        finally:
            if self.is_mounted and request_id == self.request_id:
                self.set_busy(False)

    @on(Button.Pressed, "#magic-cancel")
    def cancel_request(self) -> None:
        self.request_id += 1
        self.workers.cancel_group(self, "magic")
        if self.settings.key_status == "Checking...":
            self.settings.key_status = "Not checked"
        self.refresh_key_status()
        self.set_busy(False)
        self.status("Cancelled. Your program is unchanged.")

    @on(Button.Pressed, "#magic-apply")
    def apply_proposal(self) -> None:
        if (
            not self.busy
            and not self.applied
            and self.reviewed
            and self.reply
            and self.reply.proposal
        ):
            error = validate_proposal(self.reply.proposal)
            if error:
                self.status("Cannot apply: " + error)
                return
            self.applied = self.apply_edit(MagicEdit(self.context.source, self.reply.proposal))
            if self.applied:
                self.set_busy(False)
                self.status("Applied to editor. Ctrl+Z undo. F5 test. F2 save.")
            else:
                self.status("Editor changed or running. Send again when ready.")

    @on(Button.Pressed, "#magic-close")
    def action_close(self) -> None:
        self.request_id += 1
        self.workers.cancel_group(self, "magic")
        if self.settings.key_status == "Checking...":
            self.settings.key_status = "Not checked"
        self.refresh_key_status()
        self.history.clear()
        self.reply = None
        self.reviewed = False
        self.applied = False
        self.set_busy(False)
        self.query_one("#magic-code", Button).disabled = True
        self.query_one("#magic-diff", Button).disabled = True
        self.query_one("#magic-answer", TextArea).load_text(self.welcome_text())
        self.query_one("#magic-prompt", Input).value = ""
        self.display = False
        self.close_panel()
