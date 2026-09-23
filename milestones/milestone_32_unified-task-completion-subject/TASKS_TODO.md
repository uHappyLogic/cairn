# TASKS TODO

## Ask-In-Context Heading Search Wording

Rewrite the step 2 sentence of `core/skills/ask-in-milestone-context/SKILL.md` that calls the task-to-commit mapping "not keyed on the heading in the subject line" as a marker-agnostic heading search: completion commits carry the task heading, so searching commit subjects and bodies for the heading text usually finds the commit, while the mapping stays best-effort, the fall-back to the live files and the "never the sole source" rule are kept, and the sentence names neither the `Task-completion:` nor the retired `Tasklist-completion:` marker and describes no era of history. The milestone needs it because the old claim becomes false once every completion subject carries the heading. Verified by the sentence's absence of both markers and of the old "not keyed" claim, and `uv run scripts/build_hosts.py --check` passing with the rebuilt host trees committed.

---

## Sync Docs Pages To Unified Subject

Update the `complete-all-tasks` and `complete-task` entries of `docs/skill-reference.md` (lines 81 and 85) so both state the one subject-only `Task-completion: <task heading>` commit with no `Tasklist-completion:` marker and no heading-in-body claim, and extend the "`/complete-all-tasks` commits once per task" clause in the `## How skills commit` paragraph of `docs/workflow.md` to name that subject with no body as the same subject inline `/complete-task` uses. The milestone needs it so the docs describe the commits the runtime now makes. Verified by `grep` finding no `Tasklist-completion` under `docs/` and both pages agreeing with the rewritten orchestrator skill.

---

## CLAUDE.md Unified Subject Invariant

Extend the committing bullet of `CLAUDE.md` with one clause stating that both completion runners commit subject-only under `Task-completion: <Task Title>`, with the task's `##` heading copied exactly, and that the retired `Tasklist-completion:` marker with its heading-in-body commits must not be restored, each with its rationale: one subject for one unit of work whichever runner makes it, and the heading visible in the subject line so history can be searched without reading commit bodies. The milestone needs it so a later editor does not reintroduce the split. Verified by the committing bullet carrying the clause and both rationales, and the rest of `CLAUDE.md` naming `Tasklist-completion:` only as the retired marker.

---
