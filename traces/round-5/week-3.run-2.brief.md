## What changed

- **Debugging code nobody reads.** Cindy Sridharan proposes a debugging framework for agents that gets to a root cause without a human understanding the code. She built it from a real bug in about 9K lines of fully AI-generated code, where her usual tactics failed. The screenshots carry the TL;DR. [L037]
- **Separating the worker from the checker.** Chamath, relaying Satya Nadella's piece on models as insider risks, argues that intent, verification and evidence will gate adoption. His design rule is that the party doing the work must be separate from the party that verifies it. [L039]
- **A closed-loop software factory.** Ben Holmes sketches agents that decide what to fix, which costs to optimize and which features to build. He says it isn't here yet, and his attached article lays out his design. [L061]
- **Structured context, measured.** Harvey ran experiments on Legal Agent Bench to test whether context graphs improve online agent quality and efficiency. [L064]
- **Self-chosen harnesses.** An arXiv paper claims a model can determine its own harness once it sees the task. [L051]

## Who disagrees

- **Who designs the harness.** Levie says agents will eventually pick their own harness, and Domingos calls it "the model swallows the harness" [L051]. Chamath's position is the opposite: fixed, separate verification systems stay necessary [L039].
- **Whether humans still need to read the code.** Sridharan builds a method for when nobody reads the code [L037]. Martin Tobias says raw tools aren't enough and you still need a senior dev who knows how to use them [L059].
- **How far the loop closes.** Holmes thinks agents will eventually choose what to build, but admits they can't yet [L061]. Tobias wants human judgment in the loop [L059].

## What to do

- **Read Sridharan's debugging post.** Test its root-cause method on your next agent-written bug, and consider adding it to your teaching material. [L037]
- **Add a verifier separate from the worker.** Give an agent run its own checker with its own evidence trail, as the Nadella-derived rule says. [L039]
- **Copy the pre-ship subagent recipe.** It sends four Opus subagents to check 20 performance issues on a site, then fixes them in one pass. It is a reusable subagent pattern, and Tobias reports it noticeably improved one of his sites. [L059]
- **Look at Harvey's context-graph experiments.** They are concrete evidence on structured context for agent quality, so compare them with how you feed context to your own agents. [L064]
- **Skim Holmes's article for the factory loop.** Check which of its stages your harness already covers. [L061]
- **Try the REA skill if your agents need to inspect binaries.** It gives an agent a disassembler, and each claim comes back with the address behind it. [L070]