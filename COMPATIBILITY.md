# Compatibility report — 0.4.1

Target: GW-BASIC-style numbered source and immediate mode; QBasic is a planned extension.
No complete GW-BASIC, BASICA, PCjr, Tandy or QBasic compatibility is claimed. Tests assert
local behavior, not differential equivalence to an original interpreter.

| Capability | Status | Acceptance evidence / limitations |
| --- | --- | --- |
| Numbered source, replacement, deletion, sorted LIST | Implemented subset | program/shell tests; 0–65529 |
| Immediate execution, RUN, NEW, CLEAR, HELP, SYSTEM | Implemented subset | variables persist immediately, reset on RUN |
| LOAD / SAVE | Implemented subset | UTF-8 / DOS CP437 text loading, UTF-8 saving, confined root, failed LOAD preserves program; no tokenized/protected formats |
| PRINT / ? | Implemented subset | strings/numerics, semicolon, comma zones (14 columns); no USING, TAB, SPC or automatic screen wrap |
| INPUT | Implemented subset | optional quoted prompt, scalar/array targets, CSV fields; invalid input raises error rather than interactive retry |
| LET / implicit assignment | Implemented subset | explicit numeric/string coercion and defaults |
| IF THEN ELSE | Inline only | colons belong to branch; nested IF; literal line targets; no multiline IF |
| GOTO GOSUB RETURN | Implemented subset | line lookup, explicit return stack; no ON branch or RETURN line |
| FOR NEXT | Implemented subset | nested, signed STEP, skipped range, NEXT variable list; zero STEP rejected |
| WHILE WEND | Implemented subset | nested scans, skipped body and missing-terminator errors |
| END STOP | Partial | both halt; no CONT or resumable STOP |
| REM / apostrophe | Implemented | strings preserve embedded colons; comments end physical line |
| DIM, arrays | Implemented subset | zero-based inclusive bounds, multiple dimensions, implicit bounds 10; no OPTION BASE or REDIM |
| DATA READ RESTORE | Implemented subset | numeric/quoted string constants; RESTORE line; unquoted DATA strings unsupported |
| Operators | Implemented subset | + - * / ^ integer division MOD; comparisons; NOT AND OR XOR EQV IMP; left-associative power |
| Numeric representation | Approximation | 16-bit integer, IEEE single assignment, IEEE double arithmetic; no MBF or exact expression type propagation |
| String behavior | Approximation | Unicode Python strings, max 32767 chars; no CP437 byte semantics or MID$ assignment |
| BASIC errors | Implemented subset | source lines, syntax columns, arithmetic/types/bounds/data/control/file/budget errors; no ON ERROR/RESUME |
| Startup splash | Implemented | Animated ASCII ghost, automatic timeout, any-key/click skip, --no-splash; 80x24/120x40 and resize tests |
| Offline keyword help | Implemented | 175 topics; contextual/searchable F1, HELP keyword, --help-keyword and Markdown pages; planned topics explicitly reference-only |
| ASCII terminal UI | Implemented editor subset | Open with examples dropdown/save/new, unsaved and overwrite prompts, Run/Stop, INPUT and immediate commands; headless 80x24/120x40 plus manual TTY launch |
| Code Magic | Optional Cloud assistant | F8; remembered key/model, validity check, context toggle, syntax-check/repair, diff review, undo; tested with simulated HTTP, live inference requires a user key |
| Step API | Implemented | prepare/step, pc, instruction source line, variables; no breakpoint UI |
| CLS / BEEP | Terminal only | ANSI clear / ASCII bell; no virtual screen, backend tests or audio hardware claim |

## Implemented intrinsic inventory

ABS, INT, FIX, SQR, SIN, COS, TAN, ATN, LOG, EXP, SGN, CINT, CSNG, CDBL,
LEN, ASC, CHR$, STR$, VAL, LEFT$, RIGHT$, MID$, SPACE$, STRING$.

Arity, type errors and selected domain/boundary behavior are tested. VAL currently parses
a decimal numeric prefix only; no hex/octal VAL or embedded-space behavior. ASC/CHR$
operate on Unicode characters / codepoints 0–255 rather than DOS codepage bytes.
Hex/octal literals do not yet apply signed 16-bit reinterpretation. Formatting is approximate.
Unsuffixed literal arithmetic is double; arithmetic overflow/promotion differs from GW-BASIC.
Keywords cannot be packed into identifiers as in some tokenized legacy source forms.
The editor accepts unnumbered QBasic text for viewing/editing. Execution still requires
numbered source and rejects unnumbered programs with an explicit compatibility message.
CP437 is a fallback for BOM-less non-UTF-8 text, not general encoding detection; runtime
strings remain Unicode. A trailing DOS EOF marker and CRLF/CR line endings are normalized.

## Unsupported inventory and next acceptance targets

- Shell: AUTO, DELETE ranges, EDIT, RENUM, LIST ranges, MERGE, CHAIN, RUN filename,
  CONT, FILES and tokenized/protected SAVE/LOAD.
- Language: DEF FN, DEFINT/DEFSNG/DEFDBL/DEFSTR, SWAP, ON GOTO/GOSUB,
  ON ERROR/ERROR/ERR/ERL/RESUME, OPTION BASE, REDIM, LSET/RSET, PRINT USING,
  WRITE, LINE INPUT, RANDOMIZE/RND, INSTR, date/time and machine-specific functions.
- Disk: BASIC OPEN/CLOSE, sequential PRINT#/INPUT#/WRITE#/LINE INPUT#, EOF/LOF/LOC,
  binary/random GET/PUT/FIELD, MKI$/MKS$/MKD$/CVI/CVS/CVD, filesystem commands.
- QBasic: multiline IF/ELSEIF/END IF, DO/LOOP, EXIT, SELECT CASE, CONST,
  SUB/FUNCTION, CALL, DECLARE, local/shared/static scope, TYPE and long integers.
- Graphics/input: SCREEN, PSET/PRESET, POINT, LINE, CIRCLE, PAINT, DRAW, GET/PUT,
  PALETTE, VIEW/WINDOW, LOCATE/COLOR/WIDTH, INKEY$, keyboard/joystick/timer events.
- Audio: SOUND, PLAY, timing and synthesized optional backends.
- Machine: PEEK/POKE, DEF SEG, CALL/USR, ports, device extensions and ROM behavior.
  Require explicit virtualized capability design, never unrestricted host access.
- Product: full BASIC syntax highlighting, breakpoint/watch debugger UI, local Ollama mode, native installers.
- UI: execution requires numbered source, 80x24 minimum recommended; tiny layouts and advanced terminal
  emulators are not exhaustively tested. Thread cancellation is cooperative, not process isolation.

The inventory is a working backlog, not an exhaustive official language command catalog.
An official-manual-derived catalog and original-interpreter differential corpus are required
before reporting compatibility percentages. Every added feature needs tests, a sample where
applicable, documentation, and a row with evidence here.

## Learning gallery

Forty-two runnable examples, including ten patterns, three basic logic exercises and 22 input-based calculators, are
covered by exact-output tests in tests/test_examples.py, tests/test_patterns.py and tests/test_calculators.py. Pattern
exercises use only the implemented numbered BASIC subset; single-row cases and prime
boundaries are verified. See examples/README.md for learning steps and numeric limits.
