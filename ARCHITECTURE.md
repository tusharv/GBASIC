# Architecture

## Intent and boundaries

Ghost BASIC is an independent Python 3.12+ implementation of a GW-BASIC-style
programming environment, ultimately extended with QBasic and modern interfaces.
The interpreter remains a tested language subset. Version 0.2 adds the ASCII terminal editor. The full project specification
remains the roadmap, including graphics, audio, a full debugger and offline AI.

## Chosen approach

A handwritten tokenizer, Pratt expression parser and recursive-descent statement parser
produce immutable AST nodes. IF branches compile to internal jumps. Numbered lines map to
instruction addresses. Runtime.step executes one instruction, with an explicit program
counter, return stack, FOR stack, variable store, array store and DATA cursor.

Alternatives considered: wrapping PC-BASIC would give strong legacy compatibility but
would change the requested independent MIT implementation into a GPL-dependent product;
translating BASIC into Python would obscure BASIC semantics and violate the no-eval/exec
constraint. An independent AST interpreter fits the initial milestone and permits later
backend and debugger work. These are engineering decisions made under the user's autonomy
instructions, not a claim of separately approved design.

## Module responsibilities

| Module | Responsibility |
| --- | --- |
| lexer | Tokens with columns; string and comment boundaries |
| syntax | Immutable expression and statement AST |
| parser | Precedence, statements, inline IF branches |
| values | Tagged INTEGER/SINGLE/DOUBLE/STRING, coercion, formatting |
| evaluator | Explicit operator and intrinsic dispatch |
| program | Numbered text source insertion/replacement/deletion |
| runtime | Compilation, bounded execution, variables, arrays, control stacks |
| source | Bounded shared UTF-8 / CP437 decoder and source reader |
| devices | Workspace-confined source LOAD and UTF-8 SAVE |
| shell | Program commands and immediate-mode state |
| execution | Cancellable interpreter worker, bounded input/output event queues |
| tui | ASCII-framed Textual editor, dialogs, output, input and file state |
| help_topics | Packaged catalog loading, aliases, search and plain/Markdown rendering |
| keyword_help | Searchable ASCII F1 topic list and read-only page viewer |
| splash | Skippable startup screen, ASCII frame rendering and owned animation timer |
| cli | Interactive UI by default on a TTY; explicit shell and batch modes |

The runtime accepts text streams for keyboard input and output and has no direct disk,
network, Python eval, Python exec or host process execution. Runtime.prepare and step allow
an embedding application to inspect variables and the next source line. This is a stepping
API, not a finished debugger. Future screen/audio protocols belong outside language parsing.

## Numeric model

Values are tagged. `%` is a signed 16-bit integer, `!` and unsuffixed variables are IEEE
single precision on assignment, `#` is IEEE double and `$` is a string. Numeric literals
and arithmetic currently use double precision unless a literal suffix specifies otherwise.
Assignment narrows explicitly, using nearest-even integer rounding. This is a documented
compatibility gap relative to GW-BASIC's expression typing and MBF representation.
Comparisons produce -1 or 0. Logical operators are signed 16-bit bitwise operations.

## Execution boundaries

Each RUN has a configurable instruction budget. Arrays have a cumulative 100,000-cell
capacity and strings a 32,767-character limit. LOAD reads at most 1 MB. Source LOAD/SAVE
resolves paths against a workspace root and rejects escapes, including existing symlinks.
These controls are not an OS security boundary: disk path checks have a potential concurrent
filesystem race, output streams can block, the host controls source size through the library,
and INPUT can wait indefinitely. Use a subprocess/container with OS memory, CPU, filesystem
and wall-time limits for hostile third-party code. No claim of hardened process isolation.

## Reference inspection and licenses

Reviewed 2026-10-27:

- [SharpBasic](https://github.com/sensboston/Basic), README, LICENSE and Basic.Core/Lexer.cs:
  MIT; demonstrates separate core/platform/CLI/web layers and a broad language inventory.
- [PC-BASIC](https://github.com/robhagemans/pcbasic), README, LICENSE.md and public session
  API structure: GPL-3.0-or-later; a behavioral reference for compatibility, MBF, legacy files
  and hardware, not a source-code dependency. No PC-BASIC code was copied.
- [Microsoft GW-BASIC](https://github.com/microsoft/GW-BASIC), README: MIT historical
  source reference; not a readily buildable modern runtime.
- [Textual](https://github.com/Textualize/textual): MIT-licensed UI dependency, tested with
  6.12.0. Its TextArea widgets, modal screens and headless test Pilot provide the terminal
  editor. The core package API can still execute BASIC without importing the UI module.
- Microsoft's GW-BASIC User's Guide preservation mirror was consulted for language target
  context; individual manual pages could not be reliably retrieved in this session. A full
  official manual inventory and QBasic documentation review are pending Phase 3/4 work.

No reference implementation code, fonts, ROMs or manuals are redistributed. All package
code here was independently written. External reference claims are not acceptance evidence
for Ghost BASIC; only local tests demonstrate this implementation's behavior.

## ASCII terminal UI (0.2)

The default interactive UI uses ASCII Textual borders and normal terminal monospace text.
TextArea provides editable numbered source and a separate read-only output pane. Modal
screens handle paths, overwrite confirmation and unsaved edits. Open includes an ASCII-styled
Select populated from Disk.example_programs(), with confined BASIC-only enumeration and a
manual filename fallback for missing/empty example folders. Files use the existing Disk
capability. Runtime input/output now have minimal structural protocols so terminal, in-memory
and queued UI adapters share the same engine.

ProgramRunner owns one daemon thread. The UI drains a bounded event queue every 30 ms;
only the UI thread touches widgets. A separate one-slot queue supplies INPUT values. Stop
sets a cancellation event checked between instructions, during input waits, and while output
is backpressured. UI runs have a 200,000-character output budget, and the display retains at
most that many characters. BASIC control escapes are filtered; text is never interpreted as
Rich markup. Immediate commands preserve the worker's variables. Normal Run resets them.

Threads provide responsiveness, not hardened process isolation. Cancellation is cooperative;
parsing a pathological source cannot yet be interrupted mid-parse. A future separate process
remains required for strong wall-time/memory isolation and the full debugger.

## Legacy text loading (0.2.2)

Disk LOAD, UI Open and batch execution share a bounded source reader. It tries UTF-8-sig
first, then CP437 for BOM-less invalid UTF-8; it normalizes line endings and a trailing DOS
EOF marker. UTF-8 BOM files with invalid payloads and tokenized/protected/binary files get
explicit diagnostics. This fallback is deliberately not a claim of universal encoding detection.

The editor loads plain source without requiring executable grammar, allowing legacy QBasic
files to be inspected and edited. Program.from_source remains the execution validation
boundary and reports unsupported unnumbered execution. SAVE explicitly writes UTF-8; no
read path rewrites or copies the user's source.

## Startup splash (0.2.3)

The interactive CLI opts into SplashScreen before editor interaction. A monotonic-clock
timer updates a clipped, ASCII-only ghost flight at 12.5 frames/second and closes the
screen after 5 seconds. Any key or click closes it immediately. Timers stop on skip or
unmount; the startup key is consumed and editor actions are blocked while the splash
is active. Initial file loading still populates the editor before the splash and its
state is preserved. --no-splash bypasses this screen. Shell and batch paths do not use it.
Embedding applications can opt into show_splash=True; its default is False so embedding
does not impose a presentation delay. No images, external assets or network calls needed.

## Offline keyword reference (0.3)

A packaged JSON catalog is the single content source for F1, HELP keyword, --help-keyword
and docs/keywords/*.md. Typed topic records carry status, syntax, parameters, use cases,
examples (including input/output), limitations and aliases. Catalog coverage tests assert
that every known statement/environment keyword, parser operator and evaluator intrinsic
has a page. Tests run the numbered-program examples and environment command snippets;
reference-only examples are intentionally excluded from execution.

KeywordHelpScreen uses OptionList search/navigation and a read-only TextArea for pages.
F1 resolves a keyword at the editor cursor where possible. Editor actions are suppressed
while help is open; closing restores editor focus without replacing source. The original
keyboard guide is an indexed topic. Search/aliases, empty results, small layouts and page
scrolling are tested. Control effects such as CLS/BEEP are escaped when rendered as help,
so reading documentation cannot execute terminal controls.

The catalog is bundled in source/wheel packages. tools/export_help.py regenerates the
Markdown reference. Legacy entries are independent summaries for understanding old files,
not copied manual content or evidence that those features are implemented.
