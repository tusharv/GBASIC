# Changelog

## 0.4.1 — 2026-10-27

- Remember Ollama key/model in the native OS credential vault; reuse them on later launches.
- Show key validity in the sidebar, with explicit recheck and a hidden saved-key field.
- Distinguish invalid credentials from access, connectivity, quota and model errors.
- Add clickable official key instructions and the key-creation page.
- Keep session-only operation when the vault is unavailable, with clear storage feedback.

## 0.4.0 — 2026-10-27

- Add a right-side F8 Code Magic panel beside the current editor, with Ollama Cloud: Debug, Explain, Write and Suggest, with follow-up chat.
- Add session-only masked key/model settings and OLLAMA_API_KEY / OLLAMA_MODEL support.
- Share source and matching run diagnostics only on Send, with a context toggle.
- Compile-check proposals without running them; allow one bounded correction attempt.
- Review a complete diff before applying; preserve unsaved state and Ctrl+Z undo.
- Add cancellable asynchronous HTTPS, timeouts, response bounds and actionable provider errors.
- Add HTTP-contract and terminal UI tests, setup documentation and a real Magic screenshot.

## 0.3.0 — 2026-10-27

- Add 175 offline help topics with purpose, syntax, parameters, use cases, examples,
  expected output/effects and compatibility notes. Cover every implemented keyword,
  intrinsic, operator and shell command; mark planned legacy topics explicitly.
- Add searchable F1 reference, keyword-at-cursor help, keyboard guide, topic navigation,
  scrollable pages, HELP keyword in UI/prompt and --help-keyword for terminal use.
- Generate per-topic Markdown pages from the packaged catalog; test runnable examples
  and ensure generated pages stay synchronized. No runtime network calls.

## 0.2.3 — 2026-10-27

- Add a Ghost BASIC startup splash with a flying, bobbing ASCII ghost, automatic
  transition after 5 seconds, key/click skipping and --no-splash.
- Stop animation timers on exit; preserve startup source and block editor shortcuts
  during the splash so a skip key cannot open a hidden dialog or modify code.

- Add GBASIC as an additional installed command for the existing CLI.

- Enlarge Open to 90% of the terminal and allow the examples dropdown up to 65% of
  screen height. Save and other dialogs retain their compact sizes.

- Add 22 INPUT-based calculators: simple/compound interest and 20 everyday calculations,
  with validation, worked examples, formula comments and practice challenges.
- Verify default results, invalid inputs, boundary cases and successive INPUT values in the UI.

- Add ten beginner-friendly triangle/pattern exercises using nested FOR loops,
  alignment, conditions, counters and subroutines, plus sum, factorial and prime examples.
- Add a guided learning path, prediction challenges and exact-output/boundary tests.
- All examples appear automatically in the Open dropdown.

## 0.2.2 — 2026-10-27

- Fix loading DOS CP437 BASIC text (including box drawing) through UI, shell and batch.
- Shared bounded reader normalizes CRLF/CR and trailing DOS EOF, preserves UTF-8/BOM,
  and reports unsupported tokenized/protected/binary sources explicitly.
- Editor accepts unnumbered QBasic source for inspection; Run reports the current
  unnumbered-execution limitation instead of misleading file/encoding errors.
- Verified the reported MONEY.BAS file opens correctly without modifying the original.

## 0.2.1 — 2026-10-27

- Open dialog includes a keyboard/mouse examples dropdown, populated from the workspace
  examples directory. Filters BASIC files, sorts names, and preserves manual filename entry.
- Empty/missing examples folders leave manual opening available; paths remain confined.
- ASCII dropdown borders/arrows and UI/disk regression tests.

## 0.2.0 — 2026-10-27

- Default full-screen ASCII terminal UI in interactive terminals, using Textual.
- Numbered-source editor, Open/Save/Save as/New, unsaved-change and overwrite confirmation.
- Separate program output, responsive background Run/Stop, interactive INPUT and immediate
  statements, keyboard shortcuts, mouse menus and compact help.
- Explicit --ide and --shell modes; batch execution and pipes remain supported.
- Bounded output queues, UI output quotas, filtered control escapes and headless UI tests.
- Full debugger and syntax highlighting remain planned; existing language compatibility
  limitations still apply.

## 0.1.0 — 2026-10-27

- Initial independent Python package and command-line BASIC environment.
- Numbered source editing, immediate commands, bounded AST interpreter, tagged values,
  branching, loops, subroutines, arrays, data statements and selected intrinsics.
- Confined text LOAD/SAVE, source diagnostics and inspectable execution state.
- Runnable example gallery, automated regression suite, strict typing/linting and CI configuration.
- Compatibility gaps and complete eight-phase continuation roadmap documented.

## Website and README updates — 2026-10-27

- Add real editor, examples, keyword-help and splash screenshots to the README.
- Add a responsive static GitHub Pages landing page with screenshot tabs, examples,
  install instructions, copy controls and explicit compatibility limits.
- Add a Pages deployment workflow, local preview/deployment guide and reproducible
  screenshot capture tool with an optional CairoSVG extra.
