## What changed
- Agents now write code that no human reads, and debugging has to work without a person's knowledge of the code. Cindy Sridharan proposes a debugging framework that gets an agent to the root cause without that knowledge. It comes from a real bug in about 9K lines of AI-generated code, where her first tactics failed. The framework is in screenshots, and the full post is behind the link. [L037]
- Satya Nadella argues that models are insider risks. As models and harnesses commoditize, intent, verification and evidence set the pace of adoption. Systems should separate who does the work from who checks it. [L039]
- Ben Holmes is thinking about a closed-loop software factory, where agents decide what to fix, which costs to optimize and what features to build. The full article is behind the link. [L061]
- Harvey ran experiments on Legal Agent Bench. They found that structured context graphs improve online agent quality and efficiency. [L064]
- Prime Intellect ran a swarm of more than 2,000 agents for two weeks to rewrite its own agent in Rust. It used over 10,000 sandboxes and 16,000 agent-to-agent messages. This is a data point on running agents at scale. [L044]

## Who disagrees
- [L051] says the model will end up choosing its own harness once it sees the task. It points to a paper whose summary is "the model swallows the harness". [L039] says to build external checks that separate the doer from the verifier. Build verification outside the model for now.
- [L059] says raw tools aren't enough and you still need a senior person to direct them. [L037] goes the other way and tries to remove the need for that code knowledge.

## What to do
- Add a pre-ship pass to your Claude Code setup. Have Opus send four subagents to check 20 performance issues, then fix them in one pass. This improved the sender's site, and you can reuse it as a subagent recipe for your teaching material. [L059]
- Try the REA skill, which gives an agent a disassembler so every claim comes back with an address. It is a reusable skill for reverse engineering any binary. [L070]
- Use [L037] as the basis for a debugging step in your harness. Test it against [L039]'s doer/verifier split.
- Read the full article in [L061] before you design any closed-loop pipeline.