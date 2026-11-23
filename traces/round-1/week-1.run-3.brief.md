## What changed
- Harness design is the main change this week. Replit's "Free the models" article argues that a harness can reach frontier performance at a fraction of the cost. It says model routers are limited because they pick a model per turn. Read the original by the people who built it. [L016]
- Autonomous verification is what let one builder go from 50 to 1,000 PRs a day. The builder spent two weeks on reusable infrastructure and verification before scaling. [L002]
- Lock down your agents. Matt Pocock's summary of a talk on shipping 2,500 PRs a month says agents perform better under tight constraints than with "sharp knife" tools. The talk itself is the original source. [L003]
- A reference architecture for a deployed agent: the loop runs on the backend, outside the sandbox. The sandbox runs commands and holds the file system. A git memory folder is backed up to S3, and capabilities are packaged as skills. [L014]

## Who disagrees
- Sully has gone back from vibe coding to thorough human code review. He says unreviewed code is unusable after about four days. [L001]
- hraness pushes the opposite way, toward massive throughput with autonomous checks in place of human review. [L002] Both agree the check has to be designed deliberately. They disagree on whether a human does it.
- Lock-down versus flexibility: [L003] wants constrained agents, while [L016] wants a harness that routes freely across models.

## What to do
- Read the Replit harness article in full. Compare its per-turn routing argument with how you teach model choice. [L016]
- Watch the Lauren (poteto) talk. Pull out the constraint and lock-down rules to use as a lesson or a harness checklist item. [L003]
- Write down your own verification layer before you scale agent output. Use [L002] as the model. Decide where a human reviews and where an automated check does, in light of [L001].
- Compare [L014]'s architecture (loop outside the sandbox, skills, memory backup) with your teaching harness.