## What changed
- **Harness design at the frontier [L016].** Replit's Michele Catasta, promoted by Amjad Masad, argues that model routers have a fundamental limit. The piece describes a harness design that reaches frontier performance at a fraction of the cost. The full article is behind the link.
- **Agent harness you can inspect and control [L011].** The quoted article is "Jev + Harness Engineering". It has three builds: a requirements report, diagnostic selection and a bounded repair loop. It reports 28 of 28 correct decisions across two labelled sets. The post that carries it is a design-video pitch, so the original article is what matters. The full article is behind the link.
- **Shipping 2,500 PRs a month [L003].** Matt Pocock summarises a talk by Lauren (@poteto). Her main point is to lock agents down tightly instead of giving them "sharp knife" abstractions, because agents perform much better that way. The talk itself is the original.
- **Scaling to 1,000 PRs a day [L002].** The post says the author built reusable infrastructure and autonomous verification systems in two weeks. That took them from 50 PRs a day to 1,000. The fetch shows only a teaser, so the details aren't visible.
- **Agent architecture [L014].** The post describes how "instinct" is built. The agent loop runs on the backend, outside the sandbox. Commands and file-system control run inside the sandbox. A git memory folder is backed up to S3. Skills are given as a list.

## Who disagrees
- **Locked-down agents against "sharp knife" tools [L003].** Lauren argues for tight constraints. Humans prefer powerful tools that can cut them.
- **Speed against understanding [L001, L002].** Sully dropped vibe coding and now reviews code himself, because he can't use code he doesn't understand after about four days. The scale-up post [L002] bets on autonomous verification and volume instead of human review.
- **Routers against harness design [L016].** The article says a per-turn router can't match a designed harness.

## What to do
- Read the Replit harness article [L016] and the Jev article [L011]. Compare their cost, control and inspection approaches with your own teaching material.
- Watch Lauren's talk [L003]. Test the idea of restricting agent permissions and tools.
- Check what verification the 1,000-PR setup relies on [L002]. Build one autonomous check of your own before you scale up output.
- Compare your sandbox and memory layout with the one in [L014].