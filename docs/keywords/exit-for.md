# EXIT FOR

**Status:** Not implemented - reference only  
**Category:** Structured control

Leave the nearest active FOR loop early in QBasic.

## Syntax

```basic
EXIT FOR
```

## Parameters

- No expression; selects the enclosing FOR block.

## Use cases

- Stop a search once a value is found.

## Examples

### Example 1 (reference)

```basic
FOR I=1 TO 10
    IF I=5 THEN EXIT FOR
NEXT I
```

## Notes

- Not implemented. Plain END/STOP and numbered GOSUB/RETURN are the current supported alternatives where applicable.

[Back to keyword index](INDEX.md)
