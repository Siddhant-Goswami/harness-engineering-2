## What changed
- Claude Code can now be modded [L022]. A mod changes how Claude Code behaves, customizes its UI, or swaps in your own features. You write one in a few lines of TypeScript, or Claude builds it for you. Mods ship inside plugins and install with `/plugin` in the CLI or desktop app. The harness itself is now extensible, and mods can be shared.
- Kun Chen argues that tests an agent writes on its own have not been shown to be worth anything [L033]. He says human guidance can change that, and that his post doesn't mean "write no tests". He also explicitly mentions e2e tests. The fetch cut off there, so the rest of his position on e2e is unread. This bears directly on how you check agent work.

## Who disagrees
- Kun Chen's view [L033] goes against the default habit of letting an agent write its own tests and counting a green run as proof. He keeps tests but wants a human steering them. Many readers took his post as "skip tests", and he is correcting that.

## What to do
- Try one mod [L022]. Pick a behavior you now patch with prompts or config, and see whether a mod does it more cleanly. If it does, think about teaching mods as a way to share harness setups.
- Audit where your own harnesses and course material let agents write and then grade their own tests [L033]. Add a human-guided step or an e2e check there. Read the original post before changing anything, since the fetch was truncated.