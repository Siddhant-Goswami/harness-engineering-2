## What changed

- **Models may absorb the harness.** A new paper argues the model can pick its own harness once it sees the task [L051]. Levie calls this the eventual architecture of agents. It's early research, not something to build on yet.
- **Debugging code nobody reads.** Sridharan proposes a root-cause framework for AI-written code that the human doesn't understand. Her tactics only worked after she changed approach, on a real bug in about 9K lines of AI-generated code [L037].
- **Verification should be separate from the work.** Nadella's essay says models are now insider risks. As models and harnesses commoditize, intent, verification and evidence will limit how fast agents spread. Systems must separate who does the work from who checks it [L039].
- **Structured context has measured gains.** Harvey ran context-graph experiments on Legal Agent Bench to see how structured context affects online agent quality and efficiency [L064].
- **A model that reasons about its own training data.** Apollo reports that GLM-5.3 sometimes reasons, unprompted, about how its current actions could become training data [L063]. If that holds up, it affects how you evaluate and trust agent transcripts.
- **A small specialist model for incident investigation.** Datadog's Scout is trained on simulations and claims frontier-level investigation quality at a fraction of the cost [L072].

## Who disagrees

- **Levie says to expect a model that builds its own harness [L051]. Nadella says the checking layer must stay external and separate from the worker [L039].** Even if the model chooses its harness, the verification boundary stays outside it. Apollo's finding adds weight to Nadella's side [L063].
- **Sridharan says you can debug without understanding the code [L037]. Tobias says raw tools aren't enough and you still need a senior dev who knows how to use them [L059].** Her framework is the test case: does it work without that expertise?

## What to do

- **Try the subagent performance-audit recipe on one of your sites.** It has four subagents check 20 speed problems, then fix them in one pass. Tobias reported a real improvement [L059]. The recipe is a good template to teach, and the same pattern works for any audit.
- **Read Sridharan's debugging framework.** Use it as a checklist for agent-written code [L037].
- **Review how verification is separated from work in your harnesses.** Use Nadella's framing as the test [L039].
- **Try the REA skill for giving an agent a disassembler.** Use the repo itself [L070], not the hyped repost of it.
- **Skim the Harvey context-graph results** if you teach context design [L064].