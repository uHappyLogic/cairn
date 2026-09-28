# TASKS TODO

## Reword No-Change Branch Example Reason

In step 5 of `core/skills/goto-next-milestone/SKILL.md`, keep the no-change branch but rewrite its example reason to say only that the pointer line already matched the last commit, dropping the claim that the pointer already named that milestone, which step 1 has just contradicted. The branch still prints its one distinct no-op line, never `Milestone activated.`, and commits nothing. Verified by reading the step and by `uv run scripts/build_hosts.py --check` passing against the rebuilt host trees.

---

## Delete Bootstrap README Template Note

Delete the blockquote under the README template in `core/skills/init-milestone-base-workflow/SKILL.md` that credits the `## Completed Milestones` table to `/goto-next-milestone`, without rewording it, so the template's two sections stay and no sentence names which skill writes or reads them. Verified by reading the template and by `uv run scripts/build_hosts.py --check` passing against the rebuilt host trees.

---

## Update Invariant And Docs For Lowest Pick

In `CLAUDE.md`, make the `goto-next-milestone` pipeline line name the lowest-numbered undone pick and add an invariant recording that pick and stating that the retired single-candidate confirmation and multiple-candidate choice prompts must not be restored. In `docs/workflow.md`, `docs/skill-reference.md`, and `docs/ways-of-using-cairn.md`, rewrite the sentences that describe what the skill activates so they say it activates the lowest-numbered undone milestone without asking, stopping only on a pointer not reading `none` or on no undone milestone. Verified by reading each passage against the Goal and the Documentation scope decision.

---

## Document Skipping An Unwanted Milestone

Document the way out of an unwanted defined milestone: the `goto-next-milestone` entry of `docs/skill-reference.md` states that it is skipped by removing its directory, for example by reverting its `Milestone-definition:` commit, and step 2 of `CONTRIBUTING.md` is corrected so an abandoned reservation on `main` must be reverted rather than left as a candidate. The runtime `SKILL.md` gains no prose about it. Verified by reading both passages.

---
