## What changed
- Claude Code can now be modded. A mod can change how it behaves, change its UI, or add features. Mods are a few lines of TypeScript, or Claude can write them. They ship inside plugins and install with `/plugin` in the CLI or desktop app. This changes how you build and run your own harness [L022].
- Muse Gadgets is open-source ESP32 firmware and a Linux SDK. You point a coding agent at the repo to build hardware devices that work with Muse. It's a repo you can hand to your agent, so it counts as setup material [L021].
- Kun Chen argues that tests an agent writes on its own haven't been shown to have value. Human guidance can change that, and he says e2e tests are the exception. He also says the post is not "don't write tests" [L033]. That affects how you check agent output.

## Who disagrees
- Kun Chen's point is that agent-written tests prove nothing unless a human guides them. Many readers took his post to mean "write no tests", and he is correcting that [L033]. The post he's defending isn't in your saved links. If you teach test-first agent loops, this is the claim to check.
- I found no other disagreement among this week's saved links.

## What to do
- Try a Claude Code mod in your harness. Work out which parts of your setup (behavior tweaks, UI, extra features) could ship as a plugin you could share with students [L022].
- Point a coding agent at the Muse Gadgets repo as a test of agent-driven hardware work. This is optional [L021].
- In your agent loops, don't count agent-written tests as verification. Add human-written or human-guided tests, and e2e checks where you can [L033].