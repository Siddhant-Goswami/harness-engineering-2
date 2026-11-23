## What changed
- Google Research's harness² applies hill-climbing to the harness while the model stays fixed. Sydney Runkle points out that this is the same thing as continual learning. [L089]
- Miguel Ríos Berríos is open-sourcing parts of their harness. The latest piece is a workflow DSL that turns agentic loops into more deterministic recipes inside a self-improving loop. [L095]
- Harrison Chase lists five components of a "company harness", the shared multiplayer agent LangChain built for its marketing, sales and engineering teams. One of the components is that it lives where people already work. [L105]
- Theo wrote a long explainer of what a harness is, and it is meant to be the one reference. [L098]
- Eval practice:
  - Hamel Husain covers using decision models as judges, including tuning the threshold instead of assuming 0.5. [L090]
  - Cameron Wolfe gives a roadmap for evals on highly subjective tasks, with ways to cut noise. [L094]
  - Letta's FrontierMemory scores agent memory by downstream task performance, because recall benchmarks are saturated. [L091]
- Browser Use open-sourced rl-env-use. You describe a skill in one line and it builds a verified environment from real cases for hill-climbing. [L092]
- Elaya open-sourced an AI design skill for Claude and Cursor. [L104]

## Who disagrees
- Kun Chen agrees with Calvin Grunewald that human attention is the main bottleneck. Calvin says CI/CD, planning and PRs only look like bottlenecks because they consume attention. Kun's own gains came from overnight loops and similar changes. [L100]
- L089 and L095 both treat the harness as something the agent loop improves itself. L105 describes a human-built, shared company harness. The posts don't engage with each other, so the tension is mine to point out.

## What to do
- Read Theo's explainer [L098] and Chase's five components [L105] for how you frame harnesses when you teach them.
- Pick one hill-climbing loop to try: harness² [L089] for the idea, Ríos Berríos's workflow DSL [L095] for working code. Check it with an eval you trust.
- Use the eval material to tune your judge thresholds [L090] and to handle subjective tasks [L094]. If you test agent memory, score it with FrontierMemory [L091].
- Try rl-env-use [L092] to generate verified environments for your agents.
- Look at the design skill's repo [L104] as an example of how to package a skill.
- Try overnight loops, and design them so they need less of your attention [L100].