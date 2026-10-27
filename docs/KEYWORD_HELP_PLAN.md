# Keyword help implementation plan

Goal: offline, implementation-accurate help for every currently implemented BASIC keyword,
intrinsic, operator and shell command, with explicitly labeled reference-only legacy topics.
Execute inline under the user's existing autonomy instruction.

Architecture: packaged JSON catalog -> typed help model -> ASCII terminal reference,
shell HELP topic output, and generated Markdown pages. No network calls at runtime.
Keep supported behavior grounded in parser/evaluator/runtime/shell source; legacy reference
syntax must never be presented as runnable in the current interpreter.

Files: help_topics.py (loading/search/render), keyword_help.py (UI), data/keywords.json
(content), tools/export_help.py and docs/keywords/*.md (offline pages). Small integrations
in tui.py/shell.py, package-data configuration, tests and user documentation.

- [x] Test catalog completeness, search, aliases, content structure and runnable examples.
- [x] Author explicit per-keyword purpose, syntax, parameters, use cases, examples and limits.
- [x] Implement searchable F1 browser, details, scroll, close and empty-search behavior.
- [x] Add HELP keyword in UI/shell and contextual F1 from the editor.
- [x] Generate pages, test installed-wheel data and run the full test/lint/type/build checks.

Review focus: planned-vs-supported labels; exact BASIC numeric/IF/string semantics;
missing packaged resources; punctuation aliases; safe rendering of code containing markup;
80x24 layout, keyboard navigation and preserving editor/runtime state when closing help.
