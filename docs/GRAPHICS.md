# Graphics API

Ghost BASIC now draws into a deterministic, in-memory 16-color screen. No additional
packages, display server or original BASIC executable are required.

## Run the examples

In the editor, use **F3** to open `graphics_shapes.bas`, `graphics_palette.bas` or
`graphics_plot.bas`. Press **F5**, then **F9** after execution finishes to view the
image. Six more examples add a house, checkerboard, bar chart, spiral, flower and skyline;
see the [gallery guide](../examples/README.md#graphics-examples). Escape or Close returns to the editor. Stop a running program with F6 before
opening the preview. The preview is a downsampled, static terminal snapshot: fine
lines can disappear at small terminal sizes. Full-resolution output is available as PNG:

```sh
GBASIC examples/graphics_shapes.bas --graphics-output shapes.png
GBASIC examples/graphics_palette.bas --graphics-output palette.png
GBASIC examples/graphics_plot.bas --graphics-output plot.png
```

The requested PNG is written after successful execution; an existing output file is
replaced. BASIC drawing statements do not write files. A program ending in text mode
has no image to export and reports an error. PRINT remains ordinary console output;
it is not painted into the image.

## Supported BASIC commands

| Command | Behavior |
| --- | --- |
| `SCREEN 7` | 320 x 200, 16 fixed colors |
| `SCREEN 9` | 640 x 350, 16 fixed colors |
| `SCREEN 12` | 640 x 480, 16 fixed colors; VGA-style extension |
| `SCREEN 0` | Return to text mode and discard pixels |
| `COLOR foreground [,background]` | Set drawing and clear colors in graphics mode |
| `CLS` | Fill graphics pixels with the background color; terminal clear in text mode |
| `PSET (x,y) [,color]` | Set one pixel; defaults to foreground |
| `PRESET (x,y) [,color]` | Set one pixel; defaults to background |
| `LINE (x1,y1)-(x2,y2) [,[color][,B|BF]]` | Inclusive line, outlined box or filled box |
| `CIRCLE (x,y),radius [,color]` | Full circle with equal pixel radii |
| `POINT(x,y)` | Color at a pixel, or -1 outside the screen |

Coordinates have a top-left origin. BASIC numeric arguments round to signed 16-bit
integers; radii must be 0..32767 and colors 0..15. Offscreen drawing clips without
wrapping. `LINE (10,10)-(50,50),,BF` uses the foreground color. SCREEN clears and resets
colors to foreground 15/background 0. A fresh RUN resets to text mode; immediate commands
preserve graphics state. COLOR changes drawing defaults, not already drawn pixels;
use CLS to fill with the new background.

Palette indices: 0 black, 1 blue, 2 green, 3 cyan, 4 red, 5 magenta, 6 brown,
7 light gray, 8 dark gray, 9 bright blue, 10 bright green, 11 bright cyan,
12 bright red, 13 bright magenta, 14 yellow, 15 white.

## Python API

```python
from ghost_basic import Graphics

graphics = Graphics()
graphics.screen(7)
graphics.color(14, 1)
graphics.clear()
graphics.line(20, 20, 120, 80, box="BF")
graphics.circle(220, 100, 40, 15)
assert graphics.point(30, 30) == 14
graphics.save_png("picture.png")
```

`Runtime.graphics` exposes the same API after execution. `png()` returns PNG bytes;
`width`, `height`, `mode` and the row-major `pixels` buffer expose screen state.
Python API arguments must be integers (unlike BASIC, no implicit rounding).
Do not mutate the pixel buffer or read it concurrently with an executing runtime.

## Compatibility boundary

This is a tested drawing subset, not full GW-BASIC or QBasic graphics emulation.
No STEP/relative coordinates, implicit LINE start, line styles, CIRCLE angles/aspect,
PAINT, DRAW, palette remapping, screen pages, GET/PUT, WINDOW/VIEW, text rasterization,
animation, keyboard events or audio synthesis. Pixel-space circles do not emulate
legacy monitor aspect correction. Raster edges may differ from original hardware.
The largest framebuffer is 640x480; primitive loops are bounded by signed-16-bit
coordinates/radii. Stop is checked between BASIC statements, not within a primitive.

Syntax references: [LINE](https://gw-basic.netlify.app/files/tuts/gw-man/line),
[CIRCLE](https://gw-basic.netlify.app/files/tuts/gw-man/circle),
and [SCREEN](https://gw-basic.netlify.app/files/tuts/gw-man/screens).
