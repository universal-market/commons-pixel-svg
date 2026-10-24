"""Tests for pixel_svg.swatch (swatch-card: named palette as labelled SVG)."""

import re
import unittest

from pixel_svg.swatch import swatch_card_svg, swatch_grid_text

PALETTE = [
    ("Madder Ink", "#8B2E3A"),
    ("Indigo Warp", "#2B3A67"),
    ("Undyed Linen", "#EFE6D2"),
    ("Weld Yellow", "#E0B43A"),
    ("Sage Repeat", "#7D9B76"),
]


class SwatchCardTests(unittest.TestCase):
    def setUp(self):
        self.svg = swatch_card_svg(PALETTE)

    def test_one_swatch_per_colour_in_order(self):
        fills = re.findall(r'<rect [^>]*fill="(#[0-9A-F]{6})"', self.svg)
        self.assertEqual(fills, [hex_ for _, hex_ in PALETTE])

    def test_each_swatch_is_one_rect(self):
        # five solid swatches; background cells produce no rect
        self.assertEqual(self.svg.count("<rect "), len(PALETTE))

    def test_every_name_and_hex_is_labelled(self):
        for name, hex_ in PALETTE:
            self.assertIn(f">{name}</text>", self.svg)
            self.assertIn(f">{hex_}</text>", self.svg)

    def test_labels_sit_below_swatches(self):
        # text y must be past the four swatch rows
        ys = [float(y) for y in re.findall(r'<text x="[^"]*" y="([^"]*)"', self.svg)]
        self.assertTrue(ys and min(ys) >= 4)

    def test_viewbox_covers_all_swatches(self):
        width = len(PALETTE) * 14 - 2
        self.assertIn(f'viewBox="0 0 {width} 8"', self.svg)

    def test_grid_text_has_palette_line_then_rows(self):
        text = swatch_grid_text(PALETTE[:2])
        lines = text.splitlines()
        self.assertTrue(lines[0].startswith("A=#8B2E3A B=#2B3A67"))
        self.assertEqual(len(lines), 1 + 4 + 4)

    def test_label_text_is_escaped(self):
        svg = swatch_card_svg([("A & B", "#000000")])
        self.assertIn("A &amp; B", svg)


if __name__ == "__main__":
    unittest.main()
