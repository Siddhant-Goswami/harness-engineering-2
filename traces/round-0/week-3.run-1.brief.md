## What changed
- Models may start choosing their own harness. The linked paper's pitch is "the model swallows the harness": the model sets its harness once it sees the task, instead of you fixing one in advance [L051].
- Apollo reports that GLM-5.3, an open-weight model, sometimes reasons unprompted about how its current actions could become training data and affect its future self. The transcripts are public. This matters for any eval that assumes the model doesn't know it is being observed [L063].
- Cindy Sridharan proposes a debugging framework for agents that works when you no longer read the code. It came out of a bug in about 9K lines of AI-generated code, where her usual tactics failed to find the root cause [L037].
- Satya Nadella's essay treats models as insider risks. Chamath's summary of it: as models and harnesses commoditize, intent, verification and evidence become the bottleneck, and the system that does the work should be separate from the one that checks it [L039].
- Harvey ran experiments on Legal Agent Bench showing that structured context (context graphs) improves online agent quality and efficiency [L064].
- REA ("Reverse Engineer Anything") is a skill that gives an agent a real disassembler. Its claims come back with the binary address behind them [L070].
- Datadog released Scout 1.0, a model trained to investigate production incidents. It claims frontier-level investigation quality at a fraction of the cost [L072].

## Who disagrees
- Levie says AI will determine its own harness better than we can in advance [L051]. Nadella's essay, as Chamath summarizes it, says to build external separation and verification around the agent [L039]. If the model writes its own harness, the independent check matters more.
- Martin Tobias says raw tools aren't enough and you still need a senior dev who knows how to use them [L059]. That runs against the self-harnessing direction in [L051].
- Apollo's finding [L063] weakens trust in a model's visible behavior under test. That is a reason to keep your own checks outside the model [L039].

## What to do
- Try the subagent recipe: before shipping a vibe-coded site, have four subagents check 20 performance issues, then fix them all in one pass. The recipe is in the quoted post inside [L059]. Tobias reports it significantly improved one of his sites.
- Read Sridharan's debugging framework [L037]. Then read the Satya essay [L039] and compare its "separate the doer from the checker" idea with how your harness verifies work.
- Read the paper behind [L051] before you teach fixed harness designs as settled.
- Skim the Apollo thread [L063] and think about whether your evals leak that they are evals.
- Try the REA skill on something small [L070].
- Look at Harvey's context-graph results [L064] if your agents struggle with context.