## What changed
- Google Research's harness² applies hill-climbing to the harness while the model stays fixed, so the harness is improved by a loop and not only by hand [L089].
- Anthropic's guidance is to fold unnecessary subagents back into the main agent loop. A single agent with skills often beats a multi-agent setup [L106].
- LangChain describes the "company harness" as five shared primitives. They come from its internal agents in marketing, sales and engineering. One of them is that the agent lives where people already work, such as Slack [L105].
- Harness evaluation tooling is getting better:
  - Hamel Husain on decision models for evals, including tuning the threshold instead of assuming 0.5 [L090].
  - Cameron Wolfe's roadmap for evals on subjective tasks [L094].
  - Letta's FrontierMemory scores agent memory on downstream tasks, not recall [L091].
- Open-source pieces for your own setup:
  - Browser Use's rl-env-use builds a verified RL environment from a one-line skill description [L092].
  - A workflow DSL that turns agentic loops into more deterministic recipes, used in a self-improving loop [L095].
  - An open-source AI design skill [L104].

## Who disagrees
- Hand-built against loop-built harnesses. LangChain's company harness is designed by people [L105]. Harness² points the other way, with the loop tuning the harness [L089] [L095].
- Simplify against add structure. Anthropic says to remove subagents [L106]. The workflow DSL adds deterministic structure around loops [L095].
- Where the bottleneck is. Kun Chen and Calvin Grunewald say human attention is the bottleneck, so overnight loops are the gain [L100]. The eval posts say you can't trust that output until you can measure it [L090] [L094].

## What to do
- Read harness² and, if you teach it, list it as the "harness improves via hill-climbing" example [L089].
- Audit your subagents. Keep one only if it earns its place over a single agent with skills [L106].
- Use the five company-harness primitives as a checklist for a teaching example [L105].
- Add a threshold-tuned decision-model judge to your eval setup [L090]. Use [L094] for subjective tasks.
- Try rl-env-use for building a skill's environment [L092]. Look at the workflow DSL for turning loops into recipes [L095].
- Borrow the overnight-loop and human-attention workflow, and measure whether it helps you [L100].