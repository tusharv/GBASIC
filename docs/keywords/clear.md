# CLEAR

**Status:** Supported  
**Category:** Environment

Clear variables and arrays without deleting stored source.

## Syntax

```basic
CLEAR
```

## Parameters

- No arguments; classic memory-size arguments are not implemented.

## Use cases

- Reset immediate-mode calculations.

## Examples

### Example 1 (shell)

```basic
A=7
CLEAR
PRINT A
```

Expected output / effect:

```text
0
```

## Notes

- Supported as a prompt command, not as a numbered-program statement or the UI bottom-field command. Use RUN to reset before execution.

[Back to keyword index](INDEX.md)
