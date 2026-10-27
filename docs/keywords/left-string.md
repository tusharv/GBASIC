# LEFT$

**Status:** Supported  
**Category:** Functions

Return up to count characters from the beginning of a string.

## Syntax

```basic
LEFT$(text$, count)
```

## Parameters

- text$: source string.
- count: rounded integer >=0; a count larger than the string returns the entire string.

## Use cases

- Extract a short prefix.

## Examples

### Example 1 (program)

```basic
10 PRINT LEFT$("BASIC",2)
```

Expected output / effect:

```text
BA
```

## Notes

- Count 0 returns an empty string. Negative counts raise Illegal function call.

[Back to keyword index](INDEX.md)
