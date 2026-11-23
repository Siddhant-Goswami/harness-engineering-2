## What changed
- Cindy Sridharan proposes a debugging framework for agents that works when no human can read the code. She found the root cause of a bug in ~9K lines of fully AI-generated code only after her usual tactics failed. Her screenshots are the TL;DR. [L037]
- Harvey ran experiments on Legal Agent Bench. They show that structured context (context graphs) improves online agent quality and efficiency. [L064]
- Research argues that the model can absorb the harness and choose its own once it sees the task. [L051]
- Satya Nadella argues that as models and harnesses commoditize, intent, verification and evidence become the limit. His fix is to separate who does the work from who checks it. [L039]

## Who disagrees
- Levie and Domingos say the model will swallow the harness and pick its own, so hand-built harnesses are temporary. [L051] Nadella's view points the other way. Verification and separation of duties stay outside the model, in the harness. [L039]
- Martin Tobias says raw tools aren't enough. Good software still needs a senior person who knows how to use them. His evidence is a prompt that sped up his site. [L059]

## What to do
- Add Sridharan's debugging approach to your agent-debugging material. It covers the case where the code is too large or too generated to read. [L037]
- Reuse the pre-ship recipe in [L059]. It sends four subagents to check 20 performance problems, then fixes them all in one pass. It's a ready-made subagent pattern you can teach.
- Try context graphs in a harness, and measure them the way Harvey did, on a benchmark. [L064]
- Look at the reverse-engineering skill repo (morluto/rea). It's a skill you could add to your own agent setup. [L070]
- Read the arXiv paper behind [L051] before you decide how much harness to hand-build.