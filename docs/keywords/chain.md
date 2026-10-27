# CHAIN

**Status:** Not implemented - reference only  
**Category:** Environment

Transfer to another BASIC program with dialect-specific state sharing.

## Syntax

```basic
CHAIN "filename"
```

## Parameters

- filename: next BASIC program; extra sharing options vary by dialect.

## Use cases

- Split a legacy application across programs.

## Examples

### Example 1 (reference)

```basic
CHAIN "next.bas"
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
