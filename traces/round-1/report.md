# Report for round 1

The live setup scored 0.752 on weeks 1 to 3, the mean of 3 runs per week (traces: ../traces/round-0/, one file per week per run).
Per week: week 1: 0.875 (0.75 to 1.0), week 2: 0.667 (0.5 to 0.75), week 3: 0.714 (0.714 to 0.714)

Worst week: 2. Its worst run: ../traces/round-0/week-2.run-1.jsonl
A miss in every run is a habit of the setup. A miss in one run may be chance.

## Missed: the reader acted on these, or should have, and the brief left them out
- week 3 | L061 | X @BHolmesDev | I've been thinking about what a true, closed-loop software factory will look like. | should_have | in 3 of 3 runs

## Noise the brief called important
- week 1 | L011 | X @ArchiveExplorer | jev + opus 5.5 for design is insane... | noise | in 2 of 3 runs
- week 1 | L015 | X @everestchris6 | this is the only prompt you need to make high-end motion videos with claude opus 5.5 | noise | in 1 of 3 runs
- week 2 | L021 | X @natfriedman | 🚨 side project alert 🚨 | noise | in 3 of 3 runs
- week 2 | L023 | X @lucasmarkes__ | hairlines v0.2 is now available! | noise | in 1 of 3 runs
- week 3 | L063 | X @ApolloResearch | We have never seen a model do this before, but GLM-5.3 sometimes reasons (unprompted) about how its current actions could become training da | noise | in 3 of 3 runs
- week 3 | L072 | X @spencermateega | Every serious enterprise will soon own and control its own intelligence. | noise | in 2 of 3 runs
- week 3 | L062 | X @NeelNanda5 | This is wild... (And terrifying!) I'd love to see a bunch of investigation into what's going on in these transcripts, it's nice to have the | noise | in 1 of 3 runs

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
