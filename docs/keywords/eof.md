# EOF

**Status:** Not implemented - reference only  
**Category:** Files

Test whether an open file has reached end of input.

## Syntax

```basic
EOF(number)
```

## Parameters

- number: open file handle.

## Use cases

- Stop reading at the end of a data file.

## Examples

### Example 1 (reference)

```basic
WHILE NOT EOF(1)
    LINE INPUT #1, ROW$
WEND
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
