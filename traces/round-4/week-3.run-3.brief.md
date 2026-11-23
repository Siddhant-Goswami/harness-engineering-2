## What changed
- Debugging when nobody reads the code now has a framework. It finds the root cause without relying on a human's knowledge of the code. The author hit a bug in about 9K lines of fully AI-generated code, and the tactics they started with didn't isolate it. [L037]
- Context graphs have measured results. Harvey ran experiments on Legal Agent Bench to test whether structured context improves online agent quality and efficiency. [L064]
- Satya Nadella's piece treats models as insider risks. As models and harnesses commoditize, intent, verification and evidence become the gate. The design rule is to separate who does the work from who checks it. [L039]
- There is an argument for a closed-loop software factory, where agents decide what to fix, what costs to optimize and what to build. The author says it isn't here yet. [L061]
- New research claims "the model swallows the harness", meaning the model picks its own harness once it sees the task. [L051]

## Who disagrees
- [L051] says the harness will be absorbed into the model. [L039] and [L037] say the opposite: the checking layer (separate verifier, evidence, an explicit debugging method) must stay outside the model, because you can't trust or read what the model did.
- [L061] sits between them. It wants agents to close the loop themselves but admits that isn't reachable yet.

## What to do
- Add a "no code reading" debugging step to your harness, built from the framework in [L037]. Use it in teaching material as the counter-case to trusting agent output.
- Make verification a separate role in your agent designs: the agent that does the work shouldn't be the one that signs it off. Use [L039] as the reference.
- Before shipping a site, have an agent send four subagents to check about 20 performance items, then fix them in one pass. The recipe is in the quoted post, and it's a reusable subagent pattern. [L059]
- Read the paper behind [L051] and test whether a task-adaptive harness beats your fixed one on your own tasks.
- Look at how Harvey structures context and replicate the comparison on one of your agents. [L064]
- Read [L061] as a design sketch for a loop that chooses its own work. Don't adopt it yet.