"""Merge a parsed pixel grid into rectangles (milestone 2).

Assumptions, pending artist sign-off on the acceptance criteria:

- Rectangles carry their colour as a ``#RRGGBB`` string, so the SVG writer
  needs no palette.
- ``background`` is an optional colour; cells of that colour produce no
  rectangle. ``None`` means every cell is painted.
- Greedy: horizontal runs of identical colour first, then each run is
  extended downwards while the row below holds an identical, unused run.
  No flood fill, so the output is deterministic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Set, Tuple

from .parser import Grid


@dataclass(frozen=True)
class Rect:
    """A filled rectangle in grid cells; ``(x, y)`` is the top-left cell."""

    x: int
    y: int
    width: int
    height: int
    color: str  # #RRGGBB


def merge_rectangles(grid: Grid, background: Optional[str] = None) -> List[Rect]:
    """Cover every non-background cell exactly once with rectangles."""
    covered: Set[Tuple[int, int]] = set()
    rects: List[Rect] = []

    def free(x: int, y: int) -> bool:
        color = grid.pixels[y][x]
        return color != background and (x, y) not in covered

    for y in range(grid.height):
        x = 0
        while x < grid.width:
            if not free(x, y):
                x += 1
                continue
            color = grid.pixels[y][x]
            run = 1
            while x + run < grid.width and free(x + run, y) and grid.pixels[y][x + run] == color:
                run += 1

            height = 1
            while y + height < grid.height and all(
                free(x + i, y + height) and grid.pixels[y + height][x + i] == color
                for i in range(run)
            ):
                height += 1

            for dy in range(height):
                for dx in range(run):
                    covered.add((x + dx, y + dy))
            rects.append(Rect(x=x, y=y, width=run, height=height, color=color))
            x += run
    return rects
