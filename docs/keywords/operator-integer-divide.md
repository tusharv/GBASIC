# \

**Status:** Supported  
**Category:** Operators

Divide rounded 16-bit integer operands and truncate the quotient toward zero.

## Syntax

```basic
left \ right
```

## Parameters

- Operands: numeric expressions.

## Use cases

- Build arithmetic formulas or conditions.
- Trace how operands change the result.

## Examples

### Example 1 (program)

```basic
10 PRINT 7\2;-7\2
```

Expected output / effect:

```text
 3 -3 
```

## Notes

- Operands are rounded nearest-even to signed 16-bit before division; out-of-range operands overflow.

[Back to keyword index](INDEX.md)
