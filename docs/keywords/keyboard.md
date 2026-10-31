# KEYBOARD

**Status:** User guide  
**Category:** Getting started

Navigate the editor, open a program, run it and enter answers without leaving the terminal.

## Syntax

```basic
F1 Help | F2 Save | F3 Open | F4 Save as | F5 Run | F6 Stop | F7 Input | F8 Magic | F10 Quit
```

## Parameters

- Function keys: use Fn if your keyboard reserves them.
- Ctrl+S Save; Ctrl+O Open; Ctrl+N New; Ctrl+Q Quit; F6 Stop.
- Alt+N New; Alt+O Open; Alt+S Save; Alt+A or Ctrl+Shift+S Save as.
- Alt+R Run; Alt+T Stop; Alt+H Help; Alt+M Magic; Alt+I Input; Alt+Q Quit.
- On macOS, enable Use Option as Meta key in your terminal for Alt shortcuts.
- If Ctrl+Shift+S is sent as Ctrl+S by your terminal, use Alt+A or F4 for Save as.
- Ctrl+C Copy selection; Ctrl+X Cut selection; Ctrl+V Paste. Shift+arrows select text.
- Tab/Shift+Tab: move focus; Tab in the editor inserts indentation.

## Use cases

- Find an example with F3 and run it with F5.
- Answer INPUT prompts in the bottom command field.
- Open F8 Magic to debug, explain, write or improve BASIC with your Ollama Cloud API key.

## Examples

### Example 1 (program)

```basic
10 INPUT "Name";N$
20 PRINT "Hello ";N$
```

Input (one answer per line):

```text
Ada
```

Expected output / effect:

```text
Name? Hello Ada
```

## Notes

- Escape or F1 closes this help. In the topic list use arrows; in the page use PageDown/PageUp.
- Open lists examples; choose a file, Enter to select, Enter again to open. Unsaved edits show *.
- Startup animation lasts 5 seconds; a key/click or --no-splash skips it.
- Syntax notation: [...] is optional, {...|...} means choose an alternative, and ... means repeat. Do not type notation brackets/braces unless a code example shows them literally.
- Magic: Send shares the request and optional program/output with Ollama Cloud. Keys are remembered in the OS credential vault; Settings > Save & check verifies access. OLLAMA_API_KEY and OLLAMA_MODEL can configure it. Review Changes before Apply, Ctrl+Z to undo, F5 to test, F2 to save.
- F9 opens the finished graphics screen as a scaled snapshot. Escape closes it.

[Back to keyword index](INDEX.md)
