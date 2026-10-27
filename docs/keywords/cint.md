# CINT

**Status:** Supported  
**Category:** Functions

Convert to a signed 16-bit integer using nearest-even rounding.

## Syntax

```basic
CINT(number)
```

## Parameters

- number: numeric expression whose rounded result fits -32768 to 32767.

## Use cases

- Round an input to an integer deliberately.

## Examples

### Example 1 (program)

```basic
10 PRINT CINT(2.5)
```

Expected output / effect:

```text
 2 
```

## Notes

- Ties round to even; 2.5 becomes 2 and 3.5 becomes 4. Out-of-range results raise Overflow.

[Back to keyword index](INDEX.md)
