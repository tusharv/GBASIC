# STOP

**Status:** Supported  
**Category:** Control flow

Halt execution at this point.

## Syntax

```basic
STOP
```

## Parameters

- No arguments.

## Use cases

- Finish the main program before subroutine lines.
- Stop after validation or a final result.

## Examples

### Example 1 (program)

```basic
10 PRINT "Done"
20 STOP
30 PRINT "Skipped"
```

Expected output / effect:

```text
Done
```

## Notes

- STOP and END both halt in Ghost BASIC. CONT and resumable STOP are not implemented.

[Back to keyword index](INDEX.md)
