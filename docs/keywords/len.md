# LEN

**Status:** Supported  
**Category:** Functions

Count the characters in a string.

## Syntax

```basic
LEN(text$)
```

## Parameters

- text$: string expression, including an empty string.

## Use cases

- Check a name length.

## Examples

### Example 1 (program)

```basic
10 PRINT LEN("BASIC")
```

Expected output / effect:

```text
 5 
```

## Notes

- Counts Unicode characters, not encoded DOS bytes. Numeric arguments raise Type mismatch.

[Back to keyword index](INDEX.md)
