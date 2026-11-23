## What changed
- Claude Code can now be modded. Mods change how it behaves, its UI, and add your own features. They are a few lines of TypeScript, or Claude can write them, and they ship inside plugins that you install with `/plugin` [L022]. This is a new extension point for your harness and for what you teach.
- Kun Chen argues that tests an agent writes on its own have not been shown to add value [L033]. He says human guidance can change that, and that e2e tests are a separate case. Only the first thread post is in the saved link, so the full argument is not visible here.

## Who disagrees
- [L033] pushes against the habit of letting an agent write its own tests and counting them as verification. Kun Chen says people misread him as "write no tests". His claim is narrower: autonomous, unguided agent tests don't prove their worth.

## What to do
- Try a small mod through `/plugin` and judge whether it fits your teaching material [L022].
- In your harness, don't treat agent-written tests as a passing check. Add human-guided tests or e2e checks, and read the full post behind [L033] before you change your checking step.