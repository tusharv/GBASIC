# EXIT FUNCTION

**Status:** Not implemented - reference only  
**Category:** Structured control

Return early from a FUNCTION procedure in QBasic.

## Syntax

```basic
EXIT FUNCTION
```

## Parameters

- No expression; assign the return variable separately.

## Use cases

- Finish a function before its final line.

## Examples

### Example 1 (reference)

```basic
FUNCTION Safe(X)
    IF X<0 THEN EXIT FUNCTION
    Safe=X
END FUNCTION
```

## Notes

- Not implemented. Plain END/STOP and numbered GOSUB/RETURN are the current supported alternatives where applicable.

[Back to keyword index](INDEX.md)
