## What changed
- Claude Code can now be modded. A mod changes how it behaves, customizes the UI, or swaps in your own features. You write one in a few lines of TypeScript, or have Claude build it. Mods ship inside plugins and install with `/plugin` in the CLI or desktop app. This changes how you build and teach a harness, because behavior can now be packaged and shared as a plugin. [L022]
- Muse Gadgets is an open-source ESP32 firmware and Linux SDK. You point a coding agent at the repo to build your own device. It is useful as a worked example of a repo made to be driven by an agent. [L021]
- Kun Chen restated his point about agent-written tests. Tests written autonomously by agents have not been shown to have value. Human guidance can change that, and he calls out e2e tests explicitly. This bears directly on how you check agent output. [L033]
- `/hairline-create` is a skill for drawing your own hairlines in v0.2 of the hairlines project. It is a small example of shipping a skill with a tool. [L023]

## Who disagrees
- On agent-written tests, Kun Chen says autonomously written tests don't prove their value. Some readers took that as "don't write any tests", and he says that's a misreading. The real split is autonomous tests versus human-guided tests, with e2e as the explicit exception. The source is a clarification, so the original post isn't in this week's links. [L033]

## What to do
- Try a small Claude Code mod and package it as a plugin. Use it as teaching material for customizing a harness. [L022]
- When you teach test-writing in agent loops, separate human-guided tests and e2e tests from tests the agent writes on its own. Don't count the agent's own tests as verification. [L033]
- Skim the Muse Gadgets repo to see how it is set up for a coding agent to build against. [L021]