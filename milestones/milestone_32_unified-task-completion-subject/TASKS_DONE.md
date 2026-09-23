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

## Sync Docs Pages To Unified Subject

Update the `complete-all-tasks` and `complete-task` entries of `docs/skill-reference.md` (lines 81 and 85) so both state the one subject-only `Task-completion: <task heading>` commit with no `Tasklist-completion:` marker and no heading-in-body claim, and extend the "`/complete-all-tasks` commits once per task" clause in the `## How skills commit` paragraph of `docs/workflow.md` to name that subject with no body as the same subject inline `/complete-task` uses. The milestone needs it so the docs describe the commits the runtime now makes. Verified by `grep` finding no `Tasklist-completion` under `docs/` and both pages agreeing with the rewritten orchestrator skill.

**Verified:**

- The `complete-all-tasks` entry of `docs/skill-reference.md` states the one subject-only commit per task under `Task-completion: <task heading>` with no body, and no longer names a `Tasklist-completion:` marker or a heading-in-body commit.
- The `complete-task` entry of `docs/skill-reference.md` states the same subject-only `Task-completion: <task heading>` commit with no body.
- The "`/complete-all-tasks` commits once per task" clause of the `## How skills commit` paragraph in `docs/workflow.md` names its subject, `Task-completion: <task heading>` with no body, as the same subject inline `/complete-task` uses.
- `grep -rn Tasklist-completion docs/` finds nothing.
- Both pages agree with step 2c of `core/skills/complete-all-tasks/SKILL.md` (`git commit -m "Task-completion: <TASK_NAME>"`, no body) and with `core/skills/complete-task/SKILL.md` (SUBJECT `Task-completion: <task heading>`, no BODY).

---

## CLAUDE.md Unified Subject Invariant

Extend the committing bullet of `CLAUDE.md` with one clause stating that both completion runners commit subject-only under `Task-completion: <Task Title>`, with the task's `##` heading copied exactly, and that the retired `Tasklist-completion:` marker with its heading-in-body commits must not be restored, each with its rationale: one subject for one unit of work whichever runner makes it, and the heading visible in the subject line so history can be searched without reading commit bodies. The milestone needs it so a later editor does not reintroduce the split. Verified by the committing bullet carrying the clause and both rationales, and the rest of `CLAUDE.md` naming `Tasklist-completion:` only as the retired marker.

**Verified:**

- The committing bullet of `CLAUDE.md` carries one clause stating that both completion runners commit subject-only under `Task-completion: <Task Title>`, with the task's `##` heading copied exactly.
- The same clause states that the retired `Tasklist-completion:` marker with its heading-in-body commits must not be restored.
- The clause carries both rationales: one unit of work gets one subject whichever runner makes it, and the heading in the subject line lets history be searched without reading commit bodies.
- `grep -n Tasklist-completion CLAUDE.md` finds only that clause, naming the marker solely as retired.

---
