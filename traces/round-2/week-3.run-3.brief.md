## What changed
- Cindy Sridharan proposes a debugging framework for agents that doesn't depend on a human understanding the code. She built it from a real bug in about 9K lines of fully AI-generated code, where her usual tactics failed to find the root cause. [L037]
- Harvey ran experiments on Legal Agent Bench to test whether structured context ("context graphs") improves online agent quality and efficiency. [L064]
- A new paper argues the model can absorb the harness and choose its own for the task at hand. [L051]
- Satya Nadella's essay "Models as Insider Risks" says that as models and harnesses commoditize, intent, verification and evidence become the bottleneck. It says the system that does the work must be separated from the one that checks it. [L039]

## Who disagrees
- Aaron Levie reads the "model swallows the harness" paper as the eventual architecture: the AI will choose its own harness better than we can in advance. [L051]
- Nadella argues the opposite. The harness has to stay outside the model, because verification and separation of duties can't be left to the thing being checked. [L039]
- Martin Tobias argues raw tools aren't enough, and that a skilled senior dev who knows how to drive them still matters. His evidence is a subagent audit prompt that sped up his site. [L059]

## What to do
- Use the debugging framework in your next agent-debugging lesson. Test it on code the agent wrote and you haven't read. [L037]
- Copy the pre-ship recipe: have four subagents check 20 performance issues, then fix them all in one pass. Adapt it as a template for a parallel-subagent audit step. [L059]
- Read the Harvey context-graph experiments before adding structured context to your agents. [L064]
- Add the Nadella essay to the verification and evidence part of your material. [L039]
- Skim the paper behind the "model swallows the harness" claim, so you can answer the question of whether harness engineering becomes obsolete. [L051]
- Try the REA skill, which gives an agent a disassembler and ties every claim to an address. Use it as an example of a skill that makes an agent's claims checkable. [L070]