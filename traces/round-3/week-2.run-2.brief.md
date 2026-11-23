## What changed
- Claude Code can now be modded: you can change its behavior, customize the UI and add features with a few lines of TypeScript, or have Claude write the mod for you. Mods ship inside plugins and install with `/plugin` [L022].
- Kun Chen argues that tests an agent writes on its own have not been shown to add value. Human guidance can change that, and he says e2e tests are a separate case. This bears on how you check an agent's work [L033].

## Who disagrees
- Kun Chen is pushing back on the common habit of letting agents write their own tests and counting them as verification. He also says some readers took his post to mean "write no tests", and that isn't his claim [L033]. The fetch shows only a short excerpt of the post, so I can't give you the full argument.

## What to do
- Try a mod on your own harness, for example one that changes how Claude Code behaves or shows its checks. Mods ship as plugins, so you could also share them with your students [L022].
- Audit the agent-written tests in your setups. Keep them only where a human has guided what they cover, and don't treat them as proof on their own [L033].