from io import StringIO
from pathlib import Path

import pytest

from ghost_basic.evaluator import FUNCTIONS
from ghost_basic.help_topics import catalog, get_topic, render_markdown, render_text, search_topics
from ghost_basic.parser import _PRECEDENCE
from ghost_basic.program import Program
from ghost_basic.runtime import Runtime
from ghost_basic.shell import Shell

WORDS = set(
    "PRINT INPUT LET IF THEN ELSE FOR TO STEP NEXT GOTO GOSUB RETURN WHILE WEND DIM DATA READ RESTORE END STOP REM CLS BEEP RUN LIST LOAD SAVE NEW CLEAR HELP SYSTEM QUIT EXIT NOT AND OR XOR EQV IMP MOD".split()
)


def test_all_implemented_keywords_have_complete_help():
    topics = {topic.keyword: topic for topic in catalog()}
    assert WORDS | FUNCTIONS | set(_PRECEDENCE) <= topics.keys()
    assert len(topics) == len(catalog())
    assert len({topic.slug for topic in catalog()}) == len(catalog())
    for topic in catalog():
        assert topic.summary and topic.syntax and topic.parameters
        assert topic.use_cases and topic.examples and topic.notes
        text = render_text(topic)
        assert all(
            title in text for title in ("Syntax", "Parameters", "Use cases", "Examples", "Notes")
        )
        assert topic.keyword in text
        assert "```basic" in render_markdown(topic)


def test_aliases_and_search():
    assert get_topic("?").keyword == "PRINT"
    assert get_topic("'").keyword == "REM"
    assert get_topic("  mid$ ").keyword == "MID$"
    assert get_topic("nonexistent") is None
    assert any(t.keyword == "FOR" for t in search_topics("loop"))
    assert [t.keyword for t in search_topics("mid$")] == ["MID$"]
    assert search_topics("nothingshouldmatchthis123") == ()
    assert len(search_topics("")) == len(catalog())


def test_planned_syntax_is_marked_as_not_implemented():
    for keyword in ("SUB", "FUNCTION", "OPEN", "PAINT"):
        topic = get_topic(keyword)
        assert topic.status == "planned"
        assert "Not implemented" in render_text(topic)
        assert "Not implemented" in render_markdown(topic)
        assert all(example.mode == "reference" for example in topic.examples)


def test_shell_help_topic():
    out = StringIO()
    shell = Shell(output=out)
    shell.submit("HELP PRINT")
    assert "Syntax" in out.getvalue()
    assert "PRINT" in out.getvalue()
    assert "Examples" in out.getvalue()
    out.seek(0)
    out.truncate()
    shell.submit("HELP ?")
    assert "PRINT" in out.getvalue()


def test_shell_help_index_and_unknown_topic():
    out = StringIO()
    shell = Shell(output=out)
    shell.submit("HELP")
    assert "HELP PRINT" in out.getvalue()
    assert "FOR" in out.getvalue()
    shell.submit("HELP nonexistingkeyword")
    assert "No matching help" in out.getvalue()


PROGRAM_EXAMPLES = [
    (topic, example)
    for topic in catalog()
    if topic.status != "planned"
    for example in topic.examples
    if example.mode == "program"
]


@pytest.mark.parametrize(
    "topic, example", PROGRAM_EXAMPLES, ids=[t.keyword for t, e in PROGRAM_EXAMPLES]
)
def test_supported_help_examples_execute(topic, example):
    output = StringIO()
    Runtime(output=output, input_stream=StringIO(example.inputs)).run(
        Program.from_source(example.source)
    )
    assert output.getvalue() == example.output


def test_generated_keyword_pages_match_catalog():
    directory = Path(__file__).resolve().parents[1] / "docs" / "keywords"
    assert (directory / "INDEX.md").is_file()
    for topic in catalog():
        assert (directory / f"{topic.slug}.md").read_text(encoding="utf-8") == render_markdown(
            topic
        )


def test_context_keyword_lookup():
    from ghost_basic.help_topics import keyword_at_cursor

    assert keyword_at_cursor("10 PRINT A", 5) == "PRINT"
    assert keyword_at_cursor("20 PRINT MID$(A$,2)", 11) == "MID$"
    assert keyword_at_cursor("10 PRINT A", 0) is None


def test_terminal_effects_are_displayed_without_executing_escape_codes():
    for keyword in ("CLS", "BEEP"):
        text = render_text(get_topic(keyword))
        markdown = render_markdown(get_topic(keyword))
        assert "\x1b" not in text and "\a" not in text
        assert "\x1b" not in markdown and "\a" not in markdown
        assert "\\x" in text


@pytest.mark.parametrize(
    "keyword", ["RUN", "LIST", "LOAD", "SAVE", "NEW", "CLEAR", "HELP", "SYSTEM", "QUIT", "EXIT"]
)
def test_environment_help_examples_execute(tmp_path, keyword):
    (tmp_path / "examples").mkdir()
    (tmp_path / "examples" / "hello.bas").write_text('10 PRINT "Hello"\n')
    output = StringIO()
    shell = Shell(root=tmp_path, output=output)
    topic = get_topic(keyword)
    last = True
    for line in topic.examples[0].source.splitlines():
        last = shell.submit(line)
        if not last:
            break
    if keyword in ("SYSTEM", "QUIT", "EXIT"):
        assert not last
    elif keyword == "SAVE":
        assert (tmp_path / "practice.bas").read_text() == '10 PRINT "Saved"\n'
    elif keyword == "NEW":
        assert shell.program.listing() == ""
    elif keyword == "LOAD":
        assert shell.program.listing() == '10 PRINT "Hello"\n'
    elif keyword == "CLEAR":
        assert output.getvalue() == " 0 \n"
    elif keyword == "HELP":
        assert "Syntax" in output.getvalue() and "Parameters" in output.getvalue()
    elif keyword == "RUN":
        assert output.getvalue() == "Run works\n"
    elif keyword == "LIST":
        assert output.getvalue() == '10 PRINT "Hello"\n'
