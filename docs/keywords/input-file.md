# INPUT#

**Status:** Not implemented - reference only  
**Category:** Files

Read fields from an open BASIC input file.

## Syntax

```basic
INPUT #number, variable [, variable ...]
```

## Parameters

- number: input file handle.
- variables: targets compatible with stored field values.

## Use cases

- Load a record of scores.

## Examples

### Example 1 (reference)

```basic
INPUT #1, NAME$, SCORE
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
