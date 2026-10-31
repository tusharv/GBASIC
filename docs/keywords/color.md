# COLOR

**Status:** Supported subset  
**Category:** Terminal layout

Set drawing and clear colors from 0 through 15 in graphics mode.

## Syntax

```basic
COLOR foreground [, background]
```

## Parameters

- Arguments are numeric expressions. Drawing coordinates are rounded to signed 16-bit integers.
- Choose SCREEN 7, 9 or 12 before graphics operations; SCREEN 0 returns to text.

## Use cases

- Draw diagrams and plots; inspect the finished image with F9.

## Examples

### Example 1 (program)

```basic
10 SCREEN 7
20 COLOR 14,1
30 CLS
40 PSET (10,10)
```

## Notes

- Supported subset: fixed 16-color palette; no STEP, implicit LINE start, styles, arcs, aspect, pages, or text drawn into the image.
- SCREEN resets pixels and colors; RUN resets to text mode. CLS fills with the background color.
- F9 shows a downsampled snapshot after running. CLI --graphics-output picture.png exports full resolution.

[Back to keyword index](INDEX.md)
