# <

**Status:** Supported  
**Category:** Comparisons

Test whether the left value is less than the right value.

## Syntax

```basic
left < right
```

## Parameters

- left/right: both numeric or both strings.
- Result: -1 for true, 0 for false.

## Use cases

- Validate entered values.
- Choose an IF branch.

## Examples

### Example 1 (program)

```basic
10 PRINT 2<3
```

Expected output / effect:

```text
-1 
```

## Notes

- Strings compare lexically using Unicode codepoints, not legacy codepage bytes.
- = also introduces assignment in LET; within an expression it compares values.

[Back to keyword index](INDEX.md)
