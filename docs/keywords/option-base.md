# OPTION BASE

**Status:** Not implemented - reference only  
**Category:** Arrays

Set a default lower bound for array declarations in supporting dialects.

## Syntax

```basic
OPTION BASE 0
OPTION BASE 1
```

## Parameters

- base: default lower index, normally 0 or 1.

## Use cases

- Use one-based arrays in a legacy program.

## Examples

### Example 1 (reference)

```basic
OPTION BASE 1
DIM A(5)
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
