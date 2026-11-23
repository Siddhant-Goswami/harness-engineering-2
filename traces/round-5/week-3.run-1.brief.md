## What changed
- Agents can now be debugged without a human reading the code. Cindy Sridharan proposes a root-cause framework for code that is 100% AI-generated, tested on a real bug in about 9K lines [L037].
- Harvey ran experiments on Legal Agent Bench to see whether structured context graphs improve online agent quality and efficiency [L064].
- Satya Nadella's piece frames models as insider risks. Chamath's takeaway is that intent, verification and evidence will limit how fast enterprises adopt agents. You need systems that separate who does the work from who checks it [L039].
- Ben Holmes sketches a closed-loop software factory where agents decide what to fix, which costs to optimize and what to build. He says it isn't here yet [L061].
- A new agent skill, REA, gives an agent a real disassembler. Every claim it makes comes back with the address behind it [L070].

## Who disagrees
- Levie says a paper shows the model absorbing the harness. In his view, AI will eventually choose its own harness once it sees the task, better than we can in advance [L051]. Chamath and Nadella argue the opposite. They want an external layer that verifies work and keeps the worker separate from the checker [L039].
- Martin Tobias says raw tools aren't enough to get good software. You still need a senior dev who knows how to use them, and a good prompt is what improved his site [L059]. That conflicts with the idea of agents debugging code nobody understands [L037].

## What to do
- Read Sridharan's debugging framework and test it on a real bug in AI-written code. Consider adding it to your harness teaching material [L037].
- Try the subagent recipe in [L059]. Have four subagents check 20 performance issues, then fix them in one pass. Treat it as a template for parallel review.
- Look at Harvey's context-graph results before deciding whether structured context belongs in your agent setups [L064].
- Add a verification step that is separate from the worker. Use [L039] as your design reference, and judge [L051] by whether the paper's claim holds up on your tasks.
- Skim [L061] for its closed-loop framing.
- Try the REA skill from [L070] on a binary to see whether its address-backed claims are useful for checking agent work.