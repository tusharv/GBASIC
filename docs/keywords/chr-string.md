# CHR$

**Status:** Supported  
**Category:** Functions

Create a one-character string from a code in 0 through 255.

## Syntax

```basic
CHR$(code)
```

## Parameters

- code: numeric argument rounded to an integer from 0 to 255.

## Use cases

- Create punctuation or a double quote.

## Examples

### Example 1 (program)

```basic
10 PRINT CHR$(65)
```

Expected output / effect:

```text
A
```

## Notes

- Maps to Unicode codepoints, not CP437 glyphs; not a general Unicode constructor.

[Back to keyword index](INDEX.md)
