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

## README screenshots and landing page — 2026-10-27

**344 tests pass.** New checks cover site links/fragments, image descriptions and dimensions,
README screenshot references including Splash, honest installation/compatibility copy,
static-only Pages upload configuration and runnable BASIC snippets. JavaScript syntax is
checked with Node. Four actual Textual captures were visually inspected after rendering to
PNG. Screenshot generation is optional and does not affect BASIC runtime dependencies.

Browser QA: desktop 1280px and mobile 390px layouts, no horizontal page overflow or broken
images, screenshot/Splash tabs, keyboard switching, installation platform tabs and successful
clipboard copy. The browser reported no JavaScript errors. GitHub Pages enablement requires
repository administration; publishing status is tracked separately from these local checks.

Public deployment: Pages run 40506709301 succeeded; the landing page, CSS, JavaScript and
splash screenshot returned HTTP 200 at https://tusharv.github.io/GBASIC/.

## Code Magic / right sidebar — 2026-10-27

**391 tests pass.** HTTPX MockTransport checks cover the direct Cloud request contract,
authentication/access/quota/model/network errors, malformed/oversized/truncated responses,
credential redaction, cancellation, bounded history/context and one syntax-repair attempt.
The API endpoint and model naming were verified against current Ollama documentation and
its public model list. No live inference was attempted: no Ollama API key was configured.

Headless terminal tests cover F8/right-side layout at 80x24 and 120x40, compact masked
Settings, no request on open, editing while a request is pending, current-source context,
review-before-apply, stale-source rejection, Ctrl+Z, unsaved state, cancellation, follow-ups,
and no implicit save/run. A full UI-to-HTTP-contract test uses a simulated provider response.
Real application captures were inspected; the right sidebar and code/output on the left are
visible together. Website gallery was checked at 390px and 1280px without horizontal overflow.

Ruff lint/format and strict mypy pass (21 modules); Node validates the unchanged gallery JS.
Version 0.4.0 source and wheel builds succeed. Credential/settings storage remains session-only.

Windows CI fixture correction: website checks explicitly read UTF-8, and the CP437 batch
reader test launches its subprocess in UTF-8 mode to match the parent output decoder.
This isolates source decoding from the host console locale; it does not change runtime I/O.

## Remembered Ollama keys and inline status — 2026-10-27

The full 405-test suite passes, plus the added native-vault backend rejection regression.
Key persistence is tested with an isolated in-memory vault across app instances; tests never
read or write real user credentials. Native macOS Keychain backend availability was checked
without accessing a saved secret. Live authenticated inference still requires a user key.

Coverage includes saved-key reuse, no repeated setup text, hidden saved-key input, replacement,
environment precedence, unavailable/corrupt vaults, rejection of plaintext backends, compact
80x24 settings, key-check requests without source/history, and valid/invalid/access-denied/
unverified states. HTTP 401 alone marks a provider-rejected key invalid; quota, server and
connection errors do not. Official key-guide and creation links are present in the UI.

## Default open-file Magic context — 2026-10-27

All 407 tests pass. Ruff lint/format and strict mypy also pass. Regression coverage
checks the open filename, unsaved editor text, file switching, default context on
reopening, and the outgoing request metadata. The updated Magic screenshot was
visually checked. Cloud requests use mocked responses; no live inference was tested.

## Differential harness — 2026-10-31

Full suite: **430 passed, 1 skipped** on local macOS. The skipped test is the explicit
licensed-reference comparison: no `GHOST_BASIC_REFERENCE_COMMAND` was configured.
Twelve new local tests exercise real subprocesses, exact spacing, CRLF normalization,
input delivery, temporary-directory isolation, failed processes, timeouts, invalid
configuration, required-reference mode, and five independently specified BASIC probes.
The initial nine harness tests failed before implementation and passed afterward.

Ruff lint/format checks and strict package mypy passed. Wheel and source archive built;
archive inspection confirmed the runner, tests and JSON corpus are included. The harness
is development tooling, intentionally outside the installed runtime package. See
`docs/DIFFERENTIAL_TESTING.md` for adapter setup and resource/child-process limitations.
No legacy compatibility result is claimed from the harness's Python subprocess tests.

## Numeric literals — 2026-10-31

Full suite: **469 passed, 1 skipped** (licensed reference not configured). Thirty-nine
new regression cases cover integer/single/double classification, E/D and suffix selection,
single rounding before CDBL, signed 16-bit hexadecimal and both octal prefixes, overflow,
invalid literals, unary signs, and DATA/READ/bitwise execution. Before implementation,
25 of these tests failed and 14 existing-behavior cases passed. The comparison corpus now
contains seven probes; all pass their local Ghost BASIC expected-output checks.

Ruff lint/format and strict mypy passed. A type-check failure caused by reusing an integer
local name for a float was corrected and rechecked, with all 39 focused cases passing.
An independent read-only code review found no substantive issues within this scope.
Binary arithmetic promotion, intrinsic result types, MBF and full numeric formatting
remain pending; no original-interpreter equivalence is claimed.

## Expression precision and numeric gallery — 2026-10-31

Full suite: **505 passed, 1 skipped**. The skipped comparison still requires a licensed
reference runtime. The new batch adds 36 tests: result kinds for +, -, *, / and ABS/INT/FIX;
integer overflow promotion; intermediate single rounding; mixed double operands;
assignment after rounding; BASIC errors; and exact output from three numeric examples.
Before implementation, 25 new tests failed and 11 existing-behavior cases passed.
The expanded eight-probe differential corpus also passed all local checks.

Ruff lint/format and strict mypy passed. Independent read-only review found no substantive
issues and ran all 75 numeric-literal/expression tests successfully. Wheel and source builds
passed; source archive inspection confirmed all three numeric_*.bas examples are shipped.
Exponentiation and remaining intrinsic precision, MBF and legacy-runtime comparisons
remain outside this verification claim.

## Graphics API and examples — 2026-10-31

Full suite: **536 passed, 1 skipped** (unconfigured licensed reference). Graphics coverage
includes 24 tests for raster primitives, clipping, color and mode validation, POINT,
RUN/immediate state, PNG CRC/decompression/CLI export, failed-export file preservation,
three examples, 80x24/120x40 preview layout, active-worker guards and modal shortcuts.
Seven newly runnable help examples are also checked by the help-example suite.
The initial 15 graphics tests failed before implementation. Preview/example tests also
failed before their implementation. Independent review exposed F9 stacking and unguarded
editor actions; a failing regression was added, then the modal behavior was fixed.

Lint/format and strict mypy pass for 24 modules. Wheel and source builds pass; archive
inspection verified the graphics modules and all three graphics examples. The shapes
example was exported to PNG and visually inspected. Live Windows/Linux terminals,
original interpreter raster equivalence, and animated drawing remain unverified.
Generated Markdown retains intentional hard-break spaces and exact BASIC output spacing.

## Expanded graphics gallery — 2026-10-31

Added six examples: house, checkerboard, bars, spiral, flower and skyline. Each executes
under 20,000 steps and has tests for expected console output, characteristic pixels,
mode and color diversity. All six rendered scenes were visually inspected; solid circular
fills use horizontal scanlines to avoid holes between concentric outlines.

Full suite: **542 passed, 1 skipped** (licensed reference unconfigured). Ruff lint/format
pass. Wheel/source builds pass; the source archive contains all nine graphics examples.
