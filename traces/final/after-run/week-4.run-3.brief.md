## What changed
- Harness optimization is becoming a loop run on a fixed model. Google Research's harness² describes techniques for recursive self-improvement of the harness itself, which the author notes is also called hill climbing or continual learning [L089]. Another team is open-sourcing its workflow DSL, which turns agentic loops into deterministic recipes inside a self-improving loop [L095].
- Anthropic's own guidance now says to fold unnecessary subagents back into the main agent loop. A single agent with skills often beats a multi-agent setup. The post that surfaced it is hype, so read Anthropic's article behind it [L106].
- LangChain published a recipe for a "company harness". Its five parts are:
  - Lives in Slack.
  - Acts on behalf of the asking user, or under its own identity.
  - Has scoped memory.
  - Runs code in a sandbox.
  - Runs mostly on a schedule [L105].
  
  Tools that act as the user are limited to DMs, and only allowlisted users can use some operations.
- Theo wrote a long explainer of what a harness is, useful for teaching [L098].
- Eval practice:
  - Decision models as LLM judges, with a tuned threshold rather than the default 0.5 [L090].
  - A roadmap for evals on subjective tasks, with noise-reduction tricks [L094].
  - Letta's FrontierMemory, which scores agent memory by downstream task performance instead of recall [L091].
  - Browser Use's open-source rl-env-use, which builds a verified environment from a one-line skill description for hillclimbing [L092].

## Who disagrees
- Single agent versus many. Anthropic says to remove subagents that aren't needed [L106]. LangChain runs three separate purpose-built agents, but they share one recipe [L105]. These don't conflict much: split by identity and permission, not by task.
- Hand-built harness versus self-written harness. The harness² line has the loop improve the harness [L089]. LangChain and Theo describe harnesses designed by people [L105] [L098]. The reader should treat the loop as a tuning step on top of a designed harness.
- What the bottleneck is. Kun Chen, building on Calvin Grunewald's post, says human attention is the real limit. His gains came from overnight loops and cutting how much people have to review [L100]. LangChain's work on identity and scoped permissions points to trust and access as limits too [L105].

## What to do
- Read Anthropic's subagent article and audit your own harnesses for subagents that could become skills [L106].
- Use LangChain's five-part list and its on-behalf-of versus fixed-credential split as a checklist when teaching or building a shared agent [L105].
- Try a small hill-climbing loop on one harness with the model held fixed, and score it with a tuned LLM judge [L089] [L090] [L094].
- Look at the open-sourced workflow DSL for turning loops into recipes [L095]. Try overnight loops and review-minimizing habits [L100].
- Consider rl-env-use and FrontierMemory as ready-made ways to check agents on skills and memory [L092] [L091].
- Use Theo's explainer as course reading [L098].