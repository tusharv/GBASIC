# EXIT DO

**Status:** Not implemented - reference only  
**Category:** Structured control

Leave the nearest active DO loop early in QBasic.

## Syntax

```basic
EXIT DO
```

## Parameters

- No expression; selects the enclosing DO block.

## Use cases

- Stop an input/menu loop.

## Examples

### Example 1 (reference)

```basic
DO
    IF DONE THEN EXIT DO
LOOP
```

## Notes

- Not implemented. Plain END/STOP and numbered GOSUB/RETURN are the current supported alternatives where applicable.

[Back to keyword index](INDEX.md)
