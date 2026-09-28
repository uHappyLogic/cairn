# TASKS TODO

## Update Invariant And Docs For Lowest Pick

In `CLAUDE.md`, make the `goto-next-milestone` pipeline line name the lowest-numbered undone pick and add an invariant recording that pick and stating that the retired single-candidate confirmation and multiple-candidate choice prompts must not be restored. In `docs/workflow.md`, `docs/skill-reference.md`, and `docs/ways-of-using-cairn.md`, rewrite the sentences that describe what the skill activates so they say it activates the lowest-numbered undone milestone without asking, stopping only on a pointer not reading `none` or on no undone milestone. Verified by reading each passage against the Goal and the Documentation scope decision.

---

## Document Skipping An Unwanted Milestone

Document the way out of an unwanted defined milestone: the `goto-next-milestone` entry of `docs/skill-reference.md` states that it is skipped by removing its directory, for example by reverting its `Milestone-definition:` commit, and step 2 of `CONTRIBUTING.md` is corrected so an abandoned reservation on `main` must be reverted rather than left as a candidate. The runtime `SKILL.md` gains no prose about it. Verified by reading both passages.

---
