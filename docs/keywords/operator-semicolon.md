# ;

**Status:** Supported  
**Category:** Punctuation

Keep PRINT items on the same line without inserting a print zone.

## Syntax

```basic
PRINT expression; [expression ...]
```

## Parameters

- No value parameter: this is punctuation between PRINT items.

## Use cases

- Write a compact line of code.
- Understand PRINT formatting and statement boundaries.

## Examples

### Example 1 (program)

```basic
10 PRINT "A";"B";
20 PRINT "C"
```

Expected output / effect:

```text
ABC
```

## Notes

- A final semicolon suppresses the newline. INPUT also uses a semicolon after an optional prompt.

[Back to keyword index](INDEX.md)
