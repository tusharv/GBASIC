# LOOP

**Status:** Not implemented - reference only  
**Category:** Loops

End a DO block, optionally testing a condition after the body.

## Syntax

```basic
DO
    statements
LOOP [WHILE condition | UNTIL condition]
```

## Parameters

- condition: optional post-test expression.

## Use cases

- Run a body at least once before deciding to repeat.

## Examples

### Example 1 (reference)

```basic
DO
    N=N+1
LOOP UNTIL N>=3
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
