"""Tests for pixel_svg.cli (pixel-svg-cli: input file -> -o SVG file)."""

import contextlib
import io
import os
import tempfile
import unittest

from pixel_svg.cli import main

GOOD = ".=#000000 X=#FFFFFF\n.X.\nX.X\n"


class CliTests(unittest.TestCase):
    def setUp(self):
        self._dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._dir.cleanup)
        self.dir = self._dir.name

    def _write(self, name, text):
        path = os.path.join(self.dir, name)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        return path

    def _run(self, argv):
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            code = main(argv)
        return code, err.getvalue()

    def test_good_input_writes_svg_and_exits_zero(self):
        src = self._write("in.txt", GOOD)
        out = os.path.join(self.dir, "out.svg")
        code, err = self._run([src, "-o", out])
        self.assertEqual(code, 0)
        self.assertEqual(err, "")
        with open(out, encoding="utf-8") as handle:
            svg = handle.read()
        self.assertTrue(svg.startswith("<svg "))
        self.assertIn('viewBox="0 0 3 2"', svg)

    def test_bad_palette_exits_nonzero_with_one_line(self):
        src = self._write("in.txt", "X=#GGGGGG\nX\n")
        out = os.path.join(self.dir, "out.svg")
        code, err = self._run([src, "-o", out])
        self.assertEqual(code, 1)
        self.assertEqual(len(err.strip().splitlines()), 1)
        self.assertIn("invalid color", err)
        self.assertFalse(os.path.exists(out))

    def test_ragged_grid_exits_nonzero_with_one_line(self):
        src = self._write("in.txt", "X=#FFFFFF\nXX\nX\n")
        out = os.path.join(self.dir, "out.svg")
        code, err = self._run([src, "-o", out])
        self.assertEqual(code, 1)
        self.assertEqual(len(err.strip().splitlines()), 1)
        self.assertIn("expected 2", err)

    def test_missing_input_file_exits_two(self):
        out = os.path.join(self.dir, "out.svg")
        code, err = self._run([os.path.join(self.dir, "nope.txt"), "-o", out])
        self.assertEqual(code, 2)
        self.assertIn("cannot read", err)

    def test_output_is_required(self):
        src = self._write("in.txt", GOOD)
        with self.assertRaises(SystemExit) as ctx:
            self._run([src])
        self.assertNotEqual(ctx.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
