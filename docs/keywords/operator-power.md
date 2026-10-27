# ^

**Status:** Supported  
**Category:** Operators

Raise a numeric base to a power.

## Syntax

```basic
left ^ right
```

## Parameters

- Operands: numeric expressions.

## Use cases

- Build arithmetic formulas or conditions.
- Trace how operands change the result.

## Examples

### Example 1 (program)

```basic
10 PRINT 2^3^2;(-2)^2
```

Expected output / effect:

```text
 64  4 
```

## Notes

- Powers associate left in this implementation: 2^3^2 is (2^3)^2. Negative-base fractional powers raise an error.

[Back to keyword index](INDEX.md)
