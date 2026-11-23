## What changed
- Agent output at scale now depends on infrastructure around the agent. One builder went from 50 to 1,000 PRs/day after spending two weeks on reusable infra and autonomous verification systems [L002]. Another shipped 2,500 PRs in a month, and the talk's main lesson is to lock agents down, because agents do better in constrained environments than with "sharp knife" abstractions [L003].
- Harness design can replace model routing. A per-turn router is limited by its design. The Replit write-up argues a purpose-built harness can reach frontier performance at a fraction of the cost [L016].
- A concrete production architecture is public. The agent loop runs on the backend, outside the sandbox. It runs commands and file operations inside the sandbox. A git memory folder is backed up to S3, and capabilities are exposed as skills [L014].
- The "Jev + Harness Engineering" article describes an inspectable, controllable agent with a bounded repair loop and 28/28 correct decisions on labelled sets. The post that points to it is a video-demo pitch, so the article is the source to read [L011].

## Who disagrees
- Sizing the work: [L002] and [L003] push for maximum autonomous throughput. [L001] went back to reviewing code by hand, because unreviewed vibe-coded output stopped being usable after about four days. Both camps agree you need some verification. They differ on whether it is automated or human.
- Where intelligence sits: [L016] puts it in a custom harness. Routers put it in model selection.

## What to do
- Read the Replit harness article for cost and quality trade-offs, and use it as teaching material [L016].
- Watch the "2,500 PRs" talk and try its constrained-agent idea on your own harness [L003].
- Copy the loop-outside-sandbox, memory-in-git and skills layout as a reference design [L014].
- Read the Jev article for the bounded repair loop and labelled-set checks, and skip the video demo that links to it [L011].
- Before scaling agent count, build autonomous verification first [L002].