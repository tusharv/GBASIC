# EQV

**Status:** Supported  
**Category:** Operators

Bitwise equivalence: complement of XOR.

## Syntax

```basic
left EQV right
```

## Parameters

- Operands: numeric expressions.

## Use cases

- Build arithmetic formulas or conditions.
- Trace how operands change the result.

## Examples

### Example 1 (program)

```basic
10 PRINT 1 EQV 1
```

Expected output / effect:

```text
-1 
```

## Notes

- True comparisons use -1 (all bits set); both operands are evaluated.

[Back to keyword index](INDEX.md)
