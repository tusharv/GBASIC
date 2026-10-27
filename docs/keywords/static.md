# STATIC

**Status:** Not implemented - reference only  
**Category:** Scope

Retain procedure-local variable values between calls.

## Syntax

```basic
STATIC name
SUB name [STATIC]
```

## Parameters

- name: local variable, or procedure marked for static storage.

## Use cases

- Remember a procedure's previous result.

## Examples

### Example 1 (reference)

```basic
STATIC COUNTER AS INTEGER
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
