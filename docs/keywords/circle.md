# CIRCLE

**Status:** Supported subset  
**Category:** Graphics

Draw a full circle with equal horizontal and vertical pixel radii.

## Syntax

```basic
CIRCLE (x,y),radius [, color]
```

## Parameters

- Coordinates are rounded to signed 16-bit integers. Color indices are 0..15.
- Radius is rounded to an integer from 0..32767; drawing is clipped to screen edges.

## Use cases

- Draw diagrams and plots; inspect the finished image with F9.

## Examples

### Example 1 (program)

```basic
10 SCREEN 7
20 CIRCLE (160,100),50,14
```

## Notes

- Supported subset: fixed 16-color palette; no STEP, implicit LINE start, styles, arcs, aspect, pages, or text drawn into the image.
- SCREEN resets pixels and colors; RUN resets to text mode. CLS fills with the background color.
- F9 shows a downsampled snapshot after running. CLI --graphics-output picture.png exports full resolution.

[Back to keyword index](INDEX.md)
