# TASKS TODO

## Sync CLAUDE.md And README To New Capture Model

Reconcile the two root documentation files — `CLAUDE.md` and root `README.md` — to the milestone's new reality, now that all the underlying skill changes are done by the earlier tasks. This is the **last** task and the **sole owner** of every `CLAUDE.md`/`README.md` edit in this milestone, so one completer holds the coupled README Mermaid graphs in view at once. The new reality to reflect: (a) `/answer-open-question` now commits its manual-answer edit (subject `Manual-answer: <Short Title>`, rationale in the body, no `Answer-Principle:` trailer) and no longer chains to capture; (b) a new skill `capture-milestone-principle-updates` exists — an optional finish-time skill, recommended by `/finish-current-milestone`, that distills principles from `Manual-answer:` commits into the principle store and is its new sole writer; (c) `try-capture-answer-principle` and `reject-auto-answer` are both retired (deleted), the latter's correction role replaced by the uniform "revert the auto-answer commit, then `/answer-open-question` to re-answer, principle reconciled at finish" flow.

**Notes:**
- **README is a grep-and-edit pass; CLAUDE.md requires rewriting invariant PROSE.** A grep-and-delete sweep of `CLAUDE.md` misses invariants that never name the retired skills — those must be located by meaning and rewritten, not just name-stripped.
- **README diagrams (per milestone 4, the README is six per-phase `flowchart TD` diagrams wired through shared `D0`–`D5` seam nodes):**
  - "Iterating milestone requirements" diagram: remove the `try-capture-answer-principle` node (`ITM5`) and the `reject-auto-answer` node (`ITM6`), and fix every edge that touched them so no dangling edges remain and the `D0`–`D5` seam wiring stays intact. Update that diagram's lead-in prose paragraph (it currently names both retired skills and the auto-capture chain).
  - "Ending a milestone" diagram: add a `capture-milestone-principle-updates` node (the optional finish-time follow-up `/finish-current-milestone` recommends), wired consistently with the existing seam/style conventions.
- **README `## Skill reference`:** delete the `### try-capture-answer-principle [...]` and `### reject-auto-answer [...]` subsections; add a new `### capture-milestone-principle-updates` subsection describing the finish-time distillation skill; update `### answer-open-question` (currently says it chains to `/try-capture-answer-principle`) to state it now records AND commits the answer and no longer chains to capture; and update the `### The answer-principle-learning loop` prose block (its "Manual teaching flow" and "Correction loop" bullets name the retired skills and the auto-chain) to the new model — manual answers are committed with rationale, principles are distilled at milestone finish by `capture-milestone-principle-updates`, correction is revert-then-re-answer.
- **CLAUDE.md `## Repository layout` + skills-overview/pipeline listing:** remove `try-capture-answer-principle` and `reject-auto-answer`; add `capture-milestone-principle-updates` (finish-time principle-distillation skill, new sole writer of the principle store, recommended by `finish-current-milestone`).
- **CLAUDE.md `## Invariants to preserve` — reconcile every invariant this milestone makes false (rewrite, do not merely name-strip):**
  - The "Two orchestrators commit; individual skills never commit" invariant is now FALSE for `answer-open-question` — rewrite it to record that `answer-open-question` is a deliberate, documented exception that commits exactly its own path-scoped `requirements.md` manual-answer edit (subject `Manual-answer: <Short Title>`, rationale in body, no `Answer-Principle:` trailer).
  - The invariant that `answer-open-question` unconditionally chains to `try-capture-answer-principle` — remove/replace it (the chain is severed; capture moved to finish time).
  - The entire `reject-auto-answer` invariant paragraph — remove it; where the "bad auto-answer" correction is described, replace with the revert-then-`/answer-open-question` flow with finish-time principle reconciliation.
  - Add invariant(s) for the new skill as warranted: it resolves `<MILESTONE_DIR>` from the last `## Completed Milestones` row (NOT `get-current-milestone`); path-scoped `git log --grep='^Manual-answer: ' -- <MILESTONE_DIR>/requirements.md` commit walk excluding `Answer-Principle:`-trailer commits; new sole writer of the principle store; recommended-not-auto-run at finish.
  - Update the principle-store sole-writer attribution wherever `CLAUDE.md` states it (now `capture-milestone-principle-updates`).
- **Frozen records and other files are off-limits:** do NOT edit `milestones/README.md` history, the `milestone_02`/`03`/`04` `requirements.md`/`TASKS_DONE.md`, this milestone's own `milestone_05` `requirements.md`, or any `skills/**/SKILL.md` or `shared/**` file — those are owned by the earlier tasks. This task edits only `CLAUDE.md` and root `README.md`.
- This skill does not commit; leave all changes staged.

**Success:**
- `grep -rn "try-capture-answer-principle\|reject-auto-answer" CLAUDE.md README.md` returns no hits.
- Both `CLAUDE.md` and `README.md` reference `capture-milestone-principle-updates`.
- The README's six `flowchart TD` diagrams have no dangling edges and the `D0`–`D5` seam chain is intact; the "Ending a milestone" diagram contains a `capture-milestone-principle-updates` node and the "Iterating milestone requirements" diagram no longer contains the `ITM5`/`ITM6` nodes.
- `CLAUDE.md`'s no-commit invariant and the chain-to-capture invariant are rewritten (not merely name-stripped), and the `reject-auto-answer` invariant paragraph is gone.
- The `answer-open-question` description in both `README.md` and `CLAUDE.md` states it commits its manual-answer edit and no longer chains to capture.
- `git diff` shows `milestones/README.md`, this milestone's own `requirements.md`, every `milestone_02`/`03`/`04` `requirements.md` and `TASKS_DONE.md`, and every `skills/**/SKILL.md` and `shared/**` file unchanged by this task.

---
