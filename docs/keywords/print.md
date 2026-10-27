# PRINT

**Status:** Supported  
**Category:** Input/output

Display text and numbers; control whether the next item stays on the same line.

## Syntax

```basic
PRINT [expression [{;|,} expression] ...] [;|,]
```

## Parameters

- expression: string or numeric value.
- Semicolon (;): no extra separator and suppresses the final newline when last.
- Comma (,): advance to the next 14-character print zone.
- No expressions: print a newline.

## Use cases

- Display answers in calculators.
- Build a row of stars inside a loop.

## Examples

### Example 1 (program)

```basic
10 PRINT "Hello ";"BASIC"
20 PRINT 2+3
```

Expected output / effect:

```text
Hello BASIC
 5 
```

## Notes

- Positive numbers include a leading and trailing space. Formatting is approximate.
- PRINT USING, TAB, SPC and PRINT# are not implemented. Colon-separated IF branches keep their own PRINT statements.

Aliases: `?`

[Back to keyword index](INDEX.md)
