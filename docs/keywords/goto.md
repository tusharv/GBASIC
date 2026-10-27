# GOTO

**Status:** Supported  
**Category:** Control flow

Jump directly to an existing numbered program line.

## Syntax

```basic
GOTO line
```

## Parameters

- line: numeric expression yielding an integer line number that exists.

## Use cases

- Repeat a simple menu.
- Skip to a selected section of a numbered program.

## Examples

### Example 1 (program)

```basic
10 GOTO 30
20 PRINT "Skipped"
30 PRINT "Arrived"
```

Expected output / effect:

```text
Arrived
```

## Notes

- Undefined lines raise Undefined line number. GOTO does not save a return location.

[Back to keyword index](INDEX.md)
