# ASC

**Status:** Supported  
**Category:** Functions

Return the Unicode codepoint of the first character in a string.

## Syntax

```basic
ASC(text$)
```

## Parameters

- text$: nonempty string; later characters are ignored.

## Use cases

- Inspect the first character.

## Examples

### Example 1 (program)

```basic
10 PRINT ASC("A")
```

Expected output / effect:

```text
 65 
```

## Notes

- An empty string raises Illegal function call; behavior beyond ASCII differs from codepage-based GW-BASIC.

[Back to keyword index](INDEX.md)
