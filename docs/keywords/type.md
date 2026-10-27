# TYPE

**Status:** Not implemented - reference only  
**Category:** Types

Define a QBasic record with named fields.

## Syntax

```basic
TYPE name
    field AS type
END TYPE
```

## Parameters

- name: record type identifier.
- field/type: members and their declared types.

## Use cases

- Group related fields such as a name and score.

## Examples

### Example 1 (reference)

```basic
TYPE Student
    SCORE AS INTEGER
END TYPE
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
