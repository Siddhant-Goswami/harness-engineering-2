## What changed
- Cindy Sridharan proposes a debugging framework for agents that doesn't depend on the human understanding the code. Her test case was a real bug in about 9K lines of fully AI-generated code, where her usual tactics failed to find the root cause. [L037]
- New research (arXiv 2609.35738) suggests a model can pick its own harness once it sees the task, instead of having one fixed in advance. Levie calls this the likely end-state architecture of agents. I only saw the tweet, not the paper. [L051]
- Harvey ran experiments on Legal Agent Bench to test whether structured "context graphs" improve online agent quality and efficiency. [L064]
- Meng To points to the REA skill/repo, which gives an agent a disassembler so it can reverse-engineer a device or app. He used it to build a Mac app around a home device. [L070]
- Chamath relays Satya's point that as models and harnesses commoditize, intent, verification and evidence will gate adoption. Systems need to separate who does the work from who checks it. [L039]

## Who disagrees
- **Harness vs model:** Levie welcomes models choosing their own harness [L051]. Domingos's quoted reaction, "the model swallows the harness", reads as a warning that hand-built harness work gets absorbed. Satya, via Chamath, says the opposite: verification and evidence stay outside the model and gate adoption [L039].
- **Tools vs people:** Martin Tobias says raw tools aren't enough. He argues you still need a strong senior dev to get good software out of them, and he credits a subagent performance-audit prompt for speeding up his site [L059]. Sridharan's work goes the other way: she shows how to debug when no human reads the code [L037].

## What to do
- Read Sridharan's post and test its debugging approach on a failing agent-written codebase. It gives you a checking method to teach. [L037]
- Read the arXiv paper before you treat harness design as durable. If it holds up, plan which parts of your harness are worth keeping fixed. [L051]
- Look at Harvey's context-graph setup and decide whether structured context is worth testing in your own agents. [L064]
- Try the REA skill as an example of a skill that gives an agent a concrete tool. It's useful teaching material. [L070]
- Copy the 4-subagent pre-ship audit prompt pattern, from the Voxyz post quoted in the tweet, as a subagent recipe. [L059]
- Keep the doer/verifier separation in mind when you design checks. [L039]