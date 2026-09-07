# TASKS TODO

## Single Rewrite Confirmation Gates The Commit

Add the review loop after the in-place write: the user reviews the working-tree change with `git diff` and requests changes in conversation, the skill re-edits the file in place each round, and one confirmation gates the commit — on acceptance the store is committed path-scoped under `Principle-capture: <milestone_id>`, and on explicit rejection the skill restores the pre-write snapshot and exits without invoking `shared/commit-procedure.md`, reporting the no-op line. The report step keeps `Principles captured.` for a committed rewrite and one distinct line for every nothing-captured case (empty range, no candidates, composed store identical to the baseline, rejection). Verified when the confirmation, rejection, and report steps read exactly so.

---

## Capture Commit Body Lists Store Changes

Make the `Principle-capture: <milestone_id>` commit carry a body of one short line per store change, each naming the change kind (add, revision, prune, merge, or generalization) and the Short Title of the override answer commit that drove it, composed at commit time against the final rewrite so it cannot drift from the diff. Verified when the skill's commit step supplies that body to the shared commit procedure and states the at-commit-time composition.

---

## Answer Skills State Three-Provenance Harvest

Update the commit-step prose of `answer-open-question`, `answer-open-question-with-recommendation`, and `answer-open-question-with-alternative`, and `answer-open-question`'s opening paragraph, so they no longer claim that only `Manual-answer:` is harvested: capture reads all three subjects, with manual and alternative answers as the override signal and recommendation answers as evidence only. Verified when no file under `skills/` or `agents/` states that capture harvests only `Manual-answer:`, `finish-current-milestone` still says it never invokes capture, and the regenerated `.agents/plugins/cairn/` tree matches the source.

---

## README Documents On-Demand Capture

Rewrite the README surfaces — the "Ending a milestone" prose and its dashed optional diagram edge, the `## How skills commit` harvest sentence, the principle-learning and correction-loop bullets, and the skill-reference entries for capture and the three answer skills — so capture is an on-demand skill taking a required milestone id, harvesting all three answer provenances, prompting for override reasons, and composing a whole-store rewrite that may prune and merge, with finish phrased as the natural moment and never a precondition. Verified when README no longer mentions Completed Milestones table resolution or a `Manual-answer:`-only grep for capture and keeps the dashed edge in the "Ending a milestone" diagram.

---

## CLAUDE.md Invariants For Milestone-Id Capture

Update `CLAUDE.md` — the repository-layout line, the workflow-map entry, the recommendation/alternative-answer provenance bullet, the correction-loop bullet, the skill-layer-commit bullet's "Still true" sentence, and the finish/capture bullet — so the invariants record capture as a milestone-id-driven, on-demand harvester over all three provenances with the override-signal, evidence-only, whole-store-rewrite-with-salvage, and single-confirmation designs, and the answer subjects as provenance discriminators rather than a harvest filter. Verified when `CLAUDE.md` no longer states last-row resolution, pointer-none dependence, or a `Manual-answer:`-only harvest, and phrases the finish-time placement as a convention.

---
