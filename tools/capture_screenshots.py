"""Capture real Textual screens as portable SVG and PNG documentation assets.

Install the screenshots extra and the OS Cairo library. On macOS with Homebrew Cairo:
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python tools/capture_screenshots.py --font Menlo
"""

import argparse
import asyncio
import os
import re
from pathlib import Path

from textual.widgets import Input

from ghost_basic.tui import GhostBasicApp


async def capture(destination: Path, font: str) -> None:
    import cairosvg

    root = Path(__file__).resolve().parents[1]
    destination.mkdir(parents=True, exist_ok=True)
    os.environ.pop('NO_COLOR', None)

    def save(app: GhostBasicApp, name: str) -> None:
        svg = app.export_screenshot(title='Ghost BASIC', simplify=True)
        # Use the local terminal font; don't fetch the exporter's optional web fonts.
        svg = re.sub(r'@font-face\s*\{.*?\}', '', svg, flags=re.S)
        svg = svg.replace('font-family: Fira Code, monospace;', f'font-family: {font};')
        (destination / f'{name}.svg').write_text(svg, encoding='utf-8')
        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(destination / f'{name}.png'),
                        output_width=1600)
        print(f'Captured {name}')

    app = GhostBasicApp(root=root, filename='examples/triangle_04_pyramid.bas')
    async with app.run_test(size=(110, 36)) as pilot:
        await pilot.press('f5')
        for _ in range(100):
            await pilot.pause(0.01)
            if not app.runner.running:
                app.poll_execution()
                break
        assert '*********' in app.output_text
        save(app, 'editor')
        await pilot.press('f3', 'enter')
        save(app, 'examples')
        await pilot.press('escape', 'escape')
        await pilot.press('f1')
        app.screen.query_one('#help-search', Input).value = 'FOR'
        await pilot.pause()
        save(app, 'help')

    app = GhostBasicApp(root=root, show_splash=True)
    async with app.run_test(size=(110, 36)) as pilot:
        await pilot.pause(0.7)
        save(app, 'splash')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font', default='monospace', help='installed monospace font family')
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).resolve().parents[1] / 'site/assets/screenshots')
    args = parser.parse_args()
    asyncio.run(capture(args.output, args.font))
