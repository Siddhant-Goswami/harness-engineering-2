#!/usr/bin/env python3
"""Read saved links by id.

    python3 tools/fetch.py L001 L002      # prints the text of each link
    python3 tools/fetch.py --week 2       # every link of week 2

From a script:

    import sys; sys.path.insert(0, "tools")
    from fetch import get, ids
    for i in ids(1):            # every link id in week 1
        text = get(i)

Pages are kept in cache/ after the first fetch, so a week reads the same
every time it is run.
"""
import csv
import hashlib
import html
import re
import sys
import urllib.request
from pathlib import Path

HARNESS = Path(__file__).resolve().parent.parent
INBOX = HARNESS / "inbox"
CACHE = HARNESS / "cache"
MAX_CHARS = 4000
WEEK_CHARS = 24000   # --week stays under this, so the shell shows it instead of saving it to a file


def _rows():
    for f in sorted(INBOX.glob("week-*.csv")):
        with open(f, newline="") as fh:
            for r in csv.DictReader(fh):
                r["week"] = int(f.stem.split("-")[1])
                yield r


def ids(week):
    """The link ids of one week, oldest first."""
    return [r["id"] for r in _rows() if r["week"] == int(week)]


def cache_path(url):
    return CACHE / (hashlib.sha1(url.encode()).hexdigest()[:16] + ".txt")


def _download(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (briefing-agent)"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read(2_000_000).decode("utf-8", "replace")
    raw = re.sub(r"(?is)<(script|style|nav|footer|svg)\b.*?</\1>", " ", raw)
    text = html.unescape(re.sub(r"(?s)<[^>]+>", " ", raw))
    return re.sub(r"\s+", " ", text).strip()


def get(link_id, limit=MAX_CHARS):
    """The text of one link: title, source, date, then the page."""
    row = next((r for r in _rows() if r["id"] == link_id), None)
    if row is None:
        return f"{link_id}: no such link in inbox/"
    path = cache_path(row["url"])
    if not path.exists():
        CACHE.mkdir(exist_ok=True)
        try:
            body = _download(row["url"])
        except Exception as e:  # a dead link is still a link the reader saved
            body = f"(could not fetch the page: {e})"
        path.write_text(body)
    head = f"{row['id']} | {row['date']} | {row['source']} | {row['title']}\n{row['url']}\n"
    page = path.read_text()
    return head + page[:limit] + (" [...]" if len(page) > limit else "")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    week = sys.argv[1] == "--week" and len(sys.argv) > 2
    wanted = ids(sys.argv[2]) if week else sys.argv[1:]
    limit = min(MAX_CHARS, WEEK_CHARS // max(len(wanted), 1) - 150) if week else MAX_CHARS
    cut = False
    for link_id in wanted:
        text = get(link_id, limit)
        cut = cut or text.endswith(" [...]")
        print(text)
        print()
    if week and cut:
        print(f"(Pages marked [...] are cut to {limit} characters so the whole week fits on one "
              f"screen. For a whole page: python3 tools/fetch.py L001)")
