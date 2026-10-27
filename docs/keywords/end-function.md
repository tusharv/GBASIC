# END FUNCTION

**Status:** Not implemented - reference only  
**Category:** Structured control

Close a FUNCTION procedure definition.

## Syntax

```basic
FUNCTION name(parameters)
    name=expression
END FUNCTION
```

## Parameters

- No arguments; closes the function definition.

## Use cases

- Finish a reusable calculation function.

## Examples

### Example 1 (reference)

```basic
FUNCTION Twice(X)
    Twice=X*2
END FUNCTION
```

## Notes

- Not implemented. Plain END/STOP and numbered GOSUB/RETURN are the current supported alternatives where applicable.

[Back to keyword index](INDEX.md)
