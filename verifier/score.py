#!/usr/bin/env python3
"""The verifier. Plain code, no model.

It reads your labels (links.csv) and your decisions (decisions.csv) and
scores a brief against them. Neither agent may read or edit this folder.

    python3 verifier/score.py traces/round-0      # score the briefs in a folder
"""
import csv
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent

# The three numbers to tune after a dry run on your own 30 days.
NOISE_PENALTY = 0.5     # cost of calling one noise item important
DECISION_WEIGHT = 2     # one right decision counts as much as this many links
VISIBLE_WEEKS = [1, 2, 3]
HIDDEN_WEEK = 4

SIGNAL = {"acted", "should_have"}


def _label(raw):
    s = (raw or "").strip().lower()
    if s.startswith("act"):
        return "acted"
    if s.startswith("should"):
        return "should_have"
    if s.startswith("noise"):
        return "noise"
    return ""  # not labelled yet: shown to the agent, never scored


def _week(d, first):
    return min((date.fromisoformat(d) - first).days // 7 + 1, HIDDEN_WEEK)


def load_links():
    """Every saved link, oldest first, with an id (L001...) and a week (1 to 4)."""
    with open(HERE / "links.csv", newline="") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("url") or "").strip()]
    rows.sort(key=lambda r: r["date"])
    first = date.fromisoformat(rows[0]["date"])
    for i, r in enumerate(rows, 1):
        r["id"] = f"L{i:03d}"
        r["week"] = _week(r["date"], first)
        r["label"] = _label(r.get("label"))
    return rows


def load_decisions():
    path = HERE / "decisions.csv"
    if not path.exists():
        return []
    first = date.fromisoformat(load_links()[0]["date"])
    with open(path, newline="") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    rows.sort(key=lambda r: r["date"])
    for i, r in enumerate(rows, 1):
        r["id"] = f"D{i}"
        r["week"] = _week(r["date"], first)
        r["outcome"] = r["outcome"].strip().lower()
    return rows


def scored_part(brief):
    """Only 'What changed' and 'What to do' are scored.

    A link cited under 'Who disagrees' is neither a hit nor a penalty: the
    brief is allowed to quote the weak side of an argument.
    """
    parts = re.split(r"(?m)^#+\s*(.+)$", brief)
    if len(parts) < 3:
        return brief
    keep = []
    for heading, body in zip(parts[1::2], parts[2::2]):
        if "disagree" not in heading.lower():
            keep.append(body)
    return "\n".join(keep)


def score_week(week, brief, open_hidden=False):
    if week == HIDDEN_WEEK and not open_hidden:
        raise SystemExit("Week four stays closed. Only `loop.py final` opens it, once.")
    links = [r for r in load_links() if r["week"] == week]
    decisions = [d for d in load_decisions() if d["week"] == week]

    cited = set(re.findall(r"\bL\d{3}\b", scored_part(brief)))
    signal = [r for r in links if r["label"] in SIGNAL]
    hits = [r for r in signal if r["id"] in cited]
    missed = [r for r in signal if r["id"] not in cited]
    noise = [r for r in links if r["label"] == "noise" and r["id"] in cited]

    said = {k.upper(): v.lower() for k, v in re.findall(
        r"(?mi)^\W*(D\d+)\W*:\W*(adopt|wait|ignore)\b", brief)}
    right, wrong = [], []
    for d in decisions:
        (right if said.get(d["id"]) == d["outcome"] else wrong).append(
            {"id": d["id"], "question": d["question"],
             "brief_said": said.get(d["id"], "nothing"), "turned_out": d["outcome"]})

    total = len(signal) + DECISION_WEIGHT * len(decisions)
    points = len(hits) + DECISION_WEIGHT * len(right) - NOISE_PENALTY * len(noise)
    slim = lambda r: {k: r[k] for k in ("id", "source", "title", "label")}
    return {
        "week": week,
        "score": round(points / total, 3) if total else None,
        "hits": len(hits), "signal": len(signal), "noise_flagged": len(noise),
        "decisions_right": len(right), "decisions": len(decisions),
        "missed": [slim(r) for r in missed],
        "noise": [slim(r) for r in noise],
        "wrong_decisions": wrong,
    }


def mean(scores):
    vals = [s["score"] for s in scores if s["score"] is not None]
    return round(sum(vals) / len(vals), 3) if vals else None


def table(scores):
    lines = ["week  score   found   noise called important   decisions right"]
    for s in scores:
        lines.append(f"  {s['week']}   {s['score']:>5}   {s['hits']}/{s['signal']}     "
                     f"{s['noise_flagged']:<22}   {s['decisions_right']}/{s['decisions']}")
    lines.append(f"mean  {mean(scores):>5}")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    folder = Path(sys.argv[1])
    out = []
    for w in VISIBLE_WEEKS:
        f = folder / f"week-{w}.brief.md"
        if f.exists():
            out.append(score_week(w, f.read_text()))
    print(table(out))
