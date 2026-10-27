# Contributing

Use Python 3.12 or newer. Create a virtual environment and install `pip install -e '.[dev]'`.
Run `python -m pytest`, `ruff check src tests`, `ruff format --check src tests`, `mypy` and
`python -m build` before submitting changes. CI repeats these on Windows, macOS and Linux.

Start with a minimal BASIC program demonstrating the expected behavior. Cite the language
manual/dialect, add a failing behavioral test, implement the feature, run the entire suite,
and update COMPATIBILITY.md, ROADMAP.md, CHANGELOG.md and examples where applicable.
Test error paths, nested control flow, numeric boundaries and device limits. Do not replace
BASIC semantics with host Python evaluation. Avoid tests that merely mirror implementation.

Review existing architecture before refactoring. Keep UI, network and hardware effects out
of the parser and evaluator. Dependency and source licensing must preserve the MIT package;
never paste GPL reference code, ROM data or proprietary manual content. Differential tests
may use separately installed interpreters without bundling them.

Report security issues privately to the repository maintainer; a private contact channel
must be established before public hosting/release. Do not submit real credentials or data.

## Keyword help changes

Edit src/ghost_basic/data/keywords.json when adding/changing a keyword. Provide purpose,
syntax, named parameters, use cases, independent examples and implementation limits.
Mark non-executable planned features as planned and use reference-mode examples. Add
expected outputs based on independent reasoning, not values copied from a failing runtime.
Run `python tools/export_help.py` to regenerate docs/keywords, then the full test suite.
Keep supported status tied to actual acceptance tests; a help entry is not implementation.
