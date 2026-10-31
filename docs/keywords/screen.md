# SCREEN

**Status:** Supported subset  
**Category:** Graphics

Select text mode 0 or a 16-color graphics screen: 7 (320x200), 9 (640x350), 12 (640x480).

## Syntax

```basic
SCREEN mode
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
20 PSET (10,10),14
```

## Notes

- Supported subset: fixed 16-color palette; no STEP, implicit LINE start, styles, arcs, aspect, pages, or text drawn into the image.
- SCREEN resets pixels and colors; RUN resets to text mode. CLS fills with the background color.
- F9 shows a downsampled snapshot after running. CLI --graphics-output picture.png exports full resolution.

[Back to keyword index](INDEX.md)
