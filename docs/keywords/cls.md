# CLS

**Status:** Supported subset  
**Category:** Terminal effects

Emit a terminal clear-screen sequence.

## Syntax

```basic
CLS
```

## Parameters

- No arguments.

## Use cases

- Clear a compatible batch/prompt terminal between displays.

## Examples

### Example 1 (program)

```basic
10 PRINT "Before"
20 CLS
30 PRINT "After"
```

Expected output / effect:

```text
Before
\x1b[2J\x1b[HAfter
```

## Notes

- ANSI clear sequence is emitted; this is not an emulated BASIC screen buffer.
- The ASCII IDE filters control escapes rather than clearing its interface.

[Back to keyword index](INDEX.md)
