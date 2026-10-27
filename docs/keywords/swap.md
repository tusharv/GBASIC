# SWAP

**Status:** Not implemented - reference only  
**Category:** Variables

Exchange the values of two compatible variables.

## Syntax

```basic
SWAP left, right
```

## Parameters

- left/right: compatible variable targets.

## Use cases

- Reorder a pair without a temporary variable.

## Examples

### Example 1 (reference)

```basic
SWAP A, B
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.
- Currently use a temporary variable: T=A: A=B: B=T.

[Back to keyword index](INDEX.md)
