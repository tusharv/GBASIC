# STEP

**Status:** Supported  
**Category:** Loops

Set the increment or decrement of a FOR loop.

## Syntax

```basic
FOR counter = start TO end [STEP step]
    statements
NEXT [counter [, counter ...]]
```

## Parameters

- step: numeric value; use -1 to count down. Zero is rejected.

## Use cases

- Draw triangles with nested row/column loops.
- Add or multiply a known number of values.

## Examples

### Example 1 (program)

```basic
10 FOR I=3 TO 1 STEP -1
20 PRINT I;
30 NEXT I
```

Expected output / effect:

```text
 3  2  1 
```

## Notes

- A positive-step loop with start>end is skipped; a negative-step loop with start<end is skipped.
- NEXT must exist. Execution is bounded by --max-steps; zero STEP raises Illegal function call.

[Back to keyword index](INDEX.md)
