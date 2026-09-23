# TASKS DONE

## Orchestrator Commits Under Task-Completion Subject

Change step 2c of `core/skills/complete-all-tasks/SKILL.md` so the orchestrator commits the agent-staged index under the subject `Task-completion: <TASK_NAME>`, built from the `##` heading text step 2b already holds verbatim, dropping the `-m "<body>"` argument and the heading-in-body sentence so the commit is subject-only, while keeping its own `git diff --cached --quiet` nothing-staged guard, its own `git commit` with no pathspec, no routing through `shared/commit-procedure.md`, and the `complete-task` agent's return contract unchanged. The milestone needs it so both completion runners make one and the same subject for one unit of work. Verified by the skill naming no `Tasklist-completion:` marker and no commit body, and `uv run scripts/build_hosts.py --check` passing with the rebuilt host trees committed.

**Verified:**

- Step 2c of `core/skills/complete-all-tasks/SKILL.md` commits the agent-staged index under the subject `Task-completion: <TASK_NAME>`, built from the exact `##` heading text step 2b already holds.
- Step 2c carries no `-m "<body>"` argument and no heading-in-body sentence; the commit is subject-only (`git commit -m "Task-completion: <TASK_NAME>"`).
- Step 2c keeps its own `git diff --cached --quiet` nothing-staged guard and its own `git commit` with no pathspec, and the skill does not route through `shared/commit-procedure.md`.
- `core/agents/complete-task.md` and step 2b's DONE/FAILED return handling are unchanged.
- `grep` finds no `Tasklist-completion` and no commit body in the core or either rendered `complete-all-tasks/SKILL.md`.
- `uv run scripts/build_hosts.py --check` passes after the rebuild, with the rebuilt `hosts/claude/` and `hosts/antigravity/` copies of the skill in the change set.

---
