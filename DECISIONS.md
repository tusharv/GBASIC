# Engineering decisions

- 2026-10-27: independent MIT implementation, no PC-BASIC source reuse (GPL-3.0+).
- Zero runtime dependencies for the initial prompt; initially keep IDE/AI/backend dependencies optional. Superseded for UI in 0.2 below.
- Handwritten lexer/Pratt parser and immutable AST rather than Python eval/exec or translation.
- Numbered text is the first source format; QBasic source locations come before structured extensions.
- Public step API separates execution from future debugger/UI; source errors remain BASIC errors.
- Explicit tagged values, documented IEEE approximation; exact MBF/type propagation remain open work.
- Default bounded execution and confined source LOAD/SAVE. No claim of OS-level hostile-code isolation.
- Keep source editing text-based and defer parsing until RUN; failed LOAD replaces nothing.
- No runtime telemetry or internet requirement for BASIC execution. Optional Cloud AI added in 0.4 on explicit Send. No deceased-person simulation.
- Standard pytest/ruff/mypy/build tooling; CI defines three OSes but local results verify macOS only.

- 2026-10-27 (0.2): user requires an ASCII terminal UI. Textual 6.12.x is now a regular
  dependency so the normal installation launches the interface without an extra installation
  step. Batch and the language engine remain independent of UI imports.
- Use a background thread and bounded queues for Run/Stop/INPUT; keep future OS process
  isolation explicit. Do not run blocking INPUT on Textual's event loop.
- ASCII borders and no UI scrollbars preserve classic text appearance. Support 80x24 and
  larger terminals; source/output Unicode remains legal. Keep --shell and piped input stable.

- 2026-10-27 (0.2.2): legacy text uses UTF-8 first, then CP437 fallback when no BOM is
  present. Save remains UTF-8. Share loading policy across Disk/UI/batch and separate
  editor loading from executable-language validation. Reject binary formats explicitly.

## Code Magic (0.4)

The user explicitly requested Ollama Cloud with an API key, superseding the original local-only
AI preference. Use direct HTTPS with HTTPX async cancellation; retain the independent offline
interpreter. Session-only key entry/environment configuration avoids a new credential store.
No filesystem/shell tools: source context, compile checking and a single repair attempt are
enough for the requested companion. Every edit requires a reviewed diff and explicit Apply.
