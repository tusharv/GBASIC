# ON

**Status:** Not implemented - reference only  
**Category:** Control flow

Select a branch/subroutine by numeric index, or introduce legacy event/error handlers.

## Syntax

```basic
ON index GOTO line1, line2, ...
ON index GOSUB line1, line2, ...
```

## Parameters

- index: one-based branch selection.
- lines: candidate target line numbers.

## Use cases

- Dispatch a menu selection.

## Examples

### Example 1 (reference)

```basic
ON CHOICE GOTO 100,200,300
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
