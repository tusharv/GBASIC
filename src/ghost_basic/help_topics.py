"""Offline keyword help shared by the UI, prompt and generated documentation."""

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from importlib.resources import files
from typing import Literal, TypedDict, cast

Status = Literal["supported", "partial", "planned", "guide"]
Mode = Literal["program", "shell", "reference"]


class _ExampleData(TypedDict):
    source: str
    inputs: str
    output: str
    mode: Mode


class _TopicData(TypedDict):
    keyword: str
    slug: str
    category: str
    status: Status
    summary: str
    syntax: str
    parameters: list[str]
    use_cases: list[str]
    examples: list[_ExampleData]
    notes: list[str]
    aliases: list[str]


@dataclass(frozen=True)
class HelpExample:
    source: str
    inputs: str
    output: str
    mode: Mode


@dataclass(frozen=True)
class HelpTopic:
    keyword: str
    slug: str
    category: str
    status: Status
    summary: str
    syntax: str
    parameters: tuple[str, ...]
    use_cases: tuple[str, ...]
    examples: tuple[HelpExample, ...]
    notes: tuple[str, ...]
    aliases: tuple[str, ...]

    @property
    def support_label(self) -> str:
        return {
            "supported": "Supported",
            "partial": "Supported subset",
            "planned": "Not implemented - reference only",
            "guide": "User guide",
        }[self.status]


@lru_cache(maxsize=1)
def catalog() -> tuple[HelpTopic, ...]:
    raw = cast(
        list[_TopicData],
        json.loads(files("ghost_basic").joinpath("data/keywords.json").read_text(encoding="utf-8")),
    )
    topics = [
        HelpTopic(
            keyword=t["keyword"],
            slug=t["slug"],
            category=t["category"],
            status=t["status"],
            summary=t["summary"],
            syntax=t["syntax"],
            parameters=tuple(t["parameters"]),
            use_cases=tuple(t["use_cases"]),
            examples=tuple(HelpExample(**e) for e in t["examples"]),
            notes=tuple(t["notes"]),
            aliases=tuple(t["aliases"]),
        )
        for t in raw
    ]
    return tuple(sorted(topics, key=lambda topic: topic.keyword))


def get_topic(keyword: str) -> HelpTopic | None:
    key = keyword.strip().upper()
    return next((t for t in catalog() if key == t.keyword or key in t.aliases), None)


def search_topics(query: str) -> tuple[HelpTopic, ...]:
    query = query.strip().upper()
    exact = get_topic(query)
    if not query:
        return catalog()
    matches = [
        t
        for t in catalog()
        if t != exact
        and query in " ".join((t.keyword, t.category, t.summary, *t.aliases, *t.use_cases)).upper()
    ]
    return tuple(([exact] if exact else []) + matches)


def keyword_at_cursor(line: str, column: int) -> str | None:
    for token in re.finditer(r"[A-Za-z][A-Za-z0-9]*[$%!#]?|<>|<=|>=|[?+*/\\^=<>;,:\-]", line):
        if token.start() <= column < token.end() or column == token.end():
            topic = get_topic(token.group())
            if topic:
                return topic.keyword
    return None


def _visible_output(text: str) -> str:
    """Show terminal-control effects as text rather than executing them in help."""
    return "".join(
        char if char.isprintable() or char in "\n\t" else f"\\x{ord(char):02x}" for char in text
    )


def render_text(topic: HelpTopic) -> str:
    lines = [
        f"{topic.keyword} - {topic.support_label}",
        f"Category: {topic.category}",
        "",
        topic.summary,
        "",
        "Syntax",
        "------",
        topic.syntax,
        "",
        "Parameters",
        "----------",
    ]
    lines.extend(f"- {p}" for p in topic.parameters)
    lines += [
        "",
        "Use cases",
        "---------",
        *(f"- {u}" for u in topic.use_cases),
        "",
        "Examples",
        "--------",
    ]
    for number, example in enumerate(topic.examples, 1):
        context = {
            "program": "numbered program",
            "shell": "BASIC prompt",
            "reference": "reference only",
        }[example.mode]
        lines += [f"Example {number} ({context}):", example.source]
        if example.inputs:
            lines += ["Input (one answer per line):", example.inputs.rstrip("\n")]
        if example.output:
            lines += ["Expected output / effect:", _visible_output(example.output).rstrip("\n")]
        lines.append("")
    lines += ["Notes", "-----", *(f"- {n}" for n in topic.notes)]
    if topic.aliases:
        lines += ["", "Aliases: " + ", ".join(topic.aliases)]
    return "\n".join(lines) + "\n"


def render_markdown(topic: HelpTopic) -> str:
    lines = [
        f"# {topic.keyword}",
        "",
        f"**Status:** {topic.support_label}  ",
        f"**Category:** {topic.category}",
        "",
        topic.summary,
        "",
        "## Syntax",
        "",
        "```basic",
        topic.syntax,
        "```",
        "",
        "## Parameters",
        "",
    ]
    lines += [f"- {p}" for p in topic.parameters]
    lines += ["", "## Use cases", "", *(f"- {u}" for u in topic.use_cases), "", "## Examples", ""]
    for number, e in enumerate(topic.examples, 1):
        lines += [f"### Example {number} ({e.mode})", "", "```basic", e.source, "```", ""]
        if e.inputs:
            lines += [
                "Input (one answer per line):",
                "",
                "```text",
                e.inputs.rstrip("\n"),
                "```",
                "",
            ]
        if e.output:
            lines += [
                "Expected output / effect:",
                "",
                "```text",
                _visible_output(e.output).rstrip("\n"),
                "```",
                "",
            ]
    lines += ["## Notes", "", *(f"- {n}" for n in topic.notes), ""]
    if topic.aliases:
        lines += ["Aliases: " + ", ".join(f"`{a}`" for a in topic.aliases), ""]
    lines += ["[Back to keyword index](INDEX.md)", ""]
    return "\n".join(lines)


def help_index() -> str:
    supported = ", ".join(t.keyword for t in catalog() if t.status in ("supported", "partial"))
    return (
        "Use HELP PRINT (or HELP followed by any keyword) for syntax, parameters and examples.\n"
        'Environment: RUN LIST NEW CLEAR LOAD "file" SAVE "file" SYSTEM\n'
        "Supported keywords, functions and operators:\n" + supported + "\n"
        "F1 opens the searchable reference in the terminal UI.\n"
    )
