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

## Ask-In-Context Heading Search Wording

Rewrite the step 2 sentence of `core/skills/ask-in-milestone-context/SKILL.md` that calls the task-to-commit mapping "not keyed on the heading in the subject line" as a marker-agnostic heading search: completion commits carry the task heading, so searching commit subjects and bodies for the heading text usually finds the commit, while the mapping stays best-effort, the fall-back to the live files and the "never the sole source" rule are kept, and the sentence names neither the `Task-completion:` nor the retired `Tasklist-completion:` marker and describes no era of history. The milestone needs it because the old claim becomes false once every completion subject carries the heading. Verified by the sentence's absence of both markers and of the old "not keyed" claim, and `uv run scripts/build_hosts.py --check` passing with the rebuilt host trees committed.

**Verified:**

- The step 2 git-history sentence of `core/skills/ask-in-milestone-context/SKILL.md` describes a marker-agnostic heading search: completion commits carry the task heading, so searching commit subjects and bodies for the heading text (`git log --grep`) usually finds the commit.
- The sentence keeps the task-to-commit mapping best-effort, and the bullet keeps the fall-back to the live files and the "never the sole source" rule.
- The sentence names neither `Task-completion:` nor `Tasklist-completion:`, describes no era of history, and no longer carries the "not keyed on the heading in the subject line" claim, in `core/` and both rendered `hosts/` copies.
- `uv run scripts/build_hosts.py --check` passes after the rebuild, with the rebuilt `hosts/claude/` and `hosts/antigravity/` copies of the skill in the change set.

---
