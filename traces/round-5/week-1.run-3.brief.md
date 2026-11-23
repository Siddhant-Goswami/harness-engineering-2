## What changed
- Locking agents down works better than handing them sharp tools. Lauren (@poteto) says this in a talk on shipping 2,500 PRs a month, and Matt Pocock summarizes it. [L003]
- One operator went from 50 to 1,000 PRs a day. They spent two weeks building reusable infrastructure and autonomous verification systems first. [L002]
- Replit's harness design reaches frontier performance at a fraction of the cost. It puts the harness in charge of which model does what, instead of a per-turn router. [L016]
- An agent architecture write-up shows the agent loop running on the backend, outside the sandbox. The sandbox only executes commands and holds the file system, and the git memory folder is backed up to S3. [L014]

## Who disagrees
- Sully has gone back to reviewing code himself, because vibe coding falls apart after about four days. [L001] That conflicts with the scale-out approach, where verification is automated and humans don't read every PR. [L002]
- The model-router approach is the target of the harness-design argument. Its claim is that a router, whether heuristic or a small model, is fundamentally limited. [L016]

## What to do
- Watch Lauren's talk, which is the original behind [L003]. Compare its lockdown advice with how your harness scopes agent permissions.
- Read the harness-design article behind [L016]. Check whether your teaching material treats model selection as part of the harness.
- Borrow the loop-outside-the-sandbox split from [L014] as a reference design.
- Before scaling agent output, build the verification layer first, as [L002] did.