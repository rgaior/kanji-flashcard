import re
import unittest
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parents[1] / "kanji-data.js"


class BundledKanjiDataTests(unittest.TestCase):
    def test_data_is_exposed_with_sequential_numbers(self):
        source = DATA_FILE.read_text(encoding="utf-8")

        self.assertEqual(len(re.findall(r"^\s*\{ kanji:", source, re.MULTILINE)), 1634)
        self.assertIn(
            "].map((entry, index) => ({ ...entry, number: index + 1 }));",
            source,
        )
        self.assertIn("window.KANJI_DATA = kanjiData;", source)


if __name__ == "__main__":
    unittest.main()
