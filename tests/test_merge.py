"""Tests for pixel_svg.merge (milestone 2: rectangle merging)."""

import unittest

from pixel_svg.merge import Rect, merge_rectangles
from pixel_svg.parser import parse

BLACK = "#000000"
RED = "#FF0000"
WHITE = "#FFFFFF"


def paint(rects, width, height, background=None):
    """Paint rectangles back into a grid of colours (round-trip helper)."""
    grid = [[background] * width for _ in range(height)]
    for r in rects:
        for dy in range(r.height):
            for dx in range(r.width):
                assert grid[r.y + dy][r.x + dx] is background, "overlap"
                grid[r.y + dy][r.x + dx] = r.color
    return grid


class MergeTests(unittest.TestCase):
    def test_solid_grid_becomes_one_rectangle(self):
        grid = parse("A=#000000\nAAAA\nAAAA\nAAAA\nAAAA")
        self.assertEqual(
            merge_rectangles(grid), [Rect(0, 0, 4, 4, BLACK)]
        )

    def test_checkerboard_gives_one_rectangle_per_filled_cell(self):
        grid = parse("A=#000000 .=#FFFFFF\nA.A.\n.A.A\nA.A.\n.A.A")
        rects = merge_rectangles(grid, background=WHITE)
        self.assertEqual(len(rects), 8)
        self.assertTrue(all(r.width == 1 and r.height == 1 for r in rects))

    def test_background_cells_produce_no_rectangle(self):
        grid = parse("X=#FFFFFF\nXXXX\nXXXX")
        self.assertEqual(merge_rectangles(grid, background=WHITE), [])

    def test_no_background_paints_every_cell(self):
        grid = parse("X=#FFFFFF\nXX\nXX")
        self.assertEqual(merge_rectangles(grid), [Rect(0, 0, 2, 2, WHITE)])

    def test_vertical_merge_of_identical_runs(self):
        grid = parse("A=#000000 B=#FF0000\nAB\nAB\nAB")
        rects = merge_rectangles(grid)
        self.assertIn(Rect(0, 0, 1, 3, BLACK), rects)
        self.assertIn(Rect(1, 0, 1, 3, RED), rects)
        self.assertEqual(len(rects), 2)

    def test_round_trip_reproduces_input(self):
        grid = parse(
            "A=#000000 R=#FF0000 .=#FFFFFF\n"
            "AAR.\n"
            "AARR\n"
            ".RRA\n"
            "..AA"
        )
        rects = merge_rectangles(grid, background=WHITE)
        painted = paint(rects, grid.width, grid.height, background=WHITE)
        self.assertEqual(painted, [list(row) for row in grid.pixels])

    def test_rectangles_do_not_overlap(self):
        grid = parse("A=#000000 .=#FFFFFF\nAAAA\nAAAA\nA..A\nAAAA")
        rects = merge_rectangles(grid, background=WHITE)
        paint(rects, grid.width, grid.height, background=WHITE)  # asserts no overlap


if __name__ == "__main__":
    unittest.main()
