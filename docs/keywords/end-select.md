# END SELECT

**Status:** Not implemented - reference only  
**Category:** Structured control

Close a SELECT CASE block.

## Syntax

```basic
SELECT CASE expression
    CASE value
        statements
END SELECT
```

## Parameters

- No arguments; closes the matching selection block.

## Use cases

- Finish a multi-way branch.

## Examples

### Example 1 (reference)

```basic
SELECT CASE N
CASE 1
    PRINT "One"
END SELECT
```

## Notes

- Not implemented. Plain END/STOP and numbered GOSUB/RETURN are the current supported alternatives where applicable.

[Back to keyword index](INDEX.md)
