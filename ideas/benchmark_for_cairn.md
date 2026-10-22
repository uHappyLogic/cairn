# Benchmark for Cairn

## General idea

### What the benchmark is

The benchmark is a separate project whose only relation to Cairn is that it takes Cairn as an input and measures it. It is not part of Cairn, does not share its repository, and does not track its `main`: each benchmark run records the exact Cairn commit it exercised, and comparing Cairn versions is done by re-running the benchmark with a different pinned commit. Releases are the commits that appear in the published trend; a candidate commit is benchmarked the same way (see "How Cairn development uses the benchmark").

The benchmark executes one project under three arms, each starting from the same seed repository and the same raw prompt: a "raw single prompt" run, a "raw multi-turn" run, and a "YOLO cairn" chain. Each arm delivers its own artifact. Those artifacts are what is measured and shown: they serve as proof of whether Cairn helps, and as a way to track its behaviour across versions, models, and effort levels.

The framework has to actually help, not just pretend to. Every comparison below is set up so that a difference between arms can be attributed to Cairn's structure, not to extra compute, a stronger model, or a better prompt.

## The raw prompt

The raw prompt is one fixed text, versioned alongside the benchmark, and placed byte-identical in every arm's working tree as the project description file `PROJECT.md` at the repository root. It is never passed on the command line: the harness writes it into the clone and commits it as the first commit of the run branch (see "One run"), so the agent finds the task in the repository the way a developer would. Every arm then receives the same one-sentence pointer message, fixed as part of the arm definition:

```
Carry out the task described in PROJECT.md.
```

In the raw arms that sentence is the whole user message; in the cairn arm it is the argument of `/cairn:define-milestone-goal`, which reads the file to fill the milestone's Goal. No arm gets extra wording, hints, or clarification, and no message differs between prompts: only the file's content changes from prompt 1 to prompt 2.

The prompt is deliberately underspecified in a few named places (for example team setup, the tie, controls, persistence) so that real open questions exist for Cairn to surface. It is still specific enough that the raw arms can produce a working result; the gaps are decisions, not missing instructions. It also states nothing about the expectations the seed gives evidence for; those are the hidden requirements of the next section.

## Hidden requirements

A hidden requirement is an expectation the project's stakeholder holds that the prompt does not state and the seed gives evidence for. It differs from the gaps the prompt deliberately leaves open: a gap is a decision with several defensible answers, and its metric is whether the arm surfaced and recorded it; a hidden requirement has one right answer, and its metric is whether the artifact meets it. It exists to test the question-and-answer loop as a whole: a review pass that asks what the prompt did not, a recommendation grounded in the live project, and a decision recorded and carried into the tasks.

- **The statement never reaches an arm; the evidence does.** The requirement is written down in the inputs area and on the rating checklist and nowhere else. Its evidence lives in the seed, so every arm gets it byte-identical and a raw arm can act on it as well as the cairn chain can. Nothing in `PROJECT.md` points at it. A requirement with no evidence in the seed would measure luck, so it is not a valid hidden requirement.
- **The evidence is calibrated.** It must make one answer clearly best once the question is asked, while the prompt alone gives no reason to ask it. A seed file that states the requirement outright measures whether the agent read a file; evidence too faint to settle the question measures a guess.
- **Two measurements.** *Met*: a line on the rating checklist, applied to the artifact by a rater who does not know the arm, scored as a count where the requirement allows one. *Surfaced*: whether the run's process left a record of the question. For the cairn arm that record is the question block a review pass added, read from the run branch and judged by hand until a judge is written; for a raw arm it is only an assumption note the agent happened to leave, so surfaced is reported for the cairn arm and stated as unobservable for the others.
- **Versioning.** A hidden requirement is tied to the seed tag that carries its evidence and to the prompt blob that leaves it unstated. Changing the evidence is a seed bump, and the analysis groups by both before comparing arms.
- **One per prompt**, listed under its own heading in the project section and never in the "deliberately left open" list, so the planted-gap count of claim 1 stays clean.
- **What the chain can show.** The cairn chain accepts its own recommendations, so a met hidden requirement shows surfacing plus a grounded recommendation. With a person in the loop the same question would reach them to answer, which is the workflow's intended value and is not what this benchmark measures.

## Model and effort

One model and one effort level are pinned for the whole benchmark and used on every invocation of every arm. The pinned pair is recorded with the results. A run that mixes models or efforts inside an arm is not a valid run of this benchmark, because its result cannot be attributed.

Comparing models or efforts is a separate experiment: the whole benchmark is re-run with a different pinned pair, and the pairs are compared to each other.

```
MODEL=<model>     # e.g. opus, fable
EFFORT=<effort>   # e.g. medium, high
```

## Arm 1: raw single prompt

One headless invocation, the pointer sentence as the whole message:

```
claude -p "Carry out the task described in PROJECT.md." --dangerously-skip-permissions --model "$MODEL" --effort "$EFFORT";
```

## Arm 2: raw multi-turn

The same number of headless invocations as the cairn chain has lines (N). The first is the pointer sentence, every following one is the same fixed continuation message, sent to a fresh process, not a continued session:

```
claude -p "Carry out the task described in PROJECT.md." --dangerously-skip-permissions --model "$MODEL" --effort "$EFFORT";
claude -p "Continue the work in this repository and improve it." --dangerously-skip-permissions --model "$MODEL" --effort "$EFFORT";   # repeated N-1 times
```

This arm separates "Cairn's structure helps" from "N turns beat one turn". Its N is derived from the cairn chain and updated whenever the chain changes.

## Arm 3: YOLO cairn chain

The `YOLO cairn` chain is a sequence of the Cairn commands merged together that does not require any human input. Its first line bootstraps the milestone workflow inside the clone, so every Cairn artifact (the `milestones/` directory, its `README.md` with the pointer reading `none`, and the `## Milestone Workflow` section of `CLAUDE.md`) is created by the run itself: the seed carries none of it, and the raw arms never see Cairn's vocabulary or guidance. The bootstrap commits nothing; the files it writes are picked up by the skills that later commit them. Every line runs under the pinned model and effort:

```
claude -p "/cairn:init-milestone-base-workflow" --dangerously-skip-permissions --model "$MODEL" --effort "$EFFORT";
claude -p "/cairn:define-milestone-goal Carry out the task described in PROJECT.md." --dangerously-skip-permissions --model "$MODEL" --effort "$EFFORT";
claude -p "/cairn:goto-next-milestone" --dangerously-skip-permissions --model "$MODEL" --effort "$EFFORT";
claude -p "/cairn:specify-milestone-starting-state" --dangerously-skip-permissions --model "$MODEL" --effort "$EFFORT";
claude -p "/cairn:review-milestone-requirements" --dangerously-skip-permissions --model "$MODEL" --effort "$EFFORT";
claude -p "/cairn:provide-alternatives-to-all-open-questions" --dangerously-skip-permissions --model "$MODEL" --effort "$EFFORT";
claude -p "/cairn:recommend-all-open-questions" --dangerously-skip-permissions --model "$MODEL" --effort "$EFFORT";
claude -p "/cairn:answer-all-open-questions-with-recommendation" --dangerously-skip-permissions --model "$MODEL" --effort "$EFFORT";
claude -p "/cairn:derive-tasks" --dangerously-skip-permissions --model "$MODEL" --effort "$EFFORT";
claude -p "/cairn:complete-all-tasks" --dangerously-skip-permissions --model "$MODEL" --effort "$EFFORT";
```

## Cost and time reporting

Every run of every arm records, from the JSON output of each invocation:

- total input and output tokens, and cost in dollars,
- wall-clock duration,
- number of invocations actually made (a chain that stops early reports fewer).

These are reported per arm next to the quality results, never omitted. Cairn is expected to cost more; the benchmark states by how much and lets the reader weigh it against the quality difference. A quality win that is not accompanied by its cost is not a reportable result of this benchmark.

## Repository layout and isolation

The benchmark is its own repository, separate from the cairn repository, and it references cairn only as a pinned input. Four things in this design require that separation: the seed is an orphan commit and every run pushes a branch, which would litter the plugin repository with unrelated history; the plugin under test must be a fixed version recorded by commit, which it cannot be when it is whatever the plugin repository's `main` happens to hold; publishing is per repository and must cover the snapshot directory and nothing else; and the records grow by one full tree snapshot per run, which does not belong next to distribution trees guarded by a drift gate. The earlier eval pilot placed cases inside the cairn repository, which is fine for a small unpublished suite and wrong for this one.

Within that repository, each run executes on its own branch and its result is recorded on `main`; there is no repository per run. Three conditions make that sound:

- **Every run branches from a fixed seed tag or from its parent run, never from `main`.** The seed commit holds the seed repository (git initialised, a `CLAUDE.md` that names no Cairn concept, and a `README.md` stating what the project is for, which carries the evidence of the hidden requirements; the milestone bootstrap is not run, because the cairn chain runs it itself and the raw arms must not read its workflow guidance), is built from `seed/` as an orphan commit with no ancestor on `main`, and is tagged once. A first-prompt run branches from that tag; a second-prompt run branches from the tip of the first-prompt run it continues. Once `main` carries results, a branch taken from it would put earlier runs' output into the agent's working tree, so `main` is never a branch point.
- **Every run works in a clone that cannot see the other branches.** Cairn's starting-state skill and a raw agent may both read git history or the branch list, so in a shared checkout run 5 could read run 1's solution. Each run starts as a fresh single-branch clone of its branch point, with no tags and with the remote removed after cloning, at a path unique to that run; on completion the run script adds the remote back and pushes the branch to the canonical repository as `run/<id>`. The clone is not shallow: a second-prompt run legitimately sees its own first-prompt history, and that history is the same for every arm's second prompt.
- **Run branches are never git-merged into `main`.** Every run edits the same files, so merges would conflict and the merged tree would mean nothing. The branches stay as the record of each run (its history and commit subjects are process metrics). `main` receives a snapshot of each run's deliverable under `runs/<id>/`, written with a read-tree prefix from the run branch, plus one manifest per run under `results/<id>/`. Publishing `runs/` through GitHub Pages then makes every artifact playable by URL.

### Structure of `main`

`main` holds four kinds of content. Each kind lives in its own top-level area, and the kind decides the rules the area follows; the concrete file names follow from the rules.

```
inputs       what a run is given        seed source, raw prompts, arm definitions, the plugin under test
harness      how a run is executed      the run procedure, the seed builder, the index generator, the analysis
records      what a run produced        per id: a published snapshot, and an unpublished manifest with the invocation outputs
evaluation   what people concluded      blind ratings keyed by id, and the analysis output
```

Root-level housekeeping (the README, the instructions for working on the harness, the publishing workflow) is a fifth, incidental kind: it is never part of the seed and no run ever sees it.

**Inputs** are the things a difference between arms must not be attributed to, so they are fixed and recorded:

- Every input is byte-identical across arms and versioned by content, not by name: a run's manifest records the seed as a tag, the plugin as a commit, each prompt as a blob hash. Changing any input starts a new comparison set; the analysis groups runs by their input versions before it compares arms.
- The seed source is the one input a run does not read in place. The harness turns it into an orphan commit and tags it; runs branch from the tag, never from the source directory. It contains nothing produced by Cairn: any Cairn artifact a run needs is created by the cairn chain's own bootstrap line, so the seed is the same for all arms without leaking the plugin's guidance into the raw ones. Its README is the one place the hidden requirements' evidence lives, and nothing in it states them.
- The plugin under test is an input like any other: pinned at one commit inside the repository (a release or a candidate), loaded per invocation by the harness for the cairn arm only, and never installed at user level, so the raw arms cannot see its skills.
- An arm definition is a list of fixed messages and nothing else; no message carries prompt text, because the prompt reaches the run as the committed `PROJECT.md`. Every flag (model, effort, permissions, output format, plugin directory) is added by the harness, so the settings a run executes under are set in exactly one place. Arm 2's list is derived from the cairn chain's length at run time, not stored, so the two can never drift.
- A hidden requirement is an input too: one entry per prompt stating the requirement, the seed evidence it rests on, and the check a rater applies, keyed to the seed tag and the prompt blob. No run sees the entry; the rating instructions carry its check line.

**The harness** is the only writer of the record areas. It sees the whole repository; a run sees only its clone. A harness change must not change what a run sees or is given; a change that would (a different flag, a different continuation message) is an input change and is versioned as one.

**Records** are append-only: one directory per id in each record area, one commit per run, never hand-edited except for the manifest's entry-point field. The published half is exactly the snapshot of the run's tree (the `runs/<id>/` of the three conditions above); the unpublished half is everything that ties the id to an arm, model, cost, or branch (the `results/<id>/` manifest and the per-invocation outputs). The two halves are separate top-level directories so that publishing is "this directory and nothing else".

**Evaluation** is keyed by id only. Rating files carry no arm, and the join between ratings and manifests lives in the harness's analysis step, so blindness is a property of where the join is allowed to happen, not of rater discipline. A rating file carries the experience score and, as separate lines, the hidden-requirement checks, so the two are never folded into one number.

### Git objects

- `main` is linear and holds the harness plus the records. Each completed run adds one commit touching only `runs/<id>/` and `results/<id>/`, under the fixed subject `Run: <id>`; harness changes are separate commits.
- `seed/v<K>` tags point at orphan commits built from the seed source. They share no history with `main`, so a run's clone contains nothing but the seed tree and its own work.
- `run/<id>` branches are rooted at a seed tag (prompt 1) or at the tip of the parent run's branch (prompt 2). They are never merged, rebased, or deleted. The cairn arm's history is one commit per skill or task under Cairn's own subjects; a raw arm's history is whatever the agent chose to commit, which is itself a result.
- The canonical repository is the GitHub remote. Working clones live outside it, under one scratch directory with one subdirectory per id, and are deleted once the run's commit on `main` exists.

### One run

The run procedure, invoked with an arm, a prompt index, and for a second prompt the parent run's id, is the whole procedure; nothing about a run is done by hand.

1. **Id.** Draw an opaque id (eight characters from a random source). Refuse it if `runs/<id>` or `run/<id>` already exists.
2. **Pre-flight.** Assert: the benchmark checkout is on `main` and clean; `MODEL` and `EFFORT` are set; `--from` is given exactly when `<n>` is greater than 1, and the parent's manifest is for prompt `<n>-1` and the same arm; the cairn plugin is not installed at user level (so the raw arms cannot see its skills); no memory directory exists for the clone path (see "Clearing memory").
3. **Clone.** Single-branch, no tags, from the seed tag or from `run/<parent-id>`, into the run's unique path. Remove the remote. Create `run/<id>` from the checked-out commit.
4. **Prompt.** Write the prompt `<n>` text over `PROJECT.md` at the clone root, replacing whatever the file held (for prompt 1 the seed has none; for prompt 2 it holds prompt 1, which stays readable in the branch history), and commit it under the fixed subject `Prompt: <n>`. This commit is identical across arms and is the first commit of every run branch after its branch point; the harness makes it, so the agent never sees the prompt outside the repository.
5. **Invocations.** For each message of the arm's list, in order, run from the clone:

   ```
   claude -p "<message>" --dangerously-skip-permissions --model "$MODEL" --effort "$EFFORT" --output-format json
   ```

   The cairn arm's lines add `--plugin-dir` pointing at the pinned plugin checkout. Stdout is written to the run's invocation outputs under `results/<id>/`, one file per invocation in chain order, and stderr beside it. A non-zero exit stops the chain; the run is still recorded, with the manifest stating how many invocations were made, because an early stop is a result, not a failed measurement.
6. **Push.** Add the remote back and push `run/<id>`.
7. **Snapshot.** On the benchmark checkout, read the run branch's tree into `runs/<id>/` with a prefixed read-tree and check the files out.
8. **Manifest.** Write the manifest under `results/<id>/` from the invocation outputs and the environment.
9. **Memory.** Delete the memory directory keyed by the clone path and assert it is gone.
10. **Commit.** Regenerate the index page, then commit `runs/<id>/`, the index page, and `results/<id>/` on `main` as `Run: <id>`. Delete the clone.

### The manifest

The manifest is the only place that ties an id to its arm. Everything the analysis needs is in it or in the invocation files beside it:

```json
{
  "id": "k7f3q2xd",
  "arm": "cairn",
  "prompt": { "index": 1, "file": "PROJECT.md", "blob": "<git blob sha of the committed PROJECT.md>" },
  "parent": null,
  "seed": "seed/v1",
  "branch": { "name": "run/k7f3q2xd", "tip": "<sha>", "commits": 23 },
  "model": "opus",
  "effort": "high",
  "host": { "binary": "claude", "version": "2.1.283" },
  "plugin": { "path": "<plugin checkout>", "commit": "<sha>", "version": "1.7.3" },
  "user_config": { "claude_md_sha256": "<sha>", "settings_sha256": "<sha>" },
  "entry": "index.html",
  "started": "<iso timestamp>",
  "finished": "<iso timestamp>",
  "invocations": { "planned": 10, "made": 10, "stopped_early": false },
  "totals": { "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "duration_ms": 0 }
}
```

- `arm` is one of `raw-single`, `raw-multi`, `cairn`. `plugin` is null for the raw arms. `parent` is the id of the first-prompt run a second-prompt run continues.
- `totals` are sums over the per-invocation JSON files, which keep the per-invocation figures; the manifest never restates them.
- `entry` is the path a rater opens, relative to `runs/<id>/`. The run script detects a root `index.html`; a run that put its entry point elsewhere gets the value by hand, and that edit is the one hand-written field.
- `user_config` records digests of the user-level `CLAUDE.md` and settings that applied to the run, so a later re-run can check it ran under the same configuration.

### Hosting and blindness

- The Pages workflow uploads `runs/` and nothing else. The unpublished record half and the evaluation area exist only on `main`, so the mapping from id to arm is never on the site.
- The index page under `runs/` is generated from the manifests and lists ids with their entry links, in an order shuffled once and fixed. It names no arm, model, or prompt.
- Raters receive the index link, play each entry, and record scores in the evaluation area, one file per rater, keyed by id. The join with the manifests happens only in the analysis step, after all ratings are in.
- Known limit: the snapshot is the whole tree, so a rater who browses past the entry point can see a cairn run's `milestones/` directory. Blindness holds for a rater who follows the entry links and plays; the rating instructions say so.

### Clearing memory

Clearing the assistant's memory is a step of every benchmark run, not a manual chore:

- Claude Code keeps an auto-memory directory keyed by the working directory path. The unique clone path gives each run a fresh memory directory, and the run script deletes that directory after the run completes, so no run can inherit from another and reused paths cannot leak.
- The run script also asserts, before the first invocation, that no memory directory exists for the run's path.
- User-level configuration (`~/.claude/CLAUDE.md`, settings) applies to every arm equally and is not cleared, but its content is recorded with the results so a later re-run can reproduce it.

## How Cairn development uses the benchmark

The benchmark measures Cairn, and Cairn's development reads the measurement. That is the whole relation, and it runs through two channels only: a plugin commit goes in as an input, and metrics keyed by that commit come out as records. The benchmark never imports Cairn's test suite or build tooling, and Cairn never imports the harness; neither repository has the other as a dependency, and a change on either side that would need one is a design error.

Four uses are adopted now:

- **Any commit is a valid plugin input.** The plugin input is a commit, not a release, and the manifest already records it as such. A Cairn branch is benchmarked before it merges by pointing the pinned plugin checkout at that commit; the analysis groups runs by plugin commit, so a candidate and the release it would follow are compared like any two versions. Nothing else in the run procedure changes.
- **The cairn arm alone yields process metrics that need no rater.** The invocation outputs and the run branch of a cairn run carry signals the harness reads directly: whether the chain completed or where it stopped, questions surfaced per review pass and whether a hidden requirement is among them, alternatives and recommendations the annotating passes reported as skipped, anomalies the answer sweep reported, tasks derived, and token cost per skill. A development check runs the cairn arm only, with no raw arms and no rating, and reads these out. This is the fast loop: it costs one chain per candidate commit and gives a result the same day.
- **Cairn's design claims are the metric contract.** Cairn's `docs/design-claims.md` lists its claims, each with a named metric, and states that only one is tested. The analysis implements the subset of those metrics its data reaches, each as a function over manifests and run branches, and reports them per plugin commit. The planted gaps of claim 1 are the "deliberately left open" list under each prompt, so that claim is measurable from the first run. The hidden requirements test claims 1 and 4 together, as the one case where a surfaced question and a project-grounded answer have a right outcome to check against. A Cairn milestone that changes behaviour names the claim it expects to move, and the next run against its commit confirms or refutes it. The link between the repositories is this document on one side and the analysis on the other, never code.
- **Ablation arms attribute value to single skills.** An arm definition is a message list, so a chain without the starting-state skill, a chain without the recommendation pass, or a chain with two review passes is one more list under its own arm name. The `arm` field of the manifest takes that name. Comparing an ablated chain to the full chain on the same inputs says whether one skill earns its cost, which the three primary arms cannot say. Arm 2's length stays derived from the full chain, so the raw comparison is unaffected by which ablations exist.

Two uses are the intended ones once ratings exist:

- **Release gate.** Before a version is cut, the full three-arm benchmark runs on the candidate commit and is compared to the previous release on the same inputs. This is the slow loop. It becomes a gate rather than a report only once a baseline and a threshold are stated; until then the comparison is published next to the release notes.
- **Published trend.** Once all ratings for a comparison set are in, the per-arm aggregates per plugin commit can be published without weakening blindness, because the join is complete and no rater is still working. Cairn's changelog links to the trend for each release.

Two more are deferred as conventions rather than design: triaging a bad cairn run into a Cairn milestone goal that cites the run id, and dispatching a benchmark run from Cairn's release workflow. Both cost money or process on every use and wait until the fast loop is stable.

## Benchmark project requirements

The selected project is Closest Wins, described in the next section. It was chosen against these requirements, which any replacement project has to meet as well:

- **Experienceable.** The result must be something people can "experience" being better, not only read about. One example is a browser mini game that people can quickly play and compare, but any deliverable a person can use and judge in a few minutes qualifies. A rater is usually alone, so one person must be able to play every role the deliverable has.
- **Zero-install delivery.** Experiencing an artifact costs one click or one command with no build step, no dependency install, and no account. Each snapshot under `runs/<id>/` must be usable as it is, so it can be hosted or opened directly.
- **Two sequential prompts.** The benchmark consists of at least two raw prompts run in order: the first builds the project, the second extends or changes it. Each arm runs both prompts, the second starting from that arm's own result of the first. A single-shot build is where Cairn's advantage is smallest; the second prompt is where recorded decisions and starting-state analysis are expected to show. Both prompts follow the "raw prompt" rules above.
- **Real decisions, no canned solution.** The project must not be one whose complete solution is a well-known exercise that a model reproduces from memory. Its rules or behaviour must require genuine design decisions in the places the raw prompt leaves underspecified, so that the arms can diverge on what they decided, not only on how well they typed.
- **One milestone per prompt.** Each prompt must be completable within one Cairn milestone under the pinned model and effort, so that the cairn arm's chain runs once per prompt and the three arms stay comparable in size.
- **Room for a hidden requirement.** Each prompt must have at least one place where an unstated expectation becomes visible in the artifact, and the seed must be able to carry evidence for it that reads as a natural description of the project rather than as a planted instruction.

## Benchmark project: Closest Wins

Closest Wins is a host-run quiz for one big screen, made for this benchmark. Its fixed part is a short flow the host drives from team setup to final standings, so every arm builds against the same specification and a rater can check it by eye; everything around the flow is left open, and the questions the game asks are each arm's own to write, which is where the hidden requirement of each prompt shows.

### Rules

- One host runs the game on one screen that the whole room sees, so the host's controls are visible to everyone and the answer must stay hidden until the host reveals it.
- At the start the host sets the number of teams.
- The game comes with ten questions of its own, each with a number as its answer, and asks them one at a time. Teams answer out loud; the host keeps track of what each team said, and the game records no guesses.
- After the reveal the host gives the question's point to the team closest to the answer and moves on. After the last question the game shows the standings.

A game is ten questions and takes under two minutes with the rater playing host, so a rater can play every artifact from start to finish and compare them side by side.

### Why it was chosen

- **A flow to check against.** A rater checks that the artifact passes through team setup, hidden question, reveal, award, next question, and standings. The hard check is the hidden answer: an answer visible before the reveal, on a screen the whole room sees, ruins the round.
- **Visible by the naked eye, from across a room.** The whole game fits on one screen, and legibility at a distance is part of what a rater judges.
- **Open-ended beyond the flow.** Team naming, a tie on closeness, undoing an award, skipping a question, showing progress, keyboard control, persistence, a place to note guesses, and the reveal and standings presentation are all decisions the prompt does not make.
- **Not a canned solution, with a caveat.** The exact flow, with no answer entry and a host-judged award, matches no named exercise. It does sit nearer the common quiz-app genre than a novel ruleset would, so the raw arms may produce more uniform output, and the planted gaps and the hidden requirements carry more of the comparison than the rules do.
- **Room for hidden requirements.** The questions are the arm's to write and the storage of a prepared set is the arm's to choose, so each prompt has a place where an unstated expectation shows in the artifact.
- **Solo-ratable.** The rater plays the host; the game needs no second person and hides nothing from the host.

### The seed README

The seed's `README.md` states what the project is for. It is the evidence for both hidden requirements and states neither:

```
# Zoo members' evening

Games for the Riverside Zoo's yearly members' evening. The host prepares
everything at home and runs the games from the community hall's laptop on the
big screen.
```

The seed's `CLAUDE.md` stays an environment description that names no Cairn concept and may point at the README.

### Prompt 1: the game

The first raw prompt, the content of `PROJECT.md` for prompt 1, builds the quiz:

```
Build a browser party game called Closest Wins as a single self-contained HTML
file that opens directly from disk with no build step, no dependencies, and no
server. One host runs it on one big screen that the whole room can see. At the
start the host sets the number of teams. The game comes with ten questions of
its own, each with a number as its answer, and asks them one at a time. Teams
answer out loud and the host keeps track of what each team said. The answer
stays hidden until the host reveals it. After the reveal the host gives the
point for that question to the team closest to the answer and moves on to the
next question. After the last question the game shows the final standings.
```

Deliberately left open: whether teams get names or only numbers and what team counts are allowed, the difficulty of the questions, whether the game offers a place to note each team's answer, what the host does when two teams are equally close, whether an award can be undone, whether a question can be skipped or revisited, whether progress through the list is shown, mouse versus keyboard for the host, whether a reload loses the game, how the reveal and the standings are presented, and legibility from across a room.

Hidden requirement: every question is about an animal. Evidence: the README's zoo evening. Check: the rater counts the questions about an animal, out of ten.

### Prompt 2: the host's own questions

The second raw prompt, written over `PROJECT.md` for prompt 2, extends each arm's own result of the first:

```
Let the host write their own questions for Closest Wins and keep them for the
next party.
```

Deliberately left open: whether the editor is part of the same file, whether the built-in questions stay and whether the host chooses a set at the start, how answers stay off the big screen while the host edits, what validation an answer gets, and whether a set can be changed between questions. This is where the recorded decisions from the first milestone are expected to matter: an arm that recorded how its questions are represented and whether anything persists extends those decisions; an arm that did not has to rediscover or contradict its own behaviour.

Hidden requirement: a set prepared on one computer plays on another. Evidence: the README's host who prepares at home and plays from the hall's laptop. Check: the rater moves a prepared set to a fresh browser profile and plays it; a set kept only in browser storage fails.

### Fit with the run rules

Each prompt is one milestone: the game is a single file with a six-step flow and ten questions, and the editor is one feature on top of it. Both reach every arm as the same committed `PROJECT.md` and are versioned as its blob hash in the manifest; the hidden requirements are keyed to that hash and the seed tag. The artifact is one HTML file, so `entry` is the root `index.html` whenever the arm named it that, and the snapshot under `runs/<id>/` is playable from GitHub Pages with one click.
