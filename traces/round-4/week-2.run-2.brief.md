## What changed
- Claude Code can now be modded. A mod changes how it behaves, how its UI looks, or adds your own features. You write one in a few lines of TypeScript, or have Claude build it. Mods ship inside plugins and install with `/plugin`. This is a new extension point for your harness setup. [L022]
- Kun Chen's finding is that tests written autonomously by agents have not been shown to add value. His post says human guidance can change that, and that end-to-end tests are a separate case. Only a short clip of the post was fetched, so I haven't seen his full argument. [L033]

## Who disagrees
- The post that started this, which L033 only clarifies, says agent-written tests don't prove their worth. Readers took that as "don't write tests". Kun Chen rejects that reading. His position is that agent-written tests need human direction, and that end-to-end tests are a separate matter. [L033]

## What to do
- Try a mod on your own Claude Code setup. Start with one that changes agent behavior rather than the UI. Then decide whether it's worth teaching to your students. [L022]
- Review any workflow where an agent writes its own tests and counts passing tests as verification. Add human-written test intent or end-to-end checks instead. [L033]