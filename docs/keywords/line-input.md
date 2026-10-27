# LINE INPUT

**Status:** Not implemented - reference only  
**Category:** Input/output

Read a complete input line into a string without splitting it into fields.

## Syntax

```basic
LINE INPUT ["prompt";] text$
```

## Parameters

- text$: string target.
- prompt: optional user prompt.

## Use cases

- Read a sentence containing commas.

## Examples

### Example 1 (reference)

```basic
LINE INPUT "Description"; DESCRIPTION$
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
