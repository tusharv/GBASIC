"""Generate offline Markdown pages from the packaged keyword catalog."""

from pathlib import Path

from ghost_basic.help_topics import catalog, render_markdown


def export(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Ghost BASIC keyword reference",
        "",
        "Generated from the same offline catalog used by F1 and HELP keyword.",
        "",
        "Each page includes purpose, syntax, parameters, use cases, examples and notes.",
        "Support labels describe Ghost BASIC, not every historical BASIC dialect.",
        "Reference-only topics explain legacy source; their examples cannot run here.",
        "",
        "## Using help",
        "",
        "Press F1 for search, or enter HELP PRINT in the BASIC prompt.",
        "From a terminal: GBASIC --help-keyword PRINT. Escape/F1 closes the UI reference.",
        "",
        "## Topics",
        "",
        "| Keyword | Category | Ghost BASIC status |",
        "| --- | --- | --- |",
    ]
    for topic in catalog():
        (destination / f"{topic.slug}.md").write_text(render_markdown(topic), encoding="utf-8")
        name = topic.keyword.replace("|", "\\|")
        lines.append(f"| [{name}]({topic.slug}.md) | {topic.category} | {topic.support_label} |")
    lines += [
        "",
        "## Scope and sources",
        "",
        "The supported pages are grounded in this repository's parser, evaluator, runtime and shell.",
        "Runnable examples are executed by tests/test_keyword_help.py.",
        "Legacy pages are independently written reference summaries, not copied manual text.",
        "This is not an exhaustive catalog of every vendor extension or hardware-specific BASIC keyword.",
        "",
        "- [Original Microsoft GW-BASIC source reference](https://github.com/microsoft/GW-BASIC)",
        "- [Archived QBasic/QuickBASIC SUB manual entry](https://qbasic.net/en/qb-manual/Statement/SUB.htm)",
        "- [Archived SELECT CASE manual entry](https://qbasic.net/en/qb-manual/Statement/SELECT%20CASE.htm)",
        "- [Compatibility details](../../COMPATIBILITY.md)",
        "",
    ]
    (destination / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    export(Path(__file__).resolve().parents[1] / "docs" / "keywords")
