# GET

**Status:** Not implemented - reference only  
**Category:** Files / graphics

Read a random/binary record or capture a graphics region, depending on syntax.

## Syntax

```basic
GET #number [, record]
GET (x1,y1)-(x2,y2), array
```

## Parameters

- File form: number and optional record/position.
- Graphics form: coordinates and destination array.

## Use cases

- Read a stored record.
- Capture a sprite in a graphics program.

## Examples

### Example 1 (reference)

```basic
GET #1, 1
```

## Notes

- Not implemented in Ghost BASIC. The example explains legacy syntax and cannot run here.
- This is a reference topic, not a promise of complete GW-BASIC/QBasic compatibility.

[Back to keyword index](INDEX.md)
