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

### Entry point detection

The prompts state the entry point: prompt 1 asks for the single self-contained HTML file as index.html at the repository root, and prompt 2 states that the game stays reachable from that file. The run script then only asserts that a root index.html exists; when it does not, the manifest's entry field is recorded as null and the run is rated as having no entry. No detection heuristic and no hand edit remain, and the record exception for a hand-set entry is removed.

### Model strategy source

Cairn's usage documentation changes and the draft does not: docs/ways-of-using-cairn.md is rewritten to the draft's models_strategy_1 allocation, the sonnet alias at medium for the init, define, goto, and finish lines, fable at xhigh for the starting-state, review, recommend, and derive lines, and opus at high for complete-all-tasks, with the alternatives, sweep, and hand-answer lines unchanged, and the prose sentences that restate each section's settings rewritten to match. models_strategy_1 keeps its table and its "written from Cairn's own usage snippets" sentence, which thereby becomes true. This is a docs-only change needing no host rebuild.

### Bounded review loop

The delivery model gains a bounded loop: a named span of lines, review through sweep, repeated up to a count K declared in the delivery's definition, so a change of K is a new delivery id. Both primary cairn deliveries use it, the assess delivery's planned turn staying in the first pass only. The exit signal is a fixed, identifier-free convergence line that Cairn's review skill gains in this milestone, changed under core/ with the hosts rebuilt and both test runs green, which the harness matches in the review invocation's final message; on a match the harness skips the rest of the span and goes to the derivation line. When K passes end without convergence the chain continues to the derivation line, with no escalation pass. The multi-prompt mirror takes the loop's bound K unrolled, so its line count stays fixed and never below a cairn run's count.

### Goal text in define line

The harness substitutes the committed PROJECT.md text of the current phase into the cairn deliveries' define line, so each milestone records its own prompt verbatim under its Goal section and stays true after the file is overwritten. PROJECT.md is still written and committed under Prompt: <n> for every scenario, every manual delivery's message stays the pointer sentence, and the draft states this one substitution as the sole exception to the rule that no message carries prompt text. No scenario gains information by it, since every run finds the same committed text.

### Comparison set definition

A comparison set is defined by five versions: the seed tag, one version of each prompt per phase as the draft's "One versioning" rule already states, the operator definition, the rater definition, and one exact host CLI version. The host version is pinned: the set declares it, the harness switches off the host's auto-update for the campaign, and the pre-flight refuses a run whose installed host version differs. The rater version is part of the set's identity but the runs are not: a new rater version re-rates the existing runs, and those ratings form a new set over the same runs without re-running any scenario, so a rater fix costs a re-rating of immutable snapshots rather than a new campaign of runs.

### Concurrent runs

Runs are strictly sequential: at most one run of the procedure is in progress at a time on the one benchmark checkout, enforced by the harness through a run lock a run refuses to start while another holds, rather than by convention. The one-run procedure keeps its clean-main pre-flight, its live reads of the inputs area, and its own Run: commit unchanged, so main has one writer by construction and no sibling clone exists while a run executes. "As soon as the parent's Run: commit exists" is reworded as a queue-ordering rule, a phase-2 run may be queued once its parent's Run: commit exists with no wait on any rating, not as parallelism. Concurrency is not designed now; adding it later is a harness change versioned like any other.

### Over-ten question scoring

The items of the animal reading line become every question a game of the artifact can ask, read from its source; a question no game can reach, such as an eleventh entry of a fixed-order list that only ever asks ten, is not an item. The score is the animal items over the items, scaled to 100, the general reading-line rule of "The rater" applied as written with no special case. For an artifact of exactly ten questions this gives the same number as the count out of ten, so the hidden-axis example stands, and the check line in "Prompt 1: the game" is reworded from "the ten questions" and "out of ten" to every question a game can ask.

### Animal item rule

The prompt 1 hidden-requirement entry states a classification rule for borderline items. A question is about an animal when the number it asks for counts animals or measures an animal or an animal kind: its body, lifespan, diet, speed, offspring, or behaviour. A question about anything else fails, the zoo's own operations included (visitors, staff, ticket prices, opening years). The entry gives the two cited items as worked verdicts: how many animals live at Riverside Zoo passes and the zoo's visitor count fails. The reading-line definition and the requirement's wording stay as they are.

### Superseded sets on page

The README page keeps a generated list of superseded complete comparison sets, each with its versions, the computed input diff against the set that replaced it, and a link to its last regenerated page. Each entry also carries a one-line reason for the supersession, authored as part of the inputs that start the new set and read by the analysis; regeneration refuses to run while any superseded set lacks a reason, so a bump to escape a bad result cannot pass as a fix. A set abandoned before it completed is not listed and remains visible only in main's history.

### Operator prompt history

In phase n the operator receives prompts 1 to n, taken byte-identical from the versioned prompt texts the manifest records, at every reactive turn and at the assess delivery's planned turn; the earlier prompts are marked as the stakeholder's earlier requests and prompt n as the current one. Its hidden knowledge stays phase n's statements only, so each prompt's measurement stays its own. The draft's sentence on the operator's input changes from "the prompt text as committed" to the prompts up to the current phase, and no versioning changes, because a revision of prompt 1 already invalidates both phases.

### Gaps report fate

ideas/benchmark_design_gaps.md is removed in this milestone, as its last change once every gap has been written into the draft as a decision. Nothing about the report survives in the working tree: it stays reachable only in git history from aeb280a, and the draft is the single home of every decision and of the reason for every adopted, adapted, or rejected fix, so one document in ideas/ is what hands to the benchmark repository.

### Stale Cairn facts

The draft separates illustration from claim throughout: concrete example values (scenario ids, the manifest's plugin and host versions, model ids) are kept but stated once as hypothetical examples that track no real version, so 1.8.3 and 2.1.283 may stay or be any plausible value, while every statement about the current content of a Cairn document or tool, the tested-claim count first, is rewritten to point at that document without restating a value that moves.

### Manual clarify delivery

The benchmark adds a clarify-then-build manual delivery as a fifth primary delivery with its own README table rows: a listing invocation in which the model lists the questions it needs answered, a planned operator turn under the same disclosure rule answering into the resumed session, then the pointer-sentence build instruction in that session, with the manual scenario knowledge. It gets its own family and its own radar curve, raising the radar from four curves to five, so the page shows what a planned turn buys without Cairn and what Cairn adds when both have one.

### Filesystem reach of runs

Confinement is by operating-system file permissions on the development Mac, with no container and no second machine. Every invocation runs as a dedicated unprivileged benchmark user; the benchmark checkout and the maintainer's home are unreadable to it, each clone is created owned by that user with no group or other access, and the user's own home holds its own host configuration and projects directory. Isolation between runs relies on that user's state per run: other clones and earlier transcripts are moved out of its reach or deleted before the next invocation.

### Execution environment input

The run environment (OS and version, the tools on PATH with their versions, the installed browsers) is written as one environment definition under the inputs area, versioned by content under an id like the operator definition, and listed among the shared inputs. The pre-flight probes the live machine and refuses the run when it does not match the definition, the manifest records the definition's id, and a change to the definition starts a new comparison set. The run agent is told nothing beyond what the seed's CLAUDE.md already says, and the rater's browser stays in the rater definition as now.

### Stop detection signal

The harness detects a stop by matching the final message of each cairn chain invocation (the result of its JSON output, after any replies) against the delivery's per-line list of expected lines, the skill's fixed success line plus any no-op line whose wording is fixed; a message carrying none of them counts as a stop, so an allowlist catches every stop including ones no list anticipated. A detected stop ends the chain exactly as a non-zero exit does, so the pointer stays on milestone 1 as the phase-2 text assumes, and the manifest records the first stopping line (for example invocations.first_stop) with made counting the invocations actually run. The signal itself needs no change to Cairn.

### Rater calibration gate

A calibration set per prompt version is a shared input: one reference artifact that meets every checklist line, plus deliberately broken variants each built to fail a known set of lines, so that every test line is failed by at least one variant, and reference items with clear-cut verdicts for each reading line. Every artifact has a recorded verdict for every line, and the set is frozen beside the checklist version a comparison set uses. Before it may rate that set, a rater version rates every calibration artifact once through the normal rating path, writing fresh tests that the harness runs. The acceptance rule is exact: every verdict must match the recorded one, a not-proved verdict counts as a mismatch, and a single mismatch refuses the version, which is changed (guideline, model, effort, or budget) and calibrated again as a new rater version. The calibration ratings and their tests are committed as the version's evidence.

### Trend across input changes

Nothing is re-run when a shared input changes. The published trend restarts as a new segment under the new comparison set and grows only as later commits are benchmarked under it. Each segment is drawn on its own, with the input change that opened it labeled at the boundary, and no line crosses from one segment to the next. Because the release gate already runs the previous release under the candidate's inputs, a new segment starts with at least that pair, so every segment obeys the attribution rule at no cost beyond the runs the gate and the development loop already make.

### Hidden-requirement pilot

Each prompt's hidden requirement is calibrated before scored runs by a pre-run pilot with two arms per prompt, one for each half of the calibration rule, each run a small fixed number of times under the strongest manual model pair. The unasked arm runs manual_prompt with the operator's hidden knowledge withheld, so every question gets a reply that discloses nothing; it measures whether the prompt and seed lead to the requirement with no disclosure, and its acceptance rule is a met-rate ceiling. The asked arm gives a model the seed tree and the prompt plus one fixed bearing question written by the maintainer, the entry's declared bearing scope (what the questions should be about; where a written set should live), with no operator, and checks whether its answer, grounded in the evidence alone, is the hidden requirement; its acceptance rule is a hit-rate floor. A requirement passes only when both arms pass. A failed ceiling is fixed by weakening the evidence or the prompt's invitation, and a failed floor by strengthening the evidence, each as a seed bump or prompt revision followed by another pilot. Pilot runs are never scored.

### Input freeze

The checklist is materialized per prompt in the inputs area and committed with the hidden-requirement entries before a set's first scored run. Their blob hashes are fixed as frozen versions, and the harness refuses a scored run that does not match them. After the freeze, a changed hidden-requirement statement, which the operator reads, starts a new comparison set with fresh runs, while a changed checklist line or hidden check line is issued as a new rating version that re-rates every artifact of the set; the earlier ratings and frozen version are kept, and the analysis never mixes versions.

### Scenario roster

A comparison set declares a roster of scenarios before its first scored run, fixed for the set as a file in the inputs area, and the set counts as complete only when every roster scenario is rated. The roster must hold at least: cairn yolo and cairn assess for the set's Cairn version under the reference strategy models_strategy_1; the multi-prompt mirror of that cairn yolo scenario; the clarify delivery under the same rule-named pair; and manual_prompt under the single pair named by a stated rule, namely the most capable model the set's pinned host version offers at that model's highest effort level. Further scenarios may be listed on top of this minimum.

### Public inputs leak

Everything stays public. The draft keeps a canary in the inputs and a dated contamination flag on a comparison set whose inputs may have reached its models' training data, read from published training cutoffs against the inputs' publication date; current frontier cutoffs predate the draft, so the first sets run unflagged. A flagged set, or inputs older than a stated age where no cutoff is published, triggers a rotation before the next headline comparison set: the rotation brings new hidden requirements with new seed evidence, and the prompts or the whole project change when the leak reaches the project's own rules. Only then is the old project retired, still public.

### Runs per scenario

A comparison set requires three phase-1 runs per scenario for every scenario of its roster, declared before the set's first scored run with no stopping rule, each with its own phase-2 child, so every row rests on three runs per prompt and gives a median and a range per cell. A development or ablation run outside the roster keeps the fast loop's single run.

### Radar curve selection

Before a comparison set's first scored run, the set's definition names one reference scenario per family, for example both cairn deliveries for the current release under models_strategy_1, the multi-prompt control mirroring that yolo scenario, and one declared manual_prompt pair, and each radar curve is drawn from its declared scenario whatever the table's ranking turns out to be; every other configuration appears only in the table. With the roster's rule-named strongest manual pair as the manual reference, the baseline is the a-priori strongest rather than a best-of-several pick.

### Score spread reporting

Each score cell of the README ranking table (overall, the three axes, and the lost count) carries the minimum and maximum over the scenario's runs beside its mean, written in the cell as, for example, 82 (76–88), each run counted as one phase-1 run with its phase-2 child, whose two prompt scores are averaged as the scenario mean is; the analysis output carries the same ranges and every run's individual scores. Cost, time, invocations, and sessions stay means without spread, and the radar draws means only.

### Table claim wording

The ranking table's opening sentence is recast as an explicitly refutable expectation in the style the phase-2 paragraph already uses, stating in advance that Cairn is expected to beat the other approaches and naming the table as what would refute it, with the section's purpose sentence folded in. The radar's opening is recast the same way: it is where the expected gain is located by axis, its curves are drawn whatever they show, and a Cairn curve inside a manual one refutes the expectation on that axis; the radar's existing list of axes where the gain is expected stays as the stated expectation.

### Rank tie threshold

The tie margin is derived per comparison set from the set's own measured noise, by a declared statistical bound on the difference of two scenarios' per-run overall scores, for example overlapping intervals at a declared level, widened by the rater agreement figure where one is reported. Scenarios within that margin of their group's top row share one rank number and are marked as tied, and cost plays no part in the rank, so rows are ordered only where the set's own per-run ranges separate them.

### Hidden axis weight

The hidden axis keeps equal weight: the overall score stays the unweighted mean of the stated, hidden, and implied axes, and the rank still orders by it. The hidden requirement stays one per prompt, so the axis keeps resting on the phase-1 reading line and the phase-2 yes-or-no test line. The draft adds the reason the hidden axis keeps its third despite its two checks, that it is the outcome the benchmark exists to test and the per-axis columns, the ranges beside the overall, and the measured tie rule absorb the two-check noise as ties, and the ranking table keeps the per-axis columns beside the overall as it does now.

## Out of Scope

