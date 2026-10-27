# SAVE

**Status:** Supported  
**Category:** Environment

Save the current source as UTF-8 text.

## Syntax

```basic
SAVE "filename"
```

## Parameters

- filename: quoted path inside the workspace.

## Use cases

- Keep changes to an exercise.

## Examples

### Example 1 (shell)

```basic
10 PRINT "Saved"
SAVE "practice.bas"
```

Expected output / effect:

```text
A UTF-8 source file is written.
```

## Notes

- Prompt SAVE can overwrite a file. The UI asks before Save as replaces a different existing file.
- No tokenized or protected SAVE format; opening a DOS file does not rewrite it.

[Back to keyword index](INDEX.md)
