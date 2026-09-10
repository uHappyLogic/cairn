# TASKS TODO

## Retire Independence Invariant In CLAUDE.md

Update the `CLAUDE.md` invariants and repository-layout lines to match the new behaviour: retire the "Recommendation independence" clause and the parallel-dispatch and embed-at-end wording of the `recommend-all-open-questions` bullet in favour of sequential most-significant-first dispatch, embed-before-next, the `<depends-on>` element, the seventh gate test, the stale-tag and no-cycle-test decisions; record the disclosure duty in the `shared/recommend-procedure.md` bullet; record the three-input contract, the agree/strip branches, strip-on-doubt, and option-less removal in the `shared/answer-procedure.md` bullet; record the graph walk and cycle promotion in the answer-sweep bullet, the dependent stripping in the review invariant, the scoped diff read in the capture bullet, and the seven-test gate in the dispatched-agent-return bullet. Verified by reading: every decision in `requirements.md` is reflected and no invariant still asserts independence.

---

## Document Dependency Graph In README

Update `README.md`'s "Iterating milestone requirements" paragraph and the `## Skill reference` entries for `recommend-all-open-questions`, `recommend-open-question`, `answer-all-open-questions-with-recommendation`, the three answer skills, `review-milestone-requirements`, and `capture-milestone-principle-updates` so they describe sequential ordered dispatch, the `<depends-on>` declaration, the answer-time agree-or-strip cascade, the graph walk, and the scoped diff read. Verified by reading: no entry still claims parallel or independent dispatch, and each changed behaviour is named where its skill is documented.

---
