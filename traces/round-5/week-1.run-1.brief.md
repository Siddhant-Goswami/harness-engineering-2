## What changed
- Output scales once verification is automated. [L002] went from 50 to 1,000 PRs a day after two weeks spent building reusable infrastructure and autonomous verification systems.
- [L003] passes on a talk about shipping 2,500 PRs a month. Its main point is to lock agents down. Agents do better in tightly constrained setups than with "sharp knife" abstractions.
- [L014] sets out a concrete architecture. The agent loop runs on the backend server, outside the sandbox. The sandbox only executes commands and holds the file system. The git memory folder is backed up to S3, and capabilities are packaged as skills.
- [L016] is a write-up on harness design that reaches frontier performance at a fraction of the cost. It argues that per-turn model routers have a fundamental limit.

## Who disagrees
- [L001] says vibe coding stops working after about four days, so Sully now reviews all code by hand and accepts the slower pace. [L002] takes the other route: automated verification instead of human review. The two disagree on whether a human stays in the loop.
- [L016] disagrees with model routers, which choose a model each turn. It says a designed harness does better.

## What to do
- Read the [L016] article and compare its harness design with your routing or model-selection setup.
- Watch the talk behind [L003] and try its lock-down advice on your agents' permissions and tool surface.
- Use [L014] as a reference layout for separating the loop from the sandbox. It also covers persisting memory and exposing skills.
- Take from [L002] the order of work: build the verification layer before you scale up the number of agents.