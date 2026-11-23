## What changed
- Claude Code now supports mods. They change how it behaves, customize the UI, or add your own features. You write them in a few lines of TypeScript, or have Claude build them. They ship inside plugins and install with `/plugin` [L022].
- Muse Gadgets is an open-source ESP32 firmware and Linux SDK. You point a coding agent at the repo to build hardware devices that work with Muse [L021]. This is a repo for your own agent setup, so the hardware it targets doesn't matter.
- Kun Chen argues that tests written autonomously by agents have not been shown to have value. Human guidance can change that, and he calls out e2e tests explicitly. He says the post is not "don't write tests" [L033].

## Who disagrees
- The common assumption is that an agent can write its own tests and that this proves its work. Kun Chen disagrees. In his view the value comes from human guidance, not from the agent testing itself [L033].
- This is the only real disagreement in the week. His post is only partly visible in the saved text, so read the original before you cite it.

## What to do
- Try a mod in Claude Code. If you teach harness customization, work out how mods differ from hooks and skills [L022].
- Check your agent-written tests. Add human-written or human-guided checks, especially e2e, and don't count the agent's own tests as proof [L033].
- Skim the Muse Gadgets repo if you want a worked example of handing an agent an SDK to build against [L021].