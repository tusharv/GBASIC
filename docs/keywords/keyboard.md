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
- Ctrl+S Save; Ctrl+O Open; Ctrl+N New; Ctrl+Q Quit; Ctrl+C Stop.
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
- Magic: Send shares the request and optional program/output with Ollama Cloud. Keys stay in the session; OLLAMA_API_KEY and OLLAMA_MODEL can configure it. Review Changes before Apply, Ctrl+Z to undo, F5 to test, F2 to save.

[Back to keyword index](INDEX.md)
