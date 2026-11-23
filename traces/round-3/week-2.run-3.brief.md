## What changed
- Claude Code can now be modded. You can change its behavior, customize its UI or swap in your own features. Mods are a few lines of TypeScript, or Claude can write them for you. They ship inside plugins and install with `/plugin` in the CLI or desktop app. This is a new extension point for the harness you build and teach. [L022]
- Kun Chen argues that tests agents write on their own have not been shown to add value. Human guidance can change that, and he says end-to-end tests are a separate case. The fetch only returned a clarification of his earlier post, so I have not seen the original argument. [L033]

## Who disagrees
- Kun Chen says some readers took his post to mean "don't write any tests". He says it doesn't. His claim is narrower: autonomously written tests don't prove their worth, and human direction changes that. [L033]

## What to do
- Read the mods announcement and try one on your own setup. Check whether a mod can enforce or check agent behavior the way you currently do by hand. [L022]
- Audit any agent-written tests in your harness. Keep the ones a human guided, and the end-to-end ones. Don't count the rest as verification. [L033]