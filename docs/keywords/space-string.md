# SPACE$

**Status:** Supported  
**Category:** Functions

Return a string containing count spaces.

## Syntax

```basic
SPACE$(count)
```

## Parameters

- count: rounded integer from 0 to 32767.

## Use cases

- Indent a text pattern.

## Examples

### Example 1 (program)

```basic
10 PRINT "["+SPACE$(3)+"]"
```

Expected output / effect:

```text
[   ]
```

## Notes

- The maximum string size is 32767 characters. Negative counts raise Illegal function call.

[Back to keyword index](INDEX.md)
