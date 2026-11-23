## What changed
- Debugging agent-written code no longer needs a person who reads it. [L037] proposes a root-cause framework for code you don't understand. It comes from a real bug in about 9K lines of AI-generated code, where the usual tactics failed.
- A new paper argues that "the model swallows the harness": the model chooses its own harness once it sees the task. [L051]
- Harvey ran experiments on Legal Agent Bench that measure how structured context (context graphs) affects agent quality and efficiency. [L064]
- Nadella's essay treats models as insider risks. It says intent, verification and evidence will limit how fast enterprises adopt agents, and that the system doing the work should be separate from the one that checks it. [L039]

## Who disagrees
- [L051] says harness design will move into the model. [L039] says the harness, meaning the verification and separation of duties around the model, is what enterprises will rely on. The reader building and teaching harnesses should read the paper behind [L051] before treating either view as settled.
- [L037] works when you don't read the code. [L039] says verification and evidence should come from a separate party. Both lead to checks that don't depend on a human reading the code, but [L037] still has a person debugging, and [L039] doesn't.

## What to do
- Read the debugging framework in [L037] and compare it with your own debugging and check steps for agents.
- Reuse the subagent recipe in [L059]: before shipping, send four subagents to check 20 performance issues, then fix them all in one pass. It is shown on a website, but it applies to any project.
- Try the REA skill in [L070]. It gives an agent a real disassembler, and each claim it makes comes back with the address behind it. It is a repo for your own agent setup, not a demo.
- Skim the Harvey context-graph results in [L064] for ideas on structuring agent context.
- Read the paper behind [L051] to see how far "the model picks its own harness" holds up.