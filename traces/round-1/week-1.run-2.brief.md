## What changed
- Lock down your agents. Matt Pocock's takeaway from Lauren's talk on shipping 2,500 PRs a month is that agents do better in tightly constrained environments than with "sharp knife" tools. The original talk is the one to watch. [L003]
- Harness design can reach frontier performance at a fraction of the cost. The argument is that a per-turn model router is limited, and that the harness itself should be designed for this. Amjad Masad endorses it, and the original is Michele Catasta's article. [L016]
- Autonomous verification is what lets output scale. One builder went from 50 to 1,000 PRs a day after about 2 weeks building reusable infrastructure and autonomous verification. [L002]
- The "instinct" agent has a concrete architecture. The agent loop runs on the backend, outside the sandbox. It runs commands and controls the file system inside the sandbox. Its git-backed memory folder is backed up to S3. It is built from a set of skills. [L014]

## Who disagrees
- Sully went back to reviewing code himself, because vibe-coded output is unusable after about 4 days. [L001]
- [L002] and [L003] argue for scale: many parallel agents and thousands of PRs, with verification and constraints doing the quality work. [L001] argues for a human reading the code. The reader's harness decides who does the checking.

## What to do
- Watch Lauren's talk, linked from [L003]. Compare its constraints on agents with the permissions in your own harness.
- Read the "Free the models" article behind [L016]. Check whether its design lessons belong in what you teach.
- If you run many agents, build the verification layer first, as [L002] describes. Fix the order of the work before you add more agents.
- Use [L014] as a reference layout for separating the agent loop from the sandbox.