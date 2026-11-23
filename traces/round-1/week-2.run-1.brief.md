## What changed
- Claude Code now supports mods. They change how it behaves, its UI, and its features. You write one in a few lines of TypeScript, or Claude builds it for you. Mods ship inside plugins and install with `/plugin`. This changes how you can set up and teach a harness. [L022]
- Kun Chen's finding is that tests an agent writes on its own haven't been shown to have value. Human guidance can change that, and he says e2e tests are the exception. He is not saying to skip tests. This bears on how you check an agent's work. [L033]
- Muse Gadgets is an open-source ESP32 firmware and Linux SDK. You point a coding agent at its repo to build devices. It's a ready-made repo for an agent-driven build. [L021]
- hairlines v0.2 ships a `/hairline-create` skill, so you can draw your own. It's a skill you could reuse. [L023]

## Who disagrees
- Kun Chen is pushing back on a common habit of letting agents write their own tests. He says autonomous agent-written tests prove nothing unless a human steers them. Readers who took his post to mean "write no tests" got it wrong. [L033]
- The saved posts have no other real disagreement.

## What to do
- Try a Claude Code mod and look at the plugin packaging. It's worth showing in your teaching. [L022]
- Audit any agent-written tests in your harnesses. Keep the ones a human guided, and keep e2e. [L033]
- Skim the Muse Gadgets repo as an example of a repo written for coding agents. [L021]
- Open the `/hairline-create` skill as an example of skill structure. [L023]