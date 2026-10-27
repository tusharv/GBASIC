# NEXT

**Status:** Supported  
**Category:** Loops

Increment a FOR counter and either repeat its body or finish the loop.

## Syntax

```basic
FOR counter = start TO end [STEP step]
    statements
NEXT [counter [, counter ...]]
```

## Parameters

- counter: optional, but when present must match the current innermost FOR.
- Multiple names: NEXT J,I closes nested loops in that order.

## Use cases

- Draw triangles with nested row/column loops.
- Add or multiply a known number of values.

## Examples

### Example 1 (program)

```basic
10 FOR I=1 TO 2
20 FOR J=1 TO 2
30 PRINT I*J;
40 NEXT J,I
```

Expected output / effect:

```text
 1  2  2  4 
```

## Notes

- A positive-step loop with start>end is skipped; a negative-step loop with start<end is skipped.
- NEXT must exist. Execution is bounded by --max-steps; zero STEP raises Illegal function call.

[Back to keyword index](INDEX.md)
