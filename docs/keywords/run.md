# RUN

**Status:** Supported  
**Category:** Environment

Execute the current stored program from its beginning.

## Syntax

```basic
RUN
```

## Parameters

- No arguments; RUN filename is not supported.

## Use cases

- Run a program after LOAD or editing.

## Examples

### Example 1 (shell)

```basic
10 PRINT "Run works"
RUN
```

Expected output / effect:

```text
Run works
```

## Notes

- RUN clears variables, arrays and DATA state. F5 runs the editor buffer in the UI.

[Back to keyword index](INDEX.md)
