"""Searchable, ASCII-framed offline keyword reference for the terminal IDE."""

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, OptionList, Static, TextArea

from .help_topics import HelpTopic, catalog, get_topic, render_text, search_topics


class KeywordHelpScreen(ModalScreen[None]):
    BINDINGS = [Binding("escape", "close", "Close"), Binding("f1", "close", "Close")]
    DEFAULT_CSS = """
    #keyword-dialog {
        width: 96%; height: 94%; border: ascii #55ffff;
        background: #000080; padding: 0 1;
    }
    #help-title { height: 1; color: #ffff55; text-style: bold; }
    #help-search { height: 3; border: ascii #aaaaaa; background: #000020; color: #ffffff; }
    #help-body { height: 1fr; }
    #help-topics { width: 25; min-width: 16; height: 1fr; border: ascii #aaaaaa;
                   background: #000080; color: #ffffff; scrollbar-size: 0 0; }
    #help-topics:focus { border: ascii #55ffff; }
    #help-topics > .option-list--option { padding: 0 1; }
    #help-topics > .option-list--option-highlighted { background: #00aaaa; color: #000040; }
    #help-detail { width: 1fr; height: 1fr; border: ascii #aaaaaa;
                   background: #000020; color: #ffffff; scrollbar-size: 0 0; }
    #help-bottom { height: 3; }
    #help-hint { width: 1fr; height: 3; content-align: left middle; color: #55ffff; }
    #help-bottom #close { width: 12; height: 3; min-width: 12; margin: 0;
                         border: ascii #aaaaaa; background: #bbbbbb; color: #000040; }
    """

    def __init__(self, keyword: str | None = None) -> None:
        super().__init__()
        self.visible_topics = catalog()
        topic = get_topic(keyword or "KEYBOARD") or get_topic("KEYBOARD")
        assert topic is not None
        self.current_topic: HelpTopic = topic
        self.initial_query = keyword if keyword and get_topic(keyword) is None else ""

    def compose(self) -> ComposeResult:
        with Vertical(id="keyword-dialog"):
            yield Static("Ghost BASIC - Keyword reference", id="help-title", markup=False)
            yield Input(
                placeholder="Search keyword, function or use case (e.g. PRINT, loop)",
                id="help-search",
                max_length=120,
            )
            with Horizontal(id="help-body"):
                yield OptionList(
                    *(self.label(t) for t in self.visible_topics), id="help-topics", markup=False
                )
                yield TextArea(
                    render_text(self.current_topic),
                    id="help-detail",
                    read_only=True,
                    soft_wrap=True,
                    highlight_cursor_line=False,
                )
            with Horizontal(id="help-bottom"):
                yield Static(
                    "Tab: panels | Arrows: topics | PgDn/PgUp: page", id="help-hint", markup=False
                )
                yield Button("Close", id="close")

    @staticmethod
    def label(topic: HelpTopic) -> str:
        return topic.keyword + (" [planned]" if topic.status == "planned" else "")

    def on_mount(self) -> None:
        listing = self.query_one("#help-topics", OptionList)
        listing.border_title = " Keywords "
        self.query_one("#help-detail", TextArea).border_title = " Help page "
        listing.highlighted = self.visible_topics.index(self.current_topic)
        field = self.query_one("#help-search", Input)
        field.value = self.initial_query
        field.focus()

    @on(Input.Changed, "#help-search")
    def search_changed(self, event: Input.Changed) -> None:
        self.visible_topics = search_topics(event.value)
        listing = self.query_one("#help-topics", OptionList)
        listing.clear_options()
        listing.add_options(self.label(topic) for topic in self.visible_topics)
        listing.highlighted = 0 if self.visible_topics else None
        if self.visible_topics:
            self.show_topic(self.visible_topics[0])
        else:
            self.query_one("#help-detail", TextArea).load_text(
                "No matching help topics.\n\nTry PRINT, FOR, INPUT, MID$ or loop.\n"
                "Clear the search to restore all topics.\n"
            )

    def show_topic(self, topic: HelpTopic) -> None:
        self.current_topic = topic
        detail = self.query_one("#help-detail", TextArea)
        detail.load_text(render_text(topic))
        detail.scroll_home(animate=False)

    @on(OptionList.OptionHighlighted, "#help-topics")
    @on(OptionList.OptionSelected, "#help-topics")
    def topic_selected(
        self, event: OptionList.OptionHighlighted | OptionList.OptionSelected
    ) -> None:
        if 0 <= event.option_index < len(self.visible_topics):
            self.show_topic(self.visible_topics[event.option_index])

    @on(Button.Pressed, "#close")
    def action_close(self) -> None:
        self.dismiss(None)
