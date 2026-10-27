# USR

**Status:** Not implemented - reference only  
**Category:** Machine access

Invoke a legacy machine-language function in supporting interpreters.

## Syntax

```basic
USR(argument)
```

## Parameters

- argument: value supplied to a previously configured machine-language entry.

## Use cases

- Understand machine-specific extensions in old source.

## Examples

### Example 1 (reference)

```basic
PRINT USR(0)
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.
- Future support requires virtualized capabilities; no direct host memory access is available.

[Back to keyword index](INDEX.md)
