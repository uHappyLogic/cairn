# Milestone 5: Milestone-finish principle capture

## Goal

Move answering-principle capture from the per-answer path to an optional, recommended end-of-milestone step: /answer-open-question commits its requirements.md update with the decision's rationale in the commit body; a new /capture-milestone-principle-updates skill distills principles from those commits into the principle store at milestone finish; and /try-capture-answer-principle, with its on-demand capture, is retired. The new /capture-milestone-principle-updates skill must be authored using the /skill-creator:skill-creator skill — it is the mandated tool for creating it.

## Relevant starting state

### The per-answer capture path (`answer-open-question` → `try-capture-answer-principle`)

`skills/answer-open-question/SKILL.md` parses its arg on the first `.` (Short Title / answer), records the decision by following `shared/answer-procedure.md` inline, then **unconditionally** chains into `/try-capture-answer-principle` (step 4) — it does not itself judge whether the decision generalizes. It does **not** commit; it leaves `requirements.md` staged. This is the chain this milestone severs (retire capture, defer to milestone finish) and the skill that must start committing with rationale in the body.

`shared/answer-procedure.md` is the execution-neutral recording core (locate block by Short Title → analyse implications → remove block → fold a **clean, citation-free** prose decision into `## Decisions` → cascade to mooted entries). It is shared verbatim by `answer-open-question` and the sweep, and is explicitly told to record *only the decision*, never its provenance/rationale. The deliberation (alternatives weighed, trade-off accepted) lives only in the conversation, **not** in the document — this is exactly why the chosen design routes rationale into the commit body instead.

### `try-capture-answer-principle` (the skill being retired)

`skills/try-capture-answer-principle/SKILL.md` is the **sole writer** of the principle store. It takes no payload — it analyses the *live conversation* anchored on the most recent decision, judges whether a reusable keep/eliminate directive can be extracted, and (only on a real candidate) runs a user-confirmed **revise-vs-add by semantic overlap** flow before writing one `### <Short Title>` subsection. Its primary entry is the unconditional chain-off from `answer-open-question`; it also supports an optional free-text focus hint (used by `reject-auto-answer` to revise a specific principle) and a cold/on-demand invocation ("capture that as a principle"). Retiring it removes both the per-answer chain **and** the on-demand path; its revise-vs-add discipline and schema are what the new skill must carry forward.

### The principle store (`milestones/answer_decision_principles.md`)

A single project-wide file at the `milestones/` root (above any one milestone), currently holding 4 confirmed principles. Schema per entry: `### <Short Title>` heading (the citable handle), a generalizable keep/eliminate directive in prose, and an optional `*Origin: …*` line. Presence = confirmed; there is no status field. Its header sentence currently reads "written **only** by `try-capture-answer-principle`" — that attribution line will need updating to the new writer. This is the artifact the new finish-time skill distills into.

### The autonomous sweep and its commit convention (`try-answer-all-questions-by-principle`)

`skills/try-answer-all-questions-by-principle/SKILL.md` requires a **clean working tree**, captures `BASE=$(git rev-parse HEAD)`, then commits **one auto-answer per commit**: subject `Principle-based-answer: <Short Title>` (the answered question) with one repeated `Answer-Principle: <Short Title>` trailer line per load-bearing principle. It **never** chains to capture (the answer was already derived from a confirmed principle — capturing would be circular). Its clean-tree checkpoint relies on the user having hand-committed manual answers first; if `answer-open-question` begins committing itself, that "human-decisions vs auto-answers" git boundary shifts. The new finish-time skill must read principles, so the sweep's auto-answer commits are **not** a source for it — they must be excluded from the commit walk.

### Commit-type distinctions already in git (`reject-auto-answer`)

`skills/reject-auto-answer/SKILL.md` already defines a validation gate that classifies a `requirements.md`-touching commit: a genuine **auto-answer** commit touches *only* `requirements.md` **and** carries ≥1 `Answer-Principle:` trailer; the gate explicitly contrasts this against "a manual `requirements.md` commit" (no trailer). So the discriminator the new skill needs — manual `answer-open-question` commits vs. sweep auto-answer commits — is **already** the presence/absence of the `Answer-Principle:` trailer, provided the new `answer-open-question` commits adopt a recognizable subject/marker and omit that trailer. `reject-auto-answer` step 6 also currently closes its loop by directing the user to re-capture via `/try-capture-answer-principle` — that pointer must be redirected once capture is retired.

### Milestone-finish hook and commit-range boundary (`finish-current-milestone`)

`skills/finish-current-milestone/SKILL.md` is the natural place to *recommend* (not auto-run) the new skill — its step 8 already "suggests the next step." It currently makes no commit and resolves `<MILESTONE_DIR>` via `shared/get-current-milestone.md`. There is no existing "milestone start" git marker (no tag, no recorded base SHA) — `define-milestone-goal` and `goto-next-milestone` do not commit. So "all `answer-open-question` commits since the milestone started" has no ready-made boundary; candidate boundaries (first commit touching this milestone's `requirements.md`, a recorded base, or a `<MILESTONE_DIR>`-scoped `git log`) are an open design point.

### The no-commit invariant and `skill-creator`

CLAUDE.md states the standing invariant: "individual skills never commit … Two orchestrators commit; individual skills never commit." Making `answer-open-question` commit is a deliberate, documented break of this invariant that the requirements loop must reconcile (CLAUDE.md text + the README skill table both assert it). The `skill-creator` plugin is installed and available (`skill-creator:skill-creator`) and is the mandated tool for authoring the new `/capture-milestone-principle-updates` skill. No build system, no tests — everything is plain Markdown.

## Decisions

### Answer commit identification

An `/answer-open-question` commit identifies itself with a single shared subject-line marker: the subject is `Manual-answer: <Short Title>`, mirroring the sweep's `Principle-based-answer: <Short Title>` (subject names the answered question). The decision rationale goes in the commit body, and the commit deliberately carries **no** `Answer-Principle:` trailer — that trailer is the sweep's signature, so its absence is the existing discriminator between manual and auto-answer commits. The finish-time skill collects answer commits with an anchored `git log <range> --grep='^Manual-answer: '` and, as a guard, excludes any commit carrying an `Answer-Principle:` trailer.

### Answer commit scope

`/answer-open-question` stages and commits **only** its own `<MILESTONE_DIR>/requirements.md` edit via a path-scoped `git add <MILESTONE_DIR>/requirements.md` — never `git add -A`. This keeps each manual-answer commit clean (touching only `requirements.md`, mirroring the auto-answer commit shape that `reject-auto-answer`'s gate recognizes), prevents the skill from sweeping unrelated working-tree changes into a commit it authored, and leaves any other user changes untouched. The skill does not commit more than its own edit in order to satisfy `/try-answer-all-questions-by-principle`'s clean-tree precondition — that precondition remains the sweep's own guard, which correctly refuses on a tree left dirty by the user's unrelated changes.

### Commit-walk boundary

The finish-time skill bounds its commit walk by path-scoping the log to the current milestone's `requirements.md`: `git log --grep='^Manual-answer: ' -- <MILESTONE_DIR>/requirements.md`. That path is itself the lower boundary — it does not exist before `define-milestone-goal` creates it, so no earlier commit can touch it — which removes any need for a milestone-start marker commit or a recorded base SHA. The path filter holds regardless of how much each answer commit stages: even a `git add -A` commit still touches `<MILESTONE_DIR>/requirements.md`, so it is still matched. No `define-milestone-goal`/`goto-next-milestone` start-marker commit is introduced for this purpose.

### Cold-answer commit body

On a cold `/answer-open-question` (no `/discuss-open-question` deliberation in context), the commit body records only the rationale that genuinely exists in context — the skill neither prompts the user for a rationale nor fabricates one. The body always carries the decision and carries reasoning only when reasoning actually exists; on the cold path that means the answer text recorded verbatim, including any inline "because" clause the user chose to type. When a cold answer states no reasoning, the body holds the bare decision and finish-time principle capture yields nothing for it — a decision with no articulated rationale cannot produce a generalizable keep/eliminate directive, so that empty result is correct rather than a gap to fill. No separate rationale prompt is added: the answer string is itself the cold path's rationale affordance.

### Batch capture interaction model

The finish-time skill preserves `try-capture-answer-principle`'s per-principle, user-confirmed **revise-vs-add by semantic overlap** discipline — it does not collapse into a single batch rubber-stamp approval. Confirmation is retained because it guards the **generalization** (a principle governs every future sweep and reaches beyond the one question it came from), not the already-recorded answer. But the surrounding interaction model changes from the retired skill's event-driven single-shot to a bounded iterative conversational sweep:

1. **Internal candidate elimination first.** The skill extracts candidate keep/eliminate directives from all in-range `Manual-answer` commit bodies, drops the non-generalizable ones, and clusters the surviving candidates **against each other**. This cross-candidate dedup is the structurally new problem batch mode introduces: the retired skill only ever saw one decision at a time, so it never deduped new candidates among themselves. The commit→principle mapping is many-to-many — two commits may yield one principle, one commit may yield none.
2. **Then strongest-first user confirmation against the live store.** The skill engages the user on the surviving candidates, running revise-vs-add against the **live** store for each and re-scanning the remaining pool after every write. Each confirmed write mutates the store and can turn a later candidate's "add" into a "revise" — re-evaluation between candidates is the whole point of iterating rather than approving one static batch.

Termination is not a fuzzy judgment call: the candidate pool is finite and known up front (the in-range `Manual-answer` commits), so the loop ends when every commit's rationale has been considered and every surviving candidate resolved (add / revise / declined) with no pending merges. Each confirmation removes a candidate, so the loop provably converges.

Confirmation granularity is **per-candidate at write time**: the skill confirms and writes one candidate at a time, never grouped-per-round. It presents the surviving candidates strongest-first and, for each, runs revise-vs-add against the **live** store, takes the user's add/revise/decline, writes, then re-scans the remaining pool before moving to the next. Display granularity is separate from write granularity — the skill **may** show the full surviving pool up front for context (a "what this milestone taught" review aid), but the write/confirm step still advances one candidate at a time. Per-candidate is chosen because it honors the load-bearing `re-evaluation-after-each-write` commitment trivially (every write is followed by a re-scan by construction, so a later candidate that should become a revision of one just written is caught automatically) and continues the precedent of the retired `try-capture-answer-principle`, which only ever saw one decision at a time. Grouped-per-round is rejected: writing several candidates before re-scanning is only correct if the group is proven mutually independent (no member could become a revision of another once written), and since a milestone yields only a handful of principles, grouping saves few prompts at the cost of that independence proof.

### Bad-principle correction path

The `reject-auto-answer` skill is retired entirely; there is no dedicated correction skill. Correcting a bad auto-answer becomes the uniform "revert + re-answer" flow: revert the auto-answer commit (which, by the one-commit-=-one-auto-answer invariant, restores the reopened question block and removes the folded decision in one shot), then run `/answer-open-question` to record the new answer. The offending **principle** is reconciled at milestone finish — the re-answer's `Manual-answer` commit is picked up by `capture-milestone-principle-updates`, whose revise-vs-add-by-overlap discipline offers the new directive as a revision of the bad principle. For an urgent mid-milestone "this principle is actively wrong, remove it now" case, the user hand-edits the plain-Markdown store `milestones/answer_decision_principles.md` directly (a human deleting a wrong line does not violate the single-writer-for-adds discipline). This drops the staged-uncommitted-revert forcing function (a re-answered, clean tree lets a subsequent sweep still mis-fire the bad principle on other not-yet-answered questions until finish-time or hand-edit corrects it) and the validation gate that confirmed a target was a genuine auto-answer; both losses are accepted. Accepted residual hole: if a replacement answer does not generalize, finish-time capture has nothing to revise against and the bad principle survives into future milestones until hand-removed — self-correcting (it mis-fires and is caught), not catastrophic. Removing the skill and cleaning up its references across CLAUDE.md, README, and the starting-state section is downstream `/derive-tasks` work.

### Finish-time recommendation

`/capture-milestone-principle-updates` is **recommended, never auto-run**, as an optional follow-up *after* `/finish-current-milestone` completes — not before. `/finish-current-milestone` step 8 surfaces the recommendation after the current-milestone pointer has been cleared to `none` and the `## Completed Milestones` table row appended, ordering the two suggestions as `/capture-milestone-principle-updates` first (the milestone just closed) then `/define-milestone-goal` (the next one). It is a plain suggestion line, e.g. "Optional: run `/capture-milestone-principle-updates` to distill reusable answering principles from this milestone's recorded decisions into the principle store."

Because the pointer is `none` by the time the recommendation fires, `/capture-milestone-principle-updates` does **not** resolve its target via `shared/get-current-milestone.md`. Instead it resolves `<MILESTONE_DIR>` from the **last row of the `## Completed Milestones` table** in `milestones/README.md` (which `/finish-current-milestone` appended immediately prior), and that same path feeds its path-scoped `git log --grep='^Manual-answer: ' -- <MILESTONE_DIR>/requirements.md` commit walk.

### Empty commit range

An empty commit range is a legitimate, non-error outcome — not a special case the skill branches on. When the path-scoped `git log --grep='^Manual-answer: ' -- <MILESTONE_DIR>/requirements.md` walk returns no qualifying commits, the skill reports a single line that there are no `Manual-answer` commits in range to distill and exits, writing and staging nothing. This is the same "nothing captured" report the candidate-elimination flow already produces when in-range commits exist but no surviving candidate generalizes: the zero-commits case and the "commits exist but none generalize" case converge on the identical terminal report, so the empty range is simply the natural floor of the normal flow rather than a distinct empty-range branch.

## Open questions

## Out of Scope

