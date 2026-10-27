# NOT

**Status:** Supported  
**Category:** Operators

Bitwise complement a rounded signed 16-bit value.

## Syntax

```basic
NOT expression
```

## Parameters

- Operands: numeric expressions.

## Use cases

- Build arithmetic formulas or conditions.
- Trace how operands change the result.

## Examples

### Example 1 (program)

```basic
10 PRINT NOT 0;NOT 1=1
```

Expected output / effect:

```text
-1  0 
```

## Notes

- NOT binds below comparisons; NOT 1=1 means NOT (1=1).

[Back to keyword index](INDEX.md)
