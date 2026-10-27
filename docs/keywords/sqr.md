# SQR

**Status:** Supported  
**Category:** Functions

Return the nonnegative square root.

## Syntax

```basic
SQR(number)
```

## Parameters

- number: numeric expression >= 0.

## Use cases

- Limit trial division in a prime test.

## Examples

### Example 1 (program)

```basic
10 PRINT SQR(9)
```

Expected output / effect:

```text
 3 
```

## Notes

- A negative argument raises Illegal function call. Use ^2 to square a value.

[Back to keyword index](INDEX.md)
