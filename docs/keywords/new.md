# NEW

**Status:** Supported  
**Category:** Environment

Start a new source program; the classic prompt also clears variables and arrays immediately.

## Syntax

```basic
NEW
```

## Parameters

- No arguments.

## Use cases

- Start a new exercise.

## Examples

### Example 1 (shell)

```basic
10 PRINT "old"
NEW
LIST
```

Expected output / effect:

```text
The program listing is empty.
```

## Notes

- Prompt NEW discards source immediately. The UI asks before discarding unsaved editor changes.
- In the UI, NEW replaces the editor buffer; the next RUN resets runtime variables.

[Back to keyword index](INDEX.md)
