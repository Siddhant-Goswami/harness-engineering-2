## What changed

- Matt Pocock summarizes a talk by Lauren (@poteto) on shipping 2,500 PRs a month. His first takeaway is to lock agents down. He says agents perform much better in tightly constrained environments than with "sharp knife" abstractions. Watch the talk for the details [L003].
- Amjad Masad shares Replit's article "Free the models: harness design at the frontier". It argues that a harness can reach frontier performance at a fraction of the cost. The article says per-turn model routers are fundamentally limited [L016].
- @hraness went from 50 to 1,000 PRs a day. They say the jump took two weeks of work on reusable infrastructure and autonomous verification systems, which they decided to build up front [L002].
- @RMladek lays out how the "instinct" agent is built [L014]:
  - The agent loop runs on the backend server, outside the sandbox.
  - Commands and file-system control run inside the sandbox.
  - The git memory folder is backed up to S3.
  - The agent gets skills such as agent-mail and authenticator-codes.

## Who disagrees

- @SullyOmarr has gone back on vibe coding. He says it is fun for about four days, then the code is unusable. He now reviews the code himself and accepts the small time cost [L001].
- @hraness gets scale by building verification systems that run without a human reader [L002].
- Lauren's talk, as Pocock summarizes it, controls agents by constraining them [L003]. This is a third approach.
- Replit's article questions routing each turn to a different model. Its alternative is to design the harness so cheaper models reach frontier results [L016].

## What to do

- Watch Lauren's talk and test the "lock down the agent" idea on your own harness. Constrain what the agent can do before you give it more freedom [L003].
- Read the Replit article, and compare its approach with any per-turn model routing you use [L016].
- Before you scale up agent output, build the autonomous verification layer first, as @hraness did [L002].
- Check your agent architecture against @RMladek's split. The loop runs outside the sandbox, the sandbox only executes, and memory is backed up off the box [L014].
- Review agent-written code yourself, as Sully does, wherever your verification is still weak [L001].