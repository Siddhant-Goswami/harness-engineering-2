## What changed
- Agent factories are scaling on verification infrastructure. One builder went from 50 to 1,000 PRs/day after two weeks spent building reusable infra and autonomous verification [L002]. Another shipped 2,500 PRs in a month, and the talk's main lesson is to lock agents down instead of giving them "sharp knife" tools [L003].
- Replit published a harness-design write-up on reaching frontier performance at a fraction of the cost. It argues that per-turn model routers have a basic limit [L016].
- A reference architecture for a production agent: the loop runs on the backend, outside the sandbox. The agent runs commands and controls the filesystem inside the sandbox. It backs up its git-based memory folder to S3 and gets capabilities through skills [L014].

## Who disagrees
- [L016] disputes model routers, whether heuristic or small-model, in favor of a purpose-built harness.
- [L003] prefers tightly constrained agents over powerful, flexible tools.
- [L002] gets its gains from volume. It runs many parallel agents with automated checks and no human review. [L003] gets its gains from constraints on the agent. The scaling posts don't say whether the checks catch problems that a human reviewer would.

## What to do
- Read [L016] and compare its approach with your own model-routing setup.
- Watch [L003], the original talk, rather than the summary. Test whether locking down an agent's tools improves its results in your harness.
- Use [L014] as a template for the loop/sandbox split and for memory persistence when you teach agent architecture.
- Look at how [L002] builds its autonomous verification layer before you raise agent throughput.