# CDBL

**Status:** Supported  
**Category:** Functions

Convert a numeric expression to IEEE double precision.

## Syntax

```basic
CDBL(number)
```

## Parameters

- number: numeric expression.

## Use cases

- Store calculations in a # variable.

## Examples

### Example 1 (program)

```basic
10 PRINT CDBL(1.25)
```

Expected output / effect:

```text
 1.25 
```

## Notes

- Conversion cannot recover digits already lost in a single-precision value.

[Back to keyword index](INDEX.md)
