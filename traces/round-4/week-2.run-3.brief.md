## What changed
- Claude Code can now be modded. A mod is a few lines of TypeScript, or something Claude builds for you. It can change how the agent behaves, customize the UI, or swap in your own features. Mods ship inside plugins, which you install with /plugin in the CLI or desktop app. This is a new way to shape the harness itself. [L022]
- Kun Chen argues that tests written autonomously by agents have not been shown to add value. He says human guidance can change that, and he calls out e2e tests explicitly. He says this is not "don't write any tests". [L033]

## Who disagrees
- Kun Chen disagrees with the default that "the agent wrote tests, so the work is checked". Agent-written tests alone don't count as verification, and he says human guidance is what makes them useful. [L033]
- Boris Cherny's pitch for mods is that each person works differently, so no one should have to use an identical Claude. That runs against a single shared harness setup for everyone. [L022]

## What to do
- Read the mods announcement and try one. Decide which parts of your teaching harness should be a mod or plugin that students install, and which should stay fixed. [L022]
- Don't count agent-written tests as your check in a harness. Add human-written or human-guided tests, and keep e2e coverage. [L033]