# OPEN

**Status:** Not implemented - reference only  
**Category:** Files

Open a BASIC data file and associate it with a numbered handle.

## Syntax

```basic
OPEN "filename" FOR INPUT AS #number
OPEN "filename" FOR OUTPUT AS #number
```

## Parameters

- filename: data file path.
- mode: INPUT, OUTPUT, APPEND or a dialect-specific random/binary mode.
- number: file handle used by file statements.

## Use cases

- Read a stored table or write results to a file.

## Examples

### Example 1 (reference)

```basic
OPEN "scores.txt" FOR OUTPUT AS #1
PRINT #1, "Ada", 10
CLOSE #1
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
