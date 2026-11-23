# Report for round 4

The live setup scored 0.938 on weeks 1 to 3, the mean of 3 runs per week (traces: ../traces/round-2/, one file per week per run).
Per week: week 1: 0.958 (0.875 to 1.0), week 2: 1.0 (1.0 to 1.0), week 3: 0.857 (0.857 to 0.857)

Worst week: 3. Its worst run: ../traces/round-2/week-3.run-1.jsonl
A miss in every run is a habit of the setup. A miss in one run may be chance.

## Missed: the reader acted on these, or should have, and the brief left them out
- week 3 | L061 | X @BHolmesDev | I've been thinking about what a true, closed-loop software factory will look like. | should_have | in 3 of 3 runs

## Noise the brief called important
- week 1 | L011 | X @ArchiveExplorer | jev + opus 5.5 for design is insane... | noise | in 1 of 3 runs

## Decisions it got wrong
- none

## The failure log, kept by hand

# Failure log

One entry per failure you saw with your own eyes. A rule you add to `harness/CLAUDE.md`
because of an entry carries its tag, like `(F1)`. Tagged rules can be reworded, never deleted.

<!-- Example
## F1 · week 1
Saw: the brief led with a funding round and left out the changelog entry that broke our hooks.
Expected: changes to tools I use come first.
-->

## F1 · weeks 1 to 3
Saw: the model called 15 noise links signal. Most are things made with AI: a launch video, motion
videos, landing-page shaders, design kits, new answer interfaces (L007, L015, L028, L040, L068).
Expected: I build and teach agent harnesses. A demo of what a model can make is noise to me, however
impressive. What changes how an agent is built, run or checked is what I act on.

## F2 · weeks 1 to 3
Saw: the model called hype reposts signal because their topic is harnesses or Claude Code:
"this is pure f*cking treasure" (L027), "Boris Cherny just released a prompt..." (L036),
"It is becoming f*cking dangerous" (L067).
Expected: an account repackaging someone else's work with hype is noise. I read the original.

## F3 · weeks 1 to 3
Saw: after F1 the model called three links I acted on noise. Each hands me something for my own
agent setup, though the example is a website or a gadget: Claude mods (L022), a subagent recipe
that checks a site before shipping (L059), a reverse-engineering skill (L070).
Expected: a feature, prompt recipe, skill or repo I can use in my own agent setup is signal, whatever
it is shown working on. F1 is about what a model makes, not about what an agent is used for.
