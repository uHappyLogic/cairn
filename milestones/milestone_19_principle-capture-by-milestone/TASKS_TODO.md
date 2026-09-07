# TASKS TODO

## Override Rationale Prompts With Best Guesses

Add a prompting step that asks the user why the alternative was preferred only for override commits carrying no user rationale — every non-agreeing `Alternative-answer:` and a non-agreeing `Manual-answer:` whose body is the bare literal answer — showing the skill's best guess derived from the removed alternatives, recommendation, and recorded option, skippable per prompt, with the run opening on a one-shot choice to accept every guess or skip every prompt; deliberated manual bodies and agreeing answers are never prompted. Verified when the prompt step states exactly these eligibility rules, the best-guess display, and the one-shot opener.

---

## Override Candidates And Acceptance Evidence

Rework phase 1 so new principle candidates are distilled only from override commits — a deliberated or prompted override rationale, plus non-override and deliberated agreeing `Manual-answer:` bodies — keeping the non-generalizable filter and the cross-candidate dedup, while accepted recommendations and agreeing answers supply evidence only: each removed `<applied-principle>` reinforces its store entry and shields it from prune or narrowing in this pass, and an accepted rationale contradicting an existing entry flags that entry for the salvage path. Verified when the skill states that an accepted `Recommendation-answer:` never yields a candidate, that an agreeing `Alternative-answer:` yields none while a deliberated agreeing `Manual-answer:` still does, and that both evidence signals fall out of the diff read.

---

## Compose Whole-Store Rewrite In Place

Replace the per-candidate confirm-and-write loop with a single composition of the entire proposed store — adds, revisions, prunes, merges, generalizations, and shortenings applied together over the baseline — written directly to `milestones/answer_decision_principles.md` after taking a snapshot of the store immediately before the first write, printing no diff and no store content to the conversation. Substantive change to an entry requires the harvested milestone's own evidence, while form-only hygiene may reach any entry: directives target roughly 40-80 words and are flagged for shortening past about 100 with the "as short as it can be while still reading as an intuitive rule" test deciding, plainly duplicate entries merge, there is no ceiling on entry count, and the optional `*Origin:*` line survives as a single-line pointer. Verified when the write step describes one in-place rewrite under these rules and the `### <Short Title>` entry schema is preserved.

---

## Contradicted Entry Salvage Ladder

State in the rewrite composition how an entry contradicted by current reasoning is salvaged, attempted in this fixed order: narrow its scope clause, generalize it so the prior accepted citations and the override both fit, replace it with a fresh directive when its premise is wrong, and delete it only when nothing survives, breaking a tie between forms by whichever yields the shortest entry that still predicts both. Entries reinforced by a citation in the same pass stay shielded from prune or narrowing. Verified when the skill lists the four forms in this order with the tie-break and the shield, and notes the chosen form is visible in the working-tree change.

---

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
