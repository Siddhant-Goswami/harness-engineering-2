# Journal

Written by loop.py after every round. The optimizer reads it; it does not write it.

## Round 1: kept
- Change: Added one tagged line (R1) to memory.md: news about a model itself (releases, lab findings on model behavior, reactions to them) is noise unless it gives a concrete change to how an agent is built, run or checked.
- Predicted: Stops week 3's model-news noise: L063 (3/3 runs), L062 (1/3), and L072 as the brief described it (a model release, 2/3); it does not touch L021, L023 or the missed L061.
- Observed: 0.752 to 0.855 on weeks 1 to 3

## Round 2: kept
- Change: Added a memory.md line (R2) that narrows F3: a product launch (hardware SDK, design pack) that only says "point your agent at the repo", or ships a skill for making more of that product, is noise unless it would improve the reader's agent on any project.
- Predicted: Drops the week-2 noise L021 (2/3 runs) and L023 (1/3) while keeping L022, L059 and L070 as signal; it does not fix the missed L061 in week 3.
- Observed: 0.855 to 0.938 on weeks 1 to 3
