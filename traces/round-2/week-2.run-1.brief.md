## What changed
- Claude Code can now be modded. A mod changes how it behaves, its UI, or adds your own features. You write one in a few lines of TypeScript, or have Claude build it. Mods ship inside plugins and install with `/plugin` in the CLI or desktop app. [L022]
- Kun Chen argues that tests an agent writes on its own have not been shown to add value. He says human guidance can change that, and that this doesn't mean "write no tests". [L033]

## Who disagrees
- Some readers took [L033] to mean "don't write any tests". Kun Chen says that's a misreading. His claim is only about tests written autonomously by agents, not tests in general. The snippet I could fetch cuts off mid-point about e2e tests, so I haven't seen his full position on them.

## What to do
- Read the mods announcement and try one mod in your own harness setup. This matters most if you teach agent customization. [L022]
- Review any step in your harness where an agent writes its own tests and treats a pass as proof. Add human guidance to those tests, or a check that doesn't depend on them. [L033]