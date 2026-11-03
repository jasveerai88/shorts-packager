import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from shorts_packager import pack, truncate_at_word_boundary, LIMIT


class TestShortsPackager(unittest.TestCase):
    def test_short_title_all_fits(self):
        r = pack("Cats React to Cucumbers", "#shorts #cats #funny")
        self.assertLessEqual(len(r["title"]), LIMIT)
        self.assertEqual(r["hashtags_overflow"], [])
        self.assertEqual(r["hashtags_in_title"], ["#shorts", "#cats", "#funny"])
        self.assertIn("Cats React to Cucumbers", r["title"])
        self.assertFalse(r["truncated"])
        self.assertEqual(r["verdict"], "PASS")
        self.assertIn("Credits:", r["description"])

    def test_long_title_hashtags_overflow_to_description(self):
        title = "This Goalkeeper Made The Most Impossible Save You Will Ever See In Football History"
        r = pack(title, "#shorts #football #goalkeeper #viral #amazing")
        self.assertLessEqual(len(r["title"]), LIMIT)
        self.assertTrue(len(r["hashtags_overflow"]) >= 1, r)
        # Overflow hashtags must appear in the description
        for tag in r["hashtags_overflow"]:
            self.assertIn(tag, r["description"])
        # Title wording itself is unchanged (base title is a prefix of the result)
        self.assertTrue(r["title"].startswith(title[:20]))

    def test_overlong_title_flagged_and_not_mid_word(self):
        title = ("word " * 30).strip()  # 149 chars, no hashtags needed to overflow
        self.assertGreater(len(title), LIMIT)
        r = pack(title, "#shorts")
        self.assertTrue(r["truncated"])
        self.assertEqual(r["verdict"], "TRUNCATED")
        self.assertTrue(r["warnings"])
        self.assertLessEqual(len(r["base_title"]), LIMIT)
        # Truncation at a word boundary: base title must not end mid-word —
        # the original continues with a space after the truncated text.
        self.assertTrue(title[len(r["base_title"])] == " " or r["base_title"] == title[:LIMIT])

    def test_truncate_helper_never_mid_word(self):
        text = "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma tau upsilon phi chi psi omega extra"
        out, was = truncate_at_word_boundary(text, 50)
        self.assertTrue(was)
        self.assertLessEqual(len(out), 50)
        self.assertEqual(text[len(out)], " ")

    def test_custom_hook_and_bare_hashtags(self):
        r = pack("My Title", "shorts viral", hook="You will not believe this save")
        self.assertEqual(r["hashtags_in_title"], ["#shorts", "#viral"])
        self.assertTrue(r["description"].startswith("You will not believe this save"))

    def test_no_hashtags(self):
        r = pack("Simple Title")
        self.assertEqual(r["title"], "Simple Title")
        self.assertEqual(r["verdict"], "PASS")
        self.assertIn("Credits:", r["description"])


if __name__ == "__main__":
    unittest.main()
