"""ASCII-framed, QBasic-inspired terminal editor using the shared BASIC engine."""

import re
from collections.abc import Callable
from pathlib import Path

from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Select, Static, TextArea

from .ai import AIContext, MagicAgent, validate_proposal
from .credentials import CredentialStore
from .devices import Disk
from .errors import BasicError
from .execution import ProgramRunner
from .help_topics import keyword_at_cursor
from .keyword_help import KeywordHelpScreen
from .magic import MagicEdit, MagicPanel, MagicSettingsScreen
from .splash import SplashScreen

_STARTER = '10 REM Welcome to Ghost BASIC\n20 PRINT "Hello, world!"\n30 END\n'
# Never interpret BASIC output as terminal escapes or Rich markup.
_ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def plain_output(text: str) -> str:
    text = _ANSI.sub("", text)
    return "".join(c for c in text if c in "\n\t" or (c.isprintable() and c != "\x7f"))


class FilenameScreen(ModalScreen[str | None]):
    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def __init__(self, mode: str, filename: str, examples: tuple[str, ...] = ()) -> None:
        super().__init__()
        self.mode = mode
        self.filename = filename
        self.examples = examples

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog", classes="open-dialog" if self.mode == "Open" else ""):
            yield Static(f"{self.mode} BASIC program", classes="dialog-title")
            if self.mode == "Open":
                yield Static("Programs in examples/:")
                yield Select[str](
                    [(Text(Path(name).name), name) for name in self.examples],
                    prompt="Choose an example" if self.examples else "No .bas files in examples/",
                    disabled=not self.examples,
                    id="examples",
                )
            yield Static("Filename relative to the workspace:")
            yield Input(self.filename, placeholder="examples/hello.bas", id="filename")
            with Horizontal(classes="dialog-buttons"):
                yield Button(self.mode, id="accept", variant="primary")
                yield Button("Cancel", id="cancel")

    def on_mount(self) -> None:
        if self.mode == "Open":
            self.query_one("#examples .down-arrow", Static).update("v")
            self.query_one("#examples .up-arrow", Static).update("^")
        if self.mode == "Open" and self.examples:
            self.query_one("#examples", Select).focus()
        else:
            self.query_one(Input).focus()

    @on(Select.Changed, "#examples")
    def example_selected(self, event: Select.Changed) -> None:
        if isinstance(event.value, str):
            self.query_one("#filename", Input).value = event.value
            self.query_one("#filename", Input).focus()

    @on(Input.Submitted)
    def accept_input(self) -> None:
        self.accept_file()

    @on(Button.Pressed, "#accept")
    def accept_file(self) -> None:
        name = self.query_one(Input).value.strip()
        if name:
            self.dismiss(name)

    @on(Button.Pressed, "#cancel")
    def action_cancel(self) -> None:
        self.dismiss(None)


class ConfirmScreen(ModalScreen[bool]):
    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def __init__(
        self, message: str, label: str = "Discard", title: str = "Unsaved changes"
    ) -> None:
        super().__init__()
        self.message = message
        self.label = label
        self.title_text = title

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Static(self.title_text, classes="dialog-title")
            yield Static(self.message, markup=False)
            with Horizontal(classes="dialog-buttons"):
                yield Button("Cancel", id="cancel", variant="primary")
                yield Button(self.label, id="discard")

    @on(Button.Pressed, "#discard")
    def discard(self) -> None:
        self.dismiss(True)

    @on(Button.Pressed, "#cancel")
    def action_cancel(self) -> None:
        self.dismiss(False)


class GhostBasicApp(App[None]):
    TITLE = "Ghost BASIC"
    ENABLE_COMMAND_PALETTE = False
    CSS = """
    Screen { background: #000080; color: #eeeeee; }
    #title { height: 1; background: #00aaaa; color: #000040; text-style: bold; padding: 0 1; }
    #menu { height: 1; background: #bbbbbb; }
    #menu Button { border: none; height: 1; min-width: 7; width: auto; padding: 0 1;
                   background: #bbbbbb; color: #000040; }
    #menu Button:focus, #menu Button:hover { background: #000080; color: #ffffff; }
    TextArea { border: ascii #aaaaaa; background: #000080; color: #ffffff;
               scrollbar-size: 0 0; padding: 0; }
    TextArea:focus { border: ascii #55ffff; }
    #workspace { height: 1fr; }
    #program { width: 1fr; height: 1fr; }
    #editor { height: 3fr; min-height: 7; }
    #output { height: 2fr; min-height: 5; background: #000020; }
    #command { height: 3; border: ascii #aaaaaa; background: #000020; color: #ffffff; }
    #command:focus { border: ascii #55ffff; }
    #status { height: 1; background: #00aaaa; color: #000040; padding: 0 1; }
    #shortcuts { height: 1; background: #bbbbbb; color: #000040; padding: 0 1; }
    ModalScreen { align: center middle; background: #000000 55%; }
    SplashScreen { background: #000080; }
    #dialog { width: 66; max-width: 95%; height: auto; max-height: 95%; padding: 1 2;
              border: ascii #55ffff; background: #000080; }
    #dialog.open-dialog { width: 90%; height: 90%; }
    #dialog.open-dialog SelectOverlay { max-height: 65vh; }
    .dialog-title { text-style: bold; color: #ffff55; margin-bottom: 1; }
    #dialog Input { border: ascii #aaaaaa; background: #000020; color: #ffffff; }
    #dialog SelectCurrent, #dialog Select:focus SelectCurrent {
        border: ascii #aaaaaa; background: #000020; color: #ffffff;
    }
    #dialog SelectOverlay {
        border: ascii #55ffff; background: #000020; color: #ffffff;
        max-height: 6; scrollbar-size: 0 0;
    }
    .dialog-buttons { height: 3; margin-top: 1; }
    .dialog-buttons Button, #close { border: ascii #aaaaaa; min-width: 12; margin-right: 2;
                                    background: #bbbbbb; color: #000040; }
    .dialog-buttons Button:focus, #close:focus { background: #00aaaa; }
    """
    BINDINGS = [
        Binding("f1", "help", "Help", priority=True),
        Binding("f2,ctrl+s", "save", "Save", priority=True),
        Binding("f3,ctrl+o", "open", "Open", priority=True),
        Binding("f4", "save_as", "Save as", priority=True),
        Binding("f5", "run", "Run", priority=True),
        Binding("f6,ctrl+c", "stop", "Stop", priority=True),
        Binding("f7", "command", "Command", priority=True),
        Binding("f8", "magic", "Magic", priority=True),
        Binding("ctrl+n", "new", "New", priority=True),
        Binding("f10,ctrl+q", "request_quit", "Quit", priority=True),
    ]

    def __init__(
        self,
        *,
        root: Path | None = None,
        filename: str | None = None,
        max_steps: int = 100_000,
        show_splash: bool = False,
        magic_agent: MagicAgent | None = None,
    ) -> None:
        super().__init__()
        self.show_splash = show_splash
        self.magic_agent = magic_agent or MagicAgent()
        self.credential_store = CredentialStore()
        self.ai_settings = self.credential_store.load()
        self.last_run_source: str | None = None
        self.disk = Disk(root or Path.cwd())
        self.filename = filename
        self.runner = ProgramRunner(max_steps=max_steps)
        self.saved_source = _STARTER
        self.output_text = ""
        self.status_text = "Ready | F3 Open a program | F1 Help"
        self.waiting_input = False
        self.run_had_error = False
        self.deferred: Callable[[], object] | None = None

    @property
    def dirty(self) -> bool:
        return self.query_one("#editor", TextArea).text != self.saved_source

    def compose(self) -> ComposeResult:
        yield Static("GHOST BASIC | Python BASIC programming environment", id="title", markup=False)
        with Horizontal(id="menu"):
            for label, action in [
                ("New", "new"),
                ("Open", "open"),
                ("Save", "save"),
                ("Save as", "save_as"),
                ("Run", "run"),
                ("Stop", "stop"),
                ("Help", "help"),
                ("Magic", "magic"),
                ("Quit", "quit"),
            ]:
                yield Button(label, id=f"menu-{action}", compact=True)
        with Horizontal(id="workspace"):
            with Vertical(id="program"):
                yield TextArea(_STARTER, id="editor", soft_wrap=False, tab_behavior="indent")
                yield TextArea(
                    "", id="output", read_only=True, soft_wrap=True, highlight_cursor_line=False
                )
                yield Input(
                    placeholder="Immediate BASIC command (F7) / program INPUT",
                    id="command",
                    max_length=32767,
                )
            yield MagicPanel(
                self.ai_settings,
                self.magic_agent,
                credential_store=self.credential_store,
                get_context=self.magic_context,
                apply_edit=self.magic_applied,
                close_panel=self.magic_closed,
            )
        yield Static(self.status_text, id="status", markup=False)
        yield Static(
            "F1 Help F2 Save F3 Open F4 SaveAs F5 Run F6 Stop F7 Input F8 Magic F10 Quit",
            id="shortcuts",
            markup=False,
        )

    def on_mount(self) -> None:
        self.query_one("#output", TextArea).border_title = " Program output "
        self.query_one("#command", Input).border_title = " Immediate / Input "
        if self.filename:
            name = self.filename
            self.filename = None
            self.open_file(name)
        self.update_title()
        self.query_one("#editor", TextArea).focus()
        self.set_interval(0.03, self.poll_execution)
        if self.show_splash:
            self.push_screen(SplashScreen(), self.splash_closed)

    def splash_closed(self, result: None) -> None:
        self.query_one("#editor", TextArea).focus()

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        if self.screen_stack and isinstance(self.screen, (SplashScreen, MagicSettingsScreen)):
            return False
        if (
            self.screen_stack
            and isinstance(self.screen, KeywordHelpScreen)
            and action in {"new", "open", "save", "save_as", "run", "stop", "command", "magic"}
        ):
            return False
        return super().check_action(action, parameters)

    def on_unmount(self) -> None:
        self.runner.stop()
        self.runner.join()

    @on(TextArea.Changed, "#editor")
    def editor_changed(self) -> None:
        self.update_title()

    def update_title(self) -> None:
        name = self.filename or "Untitled.bas"
        marker = " *" if self.dirty else ""
        self.query_one("#editor", TextArea).border_title = Text(f" {name}{marker} ")
        if self.magic_panel.is_mounted:
            self.magic_panel.refresh_context_label()

    def status(self, message: str) -> None:
        self.status_text = message
        self.query_one("#status", Static).update(message)

    def append_output(self, text: str) -> None:
        self.output_text = (self.output_text + plain_output(text))[-200_000:]
        output = self.query_one("#output", TextArea)
        output.load_text(self.output_text)
        output.scroll_end(animate=False)

    @on(Button.Pressed)
    def menu_pressed(self, event: Button.Pressed) -> None:
        name = event.button.id or ""
        if name.startswith("menu-"):
            action = name[5:]
            actions: dict[str, Callable[[], object]] = {
                "new": self.action_new,
                "open": self.action_open,
                "save": self.action_save,
                "save_as": self.action_save_as,
                "run": self.action_run,
                "stop": self.action_stop,
                "help": self.action_help,
                "magic": self.action_magic,
                "quit": self.action_request_quit,
            }
            actions[action]()

    def confirm_discard(self, action: Callable[[], object]) -> None:
        if self.dirty:

            def after_confirm(confirmed: bool | None) -> None:
                if confirmed:
                    action()

            self.push_screen(
                ConfirmScreen("Discard your unsaved edits? Save with F2 to keep them."),
                after_confirm,
            )
        else:
            action()

    def when_idle(self, action: Callable[[], object]) -> None:
        if self.runner.running:
            self.deferred = action
            self.runner.stop()
            self.status("Stopping program...")
        else:
            action()

    def action_new(self) -> None:
        self.confirm_discard(lambda: self.when_idle(self.new_file))

    def new_file(self) -> None:
        self.filename = None
        self.saved_source = ""
        self.query_one("#editor", TextArea).load_text("")
        self.update_title()
        self.status("New program | Enter numbered BASIC source")

    def action_open(self) -> None:
        self.confirm_discard(
            lambda: self.push_screen(
                FilenameScreen("Open", "", self.disk.example_programs()), self.open_file
            )
        )

    def open_file(self, name: str | None) -> None:
        if not name:
            return
        try:
            source = self.disk.read(name)
        except BasicError as error:
            self.status(str(error))
            return
        self.when_idle(lambda: self.replace_source(name, source))

    def replace_source(self, name: str, source: str) -> None:
        self.filename = name
        self.saved_source = source
        self.query_one("#editor", TextArea).load_text(source)
        self.update_title()
        self.status(f"Opened {name} | F5 Run")

    def action_save(self) -> None:
        if self.filename:
            self.save_file(self.filename)
        else:
            self.action_save_as()

    def action_save_as(self) -> None:
        self.push_screen(FilenameScreen("Save", self.filename or "untitled.bas"), self.save_file)

    def save_file(self, name: str | None, *, overwrite: bool = False) -> None:
        if not name:
            return
        try:
            path = self.disk.path(name)
            current = self.disk.path(self.filename) if self.filename else None
            if path.exists() and path != current and not overwrite:
                self.push_screen(
                    ConfirmScreen(f"Replace {name}?", "Replace", "File exists"),
                    lambda yes: self.save_file(name, overwrite=True) if yes else None,
                )
                return
            source = self.query_one("#editor", TextArea).text
            self.disk.write(name, source)
        except BasicError as error:
            self.status(str(error))
            return
        self.filename = name
        self.saved_source = source
        self.update_title()
        self.status(f"Saved {name}")

    def action_run(self) -> None:
        if self.runner.running:
            self.status("Already running | F6 Stop")
            return
        self.output_text = ""
        self.query_one("#output", TextArea).load_text("")
        self.start_execution(self.query_one("#editor", TextArea).text)

    def start_execution(self, source: str, *, immediate: bool = False) -> None:
        self.last_run_source = None if immediate else source
        self.run_had_error = False
        self.waiting_input = False
        self.runner.start(source, immediate=immediate)
        self.status("Running | F6 Stop")

    def action_stop(self) -> None:
        if self.runner.running:
            self.runner.stop()
            self.status("Stopping program...")

    def poll_execution(self) -> None:
        changed = ""
        for event in self.runner.drain():
            if event.kind == "output":
                changed += event.text
            elif event.kind == "input":
                self.waiting_input = True
                self.query_one("#command", Input).focus()
                self.status("Waiting for INPUT | Enter answer below | F6 Stop")
            elif event.kind in ("error", "stopped"):
                self.run_had_error = True
                changed += "\n" + event.text + "\n"
                self.status(event.text)
            elif event.kind == "done":
                self.waiting_input = False
                if not self.run_had_error:
                    self.status("Finished | F5 Run again")
        if changed:
            self.append_output(changed)
        if self.deferred and not self.runner.running:
            action, self.deferred = self.deferred, None
            action()

    def action_command(self) -> None:
        self.query_one("#command", Input).focus()

    @on(Input.Submitted, "#command")
    def command_submitted(self, event: Input.Submitted) -> None:
        text = event.value
        if self.waiting_input:
            self.runner.send_input(text)
            self.waiting_input = False
            event.input.value = ""
            self.append_output(text + "\n")
            self.status("Running | F6 Stop")
            return
        if self.runner.running:
            self.status("Program is running | F6 Stop")
            return
        if not text.strip():
            return
        event.input.value = ""
        command = text.strip().upper()
        if command == "RUN":
            self.action_run()
        elif command.startswith("HELP "):
            self.action_help(text.strip()[5:])
        elif command == "LIST":
            self.append_output(self.query_one("#editor", TextArea).text + "\n")
        elif command in ("NEW", "SYSTEM", "QUIT", "EXIT", "HELP"):
            {
                "NEW": self.action_new,
                "SYSTEM": self.action_request_quit,
                "QUIT": self.action_request_quit,
                "EXIT": self.action_request_quit,
                "HELP": self.action_help,
            }[command]()
        elif re.match(r'(LOAD|SAVE)(?=\s|"|$)', text, re.IGNORECASE):
            match = re.fullmatch(r'\s*(LOAD|SAVE)\s+"([^"\r\n]+)"\s*', text, re.IGNORECASE)
            if not match:
                self.status('Syntax error: use LOAD "file.bas" or SAVE "file.bas"')
            elif match[1].upper() == "LOAD":
                self.confirm_discard(lambda: self.open_file(match[2]))
            else:
                self.save_file(match[2])
        else:
            self.append_output("> " + text + "\n")
            self.start_execution(text, immediate=True)

    def action_help(self, keyword: str | None = None) -> None:
        if isinstance(self.screen, KeywordHelpScreen):
            self.screen.action_close()
            return
        if keyword is None:
            editor = self.query_one("#editor", TextArea)
            if editor.has_focus:
                row, column = editor.cursor_location
                lines = editor.text.splitlines()
                if row < len(lines):
                    keyword = keyword_at_cursor(lines[row], column)
        self.push_screen(KeywordHelpScreen(keyword), self.help_closed)

    def help_closed(self, result: None) -> None:
        self.query_one("#editor", TextArea).focus()

    @property
    def magic_panel(self) -> MagicPanel:
        return self.query_one(MagicPanel)

    def magic_context(self) -> AIContext:
        source = self.query_one("#editor", TextArea).text
        diagnostics = self.output_text if self.last_run_source == source else ""
        return AIContext(
            source, diagnostics, Path(self.filename or "Untitled.bas").name, self.dirty
        )

    def action_magic(self) -> None:
        if self.magic_panel.display:
            self.magic_panel.action_close()
            return
        if self.runner.running:
            self.status("Stop the program with F6 before opening Magic.")
            return
        context = self.magic_context()
        self.magic_panel.open_panel(has_error=bool(context.diagnostics and self.run_had_error))

    def magic_closed(self) -> None:
        self.query_one("#editor", TextArea).focus()

    def magic_applied(self, edit: MagicEdit) -> bool:
        editor = self.query_one("#editor", TextArea)
        if self.runner.running:
            self.status("Stop the program with F6 before applying Magic changes.")
            return False
        if editor.text != edit.original:
            self.status("Program changed since the suggestion. Send a new request to Magic.")
            return False
        if validate_proposal(edit.replacement):
            self.status("Magic suggestion failed the local syntax check; editor unchanged.")
            return False
        editor.history.checkpoint()
        editor.replace(edit.replacement, (0, 0), editor.document.end)
        editor.history.checkpoint()
        editor.focus()
        self.update_title()
        self.status("Magic applied | Ctrl+Z Undo | F5 Run to test | F2 Save")
        return True

    def action_request_quit(self) -> None:
        self.confirm_discard(lambda: self.when_idle(self.exit))
