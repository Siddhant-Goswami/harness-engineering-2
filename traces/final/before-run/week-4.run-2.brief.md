## What changed
- Anthropic now advises folding unnecessary subagents back into the main agent loop. A single agent with skills often beats a multi-agent setup. This is reported second-hand, so check the original post. [L106]
- LangChain published its recipe for a "company harness", built from five parts. It lives in Slack. It uses on-behalf-of identity for some tools and fixed credentials for others. It has scoped memory. Code runs in a sandbox. Many of its runs are scheduled. [L105]
- Google Research's harness² describes hill-climbing on the harness while the model stays fixed. [L089]
- Browser Use open-sourced rl-env-use. From a one-line skill description, it builds a verified environment for hill-climbing. [L092]
- Open-sourced parts of a harness: a workflow DSL that turns agentic loops into more deterministic recipes, used in a self-improving loop. [L095]
- Evals:
  - Cameron Wolfe's roadmap for evals on subjective tasks. [L094]
  - Hamel Husain on decision models for evals, with a tuned threshold. [L090]
  - Letta's FrontierMemory, which scores agent memory by downstream task performance. [L091]
- Theo's explainer sets out what a harness is: tools, a call syntax, a parser, results fed back, and a tool list. [L098]

## Who disagrees
- "The End of Harness Engineering" argues that the loop that runs the model should write the harness file, not a person. LangChain's recipe is the opposite: a hand-built, multi-primitive design. [L088] is a hyped repost, so find the paper itself. [L105]
- Anthropic's advice to use fewer subagents cuts against the habit of splitting work across many agents. [L106]
- Theo says Claude Code is only partly a harness. He splits it into an interface and a harness. [L098]

## What to do
- Audit your subagents. Fold into the main loop any that a skill could replace. [L106]
- Use LangChain's five-part recipe as a checklist for a multi-user harness. Settle identity first, meaning on-behalf-of or fixed credentials per tool. [L105]
- Read the harness² paper and try its hill-climbing idea on your own harness. [L089]
- Try rl-env-use to build environments for your skills. [L092]
- Use [L090] and [L094] when you build evals or LLM judges. Tune the judge's threshold instead of assuming 0.5.
- Use Theo's article as a teaching reference. [L098]
- Look at the open-sourced workflow DSL for making loops deterministic. [L095]