#!/usr/bin/env python3
"""The outer loop around the briefing agent.

Nine steps. Two of them call a model (marked MODEL). The rest is plain code.

    1  split the saved links into weeks          prepare
    2  write a brief for weeks 1 to 3     MODEL  brief
    3  score each brief against the labels       (verifier/score.py)
    4  pick the worst week, write a report       report
    5  propose one change, with a reason  MODEL  optimize
    6  check the change stayed inside the walls  walls
    7  run steps 2 and 3 again on the new setup
    8  keep the change if the score rose, else revert
    9  after the last round, open week four once final

Commands:

    python3 loop.py prepare        step 1
    python3 loop.py brief 1        one brief, printed (no scoring)
    python3 loop.py baseline       steps 2-3 on the setup as it is now; tags it `baseline`
    python3 loop.py round          steps 4-8, once
    python3 loop.py run 5          five rounds
    python3 loop.py final          step 9
    python3 loop.py status         the scores so far
"""
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HARNESS, TRACES, OPTIMIZER = ROOT / "harness", ROOT / "traces", ROOT / "optimizer"
sys.path.insert(0, str(ROOT / "verifier"))
import score as verifier  # noqa: E402

BRIEF_MODEL = os.environ.get("BRIEF_MODEL", "sonnet")   # writes the briefs
OPT_MODEL = os.environ.get("OPT_MODEL", "opus")         # proposes the changes
MIN_GAIN = 0.01      # a change must beat the current score by this much to stay
MAX_TURNS = 40
SCORES = ROOT / "scores.csv"
OPENED = ROOT / "verifier" / "week4-opened.json"
WEEKS = verifier.VISIBLE_WEEKS


# ---------------------------------------------------------------- helpers

def git(*args, check=True):
    return subprocess.run(["git", *args], cwd=ROOT, check=check,
                          capture_output=True, text=True).stdout.strip()


def claude(prompt, cwd, model, trace, extra=()):
    """One headless Claude Code run. The raw trace goes to a file; the result comes back."""
    trace.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["claude", "-p", prompt, "--model", model,
           "--output-format", "stream-json", "--verbose",
           "--setting-sources", "project",      # this folder's rules only, not your own
           "--settings", str(HARNESS / ".claude" / "settings.json"),
           "--strict-mcp-config",               # no connectors
           "--permission-mode", "dontAsk",      # anything not allowed is refused
           "--no-session-persistence", "--max-turns", str(MAX_TURNS), *extra]
    with open(trace, "w") as out:
        subprocess.run(cmd, cwd=cwd, stdout=out, stderr=subprocess.DEVNULL,
                       stdin=subprocess.DEVNULL, timeout=1200)
    result = {}
    for e in events(trace):
        if e.get("type") == "result":
            result = e
    return result


def events(trace):
    for line in open(trace):
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            pass


def tool_inputs(trace):
    for e in events(trace):
        if e.get("type") == "assistant":
            for c in e["message"].get("content", []):
                if c.get("type") == "tool_use":
                    yield c["name"], json.dumps(c.get("input", {}))


def tokens(result):
    u = result.get("usage", {})
    return (u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
            + u.get("cache_creation_input_tokens", 0) + u.get("output_tokens", 0))


def folder_hash(*folders):
    h = hashlib.sha1()
    for folder in folders:
        for f in sorted(Path(folder).rglob("*")):
            if f.is_file():
                h.update(str(f.relative_to(folder)).encode() + f.read_bytes())
    return h.hexdigest()


def rows():
    if not SCORES.exists():
        return []
    with open(SCORES, newline="") as f:
        return list(csv.DictReader(f))


def add_row(name, scores, verdict, reason):
    new = not SCORES.exists()
    with open(SCORES, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["round", "week1", "week2", "week3", "mean", "verdict", "reason"])
        w.writerow([name, *[s["score"] for s in scores], verifier.mean(scores), verdict, reason])


def current():
    """The round whose setup is live now: the baseline, or the last change that was kept."""
    kept = [r for r in rows() if r["verdict"] in ("baseline", "kept")]
    if not kept:
        raise SystemExit("No baseline yet. Run: python3 loop.py baseline")
    return kept[-1]["round"], float(kept[-1]["mean"])


# ---------------------------------------------------------------- step 1

def prepare():
    """Split the labelled links into weeks. The agent's copy carries no labels."""
    links = verifier.load_links()
    inbox, cache = HARNESS / "inbox", HARNESS / "cache"
    inbox.mkdir(exist_ok=True)
    cache.mkdir(exist_ok=True)
    cols = ["id", "date", "source", "title", "url"]
    for w in WEEKS:
        with open(inbox / f"week-{w}.csv", "w", newline="") as f:
            out = csv.DictWriter(f, cols, extrasaction="ignore")
            out.writeheader()
            out.writerows(r for r in links if r["week"] == w)
    if not OPENED.exists():
        (inbox / "week-4.csv").unlink(missing_ok=True)

    # The sample pages are fictional, so their text ships with the sample.
    sys.path.insert(0, str(HARNESS / "tools"))
    from fetch import cache_path
    sample = ROOT / "verifier" / "sample" / "links.csv"
    if sample.exists():
        with open(sample, newline="") as f:
            for r in csv.DictReader(f):
                cache_path(r["url"]).write_text(r["text"])

    sources = HARNESS / "sources.md"
    if not sources.exists():
        names = sorted({r["source"] for r in links if r["week"] in WEEKS and r["source"]})
        sources.write_text("# Sources\n\nWhere this reader's saved links come from. "
                           "No notes on any of them yet.\n\n"
                           + "\n".join(f"- {n}" for n in names) + "\n")

    print("week  links  acted  should have  noise  not labelled  decisions")
    decisions = verifier.load_decisions()
    for w in [*WEEKS, verifier.HIDDEN_WEEK]:
        wk = [r for r in links if r["week"] == w]
        n = lambda label: sum(r["label"] == label for r in wk)
        print(f"  {w}    {len(wk):>4}   {n('acted'):>4}   {n('should_have'):>10}   "
              f"{n('noise'):>4}   {n(''):>11}   {sum(d['week'] == w for d in decisions):>8}"
              + ("   (hidden)" if w == verifier.HIDDEN_WEEK else ""))


# ---------------------------------------------------------------- step 2

def brief_prompt(week):
    p = f"Write the brief for week {week}. Its links are in inbox/week-{week}.csv."
    decisions = [d for d in verifier.load_decisions() if d["week"] == week]
    if decisions:
        p += "\n\nThe reader has to decide this week. Answer each with adopt, wait or ignore:\n"
        p += "\n".join(f"{d['id']}: {d['question']}" for d in decisions)
    return p


def brief(week, folder, harness=HARNESS):
    """MODEL. The briefing agent writes one week's brief."""
    trace = folder / f"week-{week}.jsonl"
    result = claude(brief_prompt(week), harness, BRIEF_MODEL, trace,
                    ["--tools", "Bash,Read,Write,Edit,Skill"])
    text = result.get("result") or ""
    # A wall, checked in code: a run that reached outside its folder does not count.
    for name, inp in tool_inputs(trace):
        if re.search(r"verifier|traces/|optimizer|scores\.csv|\.\./", inp):
            print(f"  week {week}: run thrown away, {name} reached outside harness/")
            text = ""
    (folder / f"week-{week}.brief.md").write_text(text)
    return text


def briefs_and_scores(folder):
    """Steps 2 and 3 for the visible weeks."""
    with ThreadPoolExecutor(len(WEEKS)) as pool:
        texts = list(pool.map(lambda w: brief(w, folder), WEEKS))
    scores = [verifier.score_week(w, t) for w, t in zip(WEEKS, texts)]
    (folder / "scores.json").write_text(json.dumps(scores, indent=1))
    print(verifier.table(scores))
    return scores


def baseline():
    if rows():
        raise SystemExit("There is already a baseline. Delete scores.csv and traces/ to start over.")
    if git("status", "--porcelain"):
        raise SystemExit("Commit your work first, so the baseline is a commit.")
    scores = briefs_and_scores(TRACES / "round-0")
    add_row("0", scores, "baseline", "the setup before any round")
    git("add", "scores.csv")
    git("commit", "-m", f"baseline: {verifier.mean(scores)}")
    git("tag", "-f", "baseline")


# ---------------------------------------------------------------- step 4

def report(n, folder):
    """Plain code turns the last scores into a report the optimizer can start from."""
    live, best = current()
    scores = json.loads((TRACES / f"round-{live}" / "scores.json").read_text())
    worst = min(scores, key=lambda s: s["score"])
    line = lambda r, w: f"- week {w} | {r['id']} | {r['source']} | {r['title']} | {r['label']}"
    out = [f"# Report for round {n}", "",
           f"The live setup scored {best} on weeks 1 to 3 (run: traces/round-{live}/).",
           "Per week: " + ", ".join(f"week {s['week']}: {s['score']}" for s in scores), "",
           f"Worst week: {worst['week']}. Raw trace: ../traces/round-{live}/week-{worst['week']}.jsonl",
           "", "## Missed: the reader acted on these, or should have, and the brief left them out"]
    out += [line(r, s["week"]) for s in scores for r in s["missed"]] or ["- none"]
    out += ["", "## Noise the brief called important"]
    out += [line(r, s["week"]) for s in scores for r in s["noise"]] or ["- none"]
    out += ["", "## Decisions it got wrong"]
    out += [f"- week {s['week']} | {d['id']} | {d['question']} | brief said {d['brief_said']}, "
            f"it turned out: {d['turned_out']}" for s in scores for d in s["wrong_decisions"]] or ["- none"]
    out += ["", "## The failure log, kept by hand", "", (ROOT / "failures.md").read_text()]
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "report.md").write_text("\n".join(out))


# ---------------------------------------------------------------- step 5

def optimize(n, folder):
    """MODEL. In its own context: reads traces, changes one thing, says why."""
    h = HARNESS.as_posix()
    result = claude(
        f"Round {n}. Start from ../traces/round-{n}/report.md.",
        OPTIMIZER, OPT_MODEL, folder / "optimizer.jsonl",
        ["--tools", "Read,Grep,Glob,Edit,Write",
         "--add-dir", str(HARNESS), str(TRACES),
         "--allowedTools", f"Read(/{h}/**)", f"Read(/{TRACES.as_posix()}/**)",
         f"Edit(/{h}/**)", f"Edit(/{OPTIMIZER.as_posix()}/proposals.md)",
         "--disallowedTools", f"Edit(/{h}/.claude/settings.json)"])
    text = result.get("result") or ""
    find = lambda key: (re.findall(rf"(?m)^{key}:\s*(.+)$", text) or ["(none given)"])[-1].strip()
    return find("REASON"), find("PREDICT")


# ---------------------------------------------------------------- step 6

def tags():
    found = set()
    for f in HARNESS.rglob("*.md"):
        if "cache" not in f.parts:
            found |= set(re.findall(r"\((?:F|R)\d+\)", f.read_text()))
    return found


def walls(before_tags, before_data, folder):
    """Plain code checks the four lines the optimizer may not cross. Returns the breach, or ''."""
    changed = [l.split(maxsplit=1)[1].strip('"') for l in git("status", "--porcelain", "-uall").splitlines()]
    for path in changed:
        if path == "harness/.claude/settings.json":
            return "it changed a permission; only a person does that"
        if not path.startswith("harness/") and path != "optimizer/proposals.md":
            return f"it changed {path}, outside the harness"
    if not any(p.startswith("harness/") for p in changed):
        return "it made no change to the harness"
    gone = before_tags - tags()
    if gone:
        return f"it deleted a rule that traces to a logged failure: {', '.join(sorted(gone))}"
    if folder_hash(HARNESS / "inbox", HARNESS / "cache") != before_data:
        return "it touched the links or the saved pages"
    for name, inp in tool_inputs(folder / "optimizer.jsonl"):
        if "verifier" in inp or "week-4" in inp:
            return f"its {name} call reached for the labels or week four"
    return ""


def undo():
    git("checkout", "--", ".")
    git("clean", "-fdq", "harness", "optimizer")


# ---------------------------------------------------------------- steps 4 to 8

def journal(n, reason, predicted, verdict, before, after):
    with open(OPTIMIZER / "journal.md", "a") as f:
        f.write(f"\n## Round {n}: {verdict}\n- Change: {reason}\n- Predicted: {predicted}\n"
                f"- Observed: {before} to {after} on weeks 1 to 3\n")


def one_round():
    if git("status", "--porcelain"):
        raise SystemExit("Uncommitted changes. Commit or discard them before a round.")
    live, best = current()
    n = len(rows())
    folder = TRACES / f"round-{n}"
    print(f"\n=== round {n} · live score {best}")

    report(n, folder)                                             # 4
    before_tags = tags()
    before_data = folder_hash(HARNESS / "inbox", HARNESS / "cache")
    reason, predicted = optimize(n, folder)                       # 5 MODEL
    print(f"change:  {reason}\npredict: {predicted}")

    breach = walls(before_tags, before_data, folder)              # 6
    if breach:
        undo()
        print(f"blocked: {breach}")
        journal(n, reason, predicted, f"blocked ({breach})", best, "not run")
        add_row(n, [{"score": None}] * 3, "blocked", reason)
        git("add", "scores.csv", "optimizer/journal.md")
        git("commit", "-m", f"round {n} blocked: {breach}")
        return

    print(git("diff", "--stat", "--", "harness"))
    git("add", "harness", "optimizer/proposals.md")
    git("commit", "-m", f"round {n}: {reason}")

    scores = briefs_and_scores(folder)                            # 7 MODEL (step 2 again) + 3
    new = verifier.mean(scores)

    keep = new >= best + MIN_GAIN                                 # 8
    verdict = "kept" if keep else "reverted"
    if not keep:
        git("revert", "--no-commit", "HEAD")
    journal(n, reason, predicted, verdict, best, new)
    add_row(n, scores, verdict, reason)
    git("add", "scores.csv", "optimizer/journal.md")
    git("commit", "-m", f"round {n} {verdict}: {best} to {new}")
    print(f"{verdict}: {best} to {new}")


# ---------------------------------------------------------------- step 9

def final():
    """Open week four, once. Neither agent has seen its links or its labels."""
    if OPENED.exists():
        raise SystemExit("Week four is already open. A second look is not a hidden week any more.")
    live, best = current()
    start = float(rows()[0]["mean"])
    folder = TRACES / "final"
    week = verifier.HIDDEN_WEEK

    with open(HARNESS / "inbox" / f"week-{week}.csv", "w", newline="") as f:
        out = csv.DictWriter(f, ["id", "date", "source", "title", "url"], extrasaction="ignore")
        out.writeheader()
        out.writerows(r for r in verifier.load_links() if r["week"] == week)

    # The setup as it was at the baseline, rebuilt next to the live one.
    old = folder / "before"
    shutil.rmtree(old, ignore_errors=True)
    old.mkdir(parents=True)
    tar = subprocess.run(["git", "archive", "baseline", "harness"], cwd=ROOT, capture_output=True, check=True)
    subprocess.run(["tar", "-x", "-C", str(old)], input=tar.stdout, check=True)
    for d in ("inbox", "cache"):
        shutil.copytree(HARNESS / d, old / "harness" / d)

    with ThreadPoolExecutor(2) as pool:
        b = pool.submit(brief, week, folder / "before-run", old / "harness")
        a = pool.submit(brief, week, folder / "after-run", HARNESS)
    before = verifier.score_week(week, b.result(), open_hidden=True)
    after = verifier.score_week(week, a.result(), open_hidden=True)

    print("\n                 before   after")
    print(f"weeks 1 to 3     {start:>6}   {best:>5}    (the loop could see these)")
    print(f"week 4           {before['score']:>6}   {after['score']:>5}    (it could not see this)")
    seen, unseen = best - start, after["score"] - before["score"]
    if seen <= 0:
        verdict = "No change was kept, so there is nothing to test."
    elif unseen > 0:
        verdict = "Week four rose too. The harness learned something about how you decide."
    else:
        verdict = "Only the weeks it saw rose. The harness memorised your past."
    print("\n" + verdict)
    OPENED.write_text(json.dumps({"visible": [start, best], "hidden": [before, after],
                                  "verdict": verdict}, indent=1))
    git("add", str(OPENED))
    git("commit", "-m", f"week four opened: {before['score']} to {after['score']} "
                        f"(weeks 1 to 3: {start} to {best})")


def status():
    for r in rows():
        print(f"round {r['round']:>2}  {r['mean']:>6}  {r['verdict']:<9} {r['reason']}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "prepare":
        prepare()
    elif cmd == "brief":
        w = int(sys.argv[2])
        if w not in WEEKS:
            raise SystemExit("Weeks 1 to 3 only. Week four stays closed until `final`.")
        t0 = time.time()
        print(brief(w, TRACES / "try"))
        print(f"\n({time.time() - t0:.0f}s · trace: traces/try/week-{w}.jsonl)")
    elif cmd == "baseline":
        baseline()
    elif cmd == "round":
        one_round()
    elif cmd == "run":
        for _ in range(int(sys.argv[2]) if len(sys.argv) > 2 else 5):
            one_round()
        status()
    elif cmd == "final":
        final()
    elif cmd == "status":
        status()
    else:
        print(__doc__)
