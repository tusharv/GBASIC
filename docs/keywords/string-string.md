# STRING$

**Status:** Supported  
**Category:** Functions

Repeat one character count times.

## Syntax

```basic
STRING$(count, char$)
STRING$(count, code)
```

## Parameters

- count: rounded integer from 0 to 32767.
- char$: nonempty string; only its first character is repeated.
- code: numeric character code from 0 to 255 instead of char$.

## Use cases

- Draw a separator.
- Repeat a symbol in a text pattern.

## Examples

### Example 1 (program)

```basic
10 PRINT STRING$(4,"*")
```

Expected output / effect:

```text
****
```

## Notes

- An empty character string is illegal. Numeric character codes use CHR$ semantics.

[Back to keyword index](INDEX.md)
