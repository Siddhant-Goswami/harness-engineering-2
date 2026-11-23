## What changed
- Claude Code can now be modded. A mod changes how it behaves, its UI, or adds your own features. You write it in a few lines of TypeScript or have Claude build it, and it ships inside a plugin installed with /plugin. This is a new way to customize the agent you run. [L022]
- Kun Chen argues that tests written autonomously by agents have not been shown to add value. He says this is not "write no tests". Human guidance can change the result, and he calls out e2e tests explicitly. This bears directly on how you check agent work. [L033]

## Who disagrees
- Kun Chen says some readers took his conclusion as "don't write any tests". He disputes that reading: his claim covers only autonomously agent-written tests, and human-guided tests and e2e tests are outside it. [L033]

## What to do
- Try a Claude Code mod on your own setup, for example to change agent behavior or surface checks in the UI. If you teach harnesses, it is worth a demo. [L022]
- Review any agent-generated tests in your harnesses. Keep the ones a human guided and the e2e ones, and don't count autonomous unit tests as proof the work is checked. [L033]