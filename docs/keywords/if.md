# IF

**Status:** Supported  
**Category:** Control flow

Choose a branch based on a numeric condition.

## Syntax

```basic
IF condition THEN statements [ELSE statements]
```

## Parameters

- condition: zero is false, any nonzero number is true.
- then/else body: statements or a target line; ELSE is optional.

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
