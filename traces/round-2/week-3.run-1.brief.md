## What changed
- Cindy Sridharan proposes a debugging framework for agents that doesn't depend on a human understanding the code. She built it from a real bug in about 9K lines of fully AI-generated code, where her usual tactics failed to find the root cause. [L037]
- New research argues "the model swallows the harness": the model picks its own harness once it sees the task, instead of you fixing it in advance. [L051]
- Harvey ran experiments on Legal Agent Bench showing that structured context (context graphs) improves online agent quality and efficiency. [L064]
- Nadella's essay treats models as insider risks. His point is to separate the agent that does the work from the check on that work, and to require evidence. [L039]

## Who disagrees
- Levie and Domingos expect harnesses to be absorbed into the model. [L051] Nadella and Chamath say that as models and harnesses commoditize, verification and evidence will be the bottleneck. They want the doer and the checker kept separate. [L039]
- Martin Tobias says a good prompt improved his site's performance, but that raw tools still need a senior engineer to get good software. That cuts against the idea that agents can be left to run unattended. [L059]

## What to do
- Read Sridharan's debugging framework. Try it on a bug in code the agent wrote, and use it in your teaching material. [L037]
- Copy the subagent recipe in [L059]. It sends 4 subagents to check about 20 performance problems, then fixes them in one pass. The recipe is in the quoted Vox post, not in Tobias's own text, so check it before you reuse it.
- Take the REA skill, which gives an agent a real disassembler and ties each claim to an address. It may suit your own agent setup. Test it before you recommend it. [L070]
- Add a verifier that is separate from the worker agent in your harness. [L039]
- Compare structured context against plain context in your own agent evals. [L064]
- Use [L051] as a counterpoint when you teach why harnesses matter.