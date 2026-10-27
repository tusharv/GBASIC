"""Portable CLI and prompt. AI is opt-in through the terminal editor."""

import argparse
import sys
from pathlib import Path

from .errors import BasicError
from .program import Program
from .shell import Shell
from .source import read_source


def main() -> int:
    parser = argparse.ArgumentParser(description="Ghost BASIC - offline BASIC environment")
    parser.add_argument("program", nargs="?", type=Path, help="UTF-8 or DOS CP437 BASIC source")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="LOAD/SAVE workspace root")
    parser.add_argument("--max-steps", type=int, default=100_000, help="instruction budget per RUN")
    parser.add_argument(
        "--help-keyword", metavar="KEYWORD", help="print the offline reference page for a keyword"
    )
    parser.add_argument("--version", action="version", version="Ghost BASIC 0.4.0")
    parser.add_argument("--no-splash", action="store_true", help="skip the startup ghost animation")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--ide", action="store_true", help="open the ASCII terminal editor")
    mode.add_argument("--shell", action="store_true", help="use the classic BASIC prompt")
    args = parser.parse_args()
    if args.max_steps < 1:
        parser.error("--max-steps must be positive")
    if args.help_keyword:
        from .help_topics import get_topic, render_text

        topic = get_topic(args.help_keyword)
        if topic is None:
            print(f"No matching help for {args.help_keyword}", file=sys.stderr)
            return 2
        print(render_text(topic), end="")
        return 0
    interactive = sys.stdin.isatty() and sys.stdout.isatty()
    if args.ide or (interactive and not args.shell and args.program is None):
        if not interactive:
            parser.error("the terminal UI requires an interactive terminal; use --shell for pipes")
        from .tui import GhostBasicApp

        GhostBasicApp(
            root=args.root,
            filename=str(args.program) if args.program else None,
            max_steps=args.max_steps,
            show_splash=not args.no_splash,
        ).run()
        return 0
    shell = Shell(root=args.root, max_steps=args.max_steps)
    if args.program:
        try:
            source = read_source(args.program)
            shell.runtime.run(Program.from_source(source))
        except (BasicError, OSError, UnicodeError) as error:
            print(error, file=sys.stderr)
            return 1
        except KeyboardInterrupt:
            print("Break", file=sys.stderr)
            return 130
        return 0
    print("Ghost BASIC 0.4.0\nType HELP for commands. SYSTEM exits.")
    while True:
        try:
            if not shell.submit(input("Ok\n")):
                return 0
        except EOFError:
            return 0
        except KeyboardInterrupt:
            print("\nBreak")
        except BasicError as error:
            print(error)
