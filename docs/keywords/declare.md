# DECLARE

**Status:** Not implemented - reference only  
**Category:** Procedures

Describe the signature of a SUB or FUNCTION before use.

## Syntax

```basic
DECLARE SUB name [(parameters)]
DECLARE FUNCTION name [(parameters)]
```

## Parameters

- name: procedure identifier.
- parameters: formal argument names and optional types.

## Use cases

- Declare procedures near the top of a QBasic module.

## Examples

### Example 1 (reference)

```basic
DECLARE SUB Greet (N$)
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
