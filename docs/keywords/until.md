# UNTIL

**Status:** Not implemented - reference only  
**Category:** Loops

Repeat a DO loop until its condition becomes true.

## Syntax

```basic
DO UNTIL condition
    statements
LOOP
```

## Parameters

- condition: expression whose true value ends the loop.

## Use cases

- Repeat until an entered value is acceptable.

## Examples

### Example 1 (reference)

```basic
DO UNTIL N>=3
    N=N+1
LOOP
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
