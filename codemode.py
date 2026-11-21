#!/usr/bin/env python3
"""The same job, two ways. Run it and compare the two rows.

    python3 codemode.py          # week 1
    python3 codemode.py 2        # another week

Way 1: the agent calls the fetch tool once per link. Every page passes through the model.
Way 2: the agent writes one script. The script reads every page; only its answer comes back.
"""
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import json

from loop import BRIEF_MODEL, HARNESS, TRACES, claude, events, tokens

week = int(sys.argv[1]) if len(sys.argv) > 1 else 1
WORD = "Kiln"
JOB = (f"Which links in inbox/week-{week}.csv mention the word {WORD} anywhere in their text? "
       "Reply with the link ids only, comma separated, lowest first.")

WAYS = {
    "one call per link": JOB + " Read the links with `python3 tools/fetch.py`, one link id per "
                               "call. Do not write a script.",
    "one script": JOB + " Write ONE script that reads every link and prints only the matching "
                        "ids. The docstring of tools/fetch.py shows how to import it. Create the "
                        "file with the Write tool as scratch/find.py, then run exactly "
                        "`python3 scratch/find.py`. Do not fetch links any other way.",
}


def returned(trace):
    """Characters of tool output that went back through the model."""
    total = 0
    for e in events(trace):
        if e.get("type") == "user":
            for c in e["message"].get("content", []):
                if isinstance(c, dict) and c.get("type") == "tool_result":
                    total += len(json.dumps(c.get("content", "")))
    return total


def run(item):
    name, prompt = item
    t0 = time.time()
    trace = TRACES / "codemode" / f"{name.replace(' ', '-')}.jsonl"
    r = claude(prompt, HARNESS, BRIEF_MODEL, trace, ["--tools", "Bash,Read,Write,Edit"])
    return name, r, time.time() - t0, returned(trace)


with ThreadPoolExecutor(2) as pool:
    results = list(pool.map(run, WAYS.items()))

print(f"{'':<20}{'model steps':>12}{'read by the model':>19}{'tokens':>9}{'seconds':>9}   answer")
for name, r, secs, chars in results:
    answer = " ".join((r.get("result") or "").split())[:60]
    print(f"{name:<20}{r.get('num_turns', 0):>12}{chars:>13,} chars{tokens(r):>9,}{secs:>9.0f}   {answer}")

sys.path.insert(0, str(HARNESS / "tools"))
from fetch import get, ids  # noqa: E402
truth = [i for i in ids(week) if WORD.lower() in get(i).lower()]
print(f"{'plain code':<20}{0:>12}{0:>13,} chars{0:>9}{0:>9}   {', '.join(truth)}")
print("\nRaw traces: traces/codemode/")
