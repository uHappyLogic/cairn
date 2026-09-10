# TASKS TODO

## Add Dependency Resolution Gate Test

Add a seventh test to the acceptance gate in `skills/recommend-all-open-questions/SKILL.md` step 3c that resolves every returned `<depends-on>` line against the `<open-question>` blocks still present under `## Open questions` that carry embedded children (without reading `status`) and the target's `<alternative id` lines, with entity-unescaped case-folded comparison, and a miss producing a reason string that takes the single repair attempt and skips only on a second failure, exactly like the other structural misses; no cycle test is added. Update the fixed corrective message so its element ordering names the `<depends-on>` elements between the applied-principles and the recommendation. Verified by reading: the gate lists seven line-grep tests, the orchestrator never edits or drops a returned element, and the reason strings name the new test.

---

## Extend Answer Cascade With Dependency Reconciliation

Widen `shared/answer-procedure.md` to three inputs by adding an optional RECORDED OPTION (the un-escaped option or alternative id the caller lifted), whose presence selects exact id comparison and whose absence selects a judgment of whether ANSWER invalidates the assumed option, and extend step 6's cascade so that after the answered block and any mooted entries are removed, every surviving block whose `<depends-on question="…">` names a removed block is reconciled: an agreeing option deletes only that `<depends-on>` line, while a disagreeing option, an inconclusive judgment, or a target removed as a mooted entry with no option strips that dependent's embedded children transitively, leaving the bare `<open-question>` wrapper and `<question>` for the next recommend sweep. The core prints nothing and stays execution-neutral, and the fold-before-remove order is preserved. Verified by reading: both branches are stated once, "strip on doubt" is explicit, and no anchor-string parsing enters the core.

---

## Pass Recorded Option From Lifting Callers

Update the three callers of the recording core so `shared/answer-with-recommendation-procedure.md` step 4 passes the un-escaped `option` value it lifted as RECORDED OPTION, `skills/answer-open-question-with-alternative/SKILL.md` step 4 passes the un-escaped chosen `id`, and `skills/answer-open-question/SKILL.md` step 3 explicitly passes no RECORDED OPTION so the cascade takes the judgment mode. Verified by reading the three delegation sentences, with no other step in those files changed.

---

## Walk Dependency Graph In Answer Sweep

Replace the "loosely most-significant → least" ordering in `skills/answer-all-open-questions-with-recommendation/SKILL.md` step 1 with a walk of the dependency graph built over the gathered set from each block's `<depends-on question="…">` lines: edges whose target is absent from the set or carries no `<recommendation>` are dropped, questions with no resolvable edges are origins, same-depth questions go in document order, and a stranded set whose targets are never answered promotes its document-order-first member to an origin and continues the depth walk. Step 2's re-check and per-answer commit stay unchanged. Verified by reading: the significance proxy is gone and the walk is deterministic and total for any graph shape, cycles included.

---

## Strip Dependents On Review Prune And Dedup

Extend `skills/review-milestone-requirements/SKILL.md` step 2 so that when a prune or dedup removes an `<open-question>` block, every surviving sibling whose `<depends-on question="…">` names that block has its embedded children stripped transitively, leaving the bare wrapper and `<question>` for the next recommend sweep, with no new console advisory beyond the existing removal report. Verified by reading: the stripping is attached to both removal paths and the skill still records no decision.

---

## Scope Capture Diff Read To Answered Block

Reword the one disambiguating sentence in `skills/capture-milestone-principle-updates/SKILL.md` (currently "Any other removed block in the same diff is a cascaded sibling…") so only removed lines within the answered block's `-<open-question id="…">` through `-</open-question>` boundaries feed the record, covering both cascaded sibling blocks and orphan removed lines from siblings that stay in the document. The sentence stays element-agnostic and never names `<depends-on>`. Verified by reading: exactly that sentence changed and no per-element ignore list was started.

---

## Retire Independence Invariant In CLAUDE.md

Update the `CLAUDE.md` invariants and repository-layout lines to match the new behaviour: retire the "Recommendation independence" clause and the parallel-dispatch and embed-at-end wording of the `recommend-all-open-questions` bullet in favour of sequential most-significant-first dispatch, embed-before-next, the `<depends-on>` element, the seventh gate test, the stale-tag and no-cycle-test decisions; record the disclosure duty in the `shared/recommend-procedure.md` bullet; record the three-input contract, the agree/strip branches, strip-on-doubt, and option-less removal in the `shared/answer-procedure.md` bullet; record the graph walk and cycle promotion in the answer-sweep bullet, the dependent stripping in the review invariant, the scoped diff read in the capture bullet, and the seven-test gate in the dispatched-agent-return bullet. Verified by reading: every decision in `requirements.md` is reflected and no invariant still asserts independence.

---

## Document Dependency Graph In README

Update `README.md`'s "Iterating milestone requirements" paragraph and the `## Skill reference` entries for `recommend-all-open-questions`, `recommend-open-question`, `answer-all-open-questions-with-recommendation`, the three answer skills, `review-milestone-requirements`, and `capture-milestone-principle-updates` so they describe sequential ordered dispatch, the `<depends-on>` declaration, the answer-time agree-or-strip cascade, the graph walk, and the scoped diff read. Verified by reading: no entry still claims parallel or independent dispatch, and each changed behaviour is named where its skill is documented.

---
