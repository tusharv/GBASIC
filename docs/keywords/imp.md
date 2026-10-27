# IMP

**Status:** Supported  
**Category:** Operators

Bitwise implication: NOT left OR right.

## Syntax

```basic
left IMP right
```

## Parameters

- Operands: numeric expressions.

## Use cases

- Build arithmetic formulas or conditions.
- Trace how operands change the result.

## Examples

### Example 1 (program)

```basic
10 PRINT 0 IMP 0
```

Expected output / effect:

```text
-1 
```

## Notes

- Signed 16-bit operations; use parentheses when combining comparisons.

[Back to keyword index](INDEX.md)
