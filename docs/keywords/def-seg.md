# DEF SEG

**Status:** Not implemented - reference only  
**Category:** Machine access

Select a memory segment for legacy address operations.

## Syntax

```basic
DEF SEG [= segment]
```

## Parameters

- segment: optional legacy memory segment.

## Use cases

- Read machine-specific BASIC source.

## Examples

### Example 1 (reference)

```basic
DEF SEG = &HB800
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.
- Future support requires virtualized capabilities; no direct host memory access is available.

[Back to keyword index](INDEX.md)
