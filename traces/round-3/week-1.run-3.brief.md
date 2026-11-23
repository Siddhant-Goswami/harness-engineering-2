## What changed

- **Agents at volume need locked-down setups and automated checking.** Lauren (@poteto) says agents perform much better in tightly restricted environments than with "sharp knife" abstractions. She shipped 2,500 PRs in a month this way [L003]. hraness reports 1,000 PRs/day. It took them two weeks to build reusable infrastructure and autonomous verification systems before scaling [L002]. The detail is in the linked video, which I couldn't see.
- **Harness design can match frontier performance at much lower cost.** Replit's Michele Catasta argues that per-turn model routers have a fundamental limit. The article proposes a harness design that gets frontier results for a fraction of the cost [L016]. The full article is behind the link.
- **Inspectable, controllable agents:** The author's own article, "Jev + Harness Engineering", covers a requirements report, diagnostic selection and a bounded repair loop. It reports 28 of 28 correct decisions on two labelled sets [L011]. The full article is behind the link. The post that surfaced it is a design-demo hype post, so go to the original article.
- **A reference architecture for a deployed agent:** The agent loop runs on the backend, outside the sandbox. It runs commands and file operations inside the sandbox. A git memory folder is backed up to S3, and the agent gets a set of skills [L014].

## Who disagrees

- **Review versus volume:** Sully dropped vibe coding and now reviews code himself, because unreviewed code isn't usable after a few days [L001]. hraness and Lauren push for very high PR throughput. Both camps lean on verification: Sully relies on a human, while hraness relies on automated checks [L002, L003].
- **Routing versus harness design:** Catasta argues that model routers are fundamentally limited and that harness design is the better lever [L016].

## What to do

- Watch Lauren's talk and pull out her lock-down-the-agent practices for your teaching material [L003].
- Read the Replit harness article and compare its design with your own model-selection logic [L016].
- Read the Jev article and check whether its bounded repair loop and inspection approach fit your harnesses [L011].
- Compare your own agent sandbox and memory setup against the architecture in [L014].
- Treat autonomous verification as the prerequisite before scaling agent output [L002].