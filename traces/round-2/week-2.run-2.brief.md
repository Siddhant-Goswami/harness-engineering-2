## What changed
- Claude Code now supports mods. You can change how it behaves, customize the UI, or swap in your own features. A mod is a few lines of TypeScript, or Claude can write it for you. Mods ship inside plugins and install with `/plugin` in the CLI or desktop app. [L022]
- Kun Chen argues that tests an agent writes on its own have not been shown to add value. He says human guidance can change that, and he calls out e2e tests explicitly. [L033]

## Who disagrees
- Some readers took Kun Chen's post to mean "don't write any tests". He says it doesn't. His claim is narrower: autonomously written tests prove nothing by themselves. [L033]

## What to do
- Read Kun Chen's full post, not just the clarification, and check how much your harness trusts agent-written tests. Where tests gate a run, add human-written or human-reviewed tests, especially e2e. [L033]
- Try a mod to adjust Claude Code's behavior in your own setup, and consider it as teaching material for harness customization. [L022]