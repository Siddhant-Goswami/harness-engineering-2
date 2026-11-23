## What changed
- Harness design at the frontier: a harness can reach frontier performance at a fraction of the cost. The post argues this beats model routers, which pick an LLM per turn. Amjad Masad is sharing the original from the Replit team (Michele Catasta), so go to that article. [L016]
- Autonomous verification is what scales output. One builder went from 50 to 1,000 PRs/day in about two weeks, after building reusable infra and autonomous verification systems first. The post gives only the headline, so treat it as a lead. [L002]
- Lauren (@poteto) shipped 2,500 PRs in a month. Matt Pocock's takeaway is to lock agents down tightly instead of giving them "sharp knife" freedom, because agents perform better that way. The original talk is the one to watch. [L003]
- A concrete production agent architecture: the agent loop runs on the backend, outside the sandbox. It drives commands and the filesystem inside the sandbox, backs its git memory folder up to S3, and exposes skills such as agent-mail. [L014]

## Who disagrees
- Sully has gone back to reviewing code himself. In his view, vibe coding produces code you can't use past about four days. [L001]
- That conflicts with the throughput approach, where autonomous verification replaces human review at 1,000+ PRs/day. [L002] [L003]
- On control, the "lock down your agents" advice [L003] is the opposite of the "sharp knife" tooling people usually prefer.

## What to do
- Read the original harness-design article, then compare its cost and quality claims with how you route models in your own harnesses. [L016]
- Watch Lauren's talk and write up the agent lockdown pattern (restricted permissions, narrow tools) for your teaching material. [L003]
- Build verification before scaling agent count, and use it as a lesson on why it comes first. [L002]
- Compare the sandbox/loop split and the S3-backed memory in [L014] with your own harness layout.