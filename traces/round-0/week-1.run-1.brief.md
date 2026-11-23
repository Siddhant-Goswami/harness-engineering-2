## What changed
- Replit's team published a harness design that reaches frontier performance at a fraction of the cost. It argues that model routers, whether heuristic or a small model picking per turn, have a fundamental limit. [L016]
- Two people report shipping at very high PR volume. hraness reports 1,000 PRs/day, up from 50 at the end of August. The change took two weeks of reusable infra and autonomous verification systems. [L002] Lauren (@poteto) reports 2,500 PRs in a month, and her talk says to lock down your agents. Agents do better in tightly constrained setups than with "sharp knife" abstractions. [L003]
- [L014] describes the architecture of the "instinct" agent:
  - The agent loop runs on the backend, outside the sandbox.
  - Commands and file-system control run inside the sandbox.
  - A git memory folder is backed up to S3.
  - The agent gets a set of skills.
- A worked harness-engineering article, "Jev + Harness Engineering", covers a requirements report, diagnostic selection and a bounded repair loop. It reports 28 of 28 correct decisions on two labelled sets. The post that links it is a design demo, so read the article itself. [L011]
- [L015] gives a full prompt for building motion videos in code with gsap and three.js. It is a reusable prompt recipe, though the post around it is hype.

## Who disagrees
- Sully went back from vibe coding to reviewing code himself. Unreviewed code is fun for about four days and hard to use after that. [L001] hraness scales the other way, to 1,000 PRs/day, and trusts autonomous verification over human review. [L002]
- On the model side, Replit argues a single harness designed around the model beats a router. [L016]

## What to do
- Read the Replit harness-design article and compare its argument against any routing you use. [L016]
- Watch Lauren's talk for the "lock down your agents" pattern. Use it as a checklist for your own harness and for teaching. [L003]
- Look at hraness's verification setup before copying the volume. Its two-week infra investment is the part worth reusing. [L002]
- Compare your sandbox and memory design with the instinct layout: loop outside the sandbox, with git memory backed up. [L014]
- Read the Jev article for the bounded repair loop and labelled-set evaluation. [L011]
- Copy the prompt in [L015] if you want a worked example of a role-style prompt for a code-driven build.