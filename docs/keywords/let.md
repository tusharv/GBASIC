# LET

**Status:** Supported  
**Category:** Variables

Assign an evaluated expression to a variable or array element. LET itself is optional.

## Syntax

```basic
[LET] variable = expression
```

## Parameters

- variable: name, optionally ending in %, !, # or $.
- expression: must have a compatible numeric/string type.

## Use cases

- Store an interest calculation.
- Update a loop accumulator.

## Examples

### Example 1 (program)

```basic
10 LET TOTAL=5
20 TOTAL=TOTAL+2
30 PRINT TOTAL
```

Expected output / effect:

```text
 7 
```

## Notes

- % is signed 16-bit, ! and unsuffixed variables are single precision, # is double, $ is a string.
- Assignment coerces explicitly; mixing string and numeric types raises Type mismatch.

[Back to keyword index](INDEX.md)
