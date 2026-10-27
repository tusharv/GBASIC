# VAL

**Status:** Supported  
**Category:** Functions

Read a decimal numeric prefix from a string.

## Syntax

```basic
VAL(text$)
```

## Parameters

- text$: string with optional leading whitespace/sign and decimal exponent.

## Use cases

- Extract a number from a numeric text prefix.

## Examples

### Example 1 (program)

```basic
10 PRINT VAL(" -12.5tail")
```

Expected output / effect:

```text
-12.5 
```

## Notes

- Returns 0 when no decimal prefix is present. Hex/octal strings and legacy embedded-space parsing are not implemented.

[Back to keyword index](INDEX.md)
