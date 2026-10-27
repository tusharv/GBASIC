# BEEP

**Status:** Supported subset  
**Category:** Terminal effects

Emit the ASCII bell character.

## Syntax

```basic
BEEP
```

## Parameters

- No arguments.

## Use cases

- Request a terminal notification where bells are enabled.

## Examples

### Example 1 (program)

```basic
10 BEEP
```

Expected output / effect:

```text
\x07
```

## Notes

- Sound depends on the terminal settings. The IDE filters the bell; synthesized audio is not implemented.

[Back to keyword index](INDEX.md)
