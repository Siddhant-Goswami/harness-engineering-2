## What changed
- Debugging when you no longer read the code now has a method. Sridharan's framework finds root cause without relying on anyone knowing the code. It comes from a real bug in about 9K lines of AI-generated code, where her usual tactics failed. [L037]
- Nadella's "Models as Insider Risks" piece, as Chamath frames it, argues that verification and evidence will gate adoption. It says to separate the agent doing the work from the party that checks it. [L039]
- A subagent recipe for pre-ship checks: Opus 5.5 sends out 4 subagents to check 20 performance problems, then fixes them in one pass. Tobias reports it improved a site's performance. [L059]
- Harvey ran experiments on Legal Agent Bench to measure how structured context (context graphs) improves online agent quality and efficiency. [L064]
- REA is a skill and repo that gives an agent a real disassembler, and every claim it makes comes back with a binary address. It is a general check-your-claims tool, not only a way to reverse engineer a home gadget. [L070]
- Holmes sketches a closed-loop software factory. In it, agents decide what to fix, which costs to optimize and which features to build. He says it isn't there yet. [L061]

## Who disagrees
- Whether the harness lasts. The paper Levie cites ("the model swallows the harness") says models will choose their own harness once they see the task. [L051] Chamath's framing points the other way: models and harnesses commoditize, and the human-designed layers of intent, verification and separation of duties are what matter. [L039]
- Whether tooling is enough. Tobias says raw tools aren't enough and you still need a senior dev to get good software. [L059] Holmes's factory vision has agents deciding what to build with little human input. [L061]

## What to do
- Add a debugging recipe to your agent teaching material, built on Sridharan's approach for code nobody reads. [L037]
- Make the worker and the verifier separate agents with separate evidence, as in the "insider risk" argument. [L039]
- Try the 4-subagent pre-ship audit as a template for a parallel checking pattern. [L059]
- Read Harvey's context-graph experiments before deciding how to structure agent context. [L064]
- Install the REA skill and see how its address-backed claims could serve as a model for evidence-carrying agent output. [L070]
- Read the paper behind [L051] before you invest more in a hand-built harness. It is the strongest challenge to your premise this week.