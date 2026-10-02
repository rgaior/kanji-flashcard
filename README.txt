KANJI FLASHCARDS — GITHUB PAGES

The app uses the checked-in `kanji-data.js` file as its local data source and
works offline without downloading kanji at startup. The current file contains
the 434 starter entries that were previously embedded in the app.

FEATURES
- First/Last KANJIDAMAGE number range
- Randomized cards within the exact site-number range
- Kanji -> Meaning and Meaning -> Kanji
- Previous / Next and Show Answer
- Onyomi, kunyomi, and first jukugo details when present in the local data
- PWA / Add to Home Screen support

GITHUB PAGES
Upload the contents of this folder to the root of a GitHub repository.
Settings -> Pages -> Deploy from a branch -> main -> / (root).
Open the resulting HTTPS site in Safari and use Share -> Add to Home Screen.

DATA LIMITATIONS AND REGENERATION
The included starter entries preserve their KANJIDAMAGE sequence numbers and
meanings. Readings and jukugo fields are currently empty because individual
entry pages could not be collected when this dataset was prepared. Entries
beyond the included starter set are not bundled yet.

With network access, regenerate the dataset by running:
  python3 scripts/generate_kanji_data.py

The script reads the listing and linked kanji pages through Jina Reader, parses
the listing table and explicitly labelled reading/jukugo fields, and writes a
deterministic `kanji-data.js`. Unrecognized page layouts or missing labels are
left empty rather than guessed. Page links must be present in the listing for
the script to crawl them.

SOURCE
https://www.kanjidamage.com/kanji
