## What changed
- Cindy Sridharan has written up a debugging framework for agents. It finds the root cause without the human needing to know the code. Her test case was a real bug in about 9K lines of 100% AI-generated code. [L037]
- Ben Holmes sketches a closed-loop "software factory" in which agents decide what to fix, which costs to optimize and which features to build. It is his own design writing. [L061]
- Harvey ran experiments on Legal Agent Bench to measure how structured context (context graphs) improves online agent quality and efficiency. [L064]
- A reverse-engineering skill (REA) gives an agent a real disassembler, so each claim comes back with the address behind it. [L070]
- A subagent recipe has four subagents check 20 site-slowing issues, then fix them all in one pass. [L059]

## Who disagrees
- A paper argues "the model swallows the harness". Aaron Levie says agents should eventually pick their own harness once they see the task. That conflicts with the work above, which hand-designs loops, context and checks. [L051]
- Martin Tobias says raw tools aren't enough and you still need a senior person to get the most out of them. He is arguing against the idea that the model alone is sufficient. [L059]

## What to do
- Read Sridharan's debugging framework and add its root-cause steps to your agent-debugging material. [L037]
- Compare Holmes's closed-loop design with your own harness loop, specifically how the agent decides what to fix and build. [L061]
- Try Harvey's structured-context approach on one of your own agent tasks and compare the results. [L064]
- Install the REA skill and test it on a binary. [L070]
- Reuse the four-subagent audit recipe as a pre-ship check in a teaching example. [L059]
- Check the paper behind the "model swallows the harness" claim before you decide how much harness to teach. [L051]