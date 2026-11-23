## What changed
- Claude Code can now be modded. A mod changes how Claude Code behaves, what its UI looks like, or adds features of your own. You write one in a few lines of TypeScript, or have Claude build it. Mods ship inside plugins and install with `/plugin` in the CLI or desktop app. [L022]
- Kun Chen argues that tests written autonomously by agents have not been shown to have value. He says human guidance can change that, and he explicitly calls out e2e tests. He is correcting a reading of his earlier post as "don't write any tests". [L033]

## Who disagrees
- Kun Chen's point in [L033] pushes back on the habit of letting an agent write its own tests and then trusting them as the check. He is not against testing. He says the value comes from human guidance and from e2e tests. The fetch of [L033] was cut short, so I can't see the rest of his argument.

## What to do
- Try the mod and plugin route [L022]. Use it to customize your own harness, and consider it as a way to package harness setups for the people you teach.
- Don't count agent-written tests as verification unless a human has shaped them, and prefer e2e checks [L033]. Read the original post for his full argument before you change how you teach this.