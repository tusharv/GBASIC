# LIST

**Status:** Supported  
**Category:** Environment

Display stored numbered source in sorted order.

## Syntax

```basic
LIST
```

## Parameters

- No arguments; line ranges are not supported.

## Use cases

- Inspect a loaded program.

## Examples

### Example 1 (shell)

```basic
10 PRINT "Hello"
LIST
```

Expected output / effect:

```text
10 PRINT "Hello"
```

## Notes

- The UI lists the current editor text. LIST does not execute source.

[Back to keyword index](INDEX.md)
