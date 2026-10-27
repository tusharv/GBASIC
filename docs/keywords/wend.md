# WEND

**Status:** Supported  
**Category:** Loops

Close a WHILE block and return to its condition.

## Syntax

```basic
WHILE condition
    statements
WEND
```

## Parameters

- No arguments. A matching WHILE is required.

## Use cases

- Repeat until a counter reaches a limit.
- Use loops with an unknown iteration count.

## Examples

### Example 1 (program)

```basic
10 N=0
20 WHILE N<3
30 N=N+1
40 PRINT N;
50 WEND
```

Expected output / effect:

```text
 1  2  3 
```

## Notes

- A false initial condition skips the body. Infinite loops hit the instruction budget or can be stopped with F6.

[Back to keyword index](INDEX.md)
