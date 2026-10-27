# MID$

**Status:** Supported  
**Category:** Functions

Extract characters from a one-based start position.

## Syntax

```basic
MID$(text$, start [, length])
```

## Parameters

- text$: source string.
- start: rounded integer >=1; positions start at 1, not 0.
- length: optional rounded integer >=0; omit it to read to the end.

## Use cases

- Extract part of a name.
- Remove STR$ numeric padding for pattern output.

## Examples

### Example 1 (program)

```basic
10 PRINT MID$("BASIC",2,3)
```

Expected output / effect:

```text
ASI
```

## Notes

- A start beyond the end returns an empty string. MID$ assignment is not implemented.

[Back to keyword index](INDEX.md)
