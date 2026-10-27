# EXIT SUB

**Status:** Not implemented - reference only  
**Category:** Structured control

Return early from a SUB procedure in QBasic.

## Syntax

```basic
EXIT SUB
```

## Parameters

- No expression; ends the current SUB call.

## Use cases

- Reject invalid procedure arguments early.

## Examples

### Example 1 (reference)

```basic
SUB Check(X)
    IF X<0 THEN EXIT SUB
    PRINT X
END SUB
```

## Notes

- Not implemented. Plain END/STOP and numbered GOSUB/RETURN are the current supported alternatives where applicable.

[Back to keyword index](INDEX.md)
