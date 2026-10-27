# :

**Status:** Supported  
**Category:** Punctuation

Separate multiple BASIC statements on one numbered line.

## Syntax

```basic
line statement : statement
```

## Parameters

- Each separated item is a complete statement.

## Use cases

- Write a compact line of code.
- Understand PRINT formatting and statement boundaries.

## Examples

### Example 1 (program)

```basic
10 A=2: A=A+3: PRINT A
```

Expected output / effect:

```text
 5 
```

## Notes

- After IF THEN, colon-separated statements stay in that branch; comments consume the rest of the physical line.

[Back to keyword index](INDEX.md)
