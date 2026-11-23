## What changed
- Claude Code can now be modded. A mod changes how it behaves, customizes its UI, or adds features. You write one in a few lines of TypeScript, or have Claude build it. Mods ship inside plugins and install with `/plugin`. This changes how a harness gets customized and shared. [L022]
- Muse Gadgets is open source ESP32 firmware and a Linux SDK for building hardware that works with Muse. You point a coding agent at the repo to build a device. It's a repo you can hand to your own agent setup, and the device is only the example. [L021]
- Kun Chen argues that tests written autonomously by agents haven't been shown to have value. He says human guidance can change that, and that he called out e2e tests explicitly. He is correcting people who read it as "don't write any tests". The linked thread's full text isn't in the saved link. [L033]

## Who disagrees
- Kun Chen says agent-written tests don't prove their value. The usual harness practice treats an agent's own tests as its check. He draws the line at human-guided tests and e2e tests. [L033]
- Nothing else this week conflicts with it.

## What to do
- Read the ClaudeDevs mods announcement and try a small mod in your own harness. It's also material for teaching. [L022]
- Skim the Muse Gadgets repo as an example of a repo built to be driven by a coding agent. Skip it if you don't build hardware. [L021]
- Find Kun Chen's original post and review how your harness verifies work. Don't rely on agent-written tests alone. Add human-guided or e2e checks. [L033]