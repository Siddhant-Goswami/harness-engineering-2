## What changed
- Agents that write code nobody reads need a debugging method that doesn't rely on understanding the code. Cindy Sridharan proposes a root-cause framework for this. She found the usual tactics failed on a bug in about 9K lines of fully AI-written code. [L037]
- Harvey ran experiments on Legal Agent Bench to test whether structured context (context graphs) improves agent quality and efficiency. [L064]
- There is a paper arguing the model can absorb the harness and pick its own once it sees the task. [L051]
- Satya's point, as relayed by Chamath: as models and harnesses commoditize, intent, verification and evidence set the pace. He also says the system that does the work should be separate from the one that checks it. [L039] I only saw the first lines of this post.

## Who disagrees
- Levie and Domingos expect models to choose their own harness, so hand-built harnesses become temporary. [L051]
- Martin Tobias holds the opposite view: raw tools aren't enough, and skilled people who know how to use them still decide the result. [L059]
- Chamath, citing Satya, puts the value in the verification layer, not in harness design. [L039]

## What to do
- Read Sridharan's debugging framework and try it on your own agent-written code. It also works as teaching material for harness students. [L037]
- Take the pre-ship recipe in [L059]: have 4 subagents each check a list of 20 performance problems, then fix them all in one pass. It is a reusable subagent pattern. You'll need the original post by Voxyz for the full prompt.
- Look at Harvey's context-graph experiment before you add structured context to an agent. [L064]
- Try the reverse-engineering skill repo as an example of a skill you can install. [L070]
- Skim the arXiv paper to see how far "the model swallows the harness" holds up, so your course doesn't go stale. [L051]