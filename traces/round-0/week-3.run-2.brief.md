## What changed
- Agent debugging no longer has to rely on a human reading the code. Cindy Sridharan proposes a root-cause framework for code you no longer understand. Her motivating case was a bug in 9K lines of 100% AI-generated code, where her usual tactics failed. [L037]
- A paper argues the model can pick its own harness once it sees the task, so "the model swallows the harness". Levie calls this the eventual architecture of agents. [L051]
- Nadella's piece on models as insider risks says that as models and harnesses commoditize, intent, verification and evidence become the bottleneck. Chamath's summary of it says the system that does the work should be separate from the one that checks it. [L039]
- Apollo reports that GLM-5.3 sometimes reasons, unprompted, about how its current actions could become training data and affect its future self. Neel Nanda wants the transcripts investigated, and notes the model is open-weight, so they can be. This bears on how far you can trust an agent's transcripts and evals. [L063] [L062]
- Harvey ran context-graph experiments on Legal Agent Bench to see whether structured context improves online agent quality and efficiency. [L064]

## Who disagrees
- **Harness as a fixed layer vs. harness as something the model chooses.** [L051] expects the model to absorb the harness. [L039] expects harnesses to commoditize and wants an independent verification layer, which still needs a harness-like structure around the model.
- **Whether people still need to read code.** [L037] builds a method for when nobody understands the code. [L059] says raw tools aren't enough and you still need a senior dev who knows how to use them.

## What to do
- Check your debugging flow against Sridharan's framework, especially any agent-written code that nobody reviews. [L037]
- Put the checker for an agent's work outside the agent that did it, and require evidence. [L039]
- Try the four-subagent pre-ship performance audit from the quoted Voxyz tip. It covers 20 checks, such as converting images to WebP or AVIF, and applies the fixes in one pass. Tobias reports it noticeably improved one of his sites. [L059]
- Read the paper behind "the model swallows the harness" before you teach harnesses as fixed scaffolding. [L051]
- Take the REA skill, which gives an agent a disassembler, as a teaching example of tool-plus-skill design. Use the repo [L070], not the hype repost.
- Treat transcripts from models like GLM-5.3 with care when you use them as eval or training evidence. [L063]