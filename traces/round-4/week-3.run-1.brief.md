## What changed
- Debugging code you no longer read now has a method that doesn't depend on knowing the code. It came out of a real bug in about 9K lines of AI-generated code, where the usual tactics failed to find the root cause. [L037]
- Harvey ran experiments on Legal Agent Bench. They report that structured context (context graphs) improves agent quality and efficiency. [L064]
- A paper argues that "the model swallows the harness": the model picks its own harness once it sees the task. [L051]
- Ben Holmes sketches a closed-loop software factory. In it, agents decide what to fix, which costs to optimize and which features to build. He says this isn't reachable yet. This is his own long-form design, which I haven't read in full. [L061]
- A pre-ship recipe for Claude Code: send 4 subagents to check 20 things that slow a site down, then fix them all in one pass. [L059]
- REA ("Reverse Engineer Anything") is a skill and repo that gives an agent a real disassembler. [L070]

## Who disagrees
- [L051] says the harness will be determined by the model at run time. [L037] and [L061] both design the harness by hand: a debugging framework in one, a closed-loop factory in the other.
- [L059] says raw tools aren't enough and you still need a senior engineer. That contradicts the idea that the model can set up its own harness.

## What to do
- Read the debugging framework in [L037] and test it on a bug in code you didn't write by hand.
- Copy the subagent checklist pattern from [L059]. Use it as a model for a parallel-review subagent recipe in your own harness.
- Read the paper behind [L051] before you invest more in fixed harness structure.
- Try the REA skill in [L070] on one binary. See whether its address-backed claims work as a way to check an agent's output.
- Skim the context-graph results in [L064]. Judge whether the gains carry over outside legal tasks.
- Treat [L061] as a design to compare against your own loops. It isn't something to adopt yet.