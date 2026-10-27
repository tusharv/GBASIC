# END SUB

**Status:** Not implemented - reference only  
**Category:** Structured control

Close a SUB procedure definition.

## Syntax

```basic
SUB name
    statements
END SUB
```

## Parameters

- No arguments; ends the matching procedure definition.

## Use cases

- Finish a reusable subroutine.

## Examples

### Example 1 (reference)

```basic
SUB Greet
    PRINT "Hello"
END SUB
```

## Notes

- Not implemented. Plain END/STOP and numbered GOSUB/RETURN are the current supported alternatives where applicable.

[Back to keyword index](INDEX.md)
