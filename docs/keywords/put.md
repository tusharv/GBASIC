# PUT

**Status:** Not implemented - reference only  
**Category:** Files / graphics

Write a random/binary record or draw stored graphics data, depending on syntax.

## Syntax

```basic
PUT #number [, record]
PUT (x,y), array
```

## Parameters

- File form: number and optional record/position.
- Graphics form: destination coordinates and stored image array.

## Use cases

- Write a stored record.
- Draw a captured sprite.

## Examples

### Example 1 (reference)

```basic
PUT #1, 1
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
