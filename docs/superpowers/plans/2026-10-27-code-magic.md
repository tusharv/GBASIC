# Ollama Cloud Code Magic Implementation Plan

Goal: F8 opens an ASCII assistant that explains, debugs, writes and suggests BASIC code.
Architecture: an asynchronous HTTPS client, a bounded inspect/validate/repair agent, and a
right-side Textual panel (user steering), with compact modal key/model settings. The interpreter stays network-free. Requests are explicit; keys are
session-only or supplied by OLLAMA_API_KEY. Source and matching last-run output are optional
context. Proposed complete programs are reviewed as diffs, never auto-saved or executed.

Design decisions made under the user's request to implement the feature: direct Ollama Cloud
rather than a required local daemon; HTTPX for cancellable network I/O; plain explanations
plus one fenced BASIC program rather than provider-specific structured-output features.
A local syntax check and at most one corrective cloud call provide a bounded agent loop.
Syntax validity is not proof of correct runtime behavior. Full filesystem/shell tools are
unnecessary for the requested editor assistant.

Constraints: Python 3.12+, Textual 6.12, ASCII chrome, 80x24 support, fixed HTTPS provider,
no credentials in files/logs/model prompts, no automatic network on launch, two requests max
per Send, 120-second overall deadline, 60,000-character source and 128 KiB response bounds.

Review focus: keys never echoed; invalid or truncated output never applied; cancellation
closes the request; stale source cannot be overwritten; Ctrl+Z reverses an applied edit.

- [x] Add tests for the Cloud API contract, failures, response bounds and agent validation.
- [x] Implement ai.py client, supported-language prompt, response extraction and repair loop.
- [x] Add headless UI tests for setup, requests, review/apply/undo, errors and cancellation.
- [x] Implement magic.py and F8/menu integration; record source-specific run diagnostics.
- [x] Document key setup and limitations, update help/site, capture the actual Magic screen.
- [x] Run full tests, lint, type checks, package validation and visual checks; publish updates.
