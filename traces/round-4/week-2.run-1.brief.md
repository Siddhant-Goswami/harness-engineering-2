## What changed
- Claude Code can now be modded. A mod changes how it behaves, customizes the UI or swaps in your own features. You write it in a few lines of TypeScript, or have Claude build it. Mods ship inside plugins and install with `/plugin`. This changes how you can build and run your own harness setup. [L022]
- Kun Chen argues that tests an agent writes on its own have not been shown to add value. He says human guidance can change that, and he calls out e2e tests explicitly. He is clarifying that this is not a "don't write tests" conclusion. The fetch only gave a short excerpt of the post, so the full argument isn't visible. [L033]

## Who disagrees
- Kun Chen and the common habit of letting the agent write its own tests. He says autonomous tests don't prove their worth unless a human guides them. [L033]

## What to do
- Try a small mod on your own Claude Code setup and see whether it's worth teaching. [L022]
- Don't count agent-written tests as verification by themselves. Put human guidance or e2e checks in your harness. [L033]