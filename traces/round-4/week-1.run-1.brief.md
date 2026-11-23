## What changed
- Agent output is now measured in hundreds or thousands of PRs a day, and the people doing it say the work was in the infrastructure around the agents. One operator went from 50 to 1,000 PRs/day. They spent two weeks building reusable infra and autonomous verification, not changing the model. [L002]
- Lauren (@poteto) shipped 2,500 PRs in a month. Matt Pocock's takeaway is to lock agents down. Agents perform better in tightly constrained environments than behind "sharp knife" abstractions. [L003]
- Replit published its harness design for reaching frontier performance at a fraction of the cost. It argues that per-turn model routers are fundamentally limited. [L016]
- A concrete production architecture: the agent loop runs on the backend, outside the sandbox. Commands and file system work happen inside the sandbox. The git memory folder is backed up to S3, and capabilities are packaged as skills. [L014]
- A worked example of an inspectable, controllable agent: a requirements report, diagnostic selection and a bounded repair loop. It has working code and reports 28 of 28 decisions correct on two labelled sets. The link is a video post, so I only saw the article's title and teaser. [L011]

## Who disagrees
- Sully says vibe coding stops being usable after about four days. He now reviews the code himself and accepts the slower pace. That cuts against the volume-first approach in [L002]. Neither post says how much of that volume gets human review. [L001]

## What to do
- Study the verification layer from [L002] and the lockdown principle from [L003]. They are the most transferable parts for teaching and building harnesses.
- Read the harness-design article in [L016] before deciding how to route between models.
- Compare [L014] with your own sandbox and memory layout.
- Use [L011] as a teaching example of a bounded repair loop.