# TASKS TODO

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
