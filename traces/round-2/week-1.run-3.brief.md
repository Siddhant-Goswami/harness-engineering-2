## What changed
- Agents are being run at very high volume with automated checks. One builder went from 50 to 1,000 PRs a day in two weeks by building reusable infrastructure and autonomous verification first [L002]. The source for the 2,500-PRs-a-month talk is the original by poteto. Matt Pocock's takeaway is to lock agents down, because they perform better with tight limits than with "sharp knife" tools [L003].
- Replit's "Free the models" article argues that a per-turn model router is limited. It describes a harness design that reaches frontier performance at a fraction of the cost [L016].
- [L014] shows a concrete architecture:
  - The agent loop runs on the backend, outside the sandbox.
  - Commands and file-system control happen inside the sandbox.
  - The agent's git-based memory folder is backed up to S3.
  - Capabilities are exposed as skills.

## Who disagrees
- [L001] rejects heavy vibe coding. The author says it is fun for about four days, then the code is unusable, so they now review it themselves. [L002] and [L003] go the other way and scale output through automated verification and restricted agents. The disagreement is about where the check happens: a human reading the code, or a verification system.
- [L016] disagrees with model routers, which pick an LLM per turn. It prefers a designed harness.

## What to do
- Read poteto's talk behind [L003]. Test its "lock down your agents" advice on one of your harnesses, and see what it says about verification.
- Read the "Free the models" article behind [L016]. Compare its harness design with any router-based setup you use or teach.
- Use [L014] as a reference layout for agent loop, sandbox and memory separation.
- Before scaling agent output, build the verification layer first, as in [L002].