## What changed
- Harness definition: [L098] Theo's article says a harness is the tools, the call syntax, the parser that runs them, the loop that returns results to the model, and the tool list. It also says Claude Code and Codex bake a harness into their apps. Good harnesses let you bring your own tools.
- Company harness recipe: [L105] LangChain's five components for internal agents:
  - They live in Slack.
  - They have an identity model, either on-behalf-of or fixed credentials, set per tool.
  - They keep memory scoped globally or per user.
  - Code runs in a sandbox that can make authenticated requests.
  - Many runs are scheduled instead of invoked by a person.
- Harness self-improvement: [L089] Google Research's harness² hill-climbs the harness while the model stays fixed.
- Deterministic recipes: [L095] A team open-sourcing its harness turns agentic loops into deterministic workflow-DSL recipes inside a self-improving loop.
- Agent architecture: [L106] Anthropic's "When to fold subagents into your main agent loop" says a single agent with skills often beats a multi-agent setup. I saw this only through a hype repost. Read the original article, not the post.
- Evals:
  - [L090] Hamel Husain's guide to using decision models as LLM judges. It covers choosing the model, tuning the threshold instead of assuming 0.5, and reading the scores.
  - [L094] Cameron Wolfe's roadmap for evals on subjective tasks, with ways to reduce noise.
  - [L091] Letta's FrontierMemory scores agent memory on downstream task performance. Recall benchmarks are saturated.
- Hill-climbing tooling: [L092] Browser Use's open-source rl-env-use builds a verified environment from a one-line skill description.

## Who disagrees
- Subagents: [L106] says to fold them into one agent with skills. [L105] runs several specialised agents, and [L095] adds structure through routing and recipes.
- Who writes the harness: [L089] automates tuning it with a loop. [L105] and [L098] treat it as something you design by hand.
- Where the gain comes from: [L100] says minimizing human attention, with overnight loops, is the main unlock. [L105] puts the work into identity, permissions and UX around the agents.

## What to do
- Read the Anthropic subagent article behind [L106] and test one multi-agent setup of yours against a single agent with skills.
- Use [L098] as the shared definition when you teach harnesses.
- Map your own harness against the five components in [L105]. Identity and scheduled runs are the ones people most often miss.
- Try the hill-climbing loop in [L089] on one harness, with rl-env-use [L092] as the environment source.
- Apply [L090] and [L094] to your judge setup: tune the threshold, and add noise controls for subjective checks.
- Use [L091] if you evaluate agent memory.