# STR$

**Status:** Supported  
**Category:** Functions

Convert a number to text with a leading space for a nonnegative value.

## Syntax

```basic
STR$(number)
```

## Parameters

- number: numeric expression.

## Use cases

- Concatenate a number into a label.

## Examples

### Example 1 (program)

```basic
10 PRINT "["+STR$(12)+"]"
```

Expected output / effect:

```text
[ 12]
```

## Notes

- No trailing numeric padding space in the returned string. MID$(STR$(n),2) removes a positive leading space.

[Back to keyword index](INDEX.md)
