# Comparing against a reference BASIC

`tools/differential.py` runs independently written, ASCII BASIC probes in Ghost BASIC
and a separately installed reference interpreter. It compares stdout and stderr exactly
except for platform newline conversion. Spaces and prompts are significant. Both processes
must exit successfully; identical crashes are failures, not compatibility evidence.

Install the development environment, then run:

```sh
python tools/differential.py
python tools/differential.py --require-reference
```

The first command prints SKIP when no reference is configured. The second exits 2 in that
situation, suitable for a dedicated compatibility CI job. Ordinary pytest explicitly skips
its licensed-reference test without configuration while testing the harness and Ghost corpus.

Configure `GHOST_BASIC_REFERENCE_COMMAND` as a JSON array of arguments. Example shape:

```json
["/absolute/path/to/reference-adapter", "{program}"]
```

Alternatively pass that JSON string to `--reference`. No shell is used; arguments containing
spaces remain intact. Relative executable/script paths are unsuitable because every run uses
a fresh temporary working directory. `{program}` is replaced with an absolute ASCII source
file path. Standard input is delivered from the case's `inputs` field. The adapter must emit
only program output as UTF-8, send diagnostics to stderr, propagate errors as nonzero exit
codes, and exit after execution. DOS runtimes generally need a user-supplied emulator adapter
that handles loading, execution, encoding and removal of the interpreter's startup banner.
The adapter must also clean up any emulator child processes when terminated.

The default deadline is five seconds per process; override with `--timeout`. Only trusted
adapters should be configured: temporary directories are test isolation, not a security
boundary. Output is captured in memory; this is a small finite-probe harness, not a fuzzer
or an untrusted-process resource sandbox. Only ASCII probes are currently supported.

Exit codes: 0 = all comparisons matched (or optional unconfigured SKIP), 1 = at least one
mismatch/process failure, 2 = invalid configuration or missing required reference.
Failures print both observed results so spacing, diagnostics and exit status can be inspected.

The eight-case starter corpus in `tests/compatibility/cases.json` records each probe's keywords,
GW-BASIC manual URL and independently specified expected Ghost output. These are narrow
behavioral probes, not proof that a whole keyword or dialect is implemented. The full
GW-BASIC/QBasic authoritative manifest remains pending. No proprietary executable, GPL
implementation, or reference binary is included or downloaded by the tool.
