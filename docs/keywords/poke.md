# POKE

**Status:** Not implemented - reference only  
**Category:** Machine access

Write a byte to the emulated machine memory in supporting interpreters.

## Syntax

```basic
POKE address, byte
```

## Parameters

- address: target offset.
- byte: value 0 through 255.

## Use cases

- Understand legacy memory-access code.

## Examples

### Example 1 (reference)

```basic
POKE 0, 0
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.
- Future support requires virtualized capabilities; no direct host memory access is available.

[Back to keyword index](INDEX.md)
