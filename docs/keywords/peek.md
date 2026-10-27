# PEEK

**Status:** Not implemented - reference only  
**Category:** Machine access

Read a byte from the emulated machine memory in supporting interpreters.

## Syntax

```basic
PEEK(address)
```

## Parameters

- address: memory offset interpreted under the current segment/dialect.

## Use cases

- Inspect a legacy virtual machine's memory.

## Examples

### Example 1 (reference)

```basic
PRINT PEEK(0)
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.
- Future support requires virtualized capabilities; no direct host memory access is available.

[Back to keyword index](INDEX.md)
