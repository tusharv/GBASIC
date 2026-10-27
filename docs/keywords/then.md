# THEN

**Status:** Supported  
**Category:** Control flow

Introduce the branch executed when IF is true.

## Syntax

```basic
IF condition THEN statements [ELSE statements]
```

## Parameters

- condition before THEN: numeric expression.
- body after THEN: statements separated by colons, or a line number.

## Use cases

- Validate input before computing.
- Choose pass/fail or profit/loss output.

## Examples

### Example 1 (program)

```basic
10 SCORE=75
20 IF SCORE>=60 THEN PRINT "Pass" ELSE PRINT "Try again"
```

Expected output / effect:

```text
Pass
```

## Notes

- Only single-line IF is implemented; multiline IF/ELSEIF/END IF is not.
- Colons after THEN belong to that branch; nested ELSE binds to the closest unfinished IF.

[Back to keyword index](INDEX.md)
