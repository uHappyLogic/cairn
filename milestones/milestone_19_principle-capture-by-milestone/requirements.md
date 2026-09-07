# Milestone 19: Principle Capture By Milestone

## Goal

Rework `capture-milestone-principle-updates` into an argument-driven harvester: it requires a milestone id, drops the last-completed-row resolution, and infers that milestone's decision history itself from the answer commits on its `requirements.md` across all three provenances (`Manual-answer:`, `Alternative-answer:`, `Recommendation-answer:`), reconstructing from each commit's diff the recommendation and cited principles the user saw against the answer they recorded. Manual and alternative answers are the override signal: at capture time the skill asks the user why the alternative was preferred (offering its own best guess) and distills from those overrides the compact, intuitive guideline the recommender lacked, so future recommendations are accepted more often and manual or alternative answers become rarer. The store may shrink as well as grow: current reasoning takes precedence over an existing entry it contradicts, with capture pruning, merging, or generalizing entries, salvaging what it can from a decommissioned rule, and keeping each entry as short as it can be while still reading as an intuitive rule.

## Relevant starting state

### The capture skill as it stands

`skills/capture-milestone-principle-updates/SKILL.md` is argument-free. Step 1 resolves `<MILESTONE_DIR>` from the last row of the `## Completed Milestones` table in `milestones/README.md`, explicitly not via `shared/get-current-milestone.md`, because it is documented as a post-finish follow-up run after the pointer is `none`. Step 2 walks only `git log --grep='^Manual-answer: ' -- <MILESTONE_DIR>/requirements.md` and reads commit bodies. Phase 1 extracts keep/eliminate directives, drops non-generalizable ones, and clusters survivors; phase 2 walks them strongest-first, re-reads the whole store before each write, and offers the user a revise-vs-add choice per candidate by semantic overlap. The store can only be added to or have a single entry revised in place — there is no prune, merge, or generalize move. It commits under `Principle-capture: <milestone_id>` via `shared/commit-procedure.md`, path-scoped to the store, and reports `Principles captured.` or a one-line no-op. Its frontmatter description already reads "from a just-finished milestone's recorded decisions"; sibling skills that take a milestone id (`specify-milestone-starting-state`, `derive-tasks`, `review-milestone-requirements`, `recommend-all-open-questions`, `modify-milestone-goal`) take it as the directory name, e.g. `milestone_12_user-guide`.

### The principle store

`milestones/answer_decision_principles.md` holds four entries (`Prefer domain-neutral terms`, `Drop-vs-replace by ambiguity`, `Mutate live machinery last`, `Name by distinctive function`), each a `### <Short Title>` heading, a one-paragraph keep/eliminate directive of roughly 80–120 words, and an optional `*Origin:*` line naming the originating question. There is no status field; presence means confirmed. Its header paragraph names the consumers and states the file is written only by `capture-milestone-principle-updates`. All four entries were written by the retired per-answer capture skill during milestones 2–3; the finish-time skill has never run — there are zero `Principle-capture:` commits in the history, and the store's last content change was the milestone-8 header repoint.

### Answer commits and what their bodies carry

Every recorded answer is one commit touching `<MILESTONE_DIR>/requirements.md`, under one of three subjects. The commit body differs by provenance:

- `Manual-answer: <Short Title>` (`answer-open-question`): the body is the decision's rationale when deliberation was in context, otherwise the literal answer text verbatim; the skill never prompts for a rationale.
- `Recommendation-answer: <Short Title>` (single skill and the sweep orchestrator): the body is the lifted `<option> — <rationale>` text, i.e. the recommend agent's reasoning.
- `Alternative-answer: <Short Title>` (`answer-open-question-with-alternative`): the body is the chosen alternative's `<id> — <what-it-is>` text, with `<advantage>`/`<drawback>` excluded. No user rationale is captured anywhere on this path.

Counts across the history: 17 `Manual-answer:` (13 of them in milestones 6–7, before the recommend sweep existed), 66 `Recommendation-answer:` (milestones 8–17), 4 `Alternative-answer:` (milestones 11, 14, 17). Milestones 1–5 and 18 carry no answer commits at all under these subjects. No `Revert` commits exist, so the documented revert-then-re-answer correction flow has never been exercised.

### What an answer commit's diff preserves

Because `shared/answer-procedure.md` folds the decision into `## Decisions` and then removes the whole `<open-question>` block, each answer commit's diff carries as removed lines the full block the user saw: the `<question>`, every `<alternative id="...">` with its what-it-is text and `<advantage>`/`<drawback>` children, any `<applied-principle>` citations, and the `<recommendation option="...">` element with its rationale; the added lines are the new `## Decisions` entry and any cascaded removals. Comparing the removed `<recommendation option>` against the subject/body therefore reveals whether an answer accepted or overrode the recommendation, and which principle was cited when it was overridden. Across all answer commits, 19 `<applied-principle>` citation lines have been removed this way. Blocks answered before the sweep annotated them (all pre-milestone-8 manual answers) carry only `<question>` and no analysis.

### How the store is consumed

`shared/recommend-procedure.md` reads the store in place during grounding and treats a bearing principle as a weighted advisory factor that must be cited; the `recommend-open-question` agent renders each citation as an `<applied-principle>` sibling of `<recommendation>`, never inside it, so lifted answers stay provenance-free. The consumer side has no notion of principle weight, age, or retirement beyond presence in the file.

### Documentation surfaces that state the current grep boundary

The rule that capture harvests only `Manual-answer:` bodies is restated in: `CLAUDE.md` (the workflow map entry, the recommendation/alternative-answer provenance bullet, the correction-loop bullet, the skill-layer-commit bullet's "Still true" sentence, and the finish/capture bullet describing last-row resolution), `README.md` (the `## How skills commit` paragraph, the principle-learning bullets, and the skill-reference entries for `answer-open-question`, `-with-recommendation`, `-with-alternative`, and capture itself), and the commit steps of the three answer skills (`answer-open-question` says the subject exists so capture can collect it; the other two say their subject is never harvested). `finish-current-milestone` states it never invokes capture. The generated Antigravity tree under `.agents/plugins/cairn/` mirrors the skill file and is regenerated by `scripts/migrate_skills_to_agy.py`.

## Decisions

### Store rewrite confirmation

The store change is confirmed as a whole-store rewrite, once, at commit time. After the per-override rationale prompts, capture composes the entire proposed store — adds, revisions, prunes, merges, generalizations, and shortenings applied together — and writes it directly to `milestones/answer_decision_principles.md` in place, printing no diff and no store content to the conversation. The user reviews the working-tree change with `git diff` and requests changes in conversation; the skill re-edits the file in place each round. The single confirmation gates the commit, not the write: on acceptance the skill commits the store path-scoped under `Principle-capture:`, and on explicit rejection it restores the store from `HEAD` and takes the existing no-op path. This replaces the former per-candidate write-confirmation invariant.

### Repeat capture guard

A repeat run of capture against a milestone that already has a `Principle-capture:` commit warns and confirms rather than stopping or silently re-walking. The `Principle-capture: <milestone_id>` commit subject is the record that a milestone was ingested: before the commit walk, capture greps the history for that exact subject, anchored on both ends, and on a hit prints a one-line notice naming the prior commit and asks once whether to proceed; with no hit it runs unchanged. No empty commit is written to record a no-op run, so a prior run that changed nothing (an empty commit range, a composed store identical to `HEAD`, or a rejected rewrite) is not detected; this gap is accepted as harmless.

### Milestone id argument shape

The required argument is the milestone directory name under `milestones/` (e.g. `milestone_19_principle-capture-by-milestone`), exactly as `specify-milestone-starting-state` takes it, resolved as `milestones/<milestone_id>/` with a clean stop when that directory has no `requirements.md`. The value is consumed verbatim in three places: the path-scoped git-log prefix, the `Principle-capture: <milestone_id>` commit subject, and the repeat-capture guard's anchored grep for that exact subject. No bare-number form is accepted and no number-to-directory resolution exists.

### Non-override manual answers

A `Manual-answer:` whose removed block carried no recommendation to override — every pre-sweep answer, and any question the recommend sweep never annotated — is still a principle source. Capture distills candidates from its body rationale alone, exactly as the current phase-1 extraction does, because a decision the recommender never got to weigh in on is precisely a guideline it lacks. The override distinction shapes only the diff-comparison and prompting steps, never source eligibility; the existing non-generalizable filter continues to drop bare cold answers.

### Role of accepted recommendations

`Recommendation-answer:` commits, where the user accepted the recommendation as-is, are used only as evidence about entries already in the store, never mined for new principle candidates. A removed `<applied-principle>` citation counts as reinforcement of that entry and shields it from being pruned or narrowed in the same pass, and an accepted rationale that contradicts an existing entry flags it for the prune, narrow, generalize, or salvage path. New principles continue to come solely from the override commits: an accepted recommendation carries the recommender's own reasoning, so it cannot supply the guideline the recommender lacked, while both evidence signals fall out of the per-commit diff read capture already performs.

### Override rationale prompting scope

Capture prompts for the override reason only where the commit body carries no user rationale: every `Alternative-answer:`, and a `Manual-answer:` whose body is the bare literal answer with no stated reason, judged by the same bare-cold-answer test phase 1 already applies. A deliberated `Manual-answer:` body is read as the user's own answer to the why and is never re-prompted. Each prompt shows the skill's best guess at the override reason and can be skipped individually, and the run opens with a one-shot choice to accept every guess or to skip every prompt, so a backfill run over an older milestone the user no longer remembers stays workable. Misclassifying a thin-but-real rationale as deliberated is accepted: the body still surfaces in the composed store rewrite the user reviews with `git diff` before the commit is confirmed.

### Milestone eligibility

Capture runs against any milestone id whose `milestones/<milestone_id>/requirements.md` exists, the current and any unfinished milestone included, and never consults the Completed Milestones table. The id is validated by directory existence exactly as the sibling milestone-id skills do, and the path-scoped git log is the only boundary on the harvest. Because every answer commit lands during the requirements phase, finish status carries no information the harvest needs; a run against a milestone whose questions are still being answered simply harvests what exists so far, and a later pass re-walks the same path to pick up the rest.

### Entry compactness bar

Entry compactness is a soft numeric target held under the qualitative bar, not a hard cap. A directive should run roughly 40-80 words and is flagged for shortening when it exceeds about 100, while the goal's "as short as it can be while still reading as an intuitive rule" test remains the deciding standard, so a rule may keep a condition or corollary it genuinely needs. There is no ceiling on entry count; prune and merge by contradiction and overlap are the count control. The optional `*Origin:*` line survives as a single-line pointer to the originating question, because that case is what a revise-vs-salvage judgment and a human auditor read.

### Salvage form for contradicted entries

When current reasoning contradicts an existing entry, all four salvage forms are permitted and are attempted in a fixed preference order: narrow the entry's scope clause, generalize it so both the prior accepted citations and the override fit, replace it with a fresh directive when its premise is wrong, and delete it only when nothing survives. Narrowing leads because every entry already opens with an explicit scope clause, and the ladder as a whole is what the goal's mandate to prune, merge, generalize, and salvage what it can asks for. When two forms fit equally, the tie-break is whichever yields the shortest entry that still predicts both the prior accepted citations and the override. The chosen form is visible in the working-tree change the user reviews before the rewrite is committed.

### Skill framing after decoupling

Capture is documented as an on-demand skill — runnable for any milestone id at any time, with backfill over milestones already finished explicitly allowed — while keeping its home in the "Ending a milestone" stage behind the existing dashed optional edge. Finish is stated as the natural moment to run it, because a milestone's answer set is complete then, and never as a precondition. Every surface that mentions the placement, README.md and CLAUDE.md alike, must phrase it as a convention rather than a requirement, so the documented contract matches the required-id contract and does not drift back toward the pointer-none design.

### Answer agreeing with recommendation

A `Manual-answer:` or `Alternative-answer:` that records the same option the removed `<recommendation option>` named counts as an acceptance for the prompting and evidence steps only: no override prompt is shown, and its removed `<applied-principle>` lines reinforce the cited entries exactly as an accepted recommendation's do. Source eligibility is untouched by the agreement test and stays governed by the existing bare-cold-answer filter, so a deliberated agreeing `Manual-answer:` body still yields candidates while an agreeing `Alternative-answer:`, whose body is only the alternative text, yields none. Agreement is the common case for manual answers in this repo, so the false-premise prompt must be suppressed, but suppressing candidate extraction along with it would contradict the recorded "Non-override manual answers" decision and discard the deliberated rationale those commits carry. Capture therefore runs two tests per commit: agreement against the removed recommendation, then the deliberated-vs-bare body test.

### Untouched entry rewrite scope

Substantive change to an entry — adding, pruning, narrowing, generalizing, or replacing what it decides — still requires the harvested milestone's own evidence, but the composed whole-store rewrite may additionally apply form-only hygiene to any entry: shortening one past the roughly 100-word flag and merging two that plainly duplicate each other, with the applied test unchanged. Evidence gates what a rule decides, not how tersely it is written, and because the rewrite is already composed as one working-tree change the user reviews with `git diff` before the single commit confirmation, letting the compactness bar and the merge move reach untouched entries costs no extra mechanism while every substantive change stays anchored to a harvested override.

### Dirty store precondition

Capture imposes no clean-store precondition. When `milestones/answer_decision_principles.md` already carries uncommitted changes at the start of a run, capture prints a one-line notice and asks once whether to proceed — the same notice-plus-single-confirmation shape as the repeat-capture guard, never a stop — so the documented hand-edit escape hatch for pulling an actively-wrong principle stays usable. On proceed, the working-tree file rather than `HEAD` is the baseline the whole-store rewrite composes over, and capture takes a snapshot of the store immediately before its first write. The rejection path restores that snapshot instead of restoring from `HEAD`, refining the "Store rewrite confirmation" decision so rejection is lossless in the dirty and clean cases alike (in the clean case the snapshot simply equals `HEAD`), and it then exits explicitly without committing rather than falling through to `shared/commit-procedure.md`'s dirty-own-path guard, which would otherwise commit the user's surviving edits under `Principle-capture:`.

### Capture commit body content

The `Principle-capture: <milestone_id>` commit carries a body of one short line per store change, each naming the change kind — add, revision, prune, merge, or generalization — and the Short Title of the override answer commit that drove it. With the console silent and the store keeping no changelog, the commit body is the only surviving place for the why behind a prune or merge, and this project already uses commit bodies for exactly that kind of non-diff-derivable context. The rule is flat rather than scoped to the change kinds the store does not self-record: the redundancy it costs is one line per add, whose `*Origin:*` line already names its question, while the ambiguity it avoids — adjudicating whether a merge that folds a new override into an existing entry counts as an add or a retirement — is real. Because the store change is composed as a single whole-store rewrite the user may revise over several `git diff` rounds, the body is composed at commit time against the final rewrite so it cannot drift from the diff it describes.

## Out of Scope

## Open questions

