# Benchmark for Cairn

## General idea

### What the benchmark is

The benchmark is a separate project whose only relation to Cairn is that it takes Cairn as an input and measures it. It is not part of Cairn, does not share its repository, and does not track its `main`: each benchmark run records the exact Cairn commit it exercised, and comparing Cairn versions is done by re-running the benchmark with a different pinned commit. Releases are the commits that appear in the published trend; a candidate commit is benchmarked the same way (see "How Cairn development uses the benchmark").

The benchmark executes one project under a set of scenarios, each starting from the same seed repository and the same raw prompt. A scenario is one way of delivering the project paired with one model strategy, and it carries one identifier composed of the two: `cairn_1_8_3_yolo_models_strategy_1` is the YOLO cairn chain of Cairn 1.8.3 run under the model strategy named `models_strategy_1`, and `manual_prompt_opus_5_5_high` is one manual prompt run under Opus 5.5 at high effort. Each scenario delivers its own artifact. Those artifacts are what is measured and shown: they serve as proof of whether Cairn helps, and as a way to track its behaviour across versions, models, and effort levels.

The framework has to actually help, not just pretend to. A difference between two scenarios is attributed to what differs between their definitions and to nothing else, so a reader always knows what a comparison says: two scenarios that share a model strategy isolate the delivery, two that share a delivery isolate the model strategy, and the headline comparison, Cairn under the model strategy it is meant to be used with against manual prompting under one strong model, differs in both and is read next to its cost. Everything a scenario does not define (the seed, the prompt, the hidden requirements, the harness flags) is identical across scenarios, so a difference is never attributed to it.

## The raw prompt

The raw prompt is one fixed text, versioned alongside the benchmark, and placed byte-identical in every scenario's working tree as the project description file `PROJECT.md` at the repository root. It is never passed on the command line: the harness writes it into the clone and commits it as the first commit of the run branch (see "One run"), so the agent finds the task in the repository the way a developer would. Every scenario then receives the same one-sentence pointer message, fixed as part of the delivery definition:

```
Carry out the task described in PROJECT.md.
```

In the manual deliveries that sentence is the whole user message; in the cairn deliveries it is the argument of `/cairn:define-milestone-goal`, which reads the file to fill the milestone's Goal. No scenario gets extra wording, hints, or clarification, and no message differs between prompts: only the file's content changes from prompt 1 to prompt 2. The one exception is the stakeholder's brief in the `cairn_<version>_assess_answers_manually` delivery, which is that delivery's whole point and is described with it.

The prompt is deliberately underspecified in a few named places (for example team setup, the tie, controls, persistence) so that real open questions exist for Cairn to surface. It is still specific enough that the manual scenarios can produce a working result; the gaps are decisions, not missing instructions. It also states nothing about the expectations the seed gives evidence for; those are the hidden requirements of the next section.

## Hidden requirements

A hidden requirement is an expectation the project's stakeholder holds that the prompt does not state and the seed gives evidence for. It differs from the gaps the prompt deliberately leaves open: a gap is a decision with several defensible answers, and its metric is whether the scenario surfaced and recorded it; a hidden requirement has one right answer, and its metric is whether the artifact meets it. It exists to test the question-and-answer loop as a whole: a review pass that asks what the prompt did not, a recommendation grounded in the live project, and a decision recorded and carried into the tasks.

- **The statement never reaches a run's repository; the evidence does.** The requirement is written down in the inputs area and on the rating checklist and nowhere else. Its evidence lives in the seed, so every scenario gets it byte-identical and a manual scenario can act on it as well as a cairn scenario can. Nothing in `PROJECT.md` points at it. The one place a statement is spoken inside a run is the brief given to the stakeholder's stand-in in the `cairn_<version>_assess_answers_manually` delivery: a message, never a file, which the rest of that chain sees only through the decisions it led to, recorded in the milestone's own files. A requirement with no evidence in the seed would measure luck, so it is not a valid hidden requirement.
- **The evidence is calibrated.** It must make one answer clearly best once the question is asked, while the prompt alone gives no reason to ask it. A seed file that states the requirement outright measures whether the agent read a file; evidence too faint to settle the question measures a guess.
- **Two measurements.** *Met*: a line on the rating checklist, applied to the artifact by a rater who does not know the scenario, scored as a count where the requirement allows one. *Surfaced*: whether the run's process left a record of the question. For a cairn scenario that record is the question block a review pass added, read from the run branch and judged by hand until a judge is written; for a manual scenario it is only an assumption note the agent happened to leave, so surfaced is reported for the cairn scenarios and stated as unobservable for the others. The assess delivery adds two more, read from the stand-in's report (see the delivery): *covered*, whether an alternative met the requirement once it was surfaced, and *answered*, whether the stand-in recorded that alternative.
- **Versioning.** A hidden requirement is tied to the seed tag that carries its evidence and to the prompt blob that leaves it unstated. Changing the evidence is a seed bump, and the analysis groups by both before comparing scenarios.
- **One per prompt**, listed under its own heading in the project section and never in the "deliberately left open" list, so the planted-gap count of claim 1 stays clean.
- **What each chain can show.** The YOLO chain accepts its own recommendations, so a met hidden requirement there shows surfacing plus a grounded recommendation, with no person involved. The assess chain puts a stand-in for the stakeholder at the answer step, so a met requirement there shows surfacing, an alternative set that covered the right answer, and the stand-in's decision carried through to the artifact. The gap between the two, under one model strategy, is what a person who reads the questions and answers the ones that matter to them gains, which is the workflow's intended value.

## Scenarios

A scenario is a delivery paired with a model strategy. Both are definitions stored in the benchmark repository's inputs area, one file each under its own id, and the scenario id is the delivery id followed by the model strategy id. A definition is never edited once a run has used it: a change is a new id, so an id names one fixed thing for the life of the benchmark.

### Deliveries

A delivery is the way the project is delivered: a list of fixed messages, in order, each sent as one headless invocation. No message carries prompt text, because the prompt reaches the run as the committed `PROJECT.md`. A cairn delivery also names the plugin commit it runs. Four deliveries are defined here; ablations add more (see "How Cairn development uses the benchmark").

#### `manual_prompt`

One invocation, the pointer sentence as the whole message:

```
Carry out the task described in PROJECT.md.
```

#### `manual_multi_prompt_as_<cairn scenario id>`

The control that separates "Cairn's structure helps" from "N turns beat one turn". It has no definition file of its own: it mirrors the cairn scenario its id names and takes from it the number of invocations N and the model and effort of each one, line by line, so the two can never drift. Its first message is the pointer sentence; every following one is the same fixed continuation message, sent to a fresh process, not a continued session:

```
Carry out the task described in PROJECT.md.
Continue the work in this repository and improve it.   # repeated N-1 times
```

#### `cairn_<version>_yolo`

The YOLO cairn chain is a sequence of the Cairn commands merged together that does not require any human input. `<version>` is the release the delivery runs (`1_8_3`), or the short commit for a candidate that is not a release. Its first line bootstraps the milestone workflow inside the clone, so every Cairn artifact (the `milestones/` directory, its `README.md` with the pointer reading `none`, and the `## Milestone Workflow` section of `CLAUDE.md`) is created by the run itself: the seed carries none of it, and the manual deliveries never see Cairn's vocabulary or guidance. The bootstrap commits nothing; the files it writes are picked up by the skills that later commit them.

```
/cairn:init-milestone-base-workflow
/cairn:define-milestone-goal Carry out the task described in PROJECT.md.
/cairn:goto-next-milestone
/cairn:specify-milestone-starting-state
/cairn:review-milestone-requirements
/cairn:provide-alternatives-to-all-open-questions
/cairn:recommend-all-open-questions
/cairn:answer-all-open-questions-with-recommendation
/cairn:derive-tasks
/cairn:complete-all-tasks
```

#### `cairn_<version>_assess_answers_manually`

The YOLO chain with the stakeholder put back in at the one step the workflow built for them. It is the YOLO delivery's list with one message inserted after `/cairn:provide-alternatives-to-all-open-questions` and differs from it in nothing else, so the two scenarios under one model strategy isolate that turn. The inserted turn is played by a stand-in for the project's stakeholder: the person Cairn's questions are meant to reach, who knows what they want beyond what `PROJECT.md` says and who, in a real project, would read the questions and answer the ones that matter to them. The stand-in is defined by the benchmark, in the delivery definition; nothing in the plugin knows it exists. The scenario exists to show what that person gains by investing the time, measured as the hidden requirements the artifact meets.

```
/cairn:init-milestone-base-workflow
/cairn:define-milestone-goal Carry out the task described in PROJECT.md.
/cairn:goto-next-milestone
/cairn:specify-milestone-starting-state
/cairn:review-milestone-requirements
/cairn:provide-alternatives-to-all-open-questions
<the stakeholder's turn>
/cairn:recommend-all-open-questions
/cairn:answer-all-open-questions-with-recommendation
/cairn:derive-tasks
/cairn:complete-all-tasks
```

The stakeholder's turn is one headless invocation like the others. Its message is a fixed instruction followed by the brief: the statements of the hidden requirements keyed to the run's seed tag and prompt blob, one line each, inserted by the harness from the inputs area. Those of the prompt being run only, not of earlier prompts, so each prompt's measurement stays its own; and the statements only, not the evidence, which the stand-in can read in the clone like anyone else, and not the rater's check, which is the measurement.

```
You are the person this project is for. Read PROJECT.md, then the current
milestone's open questions with their alternatives. Beyond what PROJECT.md
says, you want the following:

<one line per hidden requirement of this prompt>

For every open question where one alternative serves what you want and the
others do not, record it with
/cairn:answer-open-question-with-alternative <Short Title>. <Alternative Id>
and leave every other question unanswered. Edit no file yourself. Finish
with one line per item above: the question you answered for it and the
alternative, or "no question" if none bore on it, or "no alternative" if a
question did but none of its alternatives served it.
```

What the turn may and may not do follows from what the scenario has to isolate:

- **It answers only where the brief decides.** A question the brief says nothing about is left to the recommendation pass, as in the YOLO chain. If the stand-in also answered by taste, the artifact would differ from the YOLO artifact in ways not attributable to the brief, and the comparison would say less. The stand-in does not model every user; it models the knowledge a user has and the prompt does not.
- **It answers from the alternatives only.** `answer-open-question-with-alternative` records one of the enumerated options and nothing else, so the stand-in can carry a requirement through only when the alternatives pass laid out an option that meets it. That is deliberate: Cairn's design holds that an alternative set is covering, and this is the scenario where that property has a right answer to check against. A requirement the stand-in reports as "no alternative" is a coverage failure of the alternatives pass, "no question" is a surfacing failure of the review pass, and the two are separate findings in the stand-in's report, which the harness reads from the turn's output.
- **It runs before the recommendation pass.** The stand-in sees alternatives and no recommendation, so its answers are its own, not an edit of the recommender's. The recommendation pass then runs on the remaining questions with the stand-in's decisions already recorded in `requirements.md`, which is the grounding Cairn gives a recommendation formed after a person has decided some of the siblings.
- **The brief leaves no trace but decisions.** The message is never written to the clone, and the later invocations are fresh processes that see only the milestone files. After the turn the harness asserts that the work tree is clean, that every commit the turn added is an `Alternative-answer:` commit, and that the auto-memory directory for the clone path is byte-identical to before the turn. A failed assertion stops the chain there, recorded like any early stop, because a brief that reached the rest of the chain by another route makes the run attributable to nothing.
- **Recorded as sent.** The harness writes the message as sent, brief included, beside the turn's invocation output, since it is the one message of any delivery whose text the definition does not fix verbatim. The model strategy keys the turn by its fixed instruction.

The scenario is read against the YOLO scenario of the same version and model strategy, which differs from it by the stakeholder's turn alone. Its multi-prompt control is derived like any other: it mirrors the turn count and the models but carries no brief, so that comparison folds the brief in with Cairn's structure, and only the comparison against YOLO isolates it.

### Model strategies

A model strategy assigns one model and one effort level to every message of the delivery it is paired with, keyed by the message, and is written in its own file in the inputs area under its id. Nothing in a run picks a model: every invocation runs under the pair its strategy assigns, and the harness refuses a scenario whose strategy leaves one of the delivery's messages unassigned. The file holds the exact `--model` value, never an alias such as `opus`, because an alias moves between host releases and the strategy must mean the same thing for the life of the trend. A strategy's id is a name when it holds several pairs (`models_strategy_1`) and the pair itself when it holds one (`opus_5_5_high`).

Cairn is meant to be used under a mixed strategy, because its skills differ in what they need: the bootstrap and pointer steps are mechanical, the review and recommendation passes are where the reasoning happens, and task completion is where the code gets written. The strategy Cairn is used with is therefore documented in the benchmark repository as an input like any other, and the reference one, `models_strategy_1`, is written from Cairn's own usage snippets, so that the benchmark measures Cairn as it is used, not under an allocation it was never meant for. As a sketch, with the host's model names abbreviated:

| message | model | effort |
|---|---|---|
| `/cairn:init-milestone-base-workflow` | Sonnet 5.5 | medium |
| `/cairn:define-milestone-goal …` | Sonnet 5.5 | medium |
| `/cairn:goto-next-milestone` | Sonnet 5.5 | medium |
| `/cairn:specify-milestone-starting-state` | Fable 5.1 | xhigh |
| `/cairn:review-milestone-requirements` | Fable 5.1 | xhigh |
| `/cairn:provide-alternatives-to-all-open-questions` | Opus 5.5 | high |
| `/cairn:recommend-all-open-questions` | Fable 5.1 | xhigh |
| `/cairn:answer-all-open-questions-with-recommendation` | Fable 5.1 | high |
| `/cairn:derive-tasks` | Fable 5.1 | xhigh |
| `/cairn:complete-all-tasks` | Opus 5.5 | high |
| the stakeholder's turn (assess delivery) | Fable 5.1 | xhigh |

The stakeholder's turn, which no Cairn snippet covers, gets the pair of the recommendation pass, because reading the whole question set and choosing is the same kind of work; the strategy keys it by its fixed instruction, since its brief varies by prompt.

Comparing models or efforts is not a separate experiment: it is the comparison of two scenarios that share a delivery, and the cost difference between them is the price of the strategy. A scenario whose strategy mixes models is a valid scenario, because the mix is its definition. What is not a valid run of this benchmark is one whose invocations depart from the strategy the scenario names, since its result cannot be attributed to any scenario.

## Cost and time reporting

Every run of every scenario records, from the JSON output of each invocation:

- total input and output tokens, and cost in dollars,
- wall-clock duration,
- number of invocations actually made (a chain that stops early reports fewer).

These are reported per scenario next to the quality results, never omitted. Cairn is expected to cost more; the benchmark states by how much and lets the reader weigh it against the quality difference. A quality win that is not accompanied by its cost is not a reportable result of this benchmark.

## Repository layout and isolation

The benchmark is its own repository, separate from the cairn repository, and it references cairn only as a pinned input. Four things in this design require that separation: the seed is an orphan commit and every run pushes a branch, which would litter the plugin repository with unrelated history; the plugin under test must be a fixed version recorded by commit, which it cannot be when it is whatever the plugin repository's `main` happens to hold; publishing is per repository and must cover the snapshot directory and nothing else; and the records grow by one full tree snapshot per run, which does not belong next to distribution trees guarded by a drift gate. The earlier eval pilot placed cases inside the cairn repository, which is fine for a small unpublished suite and wrong for this one.

Within that repository, each run executes on its own branch and its result is recorded on `main`; there is no repository per run. Three conditions make that sound:

- **Every run branches from a fixed seed tag or from its parent run, never from `main`.** The seed commit holds the seed repository (git initialised, a `CLAUDE.md` that names no Cairn concept, and a `README.md` stating what the project is for, which carries the evidence of the hidden requirements; the milestone bootstrap is not run, because the cairn chain runs it itself and the manual deliveries must not read its workflow guidance), is built from `seed/` as an orphan commit with no ancestor on `main`, and is tagged once. A first-prompt run branches from that tag; a second-prompt run branches from the tip of the first-prompt run it continues. Once `main` carries results, a branch taken from it would put earlier runs' output into the agent's working tree, so `main` is never a branch point.
- **Every run works in a clone that cannot see the other branches.** Cairn's starting-state skill and a manual agent may both read git history or the branch list, so in a shared checkout run 5 could read run 1's solution. Each run starts as a fresh single-branch clone of its branch point, with no tags and with the remote removed after cloning, at a path unique to that run; on completion the run script adds the remote back and pushes the branch to the canonical repository as `run/<id>`. The clone is not shallow: a second-prompt run legitimately sees its own first-prompt history, and that history is the same for every scenario's second prompt.
- **Run branches are never git-merged into `main`.** Every run edits the same files, so merges would conflict and the merged tree would mean nothing. The branches stay as the record of each run (its history and commit subjects are process metrics). `main` receives a snapshot of each run's deliverable under `runs/<id>/`, written with a read-tree prefix from the run branch, plus one manifest per run under `results/<id>/`. Publishing `runs/` through GitHub Pages then makes every artifact playable by URL.

### Structure of `main`

`main` holds four kinds of content. Each kind lives in its own top-level area, and the kind decides the rules the area follows; the concrete file names follow from the rules.

```
inputs       what a run is given        seed source, raw prompts, hidden requirements, scenario definitions (deliveries, model strategies), the plugin under test
harness      how a run is executed      the run procedure, the seed builder, the index generator, the analysis
records      what a run produced        per id: a published snapshot, and an unpublished manifest with the invocation outputs
evaluation   what people concluded      blind ratings keyed by id, and the analysis output
```

Root-level housekeeping (the README, the instructions for working on the harness, the publishing workflow) is a fifth, incidental kind: it is never part of the seed and no run ever sees it.

**Inputs** are of two kinds. The shared inputs (the seed source, the raw prompts, the hidden requirements) are what a difference between scenarios must never be attributed to, so they are byte-identical across scenarios and recorded by content. The scenario definitions (the deliveries, the model strategies, and the plugin commits the cairn deliveries name) are what a difference is attributed to, so each is stored under its id and read back from there by the analysis.

- Every shared input is versioned by content, not by name: a run's manifest records the seed as a tag and each prompt as a blob hash. Changing any shared input starts a new comparison set; the analysis groups runs by their shared-input versions before it compares scenarios.
- The seed source is the one input a run does not read in place. The harness turns it into an orphan commit and tags it; runs branch from the tag, never from the source directory. It contains nothing produced by Cairn: any Cairn artifact a run needs is created by the cairn chain's own bootstrap line, so the seed is the same for all scenarios without leaking the plugin's guidance into the manual ones. Its README is the one place the hidden requirements' evidence lives, and nothing in it states them.
- The plugin under test is an input like any other: each cairn delivery names one commit (a release or a candidate), which the harness checks out into a plugin checkout used by that delivery's runs only, loaded per invocation and never installed at user level, so the manual scenarios cannot see its skills. Several cairn deliveries may name several commits, one checkout each.
- A delivery definition is a list of fixed messages and, for a cairn delivery, the plugin commit, nothing else, with one exception: the stakeholder's turn of the assess delivery is a fixed instruction the harness completes with the hidden requirements of the prompt being run, so its brief is versioned by the hidden-requirement entries it is composed from. A model strategy is the model and effort per message. Every other flag (permissions, output format, plugin directory) is added by the harness, so each setting a run executes under is set in exactly one place: the strategy for model and effort, the harness for the rest. The multi-prompt control is the one definition not stored: it is derived from the cairn scenario its id names at run time, so the two can never drift.
- A hidden requirement is an input too: one entry per prompt stating the requirement, the seed evidence it rests on, and the check a rater applies, keyed to the seed tag and the prompt blob. No run sees the entry; the rating instructions carry its check line.

**The harness** is the only writer of the record areas. It sees the whole repository; a run sees only its clone. A harness change must not change what a run sees or is given; a change that would (a different flag, a different continuation message) is an input change and is versioned as one.

**Records** are append-only: one directory per id in each record area, one commit per run, never hand-edited except for the manifest's entry-point field. The published half is exactly the snapshot of the run's tree (the `runs/<id>/` of the three conditions above); the unpublished half is everything that ties the id to a scenario, cost, or branch (the `results/<id>/` manifest and the per-invocation outputs). The two halves are separate top-level directories so that publishing is "this directory and nothing else".

**Evaluation** is keyed by id only. Rating files carry no scenario, and the join between ratings and manifests lives in the harness's analysis step, so blindness is a property of where the join is allowed to happen, not of rater discipline. A rating file carries the experience score and, as separate lines, the hidden-requirement checks, so the two are never folded into one number.

### Git objects

- `main` is linear and holds the harness plus the records. Each completed run adds one commit touching only `runs/<id>/` and `results/<id>/`, under the fixed subject `Run: <id>`; harness changes are separate commits.
- `seed/v<K>` tags point at orphan commits built from the seed source. They share no history with `main`, so a run's clone contains nothing but the seed tree and its own work.
- `run/<id>` branches are rooted at a seed tag (prompt 1) or at the tip of the parent run's branch (prompt 2). They are never merged, rebased, or deleted. A cairn scenario's history is one commit per skill or task under Cairn's own subjects; a manual scenario's history is whatever the agent chose to commit, which is itself a result.
- The canonical repository is the GitHub remote. Working clones live outside it, under one scratch directory with one subdirectory per id, and are deleted once the run's commit on `main` exists.

### One run

The run procedure, invoked with a scenario id, a prompt index, and for a second prompt the parent run's id, is the whole procedure; nothing about a run is done by hand.

1. **Id.** Draw an opaque id (eight characters from a random source). Refuse it if `runs/<id>` or `run/<id>` already exists.
2. **Pre-flight.** Assert: the benchmark checkout is on `main` and clean; the scenario id resolves to a stored delivery and a stored model strategy (or, for the multi-prompt control, to the cairn scenario it mirrors) and the strategy assigns a pair to every message of the delivery; `--from` is given exactly when `<n>` is greater than 1, and the parent's manifest is for prompt `<n>-1` and the same scenario; the cairn plugin is not installed at user level (so the manual scenarios cannot see its skills); no memory directory exists for the clone path (see "Clearing memory").
3. **Clone.** Single-branch, no tags, from the seed tag or from `run/<parent-id>`, into the run's unique path. Remove the remote. Create `run/<id>` from the checked-out commit.
4. **Prompt.** Write the prompt `<n>` text over `PROJECT.md` at the clone root, replacing whatever the file held (for prompt 1 the seed has none; for prompt 2 it holds prompt 1, which stays readable in the branch history), and commit it under the fixed subject `Prompt: <n>`. This commit is identical across scenarios and is the first commit of every run branch after its branch point; the harness makes it, so the agent never sees the prompt outside the repository.
5. **Invocations.** For each message of the delivery's list, in order, run from the clone, with `<model>` and `<effort>` the pair the strategy assigns to that message:

   ```
   claude -p "<message>" --dangerously-skip-permissions --model "<model>" --effort "<effort>" --output-format json
   ```

   A cairn delivery's lines add `--plugin-dir` pointing at the checkout of the commit the delivery names. The assess delivery's stakeholder turn is composed, recorded, and checked as its section states. Stdout is written to the run's invocation outputs under `results/<id>/`, one file per invocation in chain order, with stderr and the model and effort the invocation ran under beside it. A non-zero exit stops the chain; the run is still recorded, with the manifest stating how many invocations were made, because an early stop is a result, not a failed measurement.
6. **Push.** Add the remote back and push `run/<id>`.
7. **Snapshot.** On the benchmark checkout, read the run branch's tree into `runs/<id>/` with a prefixed read-tree and check the files out.
8. **Manifest.** Write the manifest under `results/<id>/` from the invocation outputs and the environment.
9. **Memory.** Delete the memory directory keyed by the clone path and assert it is gone.
10. **Commit.** Regenerate the index page, then commit `runs/<id>/`, the index page, and `results/<id>/` on `main` as `Run: <id>`. Delete the clone.

### The manifest

The manifest is the only place that ties an id to its scenario. Everything the analysis needs is in it or in the invocation files beside it:

```json
{
  "id": "k7f3q2xd",
  "scenario": {
    "id": "cairn_1_8_3_yolo_models_strategy_1",
    "delivery": "cairn_1_8_3_yolo",
    "model_strategy": "models_strategy_1"
  },
  "prompt": { "index": 1, "file": "PROJECT.md", "blob": "<git blob sha of the committed PROJECT.md>" },
  "parent": null,
  "seed": "seed/v1",
  "branch": { "name": "run/k7f3q2xd", "tip": "<sha>", "commits": 23 },
  "host": { "binary": "claude", "version": "2.1.283" },
  "plugin": { "path": "<plugin checkout>", "commit": "<sha>", "version": "1.8.3" },
  "user_config": { "claude_md_sha256": "<sha>", "settings_sha256": "<sha>" },
  "entry": "index.html",
  "started": "<iso timestamp>",
  "finished": "<iso timestamp>",
  "invocations": { "planned": 10, "made": 10, "stopped_early": false },
  "totals": { "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "duration_ms": 0 }
}
```

- `scenario.id` is the scenario the run executed, and its two parts are the keys the analysis groups by. `plugin` is null for a manual delivery. `parent` is the id of the first-prompt run a second-prompt run continues, always of the same scenario.
- The model and effort of each invocation live in the invocation records, as the strategy assigned them; the manifest names the strategy and does not restate them. `totals` are sums over the per-invocation JSON files, which keep the per-invocation figures; the manifest never restates those either.
- `entry` is the path a rater opens, relative to `runs/<id>/`. The run script detects a root `index.html`; a run that put its entry point elsewhere gets the value by hand, and that edit is the one hand-written field.
- `user_config` records digests of the user-level `CLAUDE.md` and settings that applied to the run, so a later re-run can check it ran under the same configuration.

### Hosting and blindness

- The Pages workflow uploads `runs/` and nothing else. The unpublished record half and the evaluation area exist only on `main`, so the mapping from id to scenario is never on the site.
- The index page under `runs/` is generated from the manifests and lists ids with their entry links, in an order shuffled once and fixed. It names no scenario or prompt.
- Raters receive the index link, play each entry, and record scores in the evaluation area, one file per rater, keyed by id. The join with the manifests happens only in the analysis step, after all ratings are in.
- Known limit: the snapshot is the whole tree, so a rater who browses past the entry point can see a cairn run's `milestones/` directory. Blindness holds for a rater who follows the entry links and plays; the rating instructions say so.

### Clearing memory

Clearing the assistant's memory is a step of every benchmark run, not a manual chore:

- Claude Code keeps an auto-memory directory keyed by the working directory path. The unique clone path gives each run a fresh memory directory, and the run script deletes that directory after the run completes, so no run can inherit from another and reused paths cannot leak.
- The run script also asserts, before the first invocation, that no memory directory exists for the run's path.
- User-level configuration (`~/.claude/CLAUDE.md`, settings) applies to every scenario equally and is not cleared, but its content is recorded with the results so a later re-run can reproduce it.

## How Cairn development uses the benchmark

The benchmark measures Cairn, and Cairn's development reads the measurement. That is the whole relation, and it runs through two channels only: a plugin commit goes in as an input, and metrics keyed by that commit come out as records. The benchmark never imports Cairn's test suite or build tooling, and Cairn never imports the harness; neither repository has the other as a dependency, and a change on either side that would need one is a design error.

Four uses are adopted now:

- **Any commit is a valid plugin input.** A cairn delivery names a commit, not a release, and the manifest records it as such. A Cairn branch is benchmarked before it merges by defining a cairn delivery whose version segment is that branch's short commit; the analysis groups runs by plugin commit, so a candidate and the release it would follow are compared like any two versions, under the same model strategy. Nothing else in the run procedure changes.
- **A cairn scenario alone yields process metrics that need no rater.** The invocation outputs and the run branch of a cairn run carry signals the harness reads directly: whether the chain completed or where it stopped, questions surfaced per review pass and whether a hidden requirement is among them, alternatives and recommendations the annotating passes reported as skipped, anomalies the answer sweep reported, tasks derived, token cost per skill, and for the assess delivery the stand-in's report of which hidden requirements were surfaced, covered, and answered. A development check runs one cairn scenario only, with no manual scenarios and no rating, and reads these out. This is the fast loop: it costs one chain per candidate commit and gives a result the same day.
- **Cairn's design claims are the metric contract.** Cairn's `docs/design-claims.md` lists its claims, each with a named metric, and states that only one is tested. The analysis implements the subset of those metrics its data reaches, each as a function over manifests and run branches, and reports them per plugin commit. The planted gaps of claim 1 are the "deliberately left open" list under each prompt, so that claim is measurable from the first run. The hidden requirements test claims 1 and 4 together, as the one case where a surfaced question and a project-grounded answer have a right outcome to check against. A Cairn milestone that changes behaviour names the claim it expects to move, and the next run against its commit confirms or refutes it. The link between the repositories is this document on one side and the analysis on the other, never code.
- **Ablation deliveries attribute value to single skills.** A delivery is a message list, so a chain without the starting-state skill, a chain without the recommendation pass, or a chain with two review passes is one more delivery under its own id (`cairn_1_8_3_yolo_no_starting_state`), paired with the same model strategy, which assigns by message and so covers whichever lines the ablation keeps. Comparing an ablated chain to the full chain under one strategy says whether one skill earns its cost, which the primary scenarios cannot say. An ablation that needs the turn-count control gets its own multi-prompt scenario, derived as always from the cairn scenario it mirrors.

Two uses are the intended ones once ratings exist:

- **Release gate.** Before a version is cut, the candidate's cairn scenario and its manual controls run on the same inputs and are compared to the previous release's scenarios under the same model strategy. This is the slow loop. It becomes a gate rather than a report only once a baseline and a threshold are stated; until then the comparison is published next to the release notes.
- **Published trend.** Once all ratings for a comparison set are in, the per-scenario aggregates per plugin commit can be published without weakening blindness, because the join is complete and no rater is still working. Cairn's changelog links to the trend for each release.

Two more are deferred as conventions rather than design: triaging a bad cairn run into a Cairn milestone goal that cites the run id, and dispatching a benchmark run from Cairn's release workflow. Both cost money or process on every use and wait until the fast loop is stable.

## Benchmark project requirements

The selected project is Closest Wins, described in the next section. It was chosen against these requirements, which any replacement project has to meet as well:

- **Experienceable.** The result must be something people can "experience" being better, not only read about. One example is a browser mini game that people can quickly play and compare, but any deliverable a person can use and judge in a few minutes qualifies. A rater is usually alone, so one person must be able to play every role the deliverable has.
- **Zero-install delivery.** Experiencing an artifact costs one click or one command with no build step, no dependency install, and no account. Each snapshot under `runs/<id>/` must be usable as it is, so it can be hosted or opened directly.
- **Two sequential prompts.** The benchmark consists of at least two raw prompts run in order: the first builds the project, the second extends or changes it. Each scenario runs both prompts, the second starting from that scenario's own result of the first. A single-shot build is where Cairn's advantage is smallest; the second prompt is where recorded decisions and starting-state analysis are expected to show. Both prompts follow the "raw prompt" rules above.
- **Real decisions, no canned solution.** The project must not be one whose complete solution is a well-known exercise that a model reproduces from memory. Its rules or behaviour must require genuine design decisions in the places the raw prompt leaves underspecified, so that the scenarios can diverge on what they decided, not only on how well they typed.
- **One milestone per prompt.** Each prompt must be completable within one Cairn milestone under every model strategy the benchmark pairs with a cairn delivery, so that a cairn scenario's chain runs once per prompt and the scenarios stay comparable in size.
- **Room for a hidden requirement.** Each prompt must have at least one place where an unstated expectation becomes visible in the artifact, and the seed must be able to carry evidence for it that reads as a natural description of the project rather than as a planted instruction.

## Benchmark project: Closest Wins

Closest Wins is a host-run quiz for one big screen, made for this benchmark. Its fixed part is a short flow the host drives from team setup to final standings, so every scenario builds against the same specification and a rater can check it by eye; everything around the flow is left open, and the questions the game asks are each scenario's own to write, which is where the hidden requirement of each prompt shows.

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
- **Not a canned solution, with a caveat.** The exact flow, with no answer entry and a host-judged award, matches no named exercise. It does sit nearer the common quiz-app genre than a novel ruleset would, so the manual scenarios may produce more uniform output, and the planted gaps and the hidden requirements carry more of the comparison than the rules do.
- **Room for hidden requirements.** The questions are the scenario's to write and the storage of a prepared set is the scenario's to choose, so each prompt has a place where an unstated expectation shows in the artifact.
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

The second raw prompt, written over `PROJECT.md` for prompt 2, extends each scenario's own result of the first:

```
Let the host write their own questions for Closest Wins and keep them for the
next party.
```

Deliberately left open: whether the editor is part of the same file, whether the built-in questions stay and whether the host chooses a set at the start, how answers stay off the big screen while the host edits, what validation an answer gets, and whether a set can be changed between questions. This is where the recorded decisions from the first milestone are expected to matter: a scenario that recorded how its questions are represented and whether anything persists extends those decisions; a scenario that did not has to rediscover or contradict its own behaviour.

Hidden requirement: a set prepared on one computer plays on another. Evidence: the README's host who prepares at home and plays from the hall's laptop. Check: the rater moves a prepared set to a fresh browser profile and plays it; a set kept only in browser storage fails.

### Fit with the run rules

Each prompt is one milestone: the game is a single file with a six-step flow and ten questions, and the editor is one feature on top of it. Both reach every scenario as the same committed `PROJECT.md` and are versioned as its blob hash in the manifest; the hidden requirements are keyed to that hash and the seed tag. The artifact is one HTML file, so `entry` is the root `index.html` whenever the scenario named it that, and the snapshot under `runs/<id>/` is playable from GitHub Pages with one click.
