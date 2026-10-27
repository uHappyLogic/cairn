# Milestone 51: Benchmark design finalization

## Goal

Finalize `ideas/benchmark_for_cairn.md` so the benchmark design is ready to be implemented in its own repository: every one of the eighteen gaps in `ideas/benchmark_design_gaps.md`, the design-gaps report of 2026-10-26 committed beside the draft, ends as a decision written into the draft, adopted, adapted, or rejected with the reason stated in the text, and any further gap found on the way is resolved the same way. A gap whose fix is empirical, such as the rater's calibration set or the hidden-requirement pilot, is resolved by the draft stating the procedure and its acceptance rule, not by running it. Where the honest resolution lands in Cairn itself rather than in the draft, for example the usage documentation's model table and review loop or a skill's precondition, Cairn's docs and skills are changed in this milestone, with the hosts rebuilt and both test runs kept green as for any runtime change. Implementing or running the benchmark, and releasing Cairn, stay out of scope.

## Relevant starting state

### The benchmark draft

`ideas/benchmark_for_cairn.md` is a 572-line design document and nothing more: no benchmark repository, harness, seed, operator, or rater exists yet, here or elsewhere, and no `evals/` directory has ever been committed to this repository. It grew through eleven commits between 2026-10-22 and 2026-10-26 (`60fab12` to `8d93140`), each a revision in the open, and its sections run from the general idea through the raw prompt, hidden requirements, the operator and its three layers, the scenarios (four deliveries, the model strategies and the `models_strategy_1` table), the two phases, the scoring axes and the rater, cost reporting, repository layout and isolation with the one-run procedure and the manifest, the README page with its ranking table and radar, how Cairn development uses the benchmark, the project requirements, and the Closest Wins project with its seed README, two prompts, left-open lists, implied-requirement lists, and one hidden requirement per prompt. Its examples name Cairn `1.8.3` and a host binary version `2.1.283`, while this repository's `VERSION` reads `1.9.0`. It says `docs/design-claims.md` "states that only one is tested"; that document now says the suite runs two of its tests (claim 11, and the first part of claim 2).

### The design-gaps report

`ideas/benchmark_design_gaps.md` (282 lines, dated 2026-10-26, committed in `aeb280a` on 2026-10-27) lists eighteen numbered gaps, each with a Where, a Why it matters, and a Fix; gaps 14 to 18 share one "Smaller points" section, and a closing "Recommended order" names 1 to 4 first, then 5, 6, and 10, then 7, 11, and 12. Every `Where:` is a line number into the draft at `8d93140`, so each edit of the draft shifts the references that follow it. Every Fix is a proposal, not a decision, and several land outside the draft: in Cairn's usage documentation (gap 9), in the plugin's fixed status lines as the signal a harness would match (gap 5), and in the maintainer's execution environment (gap 4, which cites the maintainer's note that Docker Desktop blocks these runs on the development machine).

### Cairn's usage documentation

`docs/ways-of-using-cairn.md` is the "usage snippets" the draft's `models_strategy_1` says it was written from. Its chains name model families through Claude Code's aliases (`opus`, `fable`), never an exact model id, and assign `opus` at `high` to the bootstrap, define, goto, and finish lines, `fable` at `high` to the starting-state, review, recommend, answer, sweep, and derive lines, `opus` at `high` to the alternatives line, and `opus` at `xhigh` to `complete-all-tasks`. It also carries three loops a fixed message list cannot express: "Running a mixed-agent requirements review" is repeated until the review pass reports convergence, "Putting more intelligence into a stuck milestone" raises the review line to `opus` at `max` for one more pass, and "Executing tasks" re-runs `complete-all-tasks` after the account's usage window resets, because every task commits on its own. The page states no `--milestone` flag by design, and `docs/skill-reference.md` spells `answer-open-question-with-alternative <question_name>. <alternative id>`, the form the draft's planned turn outputs.

### What a chain skill prints when it stops

No skill sets a process exit code: a precondition stop is a printed message, after which the headless process ends as it does on success, so the final message is the only signal of what a skill did. On success each chain skill prints one fixed identifier-free line: `Workflow bootstrapped.`, `Milestone defined.`, `Milestone activated.`, `Starting state recorded.`, `Requirements reviewed.` (followed by the still-open Short Titles and a convergence verdict read from the tool's `list`), `Alternatives embedded.`, `Recommendations embedded.` or `Questions reordered.`, `Recommendations recorded.`, `Tasks derived.`, `All tasks completed.`, `Milestone finished.`, and `Answer recorded.` for the single-question answer skills. A no-op run prints a distinct one-line message whose wording is fixed only for the bootstrap (`Workflow already bootstrapped — nothing changed.`); elsewhere the files give an example. Stops are prose: `goto-next-milestone` on a pointer not reading `none` or no undone milestone, `derive-tasks` with `Cannot derive tasks: the following open questions must be resolved first:` and the titles, `recommend-all-open-questions` naming the blocks still lacking alternatives, the sweep's `dirty before start` and `stopped at` stops, `complete-all-tasks` on an empty task list or on a `FAILED` agent (it stops the loop and never retries), and `finish-current-milestone` only when `TASKS_TODO.md` holds a `##` section, so an empty task list finishes a milestone that derived nothing. A usage limit or an API error reaches a skill as a failed call, which no skill tells apart from any other failure, and no skill carries a time or turn limit of its own.

### The milestone-definition tool and the goal text

`define-milestone-goal` chooses a title from the description it is given and passes the description unchanged to `core/tools/define_milestone.py` on stdin through a quoted heredoc; the tool writes it under `## Goal` exactly as received, trimmed of outer whitespace, derives the directory slug from the title's first five words, numbers the milestone max-plus-one, and creates the four files. A define line carrying a whole prompt text would therefore be recorded verbatim, within the one quoting rule the usage documentation states for a `<goal>` inside `claude -p "…"`, no double quote, which neither of the draft's two prompts contains. Nothing in Cairn rewrites a recorded goal except `modify-milestone-goal`.

### The plugin as a loadable input

The Claude Code tree at `hosts/claude/` is a complete plugin root, `.claude-plugin/plugin.json` at version `1.9.0` beside `skills/`, `agents/`, `shared/`, and `tools/`, built from `core/` and installed in practice through the `uHappyLogic/cairn-claude` marketplace; the Antigravity copy loads from the global `~/.gemini/config/plugins/cairn`. The two agents, `complete-task` and `provide-alternatives-to-open-question`, declare no tool restriction in their frontmatter, so they run with every tool the host grants, web tools included; the plugin ships no settings, hooks, or MCP configuration, and nothing in it reads or restricts the user-level configuration it runs beside. Cairn has no tooling for isolating, sandboxing, or timing out a run.

### Changing Cairn in this milestone

A change under `core/` is followed by `uv run scripts/build_hosts.py`, a commit of the rebuilt `hosts/` trees with it, `uv run scripts/build_hosts.py --check`, and both pytest runs (the pinned interpreter and the 3.9 floor), as `CONTRIBUTING.md` describes under `## Development`; a change under `docs/` alone needs no rebuild. Runtime files carry no editor-facing prose and name no host, skill frontmatter stays one clause of 25 words or fewer, and host-dependent wording goes through named slots under `scripts/hosts/<host>/slots/`. `CLAUDE.md` records the invariants a change must preserve, among them that each skill's success-path console output is one fixed identifier-free status line.

## Decisions

### Web tool access

Web search and fetch stay enabled in every scenario invocation; the harness restricts neither the tools nor the network. After each run the harness reads the session's tool calls, its web search queries, its fetched URLs, and its shell commands that reach the network, and records them in the run's unpublished record. A run whose calls reached the benchmark repository, its run branches, or its Pages site is marked contaminated, and the draft states whether such a run is excluded from its comparison set or re-run.

### Infrastructure failure policy

The harness classifies how each invocation ends, and on the first infrastructure failure (a usage limit, an API overload, or a network error) it stops the chain and voids the run: the run is recorded with its outputs and a void marker naming the failure's cause and the invocation it hit, it is excluded from rating and scoring, it is never a phase-2 parent, and a fresh run of the same scenario, from the same parent for phase 2, is drawn in its place. Nothing is retried. A void is reported plainly so its cause can be addressed: the harness prints a distinct void line at the stop naming the cause and the invocation, the voided run's tokens stay in its own record and enter no scenario total, and the README reports beside each scenario's runs column how many of its runs were voided and why, while the voided artifacts stay off the published pages.

### Left-open implied overlap

An item that appears both in a prompt's deliberately-left-open list and in its implied-requirement list is split wherever a choice among ways remains: the implied line scores only that some way through exists, and the choice among ways stays an unscored left-open item. An item with no such choice left goes to exactly one list by a test the draft states: implied when a quiz lacking it would be called broken or unfinished by any builder, left open when lacking it is a defensible product choice, with the verdict recorded per item. The draft states both rules, and neither list is thinned by a blanket rule.

### Bearing-question test

Each hidden-requirement entry gains a one-line bearing scope beside its statement, versioned with the entry, naming the decision or decisions a question must ask about to receive the disclosure: for prompt 1 the topic or theme of the questions, for prompt 2 where a prepared set is stored or how it is carried to another computer. The harness inserts the scope with the statement into the operator's hidden knowledge, and the operator discloses the statement only when a question asks about something in the scope; a catch-all or an off-scope question gets nothing beyond what PROJECT.md says. The same scope governs the planned turn's "bears on" lines, so every disclosure is checkable against written text rather than the operator's private reading.

### Reply need classification

The reply-or-no-reply classification of a final message is made by a distinct model call with no tools and a fixed model and effort pair, defined and versioned with the operator definition and recorded in the manifest. It reads only the final message, never the prompt or the hidden knowledge, under one stated rule: a message that asks, confirms, or offers a choice gets a reply; one that reports completion, a stop, or an error, or closes with an offer, gets none. It outputs the verdict and a one-clause reason, and only a reply verdict invokes the operator. Every verdict and reason goes into the invocation's record file; a no-reply verdict is not an operator turn and adds no attentive session; the classifier's tokens are recorded beside the operator's, apart from the totals.

### Host configuration isolation

The harness creates a fresh host configuration directory for each run from a committed template and points every invocation of that run, replies and planned-turn answer invocations included, at it through CLAUDE_CONFIG_DIR; the directory holds no plugins, MCP servers, or hooks, so only the plugin passed by --plugin-dir loads, and no other run's transcripts or memory are inside it. The template is a shared input in the inputs area, versioned by content and recorded in the manifest in place of the user_config digests, so changing it starts a new comparison set under the existing rule. Credentials are injected per run from outside the template, as an API key in the environment or a copied login, and the directory is deleted with the clone after the Run: commit.

### Fixed stop line wording

Cairn fixes the wording of every skill's no-op and stop lines in this milestone. Every skill gets a fixed, unique, identifier-free first line for each distinct no-op and precondition-stop condition, with variable detail allowed after it, as one plugin-wide convention extending the existing fixed-success-line invariant. The lines are listed in docs/skill-reference.md, the CLAUDE.md terse-reporting invariant is extended to cover them, and a pytest test checks each listed line verbatim against the rendered skill files and checks that every line is unique, so the lines are a contract a harness can match across versions.

### Finish with no tasks

finish-current-milestone stops, writing and committing nothing, when the milestone's open_questions.xml still holds any question block, read through the open-question tool's list or the skill's own read of the file, whatever TASKS_DONE.md holds. It adds no check on completed tasks and no override flag: a decision-only milestone that answered everything still closes, and a milestone abandoned with open questions is closed by answering them. This targets the one failure path, a derivation refused on standing questions.

### Repeat rating agreement

One randomly chosen run of every scenario, for each prompt, is re-rated blind under the same rater version, so the sample grows with the roster at one repeat per scenario per prompt; scores use the first rating only. The per-line verdict agreement and the per-axis score difference are reported in one line beside the README ranking table, and the lost column carries a noise floor beside the mean lost count: the expected number of lines lost by rater disagreement alone, computed from the rate at which a line passing in one rating of an artifact fails in the other. No threshold is applied; a low agreement is published as it is.

### Checklist line test specs

Every test line gets a short specification written now into the draft's project section beside the line: prompt 1's six stated and thirteen implied lines, prompt 2's stated line and eleven implied lines, and prompt 2's carry-between-profiles hidden line. The specification names the case the test must drive the artifact into and the observable outcome it must assert, stated as an outcome rather than a means so the "any way through counts" rule still holds; for the award line, award a point, take it back, and assert the score is back to its earlier value, with a confirmation that prevents the award counting as well. The specification becomes part of the checklist, which stays derived from the draft and nothing else, and the line keeps its id.

### Not-proved scoring

A not-proved verdict does not stand on the rater's first report: the harness gives that line one more attempt by a fresh rater session under the same rater definition, and only a second not-proved scores zero, like an absent line. The line still counts in the fixed denominator, a line the second attempt proves passes, and the not-proved count beside each axis counts only verdicts that survived the re-attempt. The pass-or-fail line and the fixed denominator are kept, at the cost of a second rater session only on lines that failed to prove.

### Rater artifact scope

The harness hands the rater the entry file plus every file in the run's tree reachable from it by load or by link (src and href attributes, script and style imports, and fetch targets that name a file present in the tree), followed transitively, and nothing else of the tree. A linked editor page and its assets therefore reach the rater, while every file the artifact never points at, process files included, stays out, so the scope is defined by the artifact itself and blindness needs no exclusion list.

## Out of Scope

