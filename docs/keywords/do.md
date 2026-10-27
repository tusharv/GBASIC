# DO

**Status:** Not implemented - reference only  
**Category:** Loops

Begin a QBasic condition-controlled loop.

## Syntax

```basic
DO [WHILE condition | UNTIL condition]
    statements
LOOP
```

## Parameters

- condition: optional pre-test expression.

## Use cases

- Repeat an input menu until a condition changes.

## Examples

### Example 1 (reference)

```basic
DO WHILE N<3
    N=N+1
LOOP
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
