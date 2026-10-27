# FUNCTION

**Status:** Not implemented - reference only  
**Category:** Procedures

Define a named procedure that returns a value in an expression.

## Syntax

```basic
FUNCTION name [(parameters)]
    name = expression
END FUNCTION
```

## Parameters

- name: function identifier and return variable.
- parameters: optional input variables.

## Use cases

- Reuse a formula in expressions.

## Examples

### Example 1 (reference)

```basic
FUNCTION Twice (X)
    Twice = X*2
END FUNCTION
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
