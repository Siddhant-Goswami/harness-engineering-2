## What changed
- Agent output is now measured in PRs per day, and the people reporting it say the gain comes from verification and infrastructure. hraness went from 50 to 1,000 PRs/day. They spent two weeks building reusable infra and autonomous verification before scaling up [L002].
- Matt Pocock's notes on Lauren's talk about shipping 2,500 PRs in a month make one point to act on. Agents do better in tightly locked-down environments than with "sharp knife" abstractions [L003]. The talk itself is the original.
- Replit's Michele Catasta argues that a model router has a built-in limit, because it picks a model per turn. The alternative is a harness designed to reach frontier performance at a fraction of the cost [L016].
- Richard published the architecture of the agent "instinct". The agent loop runs on the backend server, outside the sandbox. The sandbox only executes commands and holds the file system. The git memory folder is backed up to S3, and capabilities are packaged as skills [L014].
- The "Jev + Harness Engineering" article describes three builds: a requirements report, diagnostic selection and a bounded repair loop. It reports 28 correct decisions out of 28 across two labelled sets [L011]. The post that carries it is an Opus design-video demo, so read the article and skip the video.

## Who disagrees
- **Output speed against review:** Sully dropped vibe coding after about four days and now reviews code himself, which costs a little time [L001]. hraness and Lauren push volume instead [L002] [L003]. Both sides lean on verification. The difference is whether a human or an automated system does it.
- **Router against harness:** routers pick a model per turn, and the Replit piece says that is the wrong place to put the intelligence [L016].

## What to do
- Read Lauren's talk, starting from Matt's notes, and take the "lock down your agents" idea into your harness teaching [L003].
- Write down hraness's order of work for your course: build verification first, then scale [L002].
- Compare your own harness against the instinct layout. Keep the loop outside the sandbox, put memory in git, and use skills for capabilities [L014].
- Read the Replit article before you add any model routing [L016].
- Check the Jev article's bounded repair loop and its labelled evaluation sets against how you check agents [L011].