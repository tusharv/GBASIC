# FIX

**Status:** Supported  
**Category:** Functions

Discard the fractional part, rounding toward zero.

## Syntax

```basic
FIX(number)
```

## Parameters

- number: numeric expression.

## Use cases

- Truncate a quotient.

## Examples

### Example 1 (program)

```basic
10 PRINT FIX(-1.2)
```

Expected output / effect:

```text
-1 
```

## Notes

- FIX(-1.2) is -1, whereas INT(-1.2) is -2.

[Back to keyword index](INDEX.md)
