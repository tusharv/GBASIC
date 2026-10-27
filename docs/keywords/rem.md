# REM

**Status:** Supported  
**Category:** Comments

Treat the rest of the physical line as a comment.

## Syntax

```basic
REM comment text
' comment text
```

## Parameters

- comment text: explanatory text that is not executed.

## Use cases

- Explain a formula.
- Leave a practice challenge next to a loop.

## Examples

### Example 1 (program)

```basic
10 REM Display a greeting
20 PRINT "Hello" : REM a colon inside this comment is ignored
```

Expected output / effect:

```text
Hello
```

## Notes

- Comments end at the physical newline. REM text is not parsed as statements. Apostrophe is an alias.

Aliases: `'`

[Back to keyword index](INDEX.md)
