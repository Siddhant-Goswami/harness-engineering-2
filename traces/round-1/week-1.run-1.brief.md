## What changed
- Replit's write-up on harness design says a well-built harness can reach frontier performance at a fraction of the cost. It argues this beats model routers, which pick a model per turn. [L016]
- Reports from people running agents at scale describe the same pattern. hraness went from 50 to 1,000 PRs/day after two weeks building reusable infrastructure and autonomous verification. [L002] Lauren (poteto) shipped 2,500 PRs in a month. Matt Pocock's takeaway from her talk is to lock agents down, because agents do better with tight constraints than with "sharp knife" tools. [L003]
- Instinct's architecture is a reference design. The agent loop runs on the backend, outside the sandbox. The sandbox executes commands and holds the file system. A git memory folder is backed up to S3, and capabilities are packaged as skills. [L014]

## Who disagrees
- Sully has gone back on vibe coding. He now reviews code himself, because unreviewed code is unusable after a few days. [L001] That conflicts with the high-volume, autonomous approach. [L002]
- Replit argues against model routers, which are the common way to cut cost. [L016]

## What to do
- Read the Replit harness-design article and compare its approach with any model routing you teach. [L016]
- Watch poteto's talk and test the lock-down idea: restrict agent tools and permissions, then compare results. [L003]
- When you build verification, follow hraness's order: build the autonomous verification and reusable infrastructure first, then scale up. [L002]
- Use Instinct's loop-outside-sandbox split as a template for runtime design. [L014]