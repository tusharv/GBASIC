# ASCII terminal interface

User request: Ghost BASIC should have an ASCII-based terminal UI. Implement directly
under the existing autonomous engineering instructions; retain the working interpreter.

Design: QBasic-inspired navy editor, cyan status strip, white source text, ASCII (+-|)
frames, monospace terminal text. A compact top menu and bottom shortcut strip frame a
numbered-source editor, output pane, runtime input and BASIC immediate command line.
Use Textual, as specified in the original project brief, instead of maintaining platform
specific raw-terminal input, screen diffing and editor code ourselves. Terminal monospace
serves every role; source, headers and shortcuts are differentiated by weight and color.

Interfaces: tui.py owns Textual screens, editor state, dialogs and shortcuts.
execution.py owns cancellable thread execution and bounded input/output event queues,
independent of Textual. Runtime/grammar stay shared with batch and shell modes.

Acceptance:
- [x] Failing tests for execution, input, stop, file operations, unsaved edits and headless UI.
- [x] Implement editor/open/save/new, run/stop/input/output, help and immediate commands.
- [x] Real TTY defaults to UI; --ide forces UI; --shell forces prompt; batch remains intact.
- [x] Verify headless layouts at 80x24 and larger; all frame glyphs ASCII.
- [x] Update docs, examples, full tests, lint/types and package artifacts.

Unsaved edits require discard confirmation before New/Open/Quit. Runtime input must not
block the UI. Stop cancels compute loops and input waits. BASIC output is treated as plain
text, with terminal control characters filtered. Editor/program output remain separate.

Limitations to report: this is an editor/run interface, not the full planned debugger;
advanced syntax highlighting, breakpoints and live watches remain separate acceptance tasks.
