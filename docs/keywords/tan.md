# TAN

**Status:** Supported  
**Category:** Functions

Calculate the tangent of an angle in radians.

## Syntax

```basic
TAN(angle)
```

## Parameters

- angle: numeric radians.

## Use cases

- Relate an angle to a slope.

## Examples

### Example 1 (program)

```basic
10 PRINT TAN(0)
```

Expected output / effect:

```text
 0 
```

## Notes

- Near odd multiples of pi/2 the result is numerically unstable; avoid those angles.

[Back to keyword index](INDEX.md)
