# TASKS TODO

## Sync Docs Pages To Unified Subject

Update the `complete-all-tasks` and `complete-task` entries of `docs/skill-reference.md` (lines 81 and 85) so both state the one subject-only `Task-completion: <task heading>` commit with no `Tasklist-completion:` marker and no heading-in-body claim, and extend the "`/complete-all-tasks` commits once per task" clause in the `## How skills commit` paragraph of `docs/workflow.md` to name that subject with no body as the same subject inline `/complete-task` uses. The milestone needs it so the docs describe the commits the runtime now makes. Verified by `grep` finding no `Tasklist-completion` under `docs/` and both pages agreeing with the rewritten orchestrator skill.

---

## CLAUDE.md Unified Subject Invariant

Extend the committing bullet of `CLAUDE.md` with one clause stating that both completion runners commit subject-only under `Task-completion: <Task Title>`, with the task's `##` heading copied exactly, and that the retired `Tasklist-completion:` marker with its heading-in-body commits must not be restored, each with its rationale: one subject for one unit of work whichever runner makes it, and the heading visible in the subject line so history can be searched without reading commit bodies. The milestone needs it so a later editor does not reintroduce the split. Verified by the committing bullet carrying the clause and both rationales, and the rest of `CLAUDE.md` naming `Tasklist-completion:` only as the retired marker.

---
