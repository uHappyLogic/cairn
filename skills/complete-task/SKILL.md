---
name: complete-task
description: Complete a single named task from the current milestone's TASKS_TODO.md inline in this conversation, then move it to TASKS_DONE.md. Use for one ad-hoc task you want to stay available to discuss and tweak afterwards.
---

# complete-task

Completes one named ad-hoc task **inline, in the current conversation** — not in a subagent
— so the work context stays in hand for follow-up.

For completing the whole task list unattended, use `/complete-all-tasks` instead.

## Invocation

```
/complete-task <task name>
```

`<task name>` is the full or partial text of a `##` heading in the current milestone's
`TASKS_TODO.md`.

## Workflow

### 1. Run the shared procedure inline

Read and follow the shared procedure at
`${CLAUDE_PLUGIN_ROOT}/shared/complete-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if
you need to resolve the path), carrying out every step **yourself, in this conversation**.
Never spawn the `complete-task` agent.

### 2. Commit the completion

When the procedure finishes (success criteria verified, task moved to `TASKS_DONE.md`),
read and follow the shared commit procedure at
`${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you
need to resolve the path), carrying out its steps yourself. Supply it these two inputs:

- **PATHS** — this skill's own change set: the exact paths the shared completion procedure
  recorded as it created or edited files while carrying out the task, plus the two
  milestone task-list files `<MILESTONE_DIR>/TASKS_TODO.md` (the task left it) and
  `<MILESTONE_DIR>/TASKS_DONE.md` (the task joined it). Name each path explicitly — never
  `git add -A`.
- **SUBJECT** — `Task-completion: <task heading>`.

The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the
commit. A completion that was abandoned or failed before it changed any file leaves those
paths untouched, so the guard stages nothing and commits nothing.

### 3. Hand back

On the success path — the task was completed, verified, moved to `TASKS_DONE.md`, and
committed — print exactly one fixed terse status line and nothing else:

`Task completed.`

Carry no task heading, verification detail, or commit subject, and print no follow-up
pointer.

If step 2's dirty-own-path guard fired because the completion was abandoned before it
changed any file — nothing was committed — print instead a distinct one-line no-op message
stating that nothing was completed and briefly why (e.g. `No task completed — no file
changed.`), not the terse success line.
