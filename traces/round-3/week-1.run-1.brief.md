## What changed

- **Remote agent loops, local sandboxes.** [L014] shows how "instinct" is built. The agent loop runs on a backend server, outside the sandbox. Commands and file-system control happen inside the sandbox. A git memory folder is backed up to S3, and capabilities are packaged as skills such as agent-mail and authenticator-codes.
- **Harness design instead of model routers.** [L016] is Replit's "Free the models: harness design at the frontier". It argues that per-turn model routers have a basic limit. It also sets out how to reach frontier performance at a fraction of the cost by designing the harness. The full article is behind the link.
- **Verification as the base for scaling output.** [L002] reports going from 50 to 1,000 PRs a day. The author spent two weeks building reusable infrastructure and autonomous verification systems first, and ran many agents in parallel.
- **Lock down your agents.** [L003] is Matt Pocock's summary of a talk on shipping 2,500 PRs a month. Its first point is that agents do better in tightly constrained setups than with "sharp knife" abstractions.
- **An inspectable, controllable agent.** [L011] is mostly a design-demo post. Its attached article, "Jev + Harness Engineering", is the author's own piece. It covers three builds: a requirements report, diagnostic selection and a bounded repair loop. It reports 28 of 28 decisions correct across two labelled sets. The full article is behind the link.

## Who disagrees

- **Autonomy versus human review.** [L001] says vibe coding stops working after a few days. The author now reviews the code personally and accepts the small time cost. [L002] and [L003] take the opposite approach: they scale output through autonomous verification and constrained agents, with little human review per PR.
- **Routing versus harness design.** [L016] argues that model routers are inherently limited and that the harness should do that work.

## What to do

- Read [L016] in full. Check how your harness chooses models and splits work across them, and compare that with a router approach.
- Take the verification-first order from [L002]. Build the autonomous checks before you add more parallel agents.
- Apply the constraint advice from [L003] to your harnesses. Restrict the agent's tools and actions, and compare the results.
- Use [L014] as a reference for sandbox and loop separation, and for keeping agent memory outside the sandbox.
- Read the Jev article in [L011] for a bounded repair loop with labelled evaluation sets. It could serve as a teaching example.