# MOD

**Status:** Supported  
**Category:** Operators

Return the remainder after integer division.

## Syntax

```basic
left MOD right
```

## Parameters

- Operands: numeric expressions.

## Use cases

- Build arithmetic formulas or conditions.
- Trace how operands change the result.

## Examples

### Example 1 (program)

```basic
10 PRINT 7 MOD 3;-7 MOD 3
```

Expected output / effect:

```text
 1 -1 
```

## Notes

- Operands use signed 16-bit nearest-even rounding; remainder follows the dividend sign, unlike Python modulo.

[Back to keyword index](INDEX.md)
