# REDIM

**Status:** Not implemented - reference only  
**Category:** Arrays

Declare or change dimensions of a dynamic QBasic array.

## Syntax

```basic
REDIM name(upper [, upper ...])
```

## Parameters

- name: dynamic array.
- upper: new bounds; lower-bound syntax depends on the dialect.

## Use cases

- Allocate an array after reading the required size.

## Examples

### Example 1 (reference)

```basic
REDIM SCORES(20)
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
