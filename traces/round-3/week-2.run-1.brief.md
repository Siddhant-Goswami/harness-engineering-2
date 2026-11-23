## What changed
- Claude Code can now be modded. A mod changes how it behaves, changes its UI, or adds your own features. Mods are a few lines of TypeScript, or Claude writes them for you. They ship inside plugins and install with `/plugin` in the CLI or desktop app. If you teach harness building, this is a new extension point to try. [L022]
- Kun Chen argues that tests an agent writes on its own don't show they have value. Human guidance can change that, and he says e2e tests are a separate case. His post is a clarification: he says some readers took it to mean "don't write any tests." That affects how you check agent work. [L033]

## Who disagrees
- Kun Chen and the readers who took his post as "no tests at all." He says that isn't his claim. His claim is narrower: autonomously written tests aren't proof of value unless a human guides them. [L033]
- Nothing else this week set out a competing view on building, running or checking agents.

## What to do
- Build a small mod, such as a behavior change or a status element, and see what the plugin route offers for teaching or sharing harness setups. [L022]
- Don't count agent-written tests as verification by themselves. Have a human set what gets tested, and keep e2e checks separate. [L033]