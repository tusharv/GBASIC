# GOSUB

**Status:** Supported  
**Category:** Subroutines

Call a numbered subroutine and remember where to return.

## Syntax

```basic
GOSUB line
...
line statements
RETURN
```

## Parameters

- line: existing numbered entry point.

## Use cases

- Reuse the row drawing routine in the diamond example.
- Share a calculation without duplicating statements.

## Examples

### Example 1 (program)

```basic
10 GOSUB 100
20 PRINT "Back"
30 END
100 PRINT "Called"
110 RETURN
```

Expected output / effect:

```text
Called
Back
```

## Notes

- Use END before the subroutine area to avoid falling into it. RETURN without GOSUB raises an error.
- RETURN line and QBasic SUB/FUNCTION procedures are not implemented.

[Back to keyword index](INDEX.md)
