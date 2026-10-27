# SELECT

**Status:** Not implemented - reference only  
**Category:** Control flow

Choose one matching CASE branch from a set of alternatives.

## Syntax

```basic
SELECT CASE expression
CASE value
    statements
CASE ELSE
    statements
END SELECT
```

## Parameters

- expression: value to classify.
- CASE values: alternatives; CASE ELSE handles no match.

## Use cases

- Dispatch a menu choice without many IF statements.

## Examples

### Example 1 (reference)

```basic
SELECT CASE CHOICE
CASE 1
    PRINT "One"
CASE ELSE
    PRINT "Other"
END SELECT
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
