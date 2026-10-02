import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from generate_kanji_data import parse_detail, parse_listing


class KanjiDataParserTests(unittest.TestCase):
    def test_listing_preserves_site_number_and_linked_entry_url(self):
        listing = (
            "| No. | Radical | Kanji | Meaning |\n"
            "| 12 | something | [下](https://www.kanjidamage.com/kanji/below) | below |\n"
        )
        entry, = parse_listing(listing)
        self.assertEqual(entry["number"], 12)
        self.assertEqual(entry["kanji"], "下")
        self.assertEqual(entry["meaning"], "below")
        self.assertEqual(entry["_url"], "https://www.kanjidamage.com/kanji/below")

    def test_detail_parser_extracts_labelled_reading_and_jukugo_fields(self):
        detail = (
            "| Onyomi | カ |\n"
            "| Kunyomi | した |\n"
            "First jukugo: 下手\n"
            "Meaning of first jukugo: unskilled\n"
        )
        self.assertEqual(
            parse_detail(detail),
            {
                "onyomi": "カ",
                "kunyomi": "した",
                "firstJukugo": "下手",
                "firstJukugoMeaning": "unskilled",
            },
        )


if __name__ == "__main__":
    unittest.main()
