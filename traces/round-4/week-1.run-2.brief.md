## What changed
- Output at scale now depends on verification infrastructure. One builder went from 50 to 1,000 PRs/day by spending two weeks on reusable infra and autonomous verification before adding volume [L002].
- Locking agents down works better than giving them powerful "sharp knife" tools. Agents perform much better in tightly constrained environments. This comes from a talk on shipping 2,500 PRs in a month, and the original is worth watching [L003].
- Model routers have a basic limit, because they pick one model per turn. A harness designed around several models can reach frontier performance at a fraction of the cost [L016].
- One architecture to compare with your own: the agent loop runs on the backend server, outside the sandbox. The sandbox only executes commands and holds the file system. A git memory folder is backed up to S3, and capabilities come as skills [L014].
- A worked example of a harness you can inspect and control: a requirements report, diagnostic selection and a bounded repair loop. It has working code and scored 28 of 28 correct decisions on two labelled sets. The post itself is a design demo, so read the linked article, not the video [L011].

## Who disagrees
- Review versus automation: [L001] dropped vibe coding and reviews all code by hand, so they know what the code does. [L002] scales by removing the human from verification and relying on autonomous checks instead.
- Powerful tools versus constrained ones: [L003] says to lock agents down, against the usual preference for flexible, powerful tools.
- Routing versus harness design: [L016] argues that per-turn model routers are the wrong tool. A harness designed around the models does better.

## What to do
- Read the lock-down talk behind [L003] and check how much freedom your teaching harness gives its agents. Tighten it where agents are failing.
- Read the article behind [L016] and compare its design with any model-routing you use.
- Use [L002] and [L011] as references for teaching verification and bounded repair loops. Build the verification layer before scaling agent count.
- Compare the sandbox/backend split and skill layout in [L014] with your own harness.