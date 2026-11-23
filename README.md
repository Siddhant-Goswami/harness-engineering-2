# Harness Engineering 2.0: the harness that improves itself

One agent writes you a weekly brief from the links you saved. A second agent reads the
first one's mistakes and changes its setup, one commit at a time. Plain code decides
whether each change stays. One week of your labels stays hidden until the end.

This is the repo from the masterclass. The session notes are at
https://100x-curriculum.vercel.app/harness-engineering-2/

## Start here

You need Python 3.10 or newer and git. Part 2 also needs one of three harnesses installed and
logged in: Claude Code, Codex or Hermes.

Clone the repo in your own terminal:

```
git clone https://github.com/Siddhant-Goswami/harness-engineering-2
cd harness-engineering-2
```

Then open Claude Code, Codex or Hermes in that folder and paste this:

```
Read the README. Run `python3 loop.py next` and do what it says, one step at a time.
Wait for me after each step. Do not label any link for me.
```

Clone it yourself rather than asking the agent to: Codex's sandbox has no network by default,
so a clone from inside Codex fails.

**Lost at any point? Run `python3 loop.py next`.** It looks at the folder, tells you which step
you are on, and prints the one command to run next.

A step-by-step tutorial with screenshots for all three harnesses:
https://100x-curriculum.vercel.app/harness-engineering-2/tutorial/

| | Works with | Costs |
|---|---|---|
| **Part 1**, by hand | Any chat tool: Claude, ChatGPT, Codex, Hermes | Nothing beyond your chat plan |
| **Part 2**, the loop, on the sample month | Claude Code, Codex or Hermes (see [Pick your harness](#pick-your-harness)) | About $1.50 with Claude Code |
| **Part 2** on your own month | the same | About $6.50 with Claude Code (baseline, 5 rounds and the hidden week, on 109 X posts with their text) |

The repo ships with a made-up sample month, already labelled, so every command works before you
bring your own links. To try the whole thing on the sample first, skip Part 1 steps 1 to 3.

## Part 1: by hand

This is the part no agent can do for you. It is also what the session spent its time on.

**1. Get your saved links from 30 to 60 days ago.** Not yesterday's: you cannot yet tell
whether those helped. Give a tool that can use your browser this prompt:

```
Open my bookmarks on X. For every post I saved 30 to 60 days ago, write one row:
the date, who posted it, the post's first line, the link, and the full text of the post
(with any post it quotes). Give me a CSV with the columns: date, source, title, url, text.
Do not judge the posts.
```

Use the same prompt for Instagram, YouTube or Reddit saves, or your browser history. X does not
show when you saved a post, so the post's own date is fine. The column names do not have to
match: step 2 reads most exports as they are.

**2. Bring them in.**

```
python3 loop.py import ~/Downloads/your-bookmarks.csv
```

It finds the link, date and text columns whatever they are called, keeps the links from 30 to
60 days ago, writes `verifier/links.csv`, and splits them into four weeks. It prints what it
kept and why. To pick the window yourself: `--from 2026-09-24 --to 2026-10-24`, or `--all`.

It also replaces the sample month: its decisions, its list of sources and its saved pages go.
`git checkout -- verifier harness` brings the sample back.

Read the table it prints. Lines that start with `!` are worth a second look: a week with
almost no links you acted on gives a jumpy score, and an old outlier date can push most of
your links into the hidden week.

**3. Label every link yourself.** In your own terminal (not through the agent):

```
python3 loop.py label
```

It shows each link with its text and asks for one key. Every answer is saved at once; `q`
stops, and running it again carries on where you stopped.

| Key | Label | Meaning |
|---|---|---|
| `s` | `signal` | You acted on it and it helped. (`acted` means the same.) |
| `h` | `should have` | You did not act and now wish you had. Optional. |
| `n` | `noise` | You never used it. |
| Enter | (empty) | Not sure. The agent still sees the link; it is never scored. |

You can fill the `label` column of `verifier/links.csv` in a spreadsheet instead. Label all
four weeks: week four's labels stay hidden from both agents until the end.

**4. Optional: write your decisions** in `verifier/decisions.csv`:
`date, question, outcome, how_it_turned_out`. The outcome is `adopt`, `wait` or `ignore`.

**5. Let a model label the same links, blind.**

```
python3 loop.py blank
claude -p < manual/prompt.txt > manual/links-model.csv
```

`blank` writes your first three weeks with the labels removed, and `manual/prompt.txt`: the
same links as a ready prompt. In Codex: `codex exec -o manual/links-model.csv < manual/prompt.txt`.
In any chat tool: paste `manual/prompt.txt` and save the reply as `manual/links-model.csv`.

By default the model sees what you saw in your list: the source and the title. If your titles
are only each post's first line ("This is an extremely good watch."), use `blank --text` so the
model sees the start of each post too.

**6. Compare.**

```
python3 loop.py compare manual/links-model.csv
```

It prints how many links you agreed on and lists each disagreement. Watch the two lines under
the percentage, not the percentage: most saved links are noise, so a model that says "noise" to
everything already agrees with you most of the time.

**7. Write down the mistake that repeats.** In `failures.md`: what you saw, what you expected,
tagged `F1`. Then add one rule about that kind of link to `harness/CLAUDE.md`, under
**What matters to this reader**, ending with the tag, like `(F1)`.

Go back to step 5. `blank` puts your tagged rules into the prompt by itself, so the model now
judges with them. Expect each rule to move the model's line everywhere, not only on the links
you wrote it for: a rule that fixes three misses can create two new ones. Stop when the
disagreements stop teaching you anything. Three times round is a good minimum.

In the session this was "the learning after run 1, run 2...". Those notes are the
record of how you judge. Part 2 hands the same job to a second agent.

## Part 2: the loop

**The first agent.** Read `harness/CLAUDE.md`. Then run it on week one and score the brief.

```
python3 loop.py brief 1
python3 verifier/score.py traces/try
```

A score can go below zero: that means the brief cited more noise than it found signal (see
[How a brief is scored](#how-a-brief-is-scored)).

**Record where you start.** Commit your hand-written rules, then:

```
git add -A && git commit -m "F1: ..."
python3 loop.py baseline
```

Use `git add -A`, not `git commit -am`: `-a` leaves out files you created, and the baseline
refuses to start until everything is committed.

**The second agent.** Read `optimizer/CLAUDE.md`. Then let it work. One round takes about 90 seconds.

```
python3 loop.py round      # one round: steps 4 to 8 below
python3 loop.py run 3      # three rounds
python3 loop.py status
git log --oneline
```

Do not edit files in the repo while `run` is going: the check in step 6 blames the optimizer for
any change and reverts the round, and the revert also throws away uncommitted edits. Keep notes
in `notes/`: git ignores that folder, so it is safe.

**The hidden week.**

```
python3 loop.py final
```

It runs week four on the setup you started with and on the final one, and prints both
scores. It runs once. A second look is not a hidden week any more. Until a round has been
kept it refuses to run: the two setups would be the same, and the one look would be wasted.

Read the `of which` line under the scores before you believe the verdict. If "found" did not
rise and only "noise cited" fell, the new setup learned what to leave out of a brief, not more
about what you value. And if one run of the old setup already scored as high as the new one,
the rise is inside its own spread.

## Pick your harness

The two model steps run in Claude Code unless you say otherwise. Everything else is plain
Python and stays the same.

```
python3 loop.py baseline                      # Claude Code
RUNNER=codex  python3 loop.py baseline        # Codex
RUNNER=hermes python3 loop.py baseline        # Hermes
```

Set `RUNNER` once with `export RUNNER=codex` and every command after it uses Codex.

| | Claude Code | Codex | Hermes |
|---|---|---|---|
| Install | `claude` logged in | `codex` logged in | `hermes` set up with a model |
| Models | `sonnet` writes, `opus` optimizes | your Codex default | your Hermes default |
| Change them | `BRIEF_MODEL=haiku` | `BRIEF_MODEL=... OPT_MODEL=...` | `HERMES_PROVIDER=anthropic BRIEF_MODEL=claude-sonnet-5-5`, or a local model |
| Fence while it runs | permissions file: only `python3 tools/*`, edits only in `scratch/` | sandbox: writes only inside its folder | none: it can run any command |
| Caught afterwards by code | all four walls | all four walls, plus edits a brief made to the setup | the same |
| Reads your own setup? | no (`--setting-sources project`) | no: its own home in `.runner/`, your login only | no: its own home in `.runner/`, your login and model only |

`loop.py` puts the folder's `CLAUDE.md`, with `sources.md` and `memory.md` filled in, at the top
of the Codex or Hermes prompt. So one file is the setup for all three, and the optimizer's
changes reach whichever harness you run next. (Using Codex by hand? Copy it to `AGENTS.md`.)

Every trace is written in one shape, so `loop.py trace` and the optimizer read any harness's run
the same way. The tool's own log is kept next to it as `*.raw.jsonl`.

Hermes runs with no fence, so run it on this repo and nothing else you care about. Its
optimizer gets file tools only, no shell. Hermes normally asks a person before anyone edits a
`CLAUDE.md`; the optimizer's job is exactly that edit, so the home in `.runner/hermes-home`
turns that one question off. Your `~/.hermes` is not changed. The first Hermes run sets that
home up and takes a few minutes.

A small local model may not keep to the brief's format. The scorer will show you: every link
it leaves out costs a point.

Do not compare scores across harnesses. Each starts from its own baseline; compare its before
and after.

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

## How a brief is scored

Open `verifier/score.py`. Three numbers at the top are yours to tune.

```
score = (links found + 2 x decisions right - 0.5 x noise called important)
        / (links that mattered + 2 x decisions)
```

The week from the session: 7 of 9 links found, 2 of 2 decisions right, 3 noise items
called important. (7 + 4 - 1.5) / (9 + 4) = 0.73.

- A link is "found" when its id, like `[L014]`, appears under **What changed** or **What to do**.
- Any id there counts as "this matters", even in a line like "skip these: [L007] [L009]". So a
  brief that finds every link and lists the rest as skips can score below zero.
- Links under **Who disagrees** are not scored either way. A link you acted on that only appears
  there counts as missed.
- The noise penalty exists because the cheapest way to raise the score is to cite everything.

## The walls (step 6)

Checked by code after the optimizer finishes. A change that crosses one is thrown away.

1. It changed a file outside `harness/` (it may add to `optimizer/proposals.md`).
2. It changed `harness/.claude/settings.json`. Permissions are yours to approve.
3. It deleted a tag like `(F2)` or `(R1)`. A rule that traces to a logged failure can be reworded, not removed.
4. It touched the links or saved pages, or reached for `verifier/` or week four.

The briefing agent has one wall: a run whose trace reaches outside `harness/` scores zero.

## What is in the folder

| Path | What it is | Who may change it |
|---|---|---|
| `harness/` | The briefing agent's setup: `CLAUDE.md`, `sources.md`, `memory.md`, `tools/`, skills | You and the optimizer |
| `harness/.claude/settings.json` | What the briefing agent is allowed to run | You only |
| `verifier/` | Your labels, your decisions, the scoring code | You only, before any agent runs |
| `optimizer/` | The second agent's instructions, its journal, its permission requests | You (the journal is written by code) |
| `failures.md` | Failures you saw yourself, tagged F1, F2... | You |
| `loop.py` | The outer loop. Nine steps, two of them a model | You |
| `bookmarks.py` | `import` and `label`: your export in, your labels on | You |
| `agents.py` | Runs one agent in Claude Code, Codex or Hermes | You |
| `traces/` | The raw trace of every run | Written by code |
| `manual/` | Part 1's files: the blank copy, the prompt, the model's labels | Written by code and you |
| `notes/` | Yours. Ignored by git, so safe to edit while the loop runs | You |
| `facilitator/`, `deck/`, `explainer/`, `traces-sample-run/` | Session materials. You do not need them | |

## The sample month

100 links over four weeks, 8 decisions, all made up, including the product names. The reader
runs a support agent on **Kiln** (harness), **Orchard** (models) and **Postgres with Vecstore**
(database). Nothing in the harness says so. The loop has to learn it from the labels.

Every week has the same five traps, so a rule learned on weeks 1 to 3 can pay off on week 4:

| Trap | Example | Label |
|---|---|---|
| Urgent news about a tool the reader does not use | "Advisory: Anvil plugin sandbox escape, patch now" | noise |
| A newsletter recap of a changelog | "Script mode explained: what Kiln 2.4 means for you" | noise |
| A dull title hiding a breaking change | "Vecstore 0.7.3" (new indexes switch distance metric) | acted |
| A thread with real measurements | "I timed every hook in 40 Kiln projects" | should have |
| A big-name post unrelated to the reader | "Our new image model draws hands correctly" | noise |

To change it, edit `verifier/links.csv`. Its `text` column is each made-up page.

### A finished run on the sample

The branch `sample-run` holds a finished run, so you can read one without paying for it.

| | before | after 4 rounds |
|---|---|---|
| weeks 1 to 3 | 0.739 | 0.991 |
| week 4 (hidden) | 0.666 | 0.949 |

Round 1 was reverted ("fetch every link" made it cite everything: 0.739 to 0.504). Rounds 2 to 4
were kept: the reader's stack, measured findings count as news, cite the changelog not the recap.
(It was recorded before `harness/CLAUDE.md` told the agent to leave skipped links out, so your
baseline may start higher.)

```
git log origin/sample-run --oneline
git diff sample-baseline origin/sample-run -- harness
```

### A finished run on a real month

The branch `student-run-real-bookmarks` holds a run on 109 real X bookmarks, with a journal of
every step and where it got confusing (`student-journey/JOURNAL.md`).

## What `import` does with your own month

1. Writes `verifier/links.csv` with the columns `date, source, title, url, label, text`. Labels
   you already gave are kept when you import again, matched by link.
2. Puts each post's text in `text` when the export has it, so the agent reads the post. Without
   it, pages are fetched the first time the agent reads them and kept in `harness/cache/`, so a
   week reads the same on every run. Links behind a login (X, LinkedIn) come back as title only.
3. When it replaces the sample: empties `verifier/decisions.csv` to its header, and deletes
   `harness/sources.md` and `harness/cache/`.
4. Runs `prepare`. Days 22 onward become week four.

Your labelled links live in `verifier/links.csv`, which is committed in your clone. If you push
your fork to a public repo, your bookmarks and labels go with it.

## Read a trace

```
python3 loop.py trace traces/round-2/optimizer.jsonl     # what the optimizer looked at and changed
python3 loop.py trace traces/round-0/week-1.run-1.jsonl  # what the briefing agent fetched and wrote
```

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
- A week with only one or two links you acted on scores in big steps, and once the brief finds
  both it sits at 1.0 and teaches the loop nothing. `prepare` warns you about such weeks.

## When something goes wrong

| What you see | What it means |
|---|---|
| `Could not find the url and date column` | `import` could not guess your columns. Rename the link column to `url` and the date column to `date`. |
| `None of your links fall between ...` | Your export is not from 30 to 60 days ago. Use the `--from`/`--to` it suggests, or `--all`. |
| `No keyboard here` from `label` | It was run by an agent. Run `python3 loop.py label` in your own terminal. |
| `compare`: `No row ... has an id` | The model replied with something other than a CSV. Open the file; run step 5 again. |
| A score below zero | The brief cited more noise than signal it found. See [How a brief is scored](#how-a-brief-is-scored). |
| `Commit your work first` | `git add -A && git commit -m "..."`, then run the command again. |
| A round says `blocked: it changed notes.md, outside the harness` | You edited a file while the loop ran. Keep notes in `notes/`. |
| `this sign-in can end at any time` from Claude Code | Run `claude auth login` before a long `run`, so it does not stop halfway. |

## Take-home

1. Label 30 days of your own links. Do Part 1 at least three times round.
2. `python3 loop.py run 5`, then `python3 loop.py final`.
3. Keep `git log --oneline` and both scores, before and after.
4. One paragraph for a non-engineer: why did a change help the weeks the loop saw and not the hidden one?
5. Name one change you would never have written yourself, and one you rejected on review even though the score rose.
