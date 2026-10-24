"""Write merged rectangles as a compact SVG document (milestone 3).

Assumption (pending artist sign-off): one ``<rect>`` per rectangle, with
x, y, width, height and fill as attributes, and the viewBox sized to the grid.
"""

from __future__ import annotations

from typing import List

from .merge import Rect


def rects_to_svg(rects: List[Rect], width: int, height: int) -> str:
    """Return an SVG document drawing ``rects`` on a ``width`` x ``height`` grid."""
    body = "".join(
        f'<rect x="{r.x}" y="{r.y}" width="{r.width}" height="{r.height}" '
        f'fill="{r.color}"/>'
        for r in rects
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" shape-rendering="crispEdges">'
        f"{body}</svg>"
    )


def size_report(svg: str) -> str:
    """Return a one-line byte count for an SVG document."""
    return f"{len(svg.encode('utf-8'))} bytes"
