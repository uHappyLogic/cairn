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

## Out of Scope

## Open questions

<open-question id="Untouched entry rewrite scope" status="deferred">
  <question>May the composed store rewrite shorten, merge, or generalize entries that no commit of the harvested milestone bore on, such as a pre-existing entry over the 100-word flag, or does it change only entries the evidence of that milestone reached plus new adds?</question>
  <alternative id="Evidence-scoped only">
    The composed rewrite may change only entries this milestone&apos;s evidence actually reached — the override commits, the contradicting accepted rationales, the reinforcing applied-principle citations — plus new adds; every other entry is copied through byte-identical.
    <advantage>Every store change is traceable to a specific harvested commit, so a run&apos;s diff is bounded and explainable, and the whole-store rewrite stays a pure function of the milestone it was pointed at.</advantage>
    <drawback>The compactness bar and the merge move can never reach the store&apos;s oldest entries, which are exactly the stalest — the four entries written by the retired per-answer skill, one of them already past the 100-word flag, would stay untouched until some future milestone happens to contradict them.</drawback>
  </alternative>
  <alternative id="Form-only hygiene beyond evidence">
    Substantive change — adding, pruning, narrowing, generalizing, replacing what an entry decides — still requires this milestone&apos;s evidence, but the composed rewrite may additionally apply form-only hygiene to any entry: shortening one past the roughly 100-word flag and merging two that plainly duplicate each other, with the applied test unchanged.
    <advantage>It makes the compactness bar and overlap control enforceable across the whole file rather than only on the slice a given milestone happened to touch, at no extra mechanism cost — the rewrite already composes the entire store into one working-tree change the user reviews with git diff before the single commit confirmation.</advantage>
    <drawback>The substantive-versus-form line is a judgment call, so a shortening meant as hygiene can quietly narrow or broaden what a rule decides, and a reviewer now has to read diff hunks on entries that have nothing to do with the milestone being harvested.</drawback>
  </alternative>
  <alternative id="Unrestricted rewrite">
    The rewrite is bounded only by the goal&apos;s quality bar: capture may prune, merge, generalize, or reword any entry on its own current judgment, whether or not this milestone&apos;s commits bore on it.
    <advantage>The store converges fastest on a compact, non-overlapping set, since every run is a full-store quality pass rather than a patch limited to one milestone&apos;s reach.</advantage>
    <drawback>Capture would be overwriting user-confirmed directives with no evidence behind the change, which breaks the store&apos;s one guarantee that presence means confirmed and lets an unrelated run silently drift a rule that every future recommendation leans on.</drawback>
  </alternative>
  <recommendation option="Form-only hygiene beyond evidence">Evidence should gate what a rule decides, not how tersely it is written — and since the mechanism is already a whole-store compose reviewed as one git diff before commit, letting the compactness and merge moves reach untouched entries costs nothing while keeping every substantive change anchored to a harvested override.</recommendation>
</open-question>

<open-question id="Capture commit body content" status="deferred">
  <question>Does the Principle-capture commit carry a body naming which override drove each add, revision, prune, or merge, given the console prints nothing and the store keeps no changelog, or only the subject?</question>
  <alternative id="Subject only">
    The `Principle-capture: milestone_id` commit carries no body at all, leaving the store diff as the whole record of the pass.
    <advantage>Cheapest and most uniform with the plugin&apos;s other run-scoped committers (`Requirements-review:`, `Recommendation-annotation:`, `Task-derivation:`, `Goal-revision:`), and for adds the record is not actually empty — each new entry&apos;s surviving `*Origin:*` line already names the question it came from.</advantage>
    <drawback>The store may now shrink: for a prune, merge, generalization, or narrowing the diff shows only that text vanished, and with the console silent and the store carrying no changelog nothing anywhere names the override that forced it — a contradiction-driven retirement is indistinguishable from a sloppy deletion, and the one artifact that informs every future recommendation becomes unauditable exactly where it is most dangerous.</drawback>
  </alternative>
  <alternative id="Per-change body">
    The commit carries a body of one short line per store change, each naming the change kind (add, revision, prune, merge, generalization) and the override answer commit&apos;s Short Title that drove it.
    <advantage>It is the only durable record of *why* the store moved, placed where this project already puts exactly this kind of non-diff-derivable context — `answer-open-question` puts the decision&apos;s rationale in the body precisely so capture can distil it later, and `complete-all-tasks` puts the task heading there — and the line count is bounded by the handful of entries one run touches.</advantage>
    <drawback>It is hand-composed prose no tooling consumes, and because the store change is confirmed as a single whole-store rewrite that the user may revise over several `git diff` rounds, the body must be recomposed to match at commit time or it silently drifts from the diff it describes.</drawback>
  </alternative>
  <alternative id="Harvest-set body">
    The body names only the set of override commits the run harvested, with no mapping from override to store change.
    <advantage>Bounded and mechanical to produce — it hands an auditor the exact evidence set to `git show` without requiring any per-entry attribution judgment.</advantage>
    <drawback>It records almost nothing that is not already re-derivable by re-running the same path-scoped `git log` over that milestone&apos;s `requirements.md`, and it leaves the actually-lost fact — which override drove which prune or merge — exactly as unrecoverable as carrying no body.</drawback>
  </alternative>
  <alternative id="Scoped body">
    The body carries lines only for the changes the store itself does not record — prunes, merges, generalizations, and revisions — with adds left to their `*Origin:*` line.
    <advantage>Records the genuinely lost provenance while writing nothing that duplicates what the diff already carries, the leanest option that still closes the gap.</advantage>
    <drawback>It is a conditional per-change-kind rule rather than a flat one, and its boundary is genuinely fuzzy: a merge that folds a new override into an existing entry is simultaneously an add and a retirement, so the runner must adjudicate which side of the rule it falls on every time.</drawback>
  </alternative>
  <recommendation option="Per-change body">With the console silent and the store keeping no changelog, the commit body is the only surviving place for the why behind a prune or merge, and this project already uses bodies for exactly that; a flat line-per-change beats the scoped variant because the redundancy it costs is one line per add while the ambiguity it avoids is real.</recommendation>
</open-question>

<open-question id="Dirty store precondition" status="deferred">
  <question>What does capture do when the principle store already carries uncommitted changes before the run, given the rewrite is written in place and a rejected rewrite restores the store from HEAD?</question>
  <alternative id="Clean-store precondition">
    Capture checks `git status --porcelain -- milestones/answer_decision_principles.md` before anything else and stops cleanly when the store carries uncommitted changes, telling the user to commit or stash first.
    <advantage>Makes both fragile mechanics sound by construction: the rejection path&apos;s restore-from-HEAD is then exactly a restore of the pre-run state, and `shared/commit-procedure.md`&apos;s dirty-own-path guard sees only bytes this pass wrote, so a no-op run can never commit a stranger&apos;s edits under `Principle-capture:`.</advantage>
    <drawback>Introduces the plugin&apos;s only clean-tree precondition, and blocks precisely the state CLAUDE.md documents as legitimate — the user who hand-edited the store to pull an actively-wrong principle and now wants capture to run over it.</drawback>
  </alternative>
  <alternative id="Warn, confirm, snapshot">
    Capture detects a dirty store, prints a one-line notice and asks once whether to proceed; on proceed the working-tree file is the baseline the whole-store rewrite composes over, and the rejection path restores a snapshot taken immediately before the first write rather than restoring from HEAD, exiting without commit.
    <advantage>Preserves the user&apos;s uncommitted hand-edits instead of silently destroying them, reuses the exact shape this milestone already chose for the repeat-capture guard (notice plus one confirmation, never a stop), and the snapshot restore is correct in the clean case too, where the snapshot simply equals HEAD.</advantage>
    <drawback>Adds mechanism the other decisions did not need — a pre-run copy of the store — and the rejection path must exit explicitly rather than falling through to the dirty-own-path guard, which would still see the user&apos;s surviving edits and commit them.</drawback>
  </alternative>
  <alternative id="Proceed silently">
    Capture ignores the store&apos;s working-tree state entirely, composes the rewrite over whatever bytes are there, and leaves the rejection path restoring from HEAD as already decided.
    <advantage>Costs nothing to specify and keeps the skill free of any precondition, matching the house norm that a dirty tree is never a sweep&apos;s business and matching the repeat-capture decision&apos;s willingness to name a gap and accept it.</advantage>
    <drawback>A rejected rewrite destroys uncommitted work the run never authored, which is real data loss rather than an accepted harmless gap, and a run that composed nothing still trips the dirty-own-path guard and commits the user&apos;s unrelated edits under `Principle-capture:`.</drawback>
  </alternative>
  <recommendation option="Warn, confirm, snapshot">A dirty store is a foreseeable, documented state rather than an error, so warn-and-confirm keeps the hand-edit escape hatch usable in the same shape the repeat-capture guard already established, while the pre-run snapshot makes rejection lossless in the dirty and clean cases alike — restore-from-HEAD is only safe when nothing else was pending, which is the one assumption this question exists to remove.</recommendation>
</open-question>
