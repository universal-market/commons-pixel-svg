"""Tests for pixel_svg.parser (milestone 1: palette-line grid parser)."""

import unittest

from pixel_svg.parser import Grid, ParseError, parse, parse_palette_line


class PaletteLineTests(unittest.TestCase):
    def test_parses_char_equals_color_tokens(self):
        palette = parse_palette_line(".=#000000 X=#FFFFFF *=#FF0000")
        self.assertEqual(
            palette, {".": "#000000", "X": "#FFFFFF", "*": "#FF0000"}
        )

    def test_accepts_uppercase_hex(self):
        palette = parse_palette_line("A=#AbCdEf")
        self.assertEqual(palette, {"A": "#AbCdEf"})

    def test_rejects_token_without_equals(self):
        with self.assertRaises(ParseError):
            parse_palette_line(". #000000")

    def test_rejects_multi_character_key(self):
        with self.assertRaises(ParseError):
            parse_palette_line("ab=#000000")

    def test_rejects_invalid_color(self):
        with self.assertRaises(ParseError):
            parse_palette_line(".=#00000")
        with self.assertRaises(ParseError):
            parse_palette_line(".=#0000000")
        with self.assertRaises(ParseError):
            parse_palette_line(".=notacolor")

    def test_rejects_duplicate_character(self):
        with self.assertRaises(ParseError):
            parse_palette_line(".=#000000 .=#FFFFFF")


class GridParseTests(unittest.TestCase):
    def test_simple_two_by_two(self):
        grid = parse(".=#000000 X=#FFFFFF\n.X\nX.")
        self.assertEqual(grid.width, 2)
        self.assertEqual(grid.height, 2)
        self.assertEqual(grid.palette, {".": "#000000", "X": "#FFFFFF"})
        self.assertEqual(
            grid.pixels,
            (("#000000", "#FFFFFF"), ("#FFFFFF", "#000000")),
        )
        self.assertIsInstance(grid, Grid)

    def test_single_pixel(self):
        grid = parse("#=#FF0000\n#")
        self.assertEqual(grid.width, 1)
        self.assertEqual(grid.height, 1)
        self.assertEqual(grid.pixels, (("#FF0000",),))

    def test_larger_grid(self):
        grid = parse(
            ".=#000000 X=#FFFFFF\n"
            ".X.\n"
            "XXX\n"
            ".X."
        )
        self.assertEqual(grid.width, 3)
        self.assertEqual(grid.height, 3)
        self.assertEqual(grid.pixels[1], ("#FFFFFF",) * 3)

    def test_trailing_newline_is_ignored(self):
        grid = parse(".=#000000 X=#FFFFFF\n.X\nX.\n")
        self.assertEqual(grid.height, 2)

    def test_rejects_empty_input(self):
        with self.assertRaises(ParseError):
            parse("")
        with self.assertRaises(ParseError):
            parse("   \n   ")

    def test_rejects_missing_grid_rows(self):
        with self.assertRaises(ParseError):
            parse(".=#000000")

    def test_rejects_non_rectangular_grid(self):
        with self.assertRaises(ParseError):
            parse(".=#000000 X=#FFFFFF\n.X\nX..")

    def test_rejects_unknown_character(self):
        with self.assertRaises(ParseError):
            parse(".=#000000\n.X\n?.")


if __name__ == "__main__":
    unittest.main()
