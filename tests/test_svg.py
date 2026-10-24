"""Tests for pixel_svg.svg (milestone 3: SVG writer with size report)."""

import unittest

from pixel_svg.merge import Rect, merge_rectangles
from pixel_svg.parser import parse
from pixel_svg.svg import rects_to_svg, size_report


class SvgWriterTests(unittest.TestCase):
    def test_one_rect_element_per_rectangle(self):
        svg = rects_to_svg([Rect(0, 0, 2, 1, "#000000")], 2, 2)
        self.assertEqual(svg.count("<rect "), 1)
        self.assertIn('x="0" y="0" width="2" height="1" fill="#000000"', svg)

    def test_viewbox_matches_grid_size(self):
        svg = rects_to_svg([], 16, 8)
        self.assertIn('viewBox="0 0 16 8"', svg)

    def test_end_to_end_from_grid(self):
        grid = parse("A=#000000 .=#FFFFFF\nAA.\nAA.")
        svg = rects_to_svg(merge_rectangles(grid, background="#FFFFFF"),
                           grid.width, grid.height)
        self.assertEqual(svg.count("<rect "), 1)

    def test_size_report_counts_utf8_bytes(self):
        self.assertEqual(size_report("abc"), "3 bytes")


if __name__ == "__main__":
    unittest.main()
