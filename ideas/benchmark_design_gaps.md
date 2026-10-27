# Design gaps in the Cairn benchmark draft

Date: 2026-10-26
Subject: `ideas/benchmark_for_cairn.md` (572 lines, last changed in `8d93140`)

This report lists the design gaps found in a full read of the draft. Its claims about Cairn were checked against the skills and tools in this repository. Line references such as `:523` point into `ideas/benchmark_for_cairn.md` unless another file is named.

The draft is careful within itself. The gaps below are ordered by how much they change what the benchmark's headline number means. Gaps 1–4 change it directly.

## Summary

| # | Gap | Effect |
|---|---|---|
| 1 | The left-open lists and the implied-requirement lists contradict each other | The implied axis scores taste and penalises minimal choices |
| 2 | No manual baseline gets a stakeholder turn | The assess delivery's gain over manual can't be attributed to Cairn |
| 3 | The operator's disclosure rule has a catch-all loophole | The hidden axis can measure "asked a vague question" |
| 4 | Isolation covers git only, not the filesystem or the network | Hidden requirements and earlier artifacts are reachable from a run |
| 5 | A skill that stops on its own check looks like a success | Empty milestones get closed and recorded as complete chains |
| 6 | Infrastructure failures are scored as results | Usage limits and API errors bias scores against the heaviest delivery |
| 7 | The rater's repeatability is claimed, not measured | Rater noise enters every axis and the lost count |
| 8 | The rater can miss files in multi-file artifacts | Editor lines fail as "not proved" |
| 9 | The YOLO chain and `models_strategy_1` don't match Cairn's usage docs | The benchmark doesn't measure Cairn "as it is used" |
| 10 | Milestone 1's recorded goal changes meaning in phase 2 | The phase-2 advantage the draft predicts is undermined |
| 11 | No sample size, no uncertainty, and the radar favours Cairn | Margins can be noise, and the selection is biased |
| 12 | What makes up a comparison set is unclear | Results from different conditions get mixed |
| 13 | Concurrent runs would collide | The run procedure only works one run at a time |
| 14–18 | Smaller points | Calibration, contamination, retired results, phase-2 operator, wording |

## Gaps that undercut the headline result

### 1. The left-open lists and the implied-requirement lists contradict each other

**Where:** `:27`, `:523` against `:527–539`; `:552` against `:554–566`; `:51`; `:253`.

Line 27 defines a gap as a decision with several defensible answers. Most of prompt 1's left-open items (`:523`) come back as implied-requirement lines that accept only one answer:

| Left open at `:523` | Implied line that scores one answer |
|---|---|
| whether teams get names or only numbers | `:529` the teams can be given names |
| whether an award can be undone | `:532` an award can be taken back or corrected |
| whether a question can be skipped or revisited | `:533` a question can be skipped |
| whether progress through the list is shown | `:534` the question's number out of ten is shown |
| mouse versus keyboard for the host | `:536` keyboard as well as mouse |
| whether a reload loses the game | `:537` a reload does not lose the game, or warns |

Prompt 2 does the same:

| Left open at `:552` | Implied line |
|---|---|
| whether the built-in questions stay | `:560` the built-in questions survive |
| whether the host chooses a set at the start | `:561` the host chooses which set to play |
| what validation an answer gets | `:558` an answer is checked to be a number |

**Why it matters:**
- The implied axis ends up rewarding more features. Choosing whether to have a feature at all is a decision the draft itself lists as open, so scoring it is scoring taste, which `:253` says the benchmark never does.
- A recommendation that sensibly picks the minimal option (for example "mouse only" or "no undo") loses points.
- On these same questions the operator answers "your call" (`:51`). A run is then graded on a preference the stakeholder said they don't have.
- Both lists are written by Cairn's author, who knows which questions Cairn's review pass raises. A sceptical reader will see the overlap as tilting the axis toward Cairn.

**Fix:** put each item in one list only. Line `:33` already applies this rule to hidden requirements ("a line in either list would score it twice"); extend it to the left-open and implied lists.

### 2. No manual baseline gets a stakeholder turn

**Where:** `:81`, `:156`, `:42`.

The assess delivery's advantage over the manual deliveries mixes two causes: Cairn surfacing the right question, and the run simply having a planned question-and-answer turn with the stakeholder. The multi-prompt control copies only the planned messages and has no counterpart to the turn (`:81`), and `:156` admits that this comparison "folds the turn in with Cairn's structure".

In practice, headless `claude -p` sessions rarely end by asking a question, so a manual run almost never uses the reactive turn. The manual route to the hidden knowledge is mostly theoretical.

**Why it matters:** the draft's core principle (`:11`) is that a difference between scenarios is attributed only to what differs between their definitions. Assess against manual differs in two things at once, and nothing separates them.

**Fix:** add a delivery such as `manual_clarify_then_build`:

1. "Read PROJECT.md and list the questions you need answered before building."
2. A planned operator turn that answers the list under the same disclosure rule.
3. The usual one-sentence instruction pointing at PROJECT.md.

That is the honest manual counterpart to the assess delivery.

### 3. The operator's disclosure rule has a catch-all loophole

**Where:** `:52`, `:42`.

The operator discloses a hidden requirement in reply to "a question whose answer the statement changes" (`:52`). "Anything else I should know before I start?" meets that test, since the hidden statement changes its answer.

The draft also doesn't say who decides whether a session's final message is a question that needs a reply or one that "closes with an offer" and gets none (`:42`). That decision is a model judgment, and it isn't recorded.

**Why it matters:** the hidden-requirements axis would partly measure whether a model happened to end with a vague question, not whether the process surfaced the right one.

**Fix:**
- A question counts as bearing on a requirement only if it names the requirement's subject (for example the questions' topic, or where a prepared set is kept).
- Catch-all questions get nothing beyond what PROJECT.md says.
- Every classification (reply or no reply, and why) goes into the operator's record.

### 4. Isolation covers git only, not the filesystem or the network

**Where:** `:288`, `:310`, `:324`, `:331`, `:337`, `:371`, `:401`.

Runs use `--dangerously-skip-permissions` directly on the host machine. The draft's isolation conditions are about git (single-branch clone, no tags, no remote). From its clone, an agent can still read:
- the benchmark checkout, whose inputs area holds the hidden-requirement statements (`:310`);
- sibling clones in the shared scratch directory (`:324`);
- other runs' session transcripts under `~/.claude/projects`.

Web tools are enabled too. Once the Pages site and the public run branches exist, a web search for "Closest Wins" finds earlier artifacts and the repository holding the hidden requirements.

The pre-flight only checks that Cairn isn't installed at user level (`:331`). Every other user-level plugin, MCP connector and hook still loads into every run, manual and Cairn alike. `user_config` stores only digests of the user configuration (`:371`), which can detect a change but can't recreate the configuration on another machine.

The maintainer's earlier notes record that Docker Desktop blocks these runs on this Mac, so the draft also needs to say where runs execute.

**Fix:**
- A dedicated `CLAUDE_CONFIG_DIR` for the benchmark, with no plugins other than the one passed by `--plugin-dir`.
- `--strict-mcp-config` and `--setting-sources` to shut out the user's MCP servers and settings.
- `--disallowedTools WebSearch,WebFetch`.
- A separate OS user or VM that can't read the benchmark checkout or other clones.
- State the execution environment (OS, tools on `PATH`, browsers) as a versioned shared input.

## Gaps in what the harness records

### 5. A skill that stops on its own check looks like a success

**Where:** `:42`, `:204`, `:210`, `:346`, `:383`.

When a Cairn skill stops because its preconditions aren't met, `claude -p` still exits 0. The harness treats only a non-zero exit as a stop (`:346`), and the reply rule tells it to carry on past a message that reports a stop (`:42`). The result can be a closed, empty milestone:

1. One question's alternatives never land, so it gets no recommendation.
2. The answer sweep leaves it standing, so `derive-tasks` refuses to run.
3. `complete-all-tasks` finds nothing to do.
4. `finish-current-milestone` succeeds, because it only checks that `TASKS_TODO.md` holds no sections (`core/skills/finish-current-milestone/SKILL.md:34`).

The manifest still reads 11/11 invocations made (`:383`), which the draft says "reads how far the chain got". The phase-2 text (`:210`) assumes a stopped chain leaves the pointer on milestone 1, which only happens on a non-zero exit.

**Fix:** Cairn's skills already print fixed status lines. The harness can match each invocation's final message against them, detect the first stop, and record it in the manifest (for example `invocations.first_stop`).

### 6. Infrastructure failures are scored as results

**Where:** `:346`, `:234`; `docs/ways-of-using-cairn.md` (section "Executing tasks").

"An early stop is a result, not a failed measurement" (`:346`). That also covers hitting the account's usage limit, API overload, and network errors. `docs/ways-of-using-cairn.md` itself warns that `complete-all-tasks` can hit the usage limit and says to re-run it after the window resets.

Cairn spends the most tokens, so it is the most likely to hit those limits. Counting such failures as results biases scores against it. Scenario invocations also have no time or turn limit, though the rater has one (`:234`), so a runaway session can hold a run open indefinitely.

**Fix:** classify how each invocation ends (completed, behavioural stop, infrastructure failure). Retry infrastructure failures a fixed number of times, or void the run. Add a per-invocation timeout.

### 7. The rater's repeatability is claimed, not measured

**Where:** `:238`, `:241`, `:245`, `:255`.

Line `:245` says "a second rating of the same artifact gets the same number". That holds only for re-running a test that already exists. A new rating writes new tests for every line, and those tests can differ:
- A weak test (an "Undo" button exists) passes where a strict one (the award is actually reversed) fails.
- "Not proved" scores zero, which penalises artifacts that are hard for a browser test to drive, such as canvas-based UIs, regardless of what a human host could do.
- The lost count (`:255`) compares two independent ratings, the parent's and the child's. Rater noise therefore shows up as lines lost or gained even when the behaviour didn't change.

**Fix:**
- A calibration set of reference artifacts with known verdicts per line, including deliberately broken ones. Each rater version must reproduce those verdicts before it is used.
- Rate a sample of artifacts twice and report the agreement.
- Give each checklist line a short spec of what its test must check, so tests written by different ratings check the same thing.

### 8. The rater can miss files in multi-file artifacts

**Where:** `:236`, `:328`, `:384`, `:552`.

The rater gets "a copy of the entry file and the files it loads" (`:236`). Prompt 2 deliberately leaves open whether the editor lives in the same file (`:552`). An `editor.html` reached only by a link isn't "loaded", so the rater never receives it and every editor line fails as "not proved". A saved set file next to the HTML is in the same position.

Setting `entry` by hand when a run didn't name its file `index.html` (`:384`) also contradicts "nothing about a run is done by hand" (`:328`). The person doing it opens the manifest, which names the scenario.

**Fix:** hand the rater the run's whole tree minus `.git`, `milestones/`, `CLAUDE.md` and `PROJECT.md`, and detect the entry automatically (for example the only root-level `.html` file, failing loudly otherwise).

## Gaps in whether it measures Cairn as it is used

### 9. The YOLO chain and `models_strategy_1` don't match Cairn's usage docs

**Where:** `:90–104`, `:162–177`; `docs/ways-of-using-cairn.md`.

The draft says the benchmark "measures Cairn as it is used, not under an allocation it was never meant for" (`:162`). Two things contradict that.

**The chain.** `docs/ways-of-using-cairn.md` says to repeat the review pass until `review-milestone-requirements` reports convergence. The YOLO chain runs review once. A delivery is a fixed list of messages, so it can't express "repeat until", and Cairn's own advice for a stuck milestone or a usage-limit stop can't be expressed either.

**The model strategy.** The draft says `models_strategy_1` is "written from Cairn's own usage snippets", but only 3 of its 12 rows match them:

| Message | Draft | `ways-of-using-cairn.md` |
|---|---|---|
| init, define, goto, finish | Sonnet 5.5, medium | Opus, high |
| specify, review, recommend, derive | Fable 5.1, xhigh | Fable, high |
| provide-alternatives | Opus 5.5, high | Opus, high (match) |
| answer sweep | Fable 5.1, high | Fable, high (match) |
| hand answers | Fable 5.1, high | Fable, high (match) |
| complete-all-tasks | Opus 5.5, high | Opus, xhigh |

**Fix:** align the table with the usage doc (or update the doc and say the strategy follows it). Give the delivery model a bounded loop, for example "repeat lines 5–8 up to K times until the review line prints its convergence line", and declare the bound as part of the delivery.

### 10. Milestone 1's recorded goal changes meaning in phase 2

**Where:** `:21`, `:94`, `:216`, `:222`; `core/tools/define_milestone.py:15`.

`define_milestone.py` writes the goal text under `## Goal` exactly as received (`core/tools/define_milestone.py:15`). Milestone 1's goal is therefore literally "Carry out the task described in PROJECT.md." Phase 2 overwrites PROJECT.md with prompt 2.

From then on, milestone 1's recorded goal points at prompt 2. The phase-2 starting-state pass, which the draft names as the step with no manual counterpart and the main source of Cairn's expected phase-2 margin (`:222`), reads a milestone 1 whose goal no longer describes what it built. This is also not how Cairn is used: real goals hold content, not a pointer to a file that later changes.

**Fix:** the harness puts the committed PROJECT.md text into the define line, so the milestone records the prompt itself. Manual runs still see the same text in the same file, so no scenario gets extra information. The rule at `:67` that no message carries prompt text would need a stated exception for this one substitution.

## Statistics and versioning

### 11. No sample size, no uncertainty, and the radar favours Cairn

**Where:** `:226`, `:248`, `:265`, `:411`, `:420`.

- **Sample size.** Runs per scenario is "as many times as the set calls for" (`:226`). No number is set and no stopping rule is given.
- **Uncertainty.** The ranking table has a runs column but no spread or confidence interval. The rank breaks ties by cost with no threshold below which two scores count as equal.
- **Selection bias.** The radar draws each family's *highest-ranked* scenario (`:420`), and the draft calls that what "makes the comparison fair". The best of several noisy scores is biased upward, and more so for the family with more configurations. Cairn will have many (versions × strategies); manual will have few. The selection therefore favours Cairn.
- **Weight of the hidden axis.** The hidden axis is two checks per run (one reading line out of ten in phase 1, one yes/no test in phase 2), yet it weighs a third of the overall score, the same as roughly 37 implied lines.

**Fix:** fix N per scenario before the first run. Report per-run spread or an interval beside every score. Pre-declare one configuration per family for the radar, or use the same number of configurations per family. Consider reporting the hidden axis beside the overall score rather than averaging it in at equal weight.

### 12. What makes up a comparison set is unclear

**Where:** `:55`, `:226`, `:234`, `:265`, `:369`, `:420`, `:455`.

The draft defines a comparison set as one seed tag and one version of each prompt (`:265`). But other things also change results:
- the operator version, which the draft says must start a new comparison set (`:55`);
- the rater version, which the analysis "groups by" (`:234`);
- the Claude Code CLI version, recorded in the manifest (`:369`). The CLI auto-updates, so a campaign that runs over several days spans versions.

The trend is followed "across comparison sets and plugin commits" (`:455`). That mixes changes to the inputs with changes to the plugin, against the attribution rule of `:7` and `:11`.

Nothing lists which scenarios a set must contain, so "complete" (`:226`) is undefined. The strongest manual strategy (for example manual at Fable 5.1 xhigh) can simply be left out, and the radar's claim to compare against "the strongest manual configuration" (`:420`) is only as good as what was run.

**Fix:** define a comparison set as seed, prompts, operator version, rater version and pinned CLI version, plus a declared roster of scenarios that must all be rated before it counts as complete. Keep the trend within one set by re-running earlier releases when inputs change.

### 13. Concurrent runs would collide

**Where:** `:226`, `:324`, `:331`, `:351`.

Phase 2 starts "as soon as the parent's `Run:` commit exists, with no wait on any rating or on any other scenario's phase 1" (`:226`), which implies runs in parallel. But every run's pre-flight requires the benchmark checkout to be on a clean `main` (`:331`), and every run commits to it (`:351`). Two concurrent runs would fail the check or race on the commit. Concurrent clones in the shared scratch directory can also read each other (gap 4).

**Fix:** either state that runs are sequential, or give each run its own worktree and serialise the `Run:` commit behind a lock.

## Smaller points

### 14. Hidden-requirement calibration hasn't been tested

**Where:** `:30`, `:239`, `:541`, `:568`.

- Line `:30` requires evidence that settles the question once asked, while the prompt alone gives no reason to ask. Prompt 1's "ten questions of its own" invites "what topic?", and zoo to animal questions is a one-step inference a model may make without asking. The axis may then measure whether the model read `README.md`, which `:30` rules out.
- Prompt 2's "keep them for the next party" already points at persistence, and an export/import feature is a common convention (backups). The hidden requirement sits close to an implied one.
- "About an animal" has borderline items, for example the zoo's visitor count or "how many animals live at Riverside Zoo". The reading line (`:239`) promises one defensible answer per item.
- Scoring is undefined if an artifact holds more than ten questions and draws ten per game.

**Fix:** a small pilot. Run the bare manual delivery a few times. If it nearly always meets a hidden requirement, the evidence is too strong; if never, too faint. Add a rule for artifacts with more than ten questions.

### 15. The public repo will leak into training data

**Where:** `:389`, `:466`.

Only the id-to-scenario mapping is kept off the Pages site (`:389`). `main` is a public repository, so the hidden requirements, operator records and every artifact are public. Future models will train on them, and the "no canned solution" requirement (`:466`) wears off over time.

**Fix:** keep the inputs and records in a private repository and publish only the snapshots and aggregates, or plan to rotate the project and hidden requirements. At minimum, state the risk.

### 16. Bad results can disappear

**Where:** `:405`.

The README shows only the latest complete comparison set (`:405`). A bump of the seed version replaces a bad result on the landing page. Nothing freezes the checklist and hidden requirements before the first scored run.

**Fix:** freeze the inputs before the first scored run, and keep every superseded set linked from the README with the reason it was superseded.

### 17. The phase-2 operator doesn't know the game

**Where:** `:51`, `:218`.

The operator's input is "the prompt text as committed" (`:51`), which in phase 2 is prompt 2 only. A phase-2 question about the game's existing flow reaches a stakeholder who doesn't know the game they asked for in phase 1.

**Fix:** in phase n, give the operator prompts 1 to n, while keeping only phase n's hidden statements.

### 18. Line 409 assumes the result

**Where:** `:409`, `:222`, `:420`.

Line `:409` says the table "shows that Cairn beats the other approaches". Lines `:222` and `:420` are careful to say the page draws whatever the data shows. `:409` should say the table shows *whether* Cairn beats them.

## Recommended order

Address 1–4 first, since each one changes what the headline comparison means. Then 5, 6 and 10, which decide whether a recorded run reflects what Cairn did. Then 7, 11 and 12, which decide whether a difference between scenarios is a finding rather than noise.
