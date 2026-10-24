"""Command line front end: palette-line grid file in, SVG file out.

    python -m pixel_svg.cli input.txt -o out.svg

Exit codes: 0 on success; 1 on a bad grid or palette (one-line message on
stderr); 2 on a usage or file error.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .merge import merge_rectangles
from .parser import ParseError, parse
from .svg import rects_to_svg


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pixel-svg-cli",
        description="Turn a palette-line pixel grid into SVG.",
    )
    parser.add_argument("input", help="grid file: palette line, then rows")
    parser.add_argument("-o", "--output", required=True, help="SVG file to write")
    args = parser.parse_args(argv)

    try:
        with open(args.input, encoding="utf-8") as handle:
            text = handle.read()
    except OSError as exc:
        print(f"pixel-svg-cli: cannot read {args.input}: {exc.strerror}", file=sys.stderr)
        return 2

    try:
        grid = parse(text)
    except ParseError as exc:
        print(f"pixel-svg-cli: {exc}", file=sys.stderr)
        return 1

    svg = rects_to_svg(merge_rectangles(grid), grid.width, grid.height)
    try:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(svg)
    except OSError as exc:
        print(f"pixel-svg-cli: cannot write {args.output}: {exc.strerror}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
