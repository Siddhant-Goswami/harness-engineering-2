## What changed
- Claude Code can now be modded. A mod can change its behavior, customize its UI or add features. You write one in a few lines of TypeScript, or have Claude build it. Mods ship inside plugins and install with `/plugin` in the CLI or desktop app. This is a new extension point for the harness. [L022]
- Kun Chen argues that tests written autonomously by agents don't prove their value. Human guidance can change that, and he calls out e2e tests explicitly. This bears on how you check an agent's work. [L033]

## Who disagrees
- Some readers took [L033] to mean "don't write any tests". Kun Chen says that is not his claim. His claim is narrower: agent-written tests aren't evidence of value unless a human guides them.

## What to do
- Try a small mod in Claude Code and see whether it fits your teaching setup. Start from the plugin route. [L022]
- Don't treat green agent-written tests as verification. Add human-directed tests, especially e2e, to your harness checks. [L033]