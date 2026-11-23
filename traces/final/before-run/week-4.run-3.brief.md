## What changed
- Harness work is moving from hand-written to self-improving. Google Research's harness² describes hill-climbing on the harness while the model stays fixed [L089]. Another team is open-sourcing a workflow DSL that turns agentic loops into more deterministic recipes inside a self-improving loop [L095].
- Two first-party write-ups define what a harness is and how to build one for a team. Theo's explainer covers the basics [L098]. LangChain's post gives five components of a shared "company harness" [L105].
- Eval tooling got more concrete. Hamel Husain covers choosing a decision model for LLM-judge evals and tuning its threshold [L090]. Cameron Wolfe has a roadmap for evals on subjective tasks [L094]. Letta's FrontierMemory scores agent memory on downstream tasks, because recall benchmarks are saturated [L091].
- Browser Use open-sourced rl-env-use, which builds a verified RL environment from a one-line skill description [L092].
- An open-source AI design skill for Claude Code and Cursor can be installed into your own setup [L104].
- One builder says the biggest productivity gains came from overnight loops and cutting the human attention each task needs [L100].

## Who disagrees
- Hand-built against self-written harnesses. LangChain and Theo treat the harness as something people design [L098] [L105]. Harness² points the other way, with the loop tuning the harness itself [L089]. The DSL work sits between the two: humans fix the recipe, and the loop improves it [L095].
- Memory is judged two ways. Letta says recall benchmarks are saturated and scores memory on downstream task performance [L091]. I haven't read past.dev's pitch, which claims #1 on BEAM, a recall-style benchmark [L082].

## What to do
- Read harness² [L089] and the LangChain post [L105]. Check whether the "loop rewrites the harness" idea fits your course material.
- Add a threshold-tuned decision-model judge to your eval examples [L090], and use the subjective-eval roadmap for tasks with no clean answer [L094].
- Try rl-env-use [L092] and the design skill [L104] as sample material for teaching.
- Try overnight loops, and track how much human attention each task still needs [L100].