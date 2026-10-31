# Differential compatibility testing implementation plan

Goal: deliver the subprocess comparison portion of ROADMAP.md continuation item 1.
Execute inline under the existing autonomous implementation instruction.

Architecture: a development-only Python runner invokes configured argument arrays without
shell expansion, in separate temporary directories, with deadlines. A small independently
written JSON corpus records manual URLs and expected output. Compare exact stdout after
newline normalization, exit status and stderr; never silently trim BASIC spacing.
No reference executable or external implementation is downloaded or distributed.

Scope: harness and starter corpus. A full authoritative dialect manifest, DOS/emulator
adapters, and actual licensed-reference verification remain separate pending work.

- [x] Test successful comparisons, whitespace mismatches, failures, deadlines, missing
  configuration, input delivery, path arguments containing spaces and directory isolation.
- [x] Implement tools/differential.py and tests/compatibility/cases.json with optional
  GHOST_BASIC_REFERENCE_COMMAND (JSON argv containing a {program} placeholder).
- [x] Test the corpus against Ghost BASIC and opt-in reference subprocesses.
- [x] Run full tests, lint, formatting, types and build; update roadmap/testing docs.

Review focus: accidental shell expansion; masking whitespace differences; passing on
nonzero exit; waiting indefinitely; claiming an absent reference runtime was tested.

Verification: 430 passed, 1 skipped; lint/format/types/build passed.
Final review: independent read-only reviewer checked the harness. Corpus packaging
was verified in the built sdist. Adapter child-process cleanup remains the adapter
responsibility, documented in the setup guide; a misbehaving adapter can leak children.
