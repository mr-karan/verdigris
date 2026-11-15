"""Run from the repository root: python3 -m unittest discover -s tests"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build  # noqa: E402
import palette as pal  # noqa: E402


def edited(change) -> pal.Palette:
    """The repository palette with one edit applied to its JSON."""
    raw = json.loads((ROOT / "palette.json").read_text())
    change(raw)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "palette.json"
        path.write_text(json.dumps(raw))
        return pal.load(path)


class Contrast(unittest.TestCase):
    def test_matches_wcag_reference_values(self):
        # WCAG's own examples: black on white is 21:1, and #777 on white
        # (4.48) misses AA where #767676 (4.54) meets it.
        self.assertAlmostEqual(pal.contrast("#000000", "#ffffff"), 21.0, places=2)
        self.assertAlmostEqual(pal.contrast("#777777", "#ffffff"), 4.48, places=2)
        self.assertAlmostEqual(pal.contrast("#767676", "#ffffff"), 4.54, places=2)
        self.assertEqual(pal.contrast("#2c6e64", "#f3f3ee"), pal.contrast("#f3f3ee", "#2c6e64"))

    def test_repository_palette_passes(self):
        self.assertEqual(pal.contrast_failures(pal.load()), [])

    def test_a_hue_made_too_light_fails(self):
        def lighten(raw):
            raw["flavours"]["limestone"]["colors"]["patina"] = "#4f9a8d"

        failures = pal.contrast_failures(edited(lighten))
        self.assertTrue(any("limestone" in f and "syntax keyword on bg" in f for f in failures), failures)

    def test_a_comment_made_too_faint_fails(self):
        def fade(raw):
            raw["flavours"]["slate"]["colors"]["fg_subtle"] = "#4a5552"

        failures = pal.contrast_failures(edited(fade))
        self.assertTrue(any("slate" in f and "syntax comment" in f for f in failures), failures)


class Palette(unittest.TestCase):
    def test_role_pointing_at_a_missing_colour_is_rejected(self):
        def break_role(raw):
            raw["roles"]["syntax"]["keyword"]["color"] = "teal"

        with self.assertRaisesRegex(pal.PaletteError, r"roles\.syntax\.keyword.*'teal'"):
            edited(break_role)

    def test_colour_that_is_not_hex_is_rejected(self):
        def break_hex(raw):
            raw["flavours"]["slate"]["colors"]["bg"] = "#15A19"

        with self.assertRaisesRegex(pal.PaletteError, r"flavours\.slate\.colors\.bg"):
            edited(break_hex)

    def test_flavours_must_define_the_same_colours(self):
        def drop(raw):
            del raw["flavours"]["slate"]["colors"]["brass"]

        with self.assertRaisesRegex(pal.PaletteError, "brass"):
            edited(drop)


class Ports(unittest.TestCase):
    def test_committed_files_match_the_palette(self):
        result = subprocess.run(
            [sys.executable, "build.py", "--check"], cwd=ROOT, capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_every_port_follows_a_palette_change(self):
        def recolour(raw):
            for flavour in raw["flavours"].values():
                flavour["colors"]["patina"] = "#123456" if flavour["appearance"] == "light" else "#abcdef"

        changed = edited(recolour)
        for name in build.port_names():
            rendered = "".join(build.render_port(name, changed).values())
            with self.subTest(port=name):
                self.assertIn("#123456", rendered)
                self.assertIn("#abcdef", rendered)

    def test_t3_theme_stays_within_t3_limits(self):
        theme = json.loads((ROOT / "ports" / "t3code" / "verdigris.json").read_text())
        self.assertEqual(len(theme["colors"]), 61)
        self.assertEqual(set(theme["colors"]), set(theme["variants"]["dark"]))
        self.assertLessEqual(len(theme["css"]), 20_000)
        self.assertLessEqual((ROOT / "ports" / "t3code" / "verdigris.json").stat().st_size, 32 * 1024)


if __name__ == "__main__":
    unittest.main()
