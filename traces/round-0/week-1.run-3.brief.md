## What changed
- Routers that pick a model per turn are being replaced by harness design that reaches frontier performance at a fraction of the cost. The original is Michele Catasta's "Free the models" article. [L016]
- Throughput is now set by verification infrastructure. One builder went from 50 to 1,000 PRs/day after two weeks building reusable infra and autonomous verification. [L002]
- Agents work better in tightly locked-down environments than with "sharp knife" tools. This comes from poteto's talk on shipping 2,500 PRs in a month, as summarized by Matt Pocock. [L003]
- One reference architecture for a production agent: the loop runs on the backend, outside the sandbox. The sandbox only runs commands and holds the file system. A git memory folder is backed up to S3, and capabilities are packaged as skills. [L014]
- The "Jev + Harness Engineering" article covers an inspectable, controllable agent with a bounded repair loop. It reports 28 of 28 correct decisions on two labelled sets. The post that links it is mostly a demo. [L011]

## Who disagrees
- Scale versus review. [L002] and [L003] push toward autonomous, high-volume PR output gated by automated verification. [L001] has gone back to reviewing code personally, because vibe-coded output isn't usable after a few days. The two views disagree on whether review is done by a human or by a system you build.
- Routing versus harness. [L016] argues a harness beats a model router. Per-turn routing is the common approach it argues against.

## What to do
- Read the original article behind [L016] and compare its harness design with your course material. Do not use the repost.
- Watch poteto's talk via [L003]. Note the lock-down-your-agents point for teaching: restrict tools and permissions before adding capability.
- Check what verification your harness has before you scale up agent runs. Autonomous verification is the stated enabler in [L002].
- Use [L014] as a worked example for sandbox, loop and memory separation.
- Read the bounded-repair-loop article behind [L011]. It is a candidate teaching example.