# Ghost BASIC implementation plan

Goal: deliver the requested first milestone as working, independently implemented software.
Architecture: Python 3.12+, no runtime dependencies; tokenizer and AST parser feed a bounded,
step-oriented runtime. Console and confined disk adapters isolate effects. No Python eval/exec.
Spec: the user-supplied Ghost BASIC assignment, summarized in ARCHITECTURE.md.
Execution: inline, autonomous, as requested by the user; no design approval checkpoint.

## Acceptance tasks
- [x] Write behavioral tests for expressions, types, editing, control flow, arrays, data,
  errors, confinement and CLI; demonstrate failure before implementation.
- [x] Implement lexer.py, syntax.py, parser.py and values.py with explicit language semantics.
- [x] Implement program.py, devices.py, runtime.py, shell.py and cli.py.
- [x] Verify full tests, lint, strict typing, wheel installation and runnable examples.
- [x] Update compatibility, phase tracker, architecture, release and contributor documentation.

## Review focus
Colon-separated IF branches, nested loops, signed integer division, malformed input,
symlink/path escapes, infinite loops and stale state across RUN must have regression tests.

## Later milestones
The full eight-phase roadmap remains in ROADMAP.md. A partial feature is never evidence
that an entire phase is complete. Full QBasic, graphics/audio, IDE, AI and native packaging
require separate acceptance evidence.
