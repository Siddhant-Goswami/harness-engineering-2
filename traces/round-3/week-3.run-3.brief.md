## What changed
- **Debugging code nobody reads.** Cindy Sridharan proposes a debugging framework for agents that finds the root cause without a human understanding the code. It came out of a real bug in about 9K lines of fully AI-written code, where her usual tactics failed. The TL;DR is in the screenshots, and the full post is linked in her reply. [L037]
- **The model swallows the harness.** A new paper has the model choose its own harness once it sees the task, instead of the harness being fixed in advance. Levie calls this the eventual architecture of agents. [L051]
- **Verification is the bottleneck.** Satya Nadella's piece, "Models as Insider Risks", argues that as models and harnesses commoditize, intent, verification and evidence set the pace. It says to separate whoever does the work from whoever checks it. Only the teaser was readable, so the full article is behind the link. [L039]
- **Closed-loop software factory.** Ben Holmes writes about agents that decide what to fix, which costs to optimize and which features to build. The full article is behind the link. [L061]
- **Structured context helps agents.** Harvey ran context-graph experiments on Legal Agent Bench to measure how structured context improves online agent performance. [L064]
- **Large agent swarms.** Prime Agent orchestrated more than 2,000 agents over two weeks to rewrite itself in Rust. It used 10,000+ sandboxes and 16,000 agent-to-agent messages. [L044]

## Who disagrees
- **Who designs the harness.** Levie expects the model to determine its own harness [L051]. Nadella wants an external layer that checks the work independently of whoever did it [L039]. These pull in opposite directions: a self-built harness has to stay checkable from outside.
- **Do you need to read the code?** Sridharan builds a method for when you don't understand the code [L037]. Martin Tobias says raw tools aren't enough and you still need a senior dev who knows how to use them [L059].

## What to do
- Read Sridharan's debugging framework and try it on your next agent-written bug. [L037]
- Reuse the subagent recipe in [L059]: before shipping, send four subagents to check 20 performance issues, then fix them all in one pass. Only a teaser of the 20-item list was visible, so open the original post for the full list.
- Add a checking step to your harness that is separate from the agent doing the work, as [L039] argues.
- Read the closed-loop factory article for ideas on letting agents choose what to fix and build. [L061]
- Optional: the REA skill gives an agent a disassembler for reverse engineering. [L070] It's worth a look if you want that capability in your own setup.