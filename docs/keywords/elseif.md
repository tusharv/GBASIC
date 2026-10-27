# ELSEIF

**Status:** Not implemented - reference only  
**Category:** Control flow

Add another condition to a multiline QBasic IF block.

## Syntax

```basic
IF condition THEN
    statements
ELSEIF condition THEN
    statements
END IF
```

## Parameters

- condition: the next expression tested if earlier conditions were false.

## Use cases

- Test several grading thresholds in order.

## Examples

### Example 1 (reference)

```basic
IF N>0 THEN
    PRINT "Positive"
ELSEIF N<0 THEN
    PRINT "Negative"
END IF
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
