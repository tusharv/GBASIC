# CASE

**Status:** Not implemented - reference only  
**Category:** Control flow

Specify a branch within a SELECT CASE block.

## Syntax

```basic
CASE value [, value ...]
CASE ELSE
```

## Parameters

- values: values to match; ranges and relational forms are dialect-specific extensions.

## Use cases

- Group several menu choices into one branch.

## Examples

### Example 1 (reference)

```basic
SELECT CASE N
CASE 1, 2
    PRINT "Small"
END SELECT
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
