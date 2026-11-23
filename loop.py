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

    python3 loop.py next           where you are, and the one command to run next
    python3 loop.py import FILE    your bookmarks export -> verifier/links.csv (any columns)
    python3 loop.py label          label your links one at a time (in your own terminal)
    python3 loop.py prepare        step 1
    python3 loop.py blank          by hand: your weeks 1-3 links with the labels removed
    python3 loop.py compare FILE   by hand: where a model's labels differ from yours
    python3 loop.py brief 1        one brief, printed (no scoring)
    python3 loop.py baseline       steps 2-3 on the setup as it is now; tags it `baseline`
    python3 loop.py round          steps 4-8, once
    python3 loop.py run 5          five rounds
    python3 loop.py final          step 9
    python3 loop.py status         the scores so far
    python3 loop.py trace FILE     a raw trace, readable: every tool call and what came back

The two MODEL steps run in Claude Code unless you pick another harness:

    RUNNER=codex  python3 loop.py ...     OpenAI Codex CLI
    RUNNER=hermes python3 loop.py ...     Hermes Agent, with whatever model it is set up for
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

from agents import BRIEF_MODEL, OPT_MODEL, RUNNER, events, tokens, tool_inputs  # noqa: E402
from agents import run as run_agent  # noqa: E402
import bookmarks  # noqa: E402
RUNS = int(os.environ.get("RUNS", "3"))  # briefs per week; the score is their mean
MIN_GAIN = 0.02      # a change must beat the current score by this much to stay
SCORES = ROOT / "scores.csv"
OPENED = ROOT / "verifier" / "week4-opened.json"
WEEKS = verifier.VISIBLE_WEEKS


# ---------------------------------------------------------------- helpers

def git(*args, check=True):
    return subprocess.run(["git", *args], cwd=ROOT, check=check,
                          capture_output=True, text=True).stdout.strip()


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

    # A link with a `text` column (the made-up sample) needs no fetch: its page is that text.
    sys.path.insert(0, str(HARNESS / "tools"))
    from fetch import cache_path
    for r in links:
        if r.get("text"):
            cache_path(r["url"]).write_text(r["text"])

    sources = HARNESS / "sources.md"
    if not sources.exists():
        names = sorted({r["source"] for r in links if r["week"] in WEEKS and r["source"]})
        sources.write_text("# Sources\n\nWhere this reader's saved links come from. "
                           "No notes on any of them yet.\n\n"
                           + "\n".join(f"- {n}" for n in names) + "\n")

    print("week  dates                     links  acted  should have  noise  not labelled  decisions")
    decisions = verifier.load_decisions()
    for w in [*WEEKS, verifier.HIDDEN_WEEK]:
        wk = [r for r in links if r["week"] == w]
        n = lambda label: sum(r["label"] == label for r in wk)
        dates = f"{wk[0]['date']} to {wk[-1]['date']}" if wk else "(no links)"
        print(f"  {w}   {dates:<24}  {len(wk):>4}   {n('acted'):>4}   {n('should_have'):>10}   "
              f"{n('noise'):>4}   {n(''):>11}   {sum(d['week'] == w for d in decisions):>8}"
              + ("   (hidden)" if w == verifier.HIDDEN_WEEK else ""))
    warnings(links)


def warnings(links):
    """What will make the scores hard to trust, said before any money is spent."""
    from datetime import date
    out = []
    span = (date.fromisoformat(links[-1]["date"]) - date.fromisoformat(links[0]["date"])).days
    if span > 35:
        late = sum(r["week"] == verifier.HIDDEN_WEEK for r in links)
        out.append(f"Your links span {span} days. Day 22 onward is all week four, so {late} of "
                   f"{len(links)} links are hidden. Import a 30-day window instead "
                   f"(python3 loop.py import FILE --from ... --to ...).")
    labelled = any(r["label"] for r in links)
    for w in WEEKS:
        wk = [r for r in links if r["week"] == w]
        sig = sum(r["label"] in verifier.SIGNAL for r in wk)
        if not wk:
            out.append(f"Week {w} has no links. Its score will be empty.")
        elif labelled and sig == 0:
            out.append(f"Week {w} has no link labelled signal or should have, so it cannot be scored.")
        elif labelled and sig < 3:
            out.append(f"Week {w} has only {sig} signal link{'s' if sig > 1 else ''}: one miss moves "
                       f"its score by {1 / sig:.2f}. Fine, but expect big jumps.")
    if not labelled:
        out.append("No labels yet. Next: python3 loop.py label   (in your own terminal)")
    for line in out:
        print("\n! " + line)


# ---------------------------------------------------------------- by hand

BLANK = ROOT / "manual" / "links-blank.csv"


PROMPT = ROOT / "manual" / "prompt.txt"


def reader_rules():
    """The rules you wrote about this reader: every paragraph of harness/CLAUDE.md with a tag."""
    text = (HARNESS / "CLAUDE.md").read_text()
    return [p.strip() for p in re.split(r"\n\s*\n", text) if re.search(r"\((?:F|R)\d+\)", p)
            and not p.lstrip().startswith(("Work only", "A tag in brackets"))]


def blank(with_text=False):
    """Your links for weeks 1 to 3 with the label column empty, and a prompt for any model.

    By default the model sees what you saw in your list: source and title. With --text it also
    sees the start of each post, which you want when titles are only a tweet's first line.
    """
    BLANK.parent.mkdir(exist_ok=True)
    links = [r for r in verifier.load_links() if r["week"] in WEEKS]
    has_text = with_text and any(r.get("text") for r in links)
    cols = ["id", "date", "source", "title", "url", "label"] + (["text"] if has_text else [])
    short = lambda s: " ".join((s or "").split())[:500]
    with open(BLANK, "w", newline="") as f:
        out = csv.DictWriter(f, cols, extrasaction="ignore")
        out.writeheader()
        out.writerows(dict(r, label="", text=short(r.get("text"))) for r in links)

    rules = reader_rules()
    PROMPT.write_text(
        "Below is a CSV of links one reader saved. For each one, guess whether this reader would\n"
        "find it worth acting on, and fill the label column with signal (worth acting on) or noise\n"
        "(not worth their time). You cannot know for sure: give your best guess for every row.\n"
        + ("\nWhat this reader has told you about how they judge links:\n\n"
           + "\n\n".join(rules) + "\n" if rules else "")
        + "\nReply with a CSV of two columns, id and label: the header row `id,label`, then one row"
          " per link. No code fences, nothing before or after.\n\n"
        + BLANK.read_text())
    print(f"{len(links)} links, no labels: {BLANK.relative_to(ROOT)}")
    print(f"The same, as a prompt for a model: {PROMPT.relative_to(ROOT)}"
          + (f" (with your {len(rules)} rule{'s' if len(rules) > 1 else ''} from harness/CLAUDE.md)"
             if rules else ""))
    print("Week four is left out so it stays hidden.")
    if not with_text and any(r.get("text") for r in links) and not any(
            "sample.invalid" in r["url"] for r in links):
        print("Your titles are only each post's first line? Give the model the posts too:\n"
              "    python3 loop.py blank --text")
    print()
    print("Have a model label them, blind. Pick one:")
    print("    claude -p < manual/prompt.txt > manual/links-model.csv")
    print("    codex exec -o manual/links-model.csv < manual/prompt.txt")
    print("    or paste manual/prompt.txt into any chat and save the reply as manual/links-model.csv")
    print("Then:")
    print("    python3 loop.py compare manual/links-model.csv")


def compare(path):
    """Where a model's signal/noise labels differ from yours. You write the lesson."""
    mine = {r["id"]: r for r in verifier.load_links() if r["week"] in WEEKS and r["label"]}
    theirs = read_model_labels(path)
    side = lambda label: "noise" if label == "noise" else "signal"
    judged = {i: r for i, r in mine.items() if theirs.get(i)}
    if not judged:
        raise SystemExit(f"No row in {path} has an id (L001...) and a label of signal or noise.\n"
                         f"Open it and check the model replied with the CSV, not a summary.")
    missed = [r for i, r in judged.items() if side(r["label"]) == "signal" and theirs[i] == "noise"]
    extra = [r for i, r in judged.items() if side(r["label"]) == "noise" and theirs[i] != "noise"]
    agree = len(judged) - len(missed) - len(extra)
    sig = sum(side(r["label"]) == "signal" for r in judged.values())
    noise = len(judged) - sig
    print(f"agreed on {agree} of {len(judged)} links ({agree / len(judged):.0%})")
    if sig:
        print(f"  your signal links: it found {sig - len(missed)} of {sig}")
    if noise:
        print(f"  your noise links:  it called {len(extra)} of {noise} signal")
    print(f"  (a model that said noise to everything would agree on {noise / len(judged):.0%}: "
          f"watch the two lines above, not the percentage)")
    if len(judged) < len(mine):
        print(f"{len(mine) - len(judged)} of your labelled links had no label in that file")
    for title, group in (("You acted on these. The model called them noise:", missed),
                         ("Noise to you. The model called them signal:", extra)):
        if group:
            print(f"\n{title}")
            for r in group:
                print(f"  {r['id']}  {r['source']}: {r['title']}")
    if missed or extra:
        print("\nPick the mistake that repeats. Write it in failures.md (what you saw, what you")
        print("expected), then add one rule about that kind of link to harness/CLAUDE.md.")


def read_model_labels(path):
    """{id: label} from a model's reply. Forgives code fences, chatter and a missing header."""
    lines = [l for l in Path(path).read_text(encoding="utf-8-sig").splitlines()
             if l.strip() and not l.strip().startswith("```")]
    words = ("signal", "noise", "acted", "should")
    out = {}
    for cells in csv.reader(lines):
        lid = next((c.strip() for c in cells if re.fullmatch(r"L\d{3}", c.strip())), None)
        lab = next((verifier._label(c) for c in reversed(cells)
                    if c.strip().lower().startswith(words) and len(c.strip()) < 15), "")
        if lid and lab:
            out[lid] = lab
    return out


# ---------------------------------------------------------------- step 2

def brief_prompt(week):
    p = f"Write the brief for week {week}. Its links are in inbox/week-{week}.csv."
    decisions = [d for d in verifier.load_decisions() if d["week"] == week]
    if decisions:
        p += "\n\nThe reader has to decide this week. Answer each with adopt, wait or ignore:\n"
        p += "\n".join(f"{d['id']}: {d['question']}" for d in decisions)
    return p


def brief(week, folder, harness=HARNESS, run=None):
    """MODEL. The briefing agent writes one week's brief."""
    name = f"week-{week}" + (f".run-{run}" if run else "")
    trace = folder / f"{name}.jsonl"
    result = run_agent("brief", brief_prompt(week), harness, trace, BRIEF_MODEL, harness)
    text = result.get("result") or ""
    # A wall, checked in code: a run that reached outside its folder does not count.
    for tool, inp in tool_inputs(trace):
        # Judge only what lies past the setup's own folder: `final` rebuilds the old setup
        # under traces/, and Hermes reads by absolute path.
        for home in {str(Path(harness)), str(Path(harness).resolve())}:
            inp = inp.replace(home, "")
        if re.search(r"verifier|traces/|optimizer|scores\.csv|\.\./", inp):
            print(f"  {name}: run thrown away, {tool} reached outside harness/")
            text = ""
    (folder / f"{name}.brief.md").write_text(text)
    return text


def many(weeks, folder, harness=HARNESS):
    """RUNS briefs for each week, all at once. Returns {week: [brief, ...]}."""
    jobs = [(w, r) for w in weeks for r in range(1, RUNS + 1)]
    with ThreadPoolExecutor(len(jobs)) as pool:
        texts = list(pool.map(lambda j: brief(j[0], folder, harness, j[1]), jobs))
    out = {w: [] for w in weeks}
    for (w, _), t in zip(jobs, texts):
        out[w].append(t)
    return out


def put_back():
    """A briefing run may write in scratch/ only. Codex and Hermes are not fenced the way
    Claude Code is, so after each batch plain code puts back anything else they changed."""
    paths = [l.split(maxsplit=1)[1].strip('"')
             for l in git("status", "--porcelain", "-uall", "--", "harness").splitlines()]
    changed = [p for p in paths if not p.startswith("harness/scratch/")]
    if changed:
        print(f"  a briefing run changed {', '.join(changed)}: put back")
        git("checkout", "--", "harness", check=False)
        git("clean", "-fdq", "--", *changed, check=False)


def briefs_and_scores(folder):
    """Steps 2 and 3 for the visible weeks, RUNS times each."""
    print(f"  writing {RUNS * len(WEEKS)} briefs ({RUNS} per week, {RUNNER})...")
    briefs = many(WEEKS, folder)
    put_back()
    scores = [verifier.score_runs(w, briefs[w]) for w in WEEKS]
    (folder / "scores.json").write_text(json.dumps(scores, indent=1))
    print(verifier.table(scores))
    return scores


def baseline():
    if rows():
        raise SystemExit("There is already a baseline. Delete scores.csv and traces/ to start over.")
    if git("status", "--porcelain"):
        raise SystemExit("Commit your work first, so the baseline is a commit:\n"
                         "    git add -A && git commit -m \"F1: my first rules\"\n"
                         "(`git add -A`, not `commit -a`: -a leaves out files you created.)")
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
    worst = min((s for s in scores if s["score"] is not None), key=lambda s: s["score"])
    k = worst["per_run"].index(min(worst["per_run"])) + 1
    runs = worst["runs"]
    line = lambda r, w: (f"- week {w} | {r['id']} | {r['source']} | {r['title']} | {r['label']}"
                         f" | in {r['runs']} of {runs} runs")
    out = [f"# Report for round {n}", "",
           f"The live setup scored {best} on weeks 1 to 3, the mean of {runs} runs per week "
           f"(traces: ../traces/round-{live}/, one file per week per run).",
           "Per week: " + ", ".join(f"week {s['week']}: {s['score']} ({s['low']} to {s['high']})"
                                    for s in scores if s["score"] is not None), "",
           f"Worst week: {worst['week']}. Its worst run: ../traces/round-{live}/week-{worst['week']}.run-{k}.jsonl",
           "A miss in every run is a habit of the setup. A miss in one run may be chance.",
           "", "## Missed: the reader acted on these, or should have, and the brief left them out"]
    out += [line(r, s["week"]) for s in scores for r in s["missed"]] or ["- none"]
    out += ["", "## Noise the brief called important"]
    out += [line(r, s["week"]) for s in scores for r in s["noise"]] or ["- none"]
    out += ["", "## Decisions it got wrong"]
    out += [f"- week {s['week']} | {d['id']} | {d['question']} | briefs said {', '.join(d['said'])}, "
            f"it turned out: {d['turned_out']} | wrong in {d['runs']} of {runs} runs"
            for s in scores for d in s["wrong_decisions"]] or ["- none"]
    out += ["", "## The failure log, kept by hand", "", (ROOT / "failures.md").read_text()]
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "report.md").write_text("\n".join(out))


# ---------------------------------------------------------------- step 5

def optimize(n, folder):
    """MODEL. In its own context: reads traces, changes one thing, says why."""
    result = run_agent("optimizer", f"Round {n}. Start from ../traces/round-{n}/report.md.",
                       OPTIMIZER, folder / "optimizer.jsonl", OPT_MODEL)
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
        raise SystemExit("Uncommitted changes. Commit them (git add -A && git commit -m \"...\") or\n"
                         "discard them before a round. Keep notes in notes/: git ignores that folder.")
    _, best = current()
    if best > 1 - MIN_GAIN:
        raise SystemExit(f"The live score is {best}: no change can beat it by {MIN_GAIN}, so another round "
                         f"cannot be kept.\nOpen the hidden week: python3 loop.py final")
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
    if live == "0" and "--anyway" not in sys.argv:
        raise SystemExit("No change has been kept yet, so the final setup is the one you started with:\n"
                         "week four would compare a setup with itself, and you only get to open it once.\n"
                         "Run more rounds first (python3 loop.py run 3). To open it anyway: "
                         "python3 loop.py final --anyway")
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

    print(f"  writing {2 * RUNS} briefs for week four ({RUNS} on each setup)...")
    with ThreadPoolExecutor(2) as pool:
        b = pool.submit(many, [week], folder / "before-run", old / "harness")
        a = pool.submit(many, [week], folder / "after-run", HARNESS)
    before = verifier.score_runs(week, b.result()[week], open_hidden=True)
    after = verifier.score_runs(week, a.result()[week], open_hidden=True)

    cell = lambda s: f"{s['score']} ({s['low']} to {s['high']})"
    found = lambda s: f"{s['hits']}/{s['signal']} found, {s['noise_flagged']} noise cited"
    print("\n                 before                 after")
    print(f"weeks 1 to 3     {start:<22} {best}    (the loop could see these)")
    print(f"week 4           {cell(before):<22} {cell(after)}    (it could not see this)")
    print(f"  of which       {found(before):<22} {found(after)}")
    seen, unseen = best - start, after["score"] - before["score"]
    if seen < MIN_GAIN:
        verdict = "No change was kept, so there is nothing to test."
    elif unseen >= MIN_GAIN:
        verdict = "Week four rose too."
        if after["hits"] <= before["hits"]:
            verdict += (" But the new setup found no more of what mattered: all of the rise is"
                        " noise it stopped citing. It learned what to leave out of a brief. Read"
                        " the kept changes and ask whether that is how you decide, or only tidier"
                        " writing.")
        else:
            verdict += " It found more of what mattered: the harness learned something about how you decide."
        if after["score"] <= before["high"]:
            verdict += (f" Note: one run of the old setup already scored {before['high']}, so the"
                        f" rise is inside its own spread and may be partly luck.")
    elif unseen > -MIN_GAIN:
        verdict = ("Week four did not move. The gain on the weeks it saw did not carry over: "
                   "it fitted your past, not how you decide.")
    else:
        verdict = "Week four got worse. The harness memorised your past and it cost you on new weeks."
    print("\n" + verdict)
    OPENED.write_text(json.dumps({"visible": [start, best], "hidden": [before, after],
                                  "verdict": verdict}, indent=1))
    git("add", str(OPENED))
    git("commit", "-m", f"week four opened: {before['score']} to {after['score']} "
                        f"(weeks 1 to 3: {start} to {best})")


def show(trace):
    """Print a raw trace the way a person reads it."""
    short = lambda x, n: " ".join(str(x).split())[:n]
    for e in events(Path(trace)):
        if e.get("type") == "assistant":
            for c in e["message"].get("content", []):
                if c.get("type") == "text":
                    print(f"\n  model:  {short(c['text'], 400)}")
                elif c.get("type") == "tool_use":
                    inp = c["input"]
                    arg = (inp.get("command") or inp.get("file_path") or inp.get("pattern")
                           or json.dumps(inp))
                    print(f"\n  {c['name']}:  {short(arg, 200)}")
                    if c["name"] in ("Edit", "Write"):
                        new = inp.get("new_string") or inp.get("content") or inp.get("patch")
                        print(f"     + {short(new, 300)}" if new else
                              f"     ({inp.get('kind', 'changed')}; Codex logs no text: run git diff)")
        elif e.get("type") == "user":
            for c in e["message"].get("content", []):
                if isinstance(c, dict) and c.get("type") == "tool_result":
                    print(f"     -> {short(c.get('content'), 160)}")
        elif e.get("type") == "result":
            cost = f", ${e['total_cost_usd']:.3f}" if "total_cost_usd" in e else ""
            print(f"\n  done: {e.get('num_turns')} model steps, {tokens(e):,} tokens{cost}"
                  + (f" ({e['runner']})" if e.get("runner") else ""))


def next_step():
    """Look at the folder and say where the student is, and the one command to run next."""
    links = verifier.load_links()
    sample = any("sample.invalid" in r["url"] for r in links)
    unlabelled = sum(not r["label"] for r in links)
    say = lambda where, *lines: print(f"You are at: {where}\n\nNext:\n" + "\n".join(f"    {l}" for l in lines))
    log = re.sub(r"(?s)<!--.*?-->", "", (ROOT / "failures.md").read_text())  # skip the example
    failures = re.findall(r"(?m)^## F\d+", log)
    model_files = sorted((ROOT / "manual").glob("links-model*.csv")) if (ROOT / "manual").exists() else []

    if sample:
        print("You are on the made-up sample month (already labelled). Every step works on it.\n"
              "To use your own links: get them (README, Part 1 step 1), then\n"
              "    python3 loop.py import path/to/your-bookmarks.csv\n")
    if rows():
        return next_part2(say)
    if not (HARNESS / "inbox" / "week-1.csv").exists():
        return say("Part 1, step 2. Your links are in, not yet split into weeks.",
                   "python3 loop.py prepare")
    if unlabelled == len(links):
        return say(f"Part 1, step 3. None of your {len(links)} links has a label.",
                   "python3 loop.py label        # in your own terminal; it asks s / h / n for each",
                   "(or fill the label column of verifier/links.csv in a spreadsheet)")
    if unlabelled and not model_files:
        print(f"Note: {unlabelled} of {len(links)} links {'has' if unlabelled == 1 else 'have'} no label. That's fine if you could not tell;"
              f" `python3 loop.py label` picks up where you stopped.\n")
    if not model_files:
        own_text = not sample and any(r.get("text") for r in links)
        return say("Part 1, step 5. Labelled. Now see how a model would label them, blind.",
                   "python3 loop.py blank" + (" --text   # your titles are tweet first lines;"
                                              " this gives the model the posts" if own_text else ""),
                   "then run the command it prints")
    if not failures:
        return say("Part 1, steps 6 and 7. A model has labelled your links.",
                   f"python3 loop.py compare {model_files[-1].relative_to(ROOT)}",
                   "then write the mistake that repeats in failures.md as F1, and one rule ending",
                   "in (F1) under 'What matters to this reader' in harness/CLAUDE.md")
    if not (TRACES / "try").exists():
        return say(f"Part 1 done ({len(failures)} failure{'s' if len(failures) > 1 else ''} logged)."
                   f" Repeat steps 5 to 7 until the "
                   f"disagreements stop teaching you anything. Then Part 2: the first agent.",
                   "python3 loop.py brief 1", "python3 verifier/score.py traces/try")
    if git("status", "--porcelain"):
        return say("Part 2. Commit your rules, so the baseline is a commit.",
                   'git add -A && git commit -m "F1: ..."', "python3 loop.py baseline")
    return say("Part 2. Record where you start.", "python3 loop.py baseline")


def next_part2(say):
    rounds = len(rows()) - 1
    if not OPENED.exists() and rounds < 5:
        return say(f"Part 2. Baseline recorded, {rounds} round{'s' if rounds != 1 else ''} so far."
                   " Don't edit files while rounds run (notes/ is safe).",
                   f"python3 loop.py run {5 - rounds}", "python3 loop.py status")
    if not OPENED.exists() and current()[1] > 1 - MIN_GAIN:
        return say(f"Part 2. The live score is {current()[1]}: no round can beat it, so open the hidden week.",
                   "git log --oneline     # read the kept changes first",
                   "python3 loop.py final  # opens week four, once")
    if not OPENED.exists() and current()[0] == "0":
        return say(f"Part 2. {rounds} rounds done, none kept, so week four has nothing to test yet.",
                   "python3 loop.py run 3", "(or read traces/round-N/report.md and add a rule yourself)")
    if not OPENED.exists():
        return say(f"Part 2. {rounds} rounds done.",
                   "git log --oneline     # read the kept changes first",
                   "python3 loop.py final  # opens week four, once")
    return say("Done: week four is open. The take-home is at the end of the README.",
               "python3 loop.py status", "git log --oneline")


def status():
    for r in rows():
        print(f"round {r['round']:>2}  {r['mean']:>6}  {r['verdict']:<9} {r['reason']}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "next":
        next_step()
    elif cmd == "import":
        if len(sys.argv) < 3:
            raise SystemExit("python3 loop.py import FILE [--all | --from YYYY-MM-DD --to YYYY-MM-DD]")
        args = sys.argv[3:]
        opt = lambda k: args[args.index(k) + 1] if k in args else None
        bookmarks.import_file(sys.argv[2], opt("--from"), opt("--to"), "--all" in args)
        prepare()
    elif cmd == "label":
        bookmarks.label(redo="--redo" in sys.argv)
    elif cmd == "prepare":
        prepare()
    elif cmd == "blank":
        blank(with_text="--text" in sys.argv)
    elif cmd == "compare":
        compare(sys.argv[2])
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
    elif cmd == "trace":
        show(sys.argv[2])
    else:
        print(__doc__)
        next_step()
