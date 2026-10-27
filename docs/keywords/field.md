# FIELD

**Status:** Not implemented - reference only  
**Category:** Files

Map sections of a random-access file record to string variables.

## Syntax

```basic
FIELD #number, length AS text$ [, length AS text$ ...]
```

## Parameters

- number: random-access handle.
- length: byte width of the associated string field.

## Use cases

- Read fixed-width legacy records.

## Examples

### Example 1 (reference)

```basic
FIELD #1, 10 AS NAME$, 4 AS VALUE$
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
