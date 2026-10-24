"""swatch-card: a named five-colour palette as a labelled pixel SVG card.

Each colour becomes a solid 12x4 pixel swatch, with its name and hex code
written underneath as ``<text>`` labels in the same SVG. The palette is used
exactly as published; no colour is altered.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple
from xml.sax.saxutils import escape

from .merge import merge_rectangles
from .parser import parse
from .svg import rects_to_svg

BACKGROUND = "#FFFFFF"
SWATCH_W = 12
SWATCH_H = 4
GAP = 2
LABEL_ROWS = 4
SLOT = SWATCH_W + GAP
_SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def swatch_grid_text(colors: Sequence[Tuple[str, str]]) -> str:
    """Return the palette-line grid text for swatches of ``(name, hex)`` colours."""
    if len(colors) > len(_SYMBOLS):
        raise ValueError("too many colours")
    width = len(colors) * SLOT - GAP
    palette = " ".join(
        f"{_SYMBOLS[i]}={hex_}" for i, (_, hex_) in enumerate(colors)
    )
    palette += f" .={BACKGROUND}"
    lines = [palette]
    for y in range(SWATCH_H + LABEL_ROWS):
        row = []
        for x in range(width):
            index, within = divmod(x, SLOT)
            if y < SWATCH_H and within < SWATCH_W:
                row.append(_SYMBOLS[index])
            else:
                row.append(".")
        lines.append("".join(row))
    return "\n".join(lines)


def swatch_card_svg(colors: Sequence[Tuple[str, str]]) -> str:
    """Return one SVG card: a pixel swatch per colour, labelled with name and hex."""
    grid = parse(swatch_grid_text(colors))
    rects = merge_rectangles(grid, background=BACKGROUND)
    labels: List[str] = []
    for i, (name, hex_) in enumerate(colors):
        x = i * SLOT
        labels.append(
            f'<text x="{x}" y="{SWATCH_H + 1.4}" font-family="monospace" '
            f'font-size="1.4">{escape(name)}</text>'
            f'<text x="{x}" y="{SWATCH_H + 2.8}" font-family="monospace" '
            f'font-size="1.4">{escape(hex_)}</text>'
        )
    return rects_to_svg(rects, grid.width, grid.height, extra="".join(labels))
