"""Bring your own month: read a bookmarks export, then label it. Plain code, no model.

    python3 loop.py import FILE                  # the links you saved 30 to 60 days ago
    python3 loop.py import FILE --all            # every link in the file
    python3 loop.py import FILE --from 2026-09-24 --to 2026-10-24
    python3 loop.py label                        # label them, one at a time, in your terminal

`import` reads any CSV with a link column and a date column, whatever the columns are called
(an X bookmarks export, a Reddit or YouTube export, the CSV from the README's prompt). When the
export has the post's text, it goes into the `text` column, so the agent reads the post and not
a login page. Labels you already gave are kept when you import again.
"""
import csv
import re
import shutil
import subprocess
import textwrap
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
LINKS = ROOT / "verifier" / "links.csv"
DECISIONS = ROOT / "verifier" / "decisions.csv"
HARNESS = ROOT / "harness"
COLS = ["date", "source", "title", "url", "label", "text"]

# Column names seen in real exports, lower case. The first one present wins.
URL = ["url", "post url", "link", "href", "permalink", "tweet url", "post link", "web url"]
DATE = ["date", "date saved", "saved", "saved at", "bookmarked at", "bookmarked", "added",
        "date added", "published at utc", "published at", "published", "created_at", "created at",
        "created", "posted at", "timestamp", "time"]
TITLE = ["title", "headline", "name"]
SOURCE = ["source", "site", "publication", "channel", "subreddit"]
# The post itself, then what it quotes or links. Joined into `text`.
BODY = ["text", "tweet", "full text", "body", "content", "selftext", "description", "summary"]
EXTRA = ["attached content and quote previews", "quoted post url", "resource urls"]

SAMPLE_HOST = "sample.invalid"


def _pick(header, names):
    low = {h.strip().lower(): h for h in header if h}
    return next((low[n] for n in names if n in low), None)


def parse_date(raw):
    s = (raw or "").strip()
    if not s:
        return None
    if re.fullmatch(r"\d{10}(\.\d+)?", s):
        return datetime.fromtimestamp(float(s), timezone.utc).date()
    if re.fullmatch(r"\d{13}", s):
        return datetime.fromtimestamp(int(s) / 1000, timezone.utc).date()
    m = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})", s)
    if m:
        return date(*map(int, m.groups()))
    for fmt in ("%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d", "%m/%d/%y", "%b %d, %Y", "%B %d, %Y",
                "%d %b %Y", "%d %B %Y", "%a %b %d %H:%M:%S %z %Y"):
        for cand in (s, s.split(" ")[0], s.split("T")[0]):
            try:
                return datetime.strptime(cand, fmt).date()
            except ValueError:
                pass
    return None


def _first_line(s):
    return next((re.sub(r"\s+", " ", l).strip() for l in (s or "").splitlines() if l.strip()), "")


def _row(r, cols):
    url = (r.get(cols["url"]) or "").strip()
    day = parse_date(r.get(cols["date"]))
    if not url or not day:
        return None
    host = urlparse(url).netloc.lower().removeprefix("www.")
    is_x = host in ("x.com", "twitter.com", "mobile.twitter.com")
    get = lambda name: (r.get(name) or "").strip() if name else ""

    bodies = [get(c) for c in cols["body"] if get(c)]
    extras = [(c, get(c)) for c in cols["extra"] if get(c)]
    handle, author = get(cols["handle"]), get(cols["author"])

    title = get(cols["title"]) or _first_line(bodies[0] if bodies else extras[0][1] if extras else "")
    source = (get(cols["source"]) or (f"X @{handle.lstrip('@')}" if is_x and handle else "")
              or handle or author or (("X " if is_x else "") + host))
    parts = []
    if get(cols["topic"]):
        parts.append(f"Topic: {get(cols['topic'])}")
    if author or handle:
        parts.append(f"Posted by {author}" + (f" (@{handle.lstrip('@')})" if handle else "")
                     + f" on {day}")
    parts += bodies
    parts += [f"{c[0].upper() + c[1:]}:\n{v}" for c, v in
              ((k.strip(), v) for k, v in extras)]
    return {"date": day.isoformat(), "source": source, "title": title[:140] or url,
            "url": url, "label": get(cols["label"]), "text": "\n\n".join(parts)}


def _git_tracked_clean(path):
    out = subprocess.run(["git", "status", "--porcelain", "--", str(path)], cwd=ROOT,
                         capture_output=True, text=True).stdout
    return not out.strip()


def import_file(path, start=None, end=None, keep_all=False):
    """Write verifier/links.csv from any bookmarks CSV. Returns nothing; prints what it did."""
    path = Path(path).expanduser()
    if not path.exists():
        raise SystemExit(f"No file at {path}.")
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        raw = list(reader)

    cols = {"url": _pick(header, URL), "date": _pick(header, DATE), "title": _pick(header, TITLE),
            "source": _pick(header, SOURCE), "label": _pick(header, ["label"]),
            "handle": _pick(header, ["handle", "username", "screen name", "screen_name"]),
            "author": _pick(header, ["author", "author name", "user", "posted by"]),
            "topic": _pick(header, ["topic", "category"]),
            "body": [h for n in BODY if (h := _pick(header, [n]))],
            "extra": [h for n in EXTRA if (h := _pick(header, [n]))]}
    if not cols["url"] or not cols["date"]:
        missing = " and ".join(k for k in ("url", "date") if not cols[k])
        raise SystemExit(
            f"Could not find the {missing} column in {path.name}.\n"
            f"Its columns are: {', '.join(header)}\n"
            f"Rename the column that holds the link to `url` and the one with the date to `date`, "
            f"then run this again.")

    rows, bad, seen = [], 0, set()
    for r in raw:
        row = _row(r, cols)
        if row is None:
            bad += 1
        elif row["url"] not in seen:
            seen.add(row["url"])
            rows.append(row)
    if not rows:
        raise SystemExit(f"No row in {path.name} has both a link and a date I can read.")

    days = sorted(r["date"] for r in rows)
    if keep_all:
        lo, hi = days[0], days[-1]
    elif start or end:
        lo, hi = start or days[0], end or days[-1]
    else:
        today = date.today()
        lo, hi = (today - timedelta(60)).isoformat(), (today - timedelta(30)).isoformat()
    kept = sorted((r for r in rows if lo <= r["date"] <= hi), key=lambda r: r["date"])
    if not kept:
        raise SystemExit(
            f"None of your links fall between {lo} and {hi}.\n"
            f"Your file runs from {days[0]} to {days[-1]}.\n"
            f"Pick a window:  python3 loop.py import {path} --from {days[0]} --to {days[-1]}\n"
            f"or keep all:    python3 loop.py import {path} --all")

    # Keep any labels already given, by link.
    replacing_sample = False
    if LINKS.exists():
        with open(LINKS, newline="") as f:
            old = list(csv.DictReader(f))
        replacing_sample = any(SAMPLE_HOST in (r.get("url") or "") for r in old)
        if not replacing_sample:
            labels = {r["url"]: r.get("label", "") for r in old if (r.get("label") or "").strip()}
            for r in kept:
                r["label"] = r["label"] or labels.get(r["url"], "")
            if old and not _git_tracked_clean(LINKS):
                shutil.copy(LINKS, LINKS.with_name("links.backup.csv"))

    with open(LINKS, "w", newline="") as f:
        w = csv.DictWriter(f, COLS)
        w.writeheader()
        w.writerows(kept)

    if replacing_sample:
        # The sample's decisions, sources and saved pages belong to the sample month.
        with open(DECISIONS, newline="") as f:
            first = f.readline()
        DECISIONS.write_text(first if first.startswith("date") else
                             "date,question,outcome,how_it_turned_out\n")
        (HARNESS / "sources.md").unlink(missing_ok=True)
        shutil.rmtree(HARNESS / "cache", ignore_errors=True)
        shutil.rmtree(HARNESS / "inbox", ignore_errors=True)
    elif (HARNESS / "sources.md").exists() and "No notes on any of them yet" in (HARNESS / "sources.md").read_text():
        (HARNESS / "sources.md").unlink()  # nothing written in it yet: rebuild from the new links

    labelled = sum(bool(r["label"].strip()) for r in kept)
    with_text = sum(bool(r["text"]) for r in kept)
    print(f"Kept {len(kept)} of {len(rows)} links, saved from {kept[0]['date']} to {kept[-1]['date']}"
          + ("" if keep_all or start or end else " (30 to 60 days ago)") + ".")
    if len(kept) < len(rows):
        print(f"  The other {len(rows) - len(kept)} are outside that window. "
              f"Change it with --from and --to, or keep everything with --all.")
    if bad:
        print(f"  Skipped {bad} rows with no link or no date I could read.")
    if cols["date"].strip().lower().startswith(("published", "created", "posted")):
        print(f"  Dates come from the `{cols['date']}` column: when the post was published. "
              f"X does not record when you saved a post, so this stands in for it. That is fine.")
    print(f"  {with_text} of {len(kept)} links carry their page text, so the agent reads the post"
          f" itself." if with_text else
          "  No column with the post's text, so the agent fetches each page. Pages behind a "
          "login (X, LinkedIn) come back as the title only.")
    if labelled:
        print(f"  {labelled} links already have a label.")
    if replacing_sample:
        print("  The made-up sample month is replaced (its decisions, sources and saved pages too).")
        print("  To bring it back:  git checkout -- verifier harness")
    print(f"Wrote {LINKS.relative_to(ROOT)}.\n")


# ---------------------------------------------------------------- label

KEYS = {"s": "signal", "h": "should have", "n": "noise"}


def label(redo=False):
    """Show each unlabelled link and ask for s / h / n. Saves after every answer."""
    import sys
    sys.path.insert(0, str(ROOT / "verifier"))
    from score import _week

    with open(LINKS, newline="") as f:
        reader = csv.DictReader(f)
        cols = list(reader.fieldnames)
        rows = list(reader)
    links = sorted((r for r in rows if (r.get("url") or "").strip()), key=lambda r: r["date"])
    first = date.fromisoformat(links[0]["date"])
    for i, r in enumerate(links, 1):
        r["_id"], r["_week"] = f"L{i:03d}", _week(r["date"], first)
    todo = [r for r in links if redo or not (r.get("label") or "").strip()]
    if not todo:
        print(f"All {len(links)} links have a label. To go through them again: "
              f"python3 loop.py label --redo")
        return

    def save():
        with open(LINKS, "w", newline="") as f:
            w = csv.DictWriter(f, cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)

    print(textwrap.dedent(f"""
        {len(todo)} links to label. For each one, ask yourself: did I act on this?

          s  signal       I acted on it and it helped
          h  should have  I did not act on it, and now wish I had
          n  noise        I never used it
          Enter           not sure: leave it empty (never scored)
          b  back one     q  save and stop (run `label` again to carry on)

        Every answer is saved at once.""").rstrip())
    i = 0
    while i < len(todo):
        r = todo[i]
        text = re.sub(r"\s+", " ", r.get("text") or "").strip()
        print("\n" + "-" * 72)
        print(f"[{i + 1}/{len(todo)}]  {r['_id']} · week {r['_week']} · {r['date']} · {r['source']}"
              + (f"   (now: {r['label']})" if (r.get("label") or "").strip() else ""))
        print(textwrap.fill(r["title"], 72))
        print(r["url"])
        if text:
            print()
            print(textwrap.fill(text[:700] + (" ..." if len(text) > 700 else ""), 72))
        try:
            ans = input("\ns / h / n, Enter to skip, b back, q stop: ").strip().lower()
        except EOFError:
            print("\nNo keyboard here. Run `python3 loop.py label` in your own terminal, "
                  "not through an agent.")
            break
        if ans == "q":
            break
        if ans == "b":
            i = max(i - 1, 0)
            continue
        if ans in KEYS:
            r["label"] = KEYS[ans]
            save()
        elif ans:
            print("  Type s, h, n, b, q, or press Enter.")
            continue
        i += 1
    save()
    left = sum(not (r.get("label") or "").strip() for r in links)
    print(f"\nSaved. {len(links) - left} of {len(links)} links labelled"
          + (f", {left} still empty." if left else "."))
