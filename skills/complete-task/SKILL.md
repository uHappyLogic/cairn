---
name: complete-task
description: Complete a single named task from the current milestone's TASKS_TODO.md inline in this conversation, then move it to TASKS_DONE.md. Use for one ad-hoc task you want to stay available to discuss and tweak afterwards.
---

# complete-task

Completes one named ad-hoc task **inline, in the current conversation** — not in a
subagent. Running inline is the whole point: the work reasoning (which files
changed, why, and what the verification showed) stays in context, so you can follow up
right after — ask why a choice was made, request a tweak, or extend the work — without the
context being thrown away.

For completing the whole task list unattended, use `/complete-all-tasks` instead — that
orchestrator deliberately runs each task in an isolated subagent and commits after each.

## Invocation

```
/complete-task <task name>
```

`<task name>` is the full or partial text of a `##` heading in the current milestone's
`TASKS_TODO.md`. The procedure resolves the current milestone itself (from `CLAUDE.md`), so
nothing needs to be looked up first.

## Workflow

### 1. Run the shared procedure inline

Read and follow the shared procedure at
`${CLAUDE_PLUGIN_ROOT}/shared/complete-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if
you need to resolve the path), carrying out every step **yourself, in this conversation**.
Do not spawn the `complete-task` agent — that would discard the working context
this skill exists to keep.

If no task matches the given name, the procedure has you stop without changes; tell the user
that and list the available `##` headings so they can retry with a correct name.

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
commit; do not restate those mechanics here. A completion that was abandoned or failed
before it changed any file leaves those paths untouched, so the guard stages nothing and
commits nothing.

### 3. Hand back

When the commit is recorded:

- Summarize what you completed, how you verified it, and the commit you made.
- Stay available: the user may now ask follow-up questions or request adjustments, with the
  full work context still in hand.

## Rules

- Run the procedure inline — never delegate this skill to the `complete-task`
  agent. (The shared file is the single source of truth, so the work is identical either
  way; only the context differs.)
