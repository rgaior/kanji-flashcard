#!/usr/bin/env python3
"""Generate the app's bundled data from KANJIDAMAGE's listing and entry pages."""

import html
import json
import re
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
INDEX_URL = "https://www.kanjidamage.com/kanji/"
OUTPUT = ROOT / "kanji-data.js"
USER_AGENT = "kanji-flashcard-data-generator/1.0"
LINK_RE = re.compile(r"\[([^\]]*)\]\((https?://[^ )]+|/kanji/[^ )]*)\)")
TAG_RE = re.compile(r"<[^>]*>")
MARKDOWN_RE = re.compile(r"[*_`]")
FIELD_LABELS = {
    "onyomi": ("on'yomi", "onyomi"),
    "kunyomi": ("kun'yomi", "kunyomi"),
    "firstJukugo": ("first jukugo",),
    "firstJukugoMeaning": ("first jukugo meaning", "meaning of first jukugo"),
}


def clean(value):
    value = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    return html.unescape(MARKDOWN_RE.sub("", TAG_RE.sub("", value))).strip()


def parse_listing(markdown):
    entries = []
    for line in markdown.splitlines():
        if not re.match(r"^\s*\|", line):
            continue
        columns = [part.strip() for part in line.split("|")]
        if len(columns) < 6 or not columns[1].isdigit():
            continue

        kanji = re.sub(r"\s+", "", clean(columns[3]))
        if kanji == "Image" or len(kanji) > 3:
            kanji = ""
        entry = {
            "number": int(columns[1]),
            "kanji": kanji,
            "meaning": clean(columns[4]),
            "onyomi": "",
            "kunyomi": "",
            "firstJukugo": "",
            "firstJukugoMeaning": "",
        }
        links = [url for _, url in LINK_RE.findall(columns[3])]
        entry["_url"] = next(
            (
                urljoin(INDEX_URL, url)
                for url in links
                if urlparse(urljoin(INDEX_URL, url)).hostname == "www.kanjidamage.com"
                and urlparse(urljoin(INDEX_URL, url)).path.rstrip("/") != "/kanji"
                and urlparse(urljoin(INDEX_URL, url)).path.startswith("/kanji/")
            ),
            "",
        )
        entries.append(entry)
    return entries


def parse_detail(markdown):
    details = {key: "" for key in FIELD_LABELS}
    for line in markdown.splitlines():
        stripped = line.strip().strip("|").strip()
        if not stripped:
            continue
        columns = [clean(part) for part in line.strip().strip("|").split("|")]
        for key, aliases in FIELD_LABELS.items():
            for alias in aliases:
                label = re.compile(rf"^\s*(?:\*\*)?{re.escape(alias)}(?:\*\*)?\s*(?::|：|\|)\s*(.*)$", re.IGNORECASE)
                match = label.match(stripped)
                if match:
                    details[key] = clean(match.group(1).split("|", 1)[0])
                    break
                if len(columns) > 1 and columns[0].strip().lower() == alias:
                    details[key] = columns[1]
                    break
    return details


def fetch_page(url):
    request = Request("https://r.jina.ai/" + url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def write_data(entries, output=OUTPUT):
    public_entries = [
        {key: value for key, value in entry.items() if not key.startswith("_")}
        for entry in entries
    ]
    output.write_text(
        "window.KANJI_DATA = "
        + json.dumps(public_entries, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )


def main():
    entries = parse_listing(fetch_page(INDEX_URL))
    if not entries:
        raise RuntimeError("No numbered kanji rows found in the KANJIDAMAGE listing")
    linked = [entry for entry in entries if entry["_url"]]
    print(f"Found {len(entries)} numbered entries; crawling {len(linked)} linked pages.")
    for index, entry in enumerate(linked):
        try:
            entry.update(parse_detail(fetch_page(entry["_url"])))
        except (OSError, URLError, UnicodeError) as error:
            print(f"Warning: could not read KANJIDAMAGE #{entry['number']}: {error}", file=sys.stderr)
        if index + 1 < len(linked):
            time.sleep(0.1)
    write_data(entries)
    print(f"Wrote {len(entries)} entries to {OUTPUT}")


if __name__ == "__main__":
    main()
