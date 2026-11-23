## What changed
- Agents now ship at factory scale. One builder went from 50 to 1,000 PRs/day by spending two weeks on reusable infrastructure and autonomous verification before adding agents [L002]. Another shipped 2,500 PRs in a month. Their main lesson is to lock agents down tightly, not give them "sharp knife" freedom [L003].
- A harness can match frontier performance at a fraction of the cost. The Replit write-up argues that a per-turn model router is limited, and it proposes harness design as the alternative [L016].
- [L014] describes a production agent layout. The agent loop runs on the backend, outside the sandbox. The sandbox runs commands and holds the file system. A git memory folder is backed up to S3. Capabilities come as skills, such as agent-mail.
- [L011] points to an article on building an inspectable, controllable agent. It has a requirements report, diagnostic selection and a bounded repair loop, and it reports 28 correct decisions out of 28 on two labelled sets. The post itself is a design demo. The original article is the part that matters.

## Who disagrees
- [L001] says vibe coding stops working after a few days. They review code themselves now, which is slower but leaves them understanding it.
- [L002] and [L003] go the other way and scale output with autonomous verification. The disagreement is over human review versus automated checks. The scale posts give no evidence about code quality.
- [L003] disagrees with giving agents freedom. It argues for tight constraints.

## What to do
- Watch the talk behind [L003] first. Its main point is to lock down agent permissions, and it's a concrete harness design choice.
- Read the harness article behind [L016]. Compare its cost-versus-quality approach to your own routing and model choices.
- Read the inspectable-agent article behind [L011]. A bounded repair loop with labelled checks is something you can copy for teaching.
- Use [L014] as a reference layout for the loop, sandbox, memory and skills split.
- Look at [L002] for how to build verification before scaling agent count. Take its method and ignore the token and PR totals.
- Try the prompt recipe in [L015], a role-based prompt for building motion video in code with GSAP and three.js. It's a recipe you can reuse, though the post around it is hype.