# Testing and verification

## Reproduce

Python 3.12+; install the development extra in an isolated environment:

```sh
python -m pip install -e '.[dev]'
python -m pytest -q
ruff check src tests
ruff format --check src tests
mypy
python -m build
```

## Local evidence — 2026-10-27

macOS ARM64, standalone CPython 3.12.0:

- **105 tests passed** in the full suite. Core semantic, error, editing, shell/disk,
  CLI/prompt, execution-step, intrinsic-inventory and seven example-gallery checks.
- Ruff lint and format checks passed; mypy strict mode passed for all 13 package modules.
- Both `ghost_basic-0.1.0-py3-none-any.whl` and `ghost_basic-0.1.0.tar.gz` built.
- Wheel installed without runtime dependencies into a separate virtual environment;
  installed CLI ran the hello sample from outside the checkout.
- Fibonacci sample executed through the installed CLI with the expected ten terms.
- Cross-platform CI is configured for Python 3.12/3.13/3.14 on Windows/macOS/Linux.
  CI has not been run remotely; those platforms are not claimed verified.

The source archive includes all documentation, tests and BASIC examples. The wheel contains
only the runtime and license/metadata; use the source archive/repository for the gallery.

## Regression discoveries

Additional tests exposed missing FOR/NEXT and WHILE/WEND termination diagnostics, giant
hex literal overflow leaking a host exception, oversized line-number conversion leaking
ValueError, cyclic filesystem links leaking RuntimeError, oversized string literals bypassing the
string limit, and command-prefix variable names being intercepted by LOAD/SAVE. Each was reproduced with a
failing regression test, fixed, and followed by a full green suite.

The very first attempted test run failed before collection: the machine's Anaconda 3.12.4
readline extension segfaulted when pytest enabled capture. Disabling capture allowed early
checks. A separate standalone CPython 3.12.0 environment ran ordinary pytest successfully;
the project-created `.venv` was rebuilt with that interpreter. This was an environment
failure, not evidence of language correctness. The suite contains no capture workaround.

## Test boundaries

Tests validate the implemented subset, not complete legacy compatibility. No original
GW-BASIC/QBasic executable differential run, Windows/Linux execution, virtual graphics/audio,
Textual UI, Ollama server, native installer, race-resistant disk isolation or long-duration
fuzzing was performed. Finite samples and fixed limits do not prove hardened sandboxing.

Follow-up testing: property-based lexer/parser fuzzing; official-manual acceptance corpus;
separately installed reference-interpreter comparisons; OS process resource isolation;
headless IDE/backend tests; all-OS wheel/install smoke tests in CI.

## ASCII UI verification — 0.2.0 (2026-10-27)

- Full suite: **125 tests passed**, including the previous language and gallery coverage.
- New independent worker tests cover normal output, BASIC errors, INPUT delivery, cancellation
  during input/compute, restart and output limits.
- New headless Textual tests cover ASCII frames at 80x24 and 120x40, editor/run/output,
  Open/Save, unsaved-edit cancellation/discard, overwrite confirmation/cancellation, INPUT,
  Stop, runtime diagnostics, path confinement, immediate statements, failed-open preservation,
  plain markup output, Help layout, resize and Quit protection.
- CLI tests verify --shell with pipes, --ide's terminal requirement, mutually exclusive mode
  flags and existing batch behavior.
- Manual pseudo-terminal smoke: default launch entered the full-screen ASCII interface and
  F10 returned cleanly with exit status 0. Inspected the composed editor/output layout using
  the Fibonacci sample. Help's Close button fits at 80x24.
- Ruff lint and format checks and strict mypy pass for 15 package modules.
- New 0.2.0 wheel and source archive built and the installed package smoke-tested.

Textual 6.12.0 and pytest-asyncio 1.4.1 were used locally with standalone CPython 3.12.0
on macOS ARM64. Live Windows/Linux terminal behavior, all terminal emulators, syntax
highlighting and a full debugger remain unverified/unimplemented. Previous notes about
having no UI tests apply to the historical 0.1 release only.

## Example picker verification — 0.2.1 (2026-10-27)

Full suite: **129 tests passed**. New regressions verify sorted case-insensitive `.bas`
discovery, directory/non-BASIC exclusion, escaping symlink rejection, missing/external
examples folders, keyboard dropdown selection through actual file loading, ASCII frame
glyphs, and manual opening with an empty picker. Inspected the expanded dropdown at 80x24.
Ruff lint/format and strict mypy pass; package artifacts rebuilt for 0.2.1.

## DOS text loading regression — 0.2.2 (2026-10-27)

**140 tests pass.** Synthetic CP437 fixtures cover the reported 0xDA box-drawing byte,
UTF-8 Unicode and BOM preservation, CRLF, DOS EOF, binary/tokenized rejection, unchanged
original bytes, UTF-8 SAVE, batch loading and headless opening of unnumbered QBasic source.
The actual user-supplied MONEY.BAS (46,225 bytes) was read and opened headlessly with
CP437 box-drawing characters intact, no initial dirty flag, and the expected explicit
unsupported-QBasic execution diagnostic. Verified original bytes remained unchanged; no
copy of the copyrighted file is included in this repository or package.

Ruff lint/format and strict mypy pass for 16 package modules. Compatibility of the complete
MONEY application is not claimed: unnumbered programs and QBasic procedures remain unsupported.

## Logic-building gallery — 2026-10-27

**166 tests passed.** Thirteen new BASIC examples have exact-output assertions and are
verified discoverable in the examples picker. All ten patterns are checked again at N=1;
prime checks include 1, 2 and the square 9. Outputs test spacing, newlines and counters,
not just successful exit. No interpreter behavior was changed to accommodate examples.
The source archive includes the exercises and their learning guide.

## Input-based calculators — 2026-10-27

**229 tests passed.** All 22 new calculators have hand-calculated output checks, invalid
numeric input checks and picker-discovery assertions. Additional boundaries cover zero
rates/years, compounding frequency, loss/break-even, savings rounding and completed goals,
negative budget balances, fractional people, temperature conversion, zero duration, grade
thresholds and both electricity slab edges. A headless UI test supplies four successive
INPUT answers to the compound-interest sample and verifies its final result. The gallery
contains 42 tested programs; source packaging includes both learning guides.

Local discovery also found the user's MONEY.BAS and NIBBLES.BAS imports. These are left
untouched and are not counted among the 42 tested learning samples. The source manifest
now selects the shipped learning examples and excludes these imported legacy files.

## Larger Open dialog — 2026-10-27

**232 tests pass.** New headless tests use 30 sample files at 80x24 and 120x40, verify
that Open fills most of the terminal, the expanded list displays more rows without going
off-screen, the final file remains keyboard-accessible, and Save stays compact. Manually
inspected the expanded 80x24 layout with the local example gallery.

## Animated startup splash — 0.2.3 (2026-10-27)

**242 tests pass.** Splash tests verify ASCII-only frames and horizontal movement, clipping
at small widths, title/animation at 80x24 and 120x40, opaque background, automatic editor
entry, any-key/click skip, shortcut interception, resize, timer cleanup through unmount,
embedding opt-out and preservation of an initially opened source file. CLI accepts
--no-splash. Manual GBASIC pseudo-terminal launch displayed the moving ghost, transitioned
to the editor and exited cleanly with F10. Lint/format and strict typing pass; local wheel
and source packages rebuilt. This animation needs no images, services or hardware backend.

Splash duration updated to 5 seconds. The automatic-transition regression verifies the
splash is still visible at 3 seconds and the editor is shown after 5 seconds; key/click
skipping remains covered by the existing suite.

## Offline keyword reference — 0.3.0 (2026-10-27)

**338 tests pass.** Coverage checks include every implemented statement/environment word,
all evaluator functions, all parser operators, aliases and content structure. Seventy-one
numbered examples and ten prompt command examples execute against the real engine/shell.
All 175 Markdown topic pages must match the shared catalog. Planned examples are clearly
labeled and not executed. Tests cover ASCII-safe control effects, searches/no matches,
contextual F1, read-only page scrolling, HELP keyword, CLI lookup and source preservation.

Headless layouts at 80x24 and 120x40 retain visible controls. Lint/format and strict mypy
pass for 19 modules. Local source and wheel artifacts include the catalog; installed-wheel
lookup and UI help are smoke-tested outside the checkout. Remote Windows/Linux CI remains
unexecuted in this session. Neither keyword pages nor reference examples imply full legacy
compatibility. A test initially used an unsupported Textual Ctrl+End binding; corrected it
to the documented PageDown navigation and verified real scrolling.
