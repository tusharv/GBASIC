# Roadmap and verified phase tracker

Updated 2026-10-31. The requested first milestone is the release gate; phases remain
partial until their full acceptance criteria are satisfied. No external blocker prevents
continued implementation; remaining work exceeds this first milestone's scope.

| Phase | Status | Delivered evidence | Remaining / next action |
| --- | --- | --- | --- |
| 1 Foundation | First milestone | package, prompt, tests, lint/type/build checks, 54 tested examples with pattern and calculator guides, docs and CI definition | execute CI on all three OSes, dependency lock/release policy, publish releases |
| 2 Core language | Tested subset | parser, values, execution, branching, loops, GOSUB, arrays, DATA; tests/test_core.py | exact type propagation, broader errors, differential corpus |
| 3 GW-BASIC | Early subset | editing, local source disk adapter, intrinsics | official command catalog; RND, ON, error handlers, sequential files, numeric fidelity, legacy file formats |
| 4 QBasic | Planned | shared core only | unnumbered source mapping; multiline IF; DO/LOOP; procedures, scopes, TYPE |
| 5 Graphics / sound | Tested graphics subset | 16-color framebuffer, SCREEN 7/9/12, pixels/lines/boxes/circles, POINT, F9 preview, PNG export, nine examples | additional drawing syntax, animation, keyboard and audio protocols/backends |
| 6 Terminal IDE | Tested editor subset | ASCII Textual editor, open/save/new, worker Run/Stop/INPUT, immediate commands, 175-topic searchable/contextual help and headless UI tests | full syntax highlighting, breakpoint/watch debugger, process isolation, Windows/Linux live terminal verification |
| 7 Ghost AI | Cloud companion implemented | F8 Debug/Explain/Write/Suggest, explicit Send, API-key/model setup, syntax-check/repair loop, diff/apply/undo, cancellable HTTP and headless tests | live user-key inference, optional local Ollama mode, semantic checks |
| 8 Release quality | In progress | local tests/lint/types/build/install, security limitations documented | cross-platform CI results, fuzz/differential tests, process isolation, native binaries, release signing |

## Precise continuation order

1. Build an authoritative GW-BASIC/QBasic statement/function manifest with manual URLs.
   Add subprocess differential tests against separately installed licensed reference runtimes;
   keep GPL code and reference binaries outside the distributed package.
   Delivered: opt-in subprocess comparison runner and eight manual-linked probes
   (`docs/DIFFERENTIAL_TESTING.md`). Full dialect manifest and actual licensed-reference
   execution remain pending; absent runtime configuration is explicitly skipped.
2. Fix numeric literal classification, expression promotion, signed hex/octal semantics and
   codepage-aware strings; lock each difference with independent behavioral tests.
   Delivered: literal classification, signed 16-bit hex/octal including short octal,
   unary precision preservation, precision-aware + - * /, ABS/INT/FIX result types,
   and three runnable numeric examples with regression/comparison cases. Exponentiation,
   remaining intrinsic type fidelity, MBF and codepage-aware runtime strings remain pending.
3. Add a disk capability API for sequential files, with handle limits, close-on-error,
   read/write quotas, EOF/LOF and traversal/symlink tests. Then implement matching BASIC syntax.
4. Add stable source locations for unnumbered programs and structured block AST nodes;
   implement multiline IF, DO/LOOP and SELECT CASE before procedures/scopes/TYPE.
5. Extend the delivered deterministic graphics API (docs/GRAPHICS.md): add remaining
   drawing syntax, keyboard/audio protocols and animation/display backends.
6. Extend the delivered Textual editor with a separate worker process and source-level
   debugger controller. Preserve headless persistence, cancellation and INPUT regression tests;
   add syntax highlighting, breakpoints, watches and execution highlighting.
7. Extend the delivered opt-in Ollama Cloud assistant with local Ollama support and richer
   semantic checks. Generated programs receive the same limits as handwritten programs.
8. Run CI, build/install artifacts on Windows/macOS/Linux, and create native launchers
   only after source-package behavior is stable. Do not label unsupported features compatible.

See TESTING.md for the exact local verification record and COMPATIBILITY.md for limitations.
