# RIGHT$

**Status:** Supported  
**Category:** Functions

Return up to count characters from the end of a string.

## Syntax

```basic
RIGHT$(text$, count)
```

## Parameters

- text$: source string.
- count: rounded integer >=0.

## Use cases

- Extract a file suffix.

## Examples

### Example 1 (program)

```basic
10 PRINT RIGHT$("BASIC",2)
```

Expected output / effect:

```text
IC
```

## Notes

- Count 0 returns an empty string; excessive count returns the whole string.

[Back to keyword index](INDEX.md)
