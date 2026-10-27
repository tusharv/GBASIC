# SUB

**Status:** Not implemented - reference only  
**Category:** Procedures

Define a named subroutine with parameters and local variables.

## Syntax

```basic
SUB name [(parameters)]
    statements
END SUB
```

## Parameters

- name: subroutine identifier.
- parameters: optional formal variables supplied by a call.

## Use cases

- Group reusable drawing or input logic.

## Examples

### Example 1 (reference)

```basic
CALL Greet
END
SUB Greet
    PRINT "Hello"
END SUB
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
