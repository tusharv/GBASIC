"""Check the teaching examples draw their characteristic features and terminate."""

from io import StringIO
from pathlib import Path

import pytest

from ghost_basic import Program, Runtime

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


@pytest.mark.parametrize(
    "name, title, samples",
    [
        ("house", "House", [(0, 0, 11), (0, 199, 2), (265, 40, 14), (150, 60, 12), (140, 130, 4)]),
        (
            "checkerboard",
            "Checkerboard",
            [(0, 0, 8), (60, 0, 15), (85, 0, 9), (60, 25, 9), (85, 25, 15)],
        ),
        (
            "bars",
            "Bar chart",
            [(40, 140, 9), (90, 90, 10), (190, 45, 12), (25, 20, 15), (300, 180, 15)],
        ),
        ("spiral", "Spiral", [(0, 0, 0), (160, 100, 9)]),
        ("flower", "Flower", [(160, 85, 14), (160, 199, 10), (0, 0, 0)]),
        ("skyline", "Skyline", [(0, 0, 1), (270, 30, 14), (8, 120, 8), (15, 130, 14)]),
    ],
)
def test_gallery_scene(name, title, samples):
    output = StringIO()
    runtime = Runtime(output=output, max_steps=20000)
    runtime.run(Program.from_source((EXAMPLES / f"graphics_{name}.bas").read_text()))
    assert output.getvalue() == f"{title} ready. Press F9 to view.\n"
    assert runtime.graphics.mode == 7
    for x, y, color in samples:
        assert runtime.graphics.point(x, y) == color, (name, x, y)
    assert len(set(runtime.graphics.pixels)) >= 3
    assert runtime.steps < 20000
