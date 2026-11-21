#!/usr/bin/env python3
"""Builds the fictional sample month. Everything in it is made up.

The reader runs a support agent on Kiln (their harness), Orchard (their model
provider) and Postgres with Vecstore (their database). Nothing in the harness
says so; the loop has to learn it from the labels.

Every week carries the same five traps, so a rule the loop learns on weeks 1 to 3
can pay off on week 4, and a rule about one link cannot:

  1. Urgent news about a tool the reader does not use (Anvil, Gemstone, Quill DB,
     MySQL). Sounds like an action item. It is noise.
  2. A newsletter recap of a changelog. The changelog counts; the recap is noise.
  3. A dull title that hides a breaking change (an API reference changelog, a
     point release). The reader acted on it.
  4. An X or Hacker thread that carries real measurements. Should have read it.
     Most threads are still noise, so "ignore threads" is the wrong rule.
  5. A big-name post that has nothing to do with the reader (an image model, an
     office opening). Noise, however well known the source.

Two decisions a week, one of them where the loud answer is the wrong one.

    python3 verifier/sample/make_sample.py      # rewrites the sample and verifier/*.csv
"""
import csv
import random
import re
from datetime import date, timedelta
from pathlib import Path

A, S, N = "acted", "should_have", "noise"
HERE = Path(__file__).resolve().parent

W = {}
W[1] = [
# acted
("Kiln changelog", "Kiln 2.4: script mode", A, "Kiln 2.4 adds script mode. The agent can write one script that calls several tools, the script runs in the sandbox, and only its printed output returns to the model. Off by default; turn it on with script_mode: true in the project settings."),
("Kiln changelog", "Kiln 2.4.1", A, "Patch release. Fixes: the status line no longer flickers on resize; long file names wrap in the diff view; the docs link in the help screen is corrected. Changed: the default timeout for hooks drops from 60 seconds to 20. Hooks that run longer are killed and the step fails. Set timeout explicitly in the hook config to keep the old behaviour."),
("Orchard Labs blog", "Pricing update: cached input tokens billed at 10% from 1 November", A, "From 1 November, cached input tokens on all Orchard models are billed at 10% of the input price, down from 25%. Cache lifetime stays at one hour. Prompts with a stable prefix get cheaper."),
("Vecstore security", "Advisory: Vecstore 0.7 can corrupt an index under concurrent writes", A, "Vecstore 0.7.0 and 0.7.1 for Postgres can corrupt a vector index when two writers insert at once. Upgrade to 0.7.2 and rebuild affected indexes. Reproduction steps and the fix commit are linked."),
("Orchard API reference", "API changelog: 14 October", A, "Added: a usage field on streaming responses. Added: two new error codes for overloaded regions. Docs: clearer examples for image input. Changed: tool_choice no longer accepts the value 'any'; send 'required' instead. From 1 November, requests that send 'any' return a 400 error."),
# should have
("Tidewater engineering blog", "We measured script mode on our nightly batch job: 78% fewer tokens", S, "We ran the same 500-ticket job two ways on Kiln 2.4: one tool call per ticket, and one script. Tokens fell 78% and wall time fell by half. The answers matched on 497 of 500 tickets. Repo, raw logs and the three mismatches are published."),
("Preprint", "Raw traces beat summaries for debugging agents (replication code included)", S, "Across 120 failed agent runs, a debugging agent given the full raw trace found the root cause in 71% of cases. Given a summary of the same trace it found 43%. Code and all 120 traces are released."),
("Orchard Labs docs", "Guide: tool descriptions that models follow, with before and after evals", S, "A tool description is read on every call. This guide rewrites six real tool descriptions and reports eval scores before and after each rewrite. The biggest gain came from saying when not to use the tool."),
("X thread", "I timed every hook in 40 Kiln projects. Thread with the data", S, "Across 40 open-source Kiln projects, 1 in 5 hooks takes longer than 20 seconds, mostly test runs and linters on large repos. The spreadsheet with every timing and the script that collected them are linked in the first post."),
# noise
("Anvil changelog", "Anvil 3.0 removes the legacy plugin API on 1 November", N, "Anvil 3.0 drops the legacy plugin API. Plugins written for Anvil 2 stop loading on 1 November. Run anvil plugins migrate to convert them. A migration guide is linked."),
("Gemstone AI blog", "Gemstone Pro input prices cut by 50%", N, "Gemstone Pro input tokens now cost half what they did. Output prices are unchanged. The new price applies to all accounts from today."),
("Quill DB security", "Advisory: upgrade Quill DB to 4.2.1 now", N, "Quill DB 4.2.0 can return results from the wrong collection under heavy load. Upgrade to 4.2.1. Quill Cloud customers are already patched."),
("AI Daily newsletter", "Script mode explained: what Kiln 2.4 means for you", N, "A summary of the Kiln 2.4 changelog entry for script mode, with no new information beyond the changelog."),
("Orchard Labs research", "Our new image model draws hands correctly", N, "Orchard's latest image model gets the number of fingers right in 98% of test images, up from 71%. Samples and the evaluation set are linked."),
("VentureWire", "Lumen AI raises $400M to build the agent OS", N, "Lumen AI closed a $400M round led by two growth funds. The company says it is building an operating system for agents. No product is public yet."),
("X thread", "Harnesses are dead. The model is all you need now", N, "A 14-post thread arguing that newer models make harness work pointless and that script mode is a gimmick. No measurements or links are given."),
("YouTube: PromptBro", "This ONE prompt makes your agent 10x smarter", N, "A 12-minute video about adding 'think step by step like a senior engineer' to a system prompt. No test set is shown."),
("Hacker thread", "Ask: is anyone actually using agents in production?", N, "A 600-comment discussion. Most replies are opinions; a few name their company without details."),
("Fern.js blog", "Fern 9 ships server islands", N, "The Fern JavaScript framework releases version 9 with server islands and a new router."),
("ReasonBench leaderboard", "Orchard 4 retakes first place on ReasonBench by 0.3 points", N, "Orchard 4 moves from second to first on the ReasonBench leaderboard, ahead by 0.3 points. The benchmark's maintainers note the gap is inside the margin of error."),
("Podcast: Next Decade", "AGI by 2028? Three founders debate", N, "A 90-minute conversation about timelines. The three guests give dates of 2028, 2031 and never."),
("X thread", "I replaced my whole team with 12 agents (thread)", N, "A founder describes running a company with 12 agents and no employees. No product, revenue or setup details are shared."),
("AgentConf", "AgentConf 2027 announces its first speakers", N, "The conference names 20 speakers for next March. Tickets go on sale next week."),
("Opinion: The Gradient Post", "Why prompt engineering is still a real career", N, "An essay arguing that prompt writing will remain a job title for the next decade."),
("AI Daily newsletter", "10 AI tools you missed this week", N, "A list of ten new tools: three image generators, two meeting note-takers, a slide maker and four browser extensions."),
]
W[2] = [
("Orchard Labs blog", "Orchard 5 Mini is available: cheaper and faster on the same API", A, "Orchard 5 Mini is live today. Input price is 40% lower than Orchard 4 Mini and median latency is 30% lower. The API is unchanged; switch by changing the model name. Eval tables are included."),
("Orchard status page", "Known issue: Orchard 5 Mini drops parallel tool calls on long contexts", A, "When the context is above 60k tokens, Orchard 5 Mini sometimes returns only the first of several parallel tool calls. Agents that fan out tool calls can silently skip work. A fix is expected within two weeks. Orchard 4 Mini is not affected."),
("Kiln changelog", "Kiln 2.5: permissions file format v2; v1 files stop loading on 1 December", A, "Kiln 2.5 introduces a new permissions file format. Version 1 files load with a warning until 1 December and then stop loading. Run kiln migrate-permissions to convert."),
("Orchard Labs blog", "Deprecation: Orchard 3 endpoints shut down on 15 January", A, "All Orchard 3 model endpoints will return errors from 15 January. Move to Orchard 4 or 5. A table maps each old model name to its replacement."),
("Kiln changelog", "Kiln 2.5.1", A, "Fixes: tab completion for long paths; a crash when the terminal is narrower than 40 columns; the update check respects proxy settings. Changed: kiln run --yes no longer approves deleting files. Deletes now wait for a person unless allow_delete is set in the permissions file. Unattended jobs that delete files will hang."),
("Tidewater engineering blog", "Postmortem: our agent looped for six hours, and the loop breaker we added", S, "A support agent retried the same failing database query 2,100 times overnight. We now stop a run when the same error text appears three times and page a person. The full timeline and the 14-line check are in the post."),
("Orchard Labs research note", "Models trained inside the standard tool loop: hand-rolled loops scored 9 points lower", S, "Orchard models are now trained while running inside the standard tool loop. In our tests, teams that replaced the loop with their own scored 9 points lower on the same tasks. The tasks and the method are published. We recommend customising instructions, tools and rules, not the loop."),
("Preprint", "A separate grader catches twice the errors of self-review (replication pack)", S, "On 400 agent outputs, the model that wrote the output found 31% of its errors when asked to review. A separate grader with a written checklist found 64%. Outputs, checklists and scores are in the replication pack."),
("Hacker thread", "Show: we ran Orchard 5 Mini on 2,000 real support tickets", S, "A small team replayed 2,000 support tickets through Orchard 4 Mini and 5 Mini. Answers matched on 94%. 5 Mini was worse on tickets that needed three or more lookups, and those are the ones it got wrong. The notebook and the anonymised tickets are linked."),
("Anvil security", "Advisory: Anvil plugin sandbox escape, patch now", N, "A plugin in Anvil 3.0 can read files outside its project folder. Anvil 3.0.2 fixes it. All Anvil users should upgrade today."),
("Gemstone status page", "Postmortem: Gemstone Flash was down for four hours", N, "Gemstone Flash returned errors for four hours on Tuesday after a bad configuration push. Gemstone is adding a staged rollout for configuration changes."),
("MySQL release notes", "MySQL 9.1 deprecates the native password plugin", N, "MySQL 9.1 marks the native password authentication plugin as deprecated. It will be removed in 10.0. Move accounts to caching_sha2_password."),
("AI Daily newsletter", "Orchard 5 Mini: everything you need to know", N, "A rewrite of the Orchard 5 Mini launch post with the same tables."),
("Orchard Labs blog", "Orchard at the World Economic Forum", N, "Orchard's CEO spoke on two panels in Davos about AI and jobs. Recordings are linked."),
("X thread", "Orchard 5 Mini CHANGES EVERYTHING. Switch today", N, "A thread urging everyone to move all agents to Orchard 5 Mini immediately. It quotes the launch post and adds no tests."),
("YouTube: BuildLoud", "I rebuilt the agent loop from scratch and you should too", N, "A 40-minute video building a custom agent loop in 200 lines. The author says it gives more control. No comparison against the standard loop is shown."),
("VentureWire", "Orchard Labs in talks at a $90B valuation", N, "Two people familiar with the matter say Orchard Labs is discussing a new round at a $90B valuation."),
("X thread", "Mini models ranked: my vibes-based tier list", N, "A ranking of small models into tiers S to D, based on the author's impressions over one weekend."),
("Hacker thread", "Kiln vs Anvil: which harness is better? (400 comments)", N, "A long argument between users of two coding harnesses. No benchmarks; mostly personal preference."),
("Fern.js blog", "Fern adds AI autocomplete to its dev tools", N, "The Fern JavaScript framework adds an autocomplete panel to its browser dev tools."),
("Opinion: The Gradient Post", "The end of software engineering, again", N, "An essay on whether software jobs will exist in five years. It concludes that nobody knows."),
("Podcast: Next Decade", "The Orchard CEO on the future of work", N, "An hour-long interview about work, education and policy. No product details."),
("X thread", "Leaked: Orchard 6 coming in December?", N, "An anonymous account posts a screenshot said to show Orchard 6 in an internal dashboard. Unconfirmed."),
("AgentConf", "Early-bird tickets for AgentConf end on Friday", N, "The early-bird price ends this Friday."),
("X thread", "Watch an agent book a full holiday, end to end (video)", N, "A screen recording of an agent booking flights and a hotel. The post does not say how many attempts it took."),
]
W[3] = [
("Orchard status page", "Resolved: parallel tool call fix for Orchard 5 Mini is live", A, "The issue where Orchard 5 Mini dropped parallel tool calls on long contexts is fixed in production as of today. No client change is needed. Our regression suite is linked."),
("Kiln changelog", "Kiln 2.5.2: skills can ship scripts; skill folder layout changes", A, "A skill can now include a scripts folder that the agent may run. The skill file moves from skill.md to SKILL.md inside a folder named after the skill. Old layouts load until 2.7."),
("Kiln security", "Advisory: prompt injection through pages returned by the fetch tool", A, "Text on a fetched web page can be read by the model as instructions. Kiln 2.5.2 adds a domain allowlist for the fetch tool. Until you upgrade, restrict fetch to domains you trust."),
("Orchard Labs blog", "Rate limits: batch requests now count separately from live traffic", A, "Batch tier requests no longer use the same rate limit pool as live requests. Nightly batch jobs will not slow daytime traffic. Limits per tier are in the table."),
("Vecstore releases", "Vecstore 0.7.3", A, "Maintenance release. Fixes: faster index builds on tables over 10 million rows; clearer error when the extension is missing; docs typos. Changed: new indexes default to inner product distance instead of cosine. Existing indexes keep their metric. Pass metric: cosine when you create an index if your code assumes cosine."),
("Preprint", "Held-out weeks: a simple test for whether a prompt optimiser learned or memorised (code included)", S, "We optimise prompts on three weeks of labelled data and test on a fourth week the optimiser never sees. In 9 of 22 runs the visible score rose while the held-out score fell. The test costs one extra evaluation. Code is included."),
("Tidewater engineering blog", "Our optimiser raised the score 14 points and made the product worse", S, "We let a loop tune our support agent against a rubric. The score rose 14 points; customer ratings fell. The loop had learned to pad answers with phrases the rubric rewarded. We now keep one week of tickets hidden from it."),
("Orchard Labs docs", "Cookbook: a pre-stop check that makes an agent cite a source for every claim", S, "Before the agent finishes, a plain script checks that every factual sentence carries a link. If one is missing, the agent is sent back once. On our test set unsupported claims fell from 18% to 3%."),
("X thread", "We planted instructions in 30 web pages and let our agent fetch them. Results", S, "11 of 30 planted pages made the agent change its plan; 4 made it try to send data out. The 30 test pages and the script that ran them are linked, so you can run the same test on your own agent."),
("Anvil changelog", "Anvil 3.1: skills support", N, "Anvil 3.1 adds skills: folders of instructions and scripts the agent loads when a task matches. Existing plugins keep working."),
("Gemstone AI blog", "Deprecation: Gemstone v1 API shuts down on 1 February", N, "The Gemstone v1 API will stop accepting requests on 1 February. Move to v2. A mapping table is linked."),
("Quill DB blog", "Quill DB 4.3 adds hybrid search", N, "Quill DB 4.3 combines keyword and vector search in one query. Benchmarks against three other vector databases are included."),
("AI Daily newsletter", "Kiln 2.5.2 in five bullet points", N, "Five bullets restating the Kiln 2.5.2 changelog: skills with scripts, the new folder layout and the fetch allowlist."),
("Orchard Labs blog", "We're opening an office in Singapore", N, "Orchard Labs is opening an office in Singapore with 40 roles across sales and support."),
("X thread", "Evals are a waste of time. Just ship", N, "A thread arguing that test sets slow teams down and that users will tell you what is broken. No data."),
("VentureWire", "Eval startup Gauge raises $60M", N, "Gauge, which sells a dashboard for model evaluation, raised a $60M Series B."),
("YouTube: PromptBro", "Self-improving agents will replace engineers in 2 months", N, "A video predicting that engineers will be replaced by February. No demonstration."),
("ReasonBench leaderboard", "A new benchmark crowns a new winner, again", N, "ReasonBench v2.5 is out and the top three models have swapped places."),
("Fern.js blog", "FernConf recap", N, "Photos and talk summaries from the Fern JavaScript conference."),
("Opinion: The Gradient Post", "Is AI in a bubble?", N, "An essay comparing current AI spending with earlier technology booms."),
("Podcast: Next Decade", "Founders on raising money in 2027", N, "Four founders talk about fundraising."),
("X thread", "95% of engineers at the big labs run self-improving harnesses", N, "A viral post with no source for the number."),
("Prompt Weekly newsletter", "Top 7 prompt templates for managers", N, "Seven templates for meeting agendas and status updates."),
("X thread", "Kiln to be acquired? Sources say talks are on", N, "An unconfirmed rumour that the company behind Kiln is in acquisition talks."),
("X thread", "An agent wrote a whole novel in a weekend", N, "The author shares a 300-page novel written by an agent. Reviews in the replies are mixed."),
]
W[4] = [
("Kiln changelog", "Kiln 2.6 beta: auto-memory (off by default)", A, "Kiln 2.6 beta can write notes to a memory folder at the end of a session and load them at the start of the next. It is off by default. Turn it on per project with auto_memory: true."),
("Kiln issue tracker", "Known issue: auto-memory shares notes across projects in 2.6 beta", A, "In 2.6 beta, notes saved in one project can load in another project on the same machine. A client's details can appear in an unrelated session. Fix planned for 2.6.1. Workaround: leave auto-memory off."),
("Postgres release notes", "Postgres 18.2: fix for a planner regression on partitioned tables", A, "18.2 fixes a regression from 18.0 where queries on partitioned tables could ignore an index and scan every partition. Upgrading needs a restart, no dump and restore."),
("Orchard Labs blog", "Pricing: Orchard 5 Mini output tokens drop 20% on 1 December", A, "From 1 December, output tokens for Orchard 5 Mini cost 20% less. Input prices do not change."),
("Orchard API reference", "API changelog: 11 November", A, "Added: a region field on usage reports. Docs: new examples for streaming tool calls. Fixed: rare duplicate events at the end of a stream. Changed: max_tokens is now required on batch requests. From 1 December, batch requests without it are rejected."),
("Tidewater engineering blog", "Six months of agent memory files: what rotted and how we prune", S, "After six months our agent's memory file had 340 lines; 90 were wrong or out of date and two contradicted each other. We now date every line, and a weekly script flags any line that no run has used in 30 days. Numbers and the script are in the post."),
("Preprint", "Optimisers keep rediscovering three mechanisms: pre-stop checks, loop breakers, persistent memory (survey, code)", S, "We reran 41 published harness-optimisation experiments. Three changes appeared in most winning harnesses: a check before the agent stops, a rule that breaks repeated failures, and memory that persists across runs. Code for all reruns is released."),
("Brightline engineering blog", "We gate agent actions by the cost of undo: our rules and the incident behind them", S, "An agent emailed 4,000 customers a draft. We now sort every action by how hard it is to undo. One-click undo runs on its own; anything that cannot be undone waits for a person. The rule table and the incident timeline are included."),
("X thread", "We cut our agent's memory file from 400 lines to 60. Pass rate went up. Diff inside", S, "A team deleted 340 lines from their agent's memory file and its pass rate on their 200-task suite rose from 71% to 77%. The thread links the before and after files and the test suite."),
("Anvil changelog", "Anvil 3.2 changes its config file format", N, "Anvil 3.2 moves configuration from anvil.toml to anvil.yaml. The old file loads with a warning until 3.4."),
("Gemstone AI blog", "Gemstone Pro 2 launches with a 2M token context", N, "Gemstone Pro 2 reads up to two million tokens in one request. Prices match Gemstone Pro."),
("Quill DB security", "Advisory: Quill DB 4.3.0 backups may be incomplete", N, "Backups taken on Quill DB 4.3.0 can skip collections created in the last hour. Upgrade to 4.3.1 and take a fresh backup."),
("AI Daily newsletter", "Kiln 2.6 beta: first look", N, "A summary of the Kiln 2.6 beta changelog with screenshots. Nothing beyond the changelog."),
("Orchard Labs research", "A model that composes music from a text prompt", N, "Orchard shows a research model that writes short pieces of music from a description. Samples are linked; no release date."),
("Kiln blog", "Photos from the Kiln community meetup", N, "Pictures from last week's meetup. Thanks to everyone who came."),
("Orchard Labs blog", "We're hiring: join the Orchard policy team", N, "Orchard Labs is hiring three people for its policy team."),
("X thread", "Auto-memory is the biggest thing since tool calling. Turn it on NOW", N, "A thread telling everyone to enable Kiln auto-memory on all projects today. It does not mention the beta's open issues."),
("VentureWire", "Kiln's maker raises a Series C", N, "The company behind Kiln raised a Series C. Terms were not disclosed."),
("YouTube: BuildLoud", "I let an agent run my life for 30 days", N, "A vlog about delegating email and calendar to an agent for a month."),
("ReasonBench leaderboard", "ReasonBench v3 results are in", N, "Version 3 of the benchmark is published. The top five models are within one point of each other."),
("Hacker thread", "Is memory just retrieval? (300 comments)", N, "A debate about definitions. No conclusion."),
("Fern.js blog", "Fern 9.1 released", N, "A minor release of the Fern JavaScript framework."),
("Opinion: The Gradient Post", "Why I quit using AI tools", N, "A personal essay by a designer who stopped using AI tools for a month."),
("Podcast: Next Decade", "AGI timelines, revisited", N, "The hosts revisit their predictions from last year."),
("X thread", "Leaked benchmarks for Orchard 6", N, "An anonymous account posts a table of scores said to be from Orchard 6. Unconfirmed."),
]

DECISIONS = [
("2026-10-23", "Should we move the nightly ticket job from one tool call per ticket to a script the agent writes?", "adopt", "Moved it in week one. Tokens fell by about three quarters."),
("2026-10-24", "Should we move our embeddings from Vecstore to Quill DB after the corruption advisory?", "ignore", "Stayed. Upgrading to 0.7.2 fixed it; Quill had its own advisory the same week."),
("2026-10-29", "Should we switch the main support agent to Orchard 5 Mini this week?", "wait", "Waited. The parallel tool call bug would have skipped work. Switched after the fix."),
("2026-10-31", "Should we write our own agent loop to get more control?", "ignore", "Did not. The standard loop is what the models are trained on."),
("2026-11-06", "Should we keep one week of tickets hidden from our prompt-tuning loop?", "adopt", "Should have done it sooner. The loop had been tuning to the rubric."),
("2026-11-07", "Should we let the support agent fetch web pages that customers link to?", "wait", "Waited for the fetch allowlist in 2.5.2. Planted pages changed the agent's plan in tests."),
("2026-11-13", "Should we turn on Kiln auto-memory for client projects now?", "wait", "Waited for 2.6.1. The beta shared notes across projects."),
("2026-11-14", "Should we move the support agent from Kiln to Anvil 3.2?", "ignore", "Stayed on Kiln. Nothing in Anvil 3.2 fixed a problem we had."),
]

START = date(2026, 10, 19)


def main():
    rows = []
    for w in (1, 2, 3, 4):
        items = list(W[w])
        random.Random(100 + w).shuffle(items)
        for pos, (src, title, label, text) in enumerate(items):
            d = START + timedelta(days=(w - 1) * 7 + pos * 7 // len(items))
            slug = re.sub(r"[^a-z0-9]+", "-", (src + " " + title).lower()).strip("-")[:70]
            rows.append([d.isoformat(), src, title, f"https://sample.invalid/{slug}", label, text])

    with open(HERE / "links.csv", "w", newline="") as f:
        out = csv.writer(f)
        out.writerow(["date", "source", "title", "url", "label", "text"])
        out.writerows(rows)
    with open(HERE.parent / "links.csv", "w", newline="") as f:   # the labels, without the page text
        out = csv.writer(f)
        out.writerow(["date", "source", "title", "url", "label"])
        out.writerows(r[:5] for r in rows)
    for path in (HERE / "decisions.csv", HERE.parent / "decisions.csv"):
        with open(path, "w", newline="") as f:
            out = csv.writer(f)
            out.writerow(["date", "question", "outcome", "how_it_turned_out"])
            out.writerows(DECISIONS)
    print(f"{len(rows)} links, {len(DECISIONS)} decisions")


if __name__ == "__main__":
    main()
