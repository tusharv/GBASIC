# FOR

**Status:** Supported  
**Category:** Loops

Repeat statements while a numeric counter moves from a start value to an end value.

## Syntax

```basic
FOR counter = start TO end [STEP step]
    statements
NEXT [counter [, counter ...]]
```

## Parameters

- counter: numeric scalar, not a string or array element.
- start/end: inclusive bounds, evaluated when FOR is entered.
- step: optional nonzero increment, default 1.

## Use cases

- Draw triangles with nested row/column loops.
- Add or multiply a known number of values.

## Examples

### Example 1 (program)

```basic
10 FOR I=1 TO 3
20 PRINT I;
30 NEXT I
```

Expected output / effect:

```text
 1  2  3 
```

## Notes

- A positive-step loop with start>end is skipped; a negative-step loop with start<end is skipped.
- NEXT must exist. Execution is bounded by --max-steps; zero STEP raises Illegal function call.

[Back to keyword index](INDEX.md)
