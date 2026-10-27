# ,

**Status:** Supported  
**Category:** Punctuation

Separate arguments, array indices or data fields; in PRINT advance to a print zone.

## Syntax

```basic
PRINT expression, expression
DIM name(upper, upper)
```

## Parameters

- Meaning depends on context: PRINT, INPUT, function arguments, DIM or DATA.

## Use cases

- Write a compact line of code.
- Understand PRINT formatting and statement boundaries.

## Examples

### Example 1 (program)

```basic
10 PRINT "A","B"
```

Expected output / effect:

```text
A             B
```

## Notes

- PRINT zones are 14 columns in this implementation; there is no automatic screen wrap.

[Back to keyword index](INDEX.md)
