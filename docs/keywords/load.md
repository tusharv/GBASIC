# LOAD

**Status:** Supported  
**Category:** Environment

Load a text source file into the current program.

## Syntax

```basic
LOAD "filename"
```

## Parameters

- filename: quoted path inside the workspace (--root).

## Use cases

- Load a sample for execution.

## Examples

### Example 1 (shell)

```basic
LOAD "examples/hello.bas"
LIST
```

Expected output / effect:

```text
The file is loaded and listed.
```

## Notes

- UTF-8/BOM and DOS CP437 text supported; SAVE writes UTF-8. Tokenized/protected files are not supported.
- Prompt LOAD requires numbered source. The UI can open unnumbered QBasic text for editing, but cannot execute it.
- A failed LOAD keeps the existing source. Files are limited to 1 MB.

[Back to keyword index](INDEX.md)
