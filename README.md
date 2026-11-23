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

**Or hand the whole run to your agent, clone included.** Open Claude Code, Codex or Hermes in
the folder where you keep your projects and paste the prompt below. It reads the repo and runs
every step, and stops only where your judgement is needed: which month, your labels, each rule,
the go for Part 2, and the hidden week. If its sandbox blocks a step, it hands you the command.

<details><summary>The prompt</summary>

```
Set up and run the Harness Engineering 2.0 repo for me, from the clone to
the hidden week. You do the work. Stop only where a step needs my judgement:
the five points listed below.

GET THE REPO
- If this folder has loop.py and README.md, you are already in it. Else, if a
  folder called harness-engineering-2 is here, go into it. Else clone it and
  go into it:
  git clone https://github.com/Siddhant-Goswami/harness-engineering-2
- If the clone fails (Codex's sandbox has no network), stop. Tell me to run
  that line in my own terminal, then to open you again inside the new folder.
- Check that python3 is 3.10 or newer and that git is installed. If not, say
  how to fix it.

READ IT BEFORE YOU RUN IT
- Read README.md, all of it. It is the source of truth: where it and this
  prompt disagree, follow the README.
- Read harness/CLAUDE.md (the briefing agent), optimizer/CLAUDE.md (the
  optimizer), the top of verifier/score.py (the score) and failures.md.
- Run `python3 loop.py next`. It looks at the folder and says which step we
  are on and the one command to run. Run it after every step, and whenever you
  are unsure.
- Then tell me in five lines what this system does and what you will do first.

HOW TO RUN THE COMMANDS
- Claude Code: run loop.py as written. Codex: put RUNNER=codex in front of
  every loop.py command. Hermes: put RUNNER=hermes in front.
- baseline, round and final call a model many times and take minutes. Give
  each one a timeout of 10 minutes, or run it in the background and wait for
  it to finish. When `next` says `run N`, run `python3 loop.py round` N times
  instead, and tell me each result.
- If a command fails because of your sandbox, a permission or a timeout, do
  not work around it. Give me the exact command to run in my own terminal,
  wait, then read what it wrote.
- If anything else fails, read "When something goes wrong" in the README, then
  run `python3 loop.py next`.

STOP AND ASK ME HERE, AND ONLY HERE
1. Which month.
   (a) The made-up sample, already labelled: about $1.50 with Claude Code.
   (b) The real month in examples/x-bookmarks.csv, already labelled: about
       $7. Load it with:
       python3 loop.py import examples/x-bookmarks.csv --all
   (c) My own saved links: give me the browser prompt from README Part 1
       step 1, wait for the path to my CSV, import it, show me the table and
       point out every line that starts with `!`.
2. My labels, own links only. Tell me to run `python3 loop.py label` in my own
   terminal, and wait until I say I am done.
3. Every rule. After each `compare`, show me how many links we agreed on, the
   two lines under the percentage, and the disagreements. Propose the mistake
   that repeats as the next F entry for failures.md, and one rule ending in
   its tag, like (F1), for harness/CLAUDE.md under "What matters to this
   reader". Write them only after I approve or rewrite them. Then blank, the
   model and compare again. At least three times round; ask me each time
   whether to go on.
4. Before Part 2. Commit with `git add -A` and `git commit`, tell me roughly
   what Part 2 will cost, and wait for my go before `baseline`.
5. Before `final`. It opens week four once, and that cannot be undone. Show me
   `git log --oneline` and `python3 loop.py status` first. Never add
   `--anyway` unless I ask.
Between these points, keep going: run the step, show me the lines of output
that matter, say what they mean in two sentences, and move on.

NEVER
- Label a link, guess a label for me, or edit the label column.
- Open verifier/links.csv yourself: week four's labels are in it, and they
  stay hidden until final. Rules come from weeks 1 to 3 only.
- Edit anything in verifier/ or harness/.claude/settings.json.
- Edit any file in the repo while baseline, round or final is running. Notes
  go in notes/.
- Change the harness yourself in Part 2. There, only the optimizer changes it.

AT THE END
Show me both scores and the "of which" line under them, and list the changes
that were kept. Then ask me the take-home questions at the end of the README,
one at a time. Do not answer them for me.
```

</details>

**Lost at any point? Run `python3 loop.py next`.** It looks at the folder, tells you which step
you are on, and prints the one command to run next.

A step-by-step tutorial with screenshots for all three harnesses:
https://100x-curriculum.vercel.app/harness-engineering-2/tutorial/

| | Works with | Costs |
|---|---|---|
| **Part 1**, by hand | Any chat tool: Claude, ChatGPT, Codex, Hermes | Nothing beyond your chat plan |
| **Part 2**, the loop, on the sample month | Claude Code, Codex or Hermes (see [Pick your harness](#pick-your-harness)) | About $1.50 with Claude Code |
| **Part 2** on your own month | the same | About $7 with Claude Code (baseline, 5 rounds and the hidden week, on 109 X posts with their text) |

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

No export of your own yet? A real month ships with the repo: 109 X bookmarks with their text and
labels, in `examples/x-bookmarks.csv`. `python3 loop.py import examples/x-bookmarks.csv --all`
loads it, and you can go straight to step 5 (see [A finished run on a real month](#a-finished-run-on-a-real-month)).

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
| Reads your own setup? | no (`--setting-sources ""`) | no: its own home in `.runner/`, your login only | no: its own home in `.runner/`, your login and model only |

`loop.py` hands every run the folder's `CLAUDE.md`, with `sources.md` and `memory.md` filled in:
appended to Claude Code's system prompt, at the top of the Codex or Hermes prompt. Claude Code
would load it by itself only in a folder you have trusted, so the loop never relies on that. One
file is the setup for all three, and the optimizer's changes reach whichever harness you run next. (Using Codex by hand? Copy it to `AGENTS.md`.)

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
| `harness/` | The briefing agent's setup: `CLAUDE.md`, `sources.md`, `memory.md`, `tools/`, and any skills you add in `.claude/skills/` | You and the optimizer (skills: you only) |
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
| `examples/x-bookmarks.csv` | A real month: 109 X bookmarks with their text and labels | You |

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

### A finished run on a real month

`examples/x-bookmarks.csv` is a real month: 109 posts saved on X from 25 September to 24 October
2026, each with its text, about agents, harnesses, evals, AI video and startups. They are labelled
for a reader who builds and teaches agent harnesses, against one written rubric: what changes how
an agent is built, run or checked is signal; demos, launches, market takes and hype are noise.
13 of the 76 links in weeks 1 to 3 are signal.

The branch `real-month` holds a finished run on it in Claude Code, commit by commit, with every
trace. Part 1, a model labelling the same links blind, one rule a round:

| Round | The rule added | Signal found | Noise called signal |
|---|---|---|---|
| 1 | none yet | 13 of 13 | 15 of 63 |
| 2 | F1: a demo of what a model can make is noise | 10 of 13 | 4 |
| 3 | F2: a hype repost of someone else's work is noise | 10 of 13 | 1 |
| 4 | F3: a tool for your own agent setup is signal, whatever it is shown on | 13 of 13 | 4 |

Part 2, the loop, starting from those three rules:

| Round | The optimizer's change | Weeks 1 to 3 | |
|---|---|---|---|
| start | F1 to F3 | 0.752 | |
| 1 | News about a model itself is noise unless it changes how an agent is built, run or checked | 0.855 | kept |
| 2 | A product launch that only says "point your agent at our repo" is not a setup tool | 0.938 | kept |
| 3 | A teaser that attaches an article is signal if the article is the author's own | 0.919 | reverted |
| 4 | The same, but not for comment on someone else's result | 0.911 | reverted |
| 5 | Judge a post by the author's own words, not by what it attaches | 0.986 | kept |

| | before | after 5 rounds |
|---|---|---|
| weeks 1 to 3 | 0.752 | 0.986 |
| week 4 (hidden) | 0.796 (8.0 of 9 found, 1.7 noise cited) | 0.852 (8.3 of 9 found, 1.3 noise cited) |

The hidden week rose less than the weeks the loop could see: part of what it learned was about
these three weeks. It cost $6.84 in Claude Code.

#### What is on the branch, and how to read it

`real-month` is `main` plus the commits of that one run, made the way you would make yours:

| On `main` | On `real-month` |
|---|---|
| The sample month in `verifier/links.csv`, with its 8 decisions | The real month, imported from `examples/x-bookmarks.csv`; no decisions |
| Empty `failures.md`, stock `harness/CLAUDE.md` | F1 to F3 in `failures.md`, and their rules in `harness/CLAUDE.md` |
| Empty `harness/memory.md` | The three rules the optimizer kept: R1, R2 and R5 |
| No `scores.csv`, empty `optimizer/journal.md` | Every round's scores and the optimizer's journal |
| No `traces/` | Every brief and trace, `verifier/week4-opened.json`, and the four Part 1 compare outputs in `part1/` |

Read it without switching to it. `git checkout real-month` would put its labels, rules and scores
in your folder in place of yours. Instead:

```
git log origin/real-month --oneline                   # the run, one commit per step
git show origin/real-month:harness/memory.md          # the three rules the optimizer kept
git diff 5cca3c2 origin/real-month -- harness         # all it changed after the baseline (5cca3c2)
git worktree add ../real-month origin/real-month      # the whole run in a folder of its own
```

In that folder, `python3 loop.py status` lists the rounds and
`python3 loop.py trace traces/round-5/optimizer.jsonl` shows what the optimizer read. Remove the
folder with `git worktree remove ../real-month`.

To make the run yourself: `python3 loop.py import examples/x-bookmarks.csv --all` in your own clone,
then Part 1 from step 5.

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
| `The live score is 1.0: no change can beat it` | Nothing is left to win on weeks 1 to 3. Read `git log --oneline`, then `python3 loop.py final`. |
| `final`: `No change has been kept yet` | It waits for a kept round, so your one look is not spent comparing a setup with itself. Run more rounds, or `final --anyway`. |
| A round says `blocked: it changed notes.md, outside the harness` | You edited a file while the loop ran. Keep notes in `notes/`. |
| `this sign-in can end at any time` from Claude Code | Run `claude auth login` before a long `run`, so it does not stop halfway. |

## Take-home

1. Label 30 days of your own links. Do Part 1 at least three times round.
2. `python3 loop.py run 5`, then `python3 loop.py final`.
3. Keep `git log --oneline` and both scores, before and after.
4. One paragraph for a non-engineer: why did a change help the weeks the loop saw and not the hidden one?
5. Name one change you would never have written yourself, and one you rejected on review even though the score rose.
