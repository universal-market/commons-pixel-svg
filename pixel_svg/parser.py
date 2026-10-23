"""Parse pixel-art text grids with a palette line.

Input format (line 1 is the palette, the rest is the grid):

    .=#000000 X=#FFFFFF *=#FF0000
    .X*.
    XXX.
    .*..

The palette line holds space-separated ``char=#RRGGBB`` tokens. Every
following line is one row of the grid, one character per pixel.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, Tuple

_HEX_COLOR = re.compile(r"^#([0-9a-fA-F]{6})$")


class ParseError(ValueError):
    """Raised when the input text is not a valid pixel grid."""


@dataclass(frozen=True)
class Grid:
    """A resolved pixel grid: width, height, palette and rows of colors."""

    width: int
    height: int
    palette: Dict[str, str]  # character -> #RRGGBB color
    pixels: Tuple[Tuple[str, ...], ...]  # rows of #RRGGBB colors


def parse_palette_line(line: str) -> Dict[str, str]:
    """Parse the palette line into a character -> color map."""
    palette: Dict[str, str] = {}
    for token in line.split():
        if "=" not in token:
            raise ParseError(f"palette token missing '=': {token!r}")
        char, color = token.split("=", 1)
        if len(char) != 1:
            raise ParseError(
                f"palette key must be a single character: {token!r}"
            )
        if not _HEX_COLOR.match(color):
            raise ParseError(
                f"invalid color {color!r} for {char!r} (expected #RRGGBB)"
            )
        if char in palette:
            raise ParseError(f"duplicate palette entry for {char!r}")
        palette[char] = color
    return palette


def parse(text: str) -> Grid:
    """Parse a palette line followed by a rectangular grid of pixels."""
    if not text or not text.strip():
        raise ParseError("input is empty")

    lines = text.splitlines()
    palette = parse_palette_line(lines[0])

    rows: list[Tuple[str, ...]] = []
    width: int | None = None
    for line_no, line in enumerate(lines[1:], start=2):
        if width is None:
            width = len(line)
        elif len(line) != width:
            raise ParseError(
                f"line {line_no} has {len(line)} cells, expected {width}"
            )
        rows.append(tuple(_resolve(char, palette, line_no) for char in line))

    if not rows:
        raise ParseError("grid has no rows")

    return Grid(
        width=width,  # type: ignore[arg-type]
        height=len(rows),
        palette=palette,
        pixels=tuple(rows),
    )


def _resolve(char: str, palette: Dict[str, str], line_no: int) -> str:
    if char not in palette:
        raise ParseError(
            f"line {line_no}: character {char!r} is not in the palette"
        )
    return palette[char]
