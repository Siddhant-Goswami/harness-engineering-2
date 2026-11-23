## What changed
- **Debugging code you don't read.** Cindy Sridharan proposes a debugging framework for agents that finds the root cause without the human knowing the code. It comes from a real bug in about 9K lines of AI-written code, where her usual tactics failed and she had to isolate the bug a different way. [L037]
- **Verification as the gate.** Satya Nadella's article, "Models as Insider Risks", argues that as models and harnesses commoditize, intent, verification and evidence set how fast agents spread. His key design rule is to separate whoever does the work from whoever checks it. The full article is behind the link; I saw only Chamath's summary. [L039]
- **The model picking its own harness.** A new paper is described as "the model swallows the harness": the model chooses its harness once it sees the task. Levie calls this the eventual architecture. I saw only the post, not the paper. [L051]
- **Closed-loop software factory.** Ben Holmes writes about agents that decide what to fix, which costs to optimize, and what features to build. He says it isn't there yet. The full article is behind the link. [L061]
- **Structured context for agents.** Harvey ran experiments on Legal Agent Bench to test whether context graphs improve agent quality and efficiency. [L064]
- **Large agent swarms.** Prime Agent ran over 2,000 agents for two weeks to rewrite itself in Rust. It used 10,000+ sandboxes and 16,000 agent-to-agent messages. This is a data point on orchestration at scale. [L044]
- **Pre-ship performance audit recipe.** A Claude Code recipe has Opus 5.5 send 4 subagents to check 20 performance items on a site, then fix them in one pass. Martin Tobias says it improved his site's performance. [L059]
- **Disassembler skill for agents.** The REA skill gives an agent a real disassembler, and every claim comes back with the address behind it. Meng To links the original repo. [L070]

## Who disagrees
- **Fixed harness vs. model-chosen harness.** Levie expects the model to pick its own harness [L051]. Nadella wants a fixed separation between doer and verifier, with evidence [L039]. Both can hold. Verification stays outside the model even if the rest of the harness becomes dynamic.
- **Human expertise vs. agent-only debugging.** Sridharan builds a method for when nobody reads the code [L037]. Tobias says raw tools aren't enough and you still need a senior person to get good results from them [L059].
- **Closed loop vs. not yet.** Holmes says a fully closed loop isn't here yet [L061]. The swarm result shows how far orchestration already goes [L044].

## What to do
- Add a root-cause debugging step to your agent setup and test it on code the agent wrote. [L037]
- In your harness, keep the agent that does the work separate from the check that approves it, and have the check produce evidence. Teach this separation. [L039]
- Read the paper behind [L051] before deciding whether to teach harnesses as fixed or as chosen by the model.
- Try the subagent audit recipe as a pre-ship check, then adapt it into a reusable subagent pattern. [L059]
- Run a small test of structured context against plain retrieval on one of your tasks. [L064]
- Read Holmes's full article for the closed-loop design. [L061]
- Try the REA skill only if reverse-engineering tasks matter to your agents. [L070]