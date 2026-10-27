# CSNG

**Status:** Supported  
**Category:** Functions

Convert a numeric expression to IEEE single precision.

## Syntax

```basic
CSNG(number)
```

## Parameters

- number: numeric value representable in single precision.

## Use cases

- Observe single-precision rounding.

## Examples

### Example 1 (program)

```basic
10 PRINT CSNG(1.25)
```

Expected output / effect:

```text
 1.25 
```

## Notes

- Equivalent precision to ! and unsuffixed variable assignment; not legacy MBF.

[Back to keyword index](INDEX.md)
