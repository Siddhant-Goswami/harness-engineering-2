# Harness Engineering 2.0: the harness that improves itself

One agent writes you a weekly brief from the links you saved. A second agent reads the
first one's mistakes and changes its setup, one commit at a time. Plain code decides
whether each change stays. One week of your labels stays hidden until the end.

It ships with a fictional sample month so every command works before you bring your own data.

## The sample month

100 links over four weeks, 8 decisions, all made up. The reader runs a support agent on
**Kiln** (harness), **Orchard** (models) and **Postgres with Vecstore** (database). Nothing in
the harness says so. The loop has to learn it from the labels.

Every week has the same five traps, so a rule learned on weeks 1 to 3 can pay off on week 4:

| Trap | Example | Label |
|---|---|---|
| Urgent news about a tool the reader does not use | "Advisory: Anvil plugin sandbox escape, patch now" | noise |
| A newsletter recap of a changelog | "Script mode explained: what Kiln 2.4 means for you" | noise |
| A dull title hiding a breaking change | "Vecstore 0.7.3" (new indexes switch distance metric) | acted |
| A thread with real measurements | "I timed every hook in 40 Kiln projects" | should have |
| A big-name post unrelated to the reader | "Our new image model draws hands correctly" | noise |

To change it, edit `verifier/sample/make_sample.py` and run it.

## What is in the folder

| Path | What it is | Who may change it |
|---|---|---|
| `harness/` | The briefing agent's setup: `CLAUDE.md`, `sources.md`, `memory.md`, `tools/`, skills | You and the optimizer |
| `harness/.claude/settings.json` | What the briefing agent is allowed to run | You only |
| `verifier/` | Your labels, your decisions, the scoring code | You only, before any agent runs |
| `optimizer/` | The second agent's instructions, its journal, its permission requests | You (the journal is written by code) |
| `failures.md` | Failures you saw yourself, tagged F1, F2... | You |
| `loop.py` | The outer loop. Nine steps, two of them a model | You |
| `codemode.py` | The same job run two ways | You |
| `traces/` | The raw trace of every run | Written by code |

## The loop

| # | Step | Who acts |
|---|---|---|
| 1 | Split the links into four weeks | code |
| 2 | Write a brief for weeks 1 to 3 | **model** (briefing agent) |
| 3 | Score each brief against the labels | code |
| 4 | Pick the worst week and write a report | code |
| 5 | Propose one change, with a reason | **model** (optimizer, in its own context) |
| 6 | Check the change stayed inside the walls | code |
| 7 | Run steps 2 and 3 again | (same as 2 and 3) |
| 8 | Keep the change if the score rose, else revert | code |
| 9 | After the last round, open week four once | code |

## Run it, in session order

You need Claude Code installed and logged in, Python 3.10 or newer, and git.

**Label (minutes 10 to 20).** Open `verifier/links.csv`. One row per saved link:
`date, source, title, url, label`. The label is `acted`, `should have` or `noise`.
A row with no label is shown to the agent and never scored. Then:

```
python3 loop.py prepare
```

**First agent (20 to 35).** Read `harness/CLAUDE.md`, then run it on week one and read the brief.

```
python3 loop.py brief 1
python3 verifier/score.py traces/try
```

Write what went wrong in `failures.md`.

**Code mode (35 to 45).**

```
python3 codemode.py
```

**Fix one by hand (45 to 60).** Add one rule to `harness/CLAUDE.md`, tagged `(F1)`. Commit. Then
record where you started:

```
git commit -am "F1: ..."
python3 loop.py baseline
```

**The optimizer and the gate (60 to 75).**

```
python3 loop.py round      # one round: steps 4 to 8
python3 loop.py run 3      # three rounds
python3 loop.py status
git log --oneline
```

**The hidden week (75 to 85).**

```
python3 loop.py final
```

It runs week four on the baseline setup and on the final one, and prints both scores next to
the visible weeks. It runs once. A second look is not a hidden week any more.

## How a brief is scored

Open `verifier/score.py`. Three numbers at the top are yours to tune.

```
score = (links found + 2 x decisions right - 0.5 x noise called important)
        / (links that mattered + 2 x decisions)
```

- A link is "found" when its id, like `[L014]`, appears under **What changed** or **What to do**.
- Links under **Who disagrees** are not scored either way.
- The noise penalty exists because the cheapest way to raise the score is to cite everything.

## The walls (step 6)

Checked by code after the optimizer finishes. A change that crosses one is thrown away.

1. It changed a file outside `harness/` (it may add to `optimizer/proposals.md`).
2. It changed `harness/.claude/settings.json`. Permissions are yours to approve.
3. It deleted a tag like `(F2)` or `(R1)`. A rule that traces to a logged failure can be reworded, not removed.
4. It touched the links or saved pages, or reached for `verifier/` or week four.

The briefing agent has one wall: a run whose trace reaches outside `harness/` scores zero.

## Read a trace

```
python3 loop.py trace traces/round-2/optimizer.jsonl     # what the optimizer looked at and changed
python3 loop.py trace traces/round-0/week-1.run-1.jsonl  # what the briefing agent fetched and wrote
```

## Bring your own month

1. Replace `verifier/links.csv` with your last 30 days (keep the header row).
2. Replace `verifier/decisions.csv` with five decisions: `date, question, outcome, how_it_turned_out`.
   The outcome is `adopt`, `wait` or `ignore`.
3. Delete `verifier/sample/`, `harness/sources.md` and `harness/cache/`.
4. `python3 loop.py prepare`

Days 22 onward become week four. Pages are fetched the first time the agent reads them and
kept in `harness/cache/`, so a week reads the same on every run. Links behind a login
(X, LinkedIn) come back as title only.

## Things to know before you trust a number

- One run per week is a small sample: on the sample, one setup scored 0.46 and 0.89 on the same
  week. So every week is run `RUNS` times (3 by default) and the score is the mean. The table
  prints the low and high run next to it. `RUNS=5 python3 loop.py ...` for a steadier number.
- `MIN_GAIN` in `loop.py` (0.02) is the smallest rise that counts. If a week's low-to-high
  range is wider than the rise, be suspicious of the rise.
- The report tells the optimizer how many runs each miss happened in. A miss in every run is a
  habit of the setup; a miss in one run may be chance.
- Kept rounds are the lucky ones, so the live score drifts a little high and later rounds
  find it harder to beat. The hidden week is where that luck gets checked.
- `BRIEF_MODEL=haiku python3 loop.py ...` and `OPT_MODEL=sonnet ...` change the two models.
- The branch `sample-run` holds a finished run on the sample, the pre-recorded backup for the
  session (its raw traces are in `traces-sample-run/`, not in git):

  | | before | after 4 rounds |
  |---|---|---|
  | weeks 1 to 3 | 0.739 | 0.991 |
  | week 4 (hidden) | 0.666 | 0.949 |

  Round 1 was reverted ("fetch every link" made it cite everything: 0.739 to 0.504). Rounds 2 to 4
  were kept: the reader's stack, measured findings count as news, cite the changelog not the recap.
  `git log sample-run --oneline` and `git diff sample-baseline sample-run -- harness` show it.

## Take-home

1. Label all 30 days and write your five decisions.
2. `python3 loop.py run 5`, then `python3 loop.py final`.
3. Submit `git log --oneline` and both scores, before and after.
4. One paragraph for a non-engineer: why did a change help the weeks the loop saw and not the hidden one?
5. Name one change you would never have written yourself, and one you rejected on review even though the score rose.
