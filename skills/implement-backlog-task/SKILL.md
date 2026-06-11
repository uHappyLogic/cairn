---
name: implement-backlog-task
description: Implement a single named task from the current milestone's TASKS_TODO.md inline in this conversation, then move it to TASKS_DONE.md. Use for one ad-hoc task you want to stay available to discuss and tweak afterwards.
---

# implement-backlog-task

Implements one named ad-hoc task **inline, in the current conversation** — not in a
subagent. Running inline is the whole point: the implementation reasoning (which files
changed, why, and what the verification showed) stays in context, so you can follow up
right after — ask why a choice was made, request a tweak, or extend the work — without the
context being thrown away.

For implementing the whole backlog unattended, use `/implement-backlog-tasks` instead — that
orchestrator deliberately runs each task in an isolated subagent and commits after each.

## Invocation

```
/implement-backlog-task <task name>
```

`<task name>` is the full or partial text of a `##` heading in the current milestone's
`TASKS_TODO.md`. The procedure resolves the current milestone itself (from `CLAUDE.md`), so
nothing needs to be looked up first.

## Workflow

### 1. Run the shared procedure inline

Read and follow the shared procedure at
`${CLAUDE_PLUGIN_ROOT}/shared/implement-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if
you need to resolve the path), carrying out every step **yourself, in this conversation**.
Do not spawn the `implement-backlog-task` agent — that would discard the working context
this skill exists to keep.

If no task matches the given name, the procedure has you stop without changes; tell the user
that and list the available `##` headings so they can retry with a correct name.

### 2. Hand back for review

When the procedure finishes (success criteria verified, task moved to `TASKS_DONE.md`):

- Summarize what you implemented and how you verified it.
- Leave the changes **staged, not committed** — committing belongs to
  `/implement-backlog-tasks` alone; an ad-hoc run leaves the diff for the user to review.
- Stay available: the user may now ask follow-up questions or request adjustments, with the
  full implementation context still in hand.

## Rules

- Run the procedure inline — never delegate this skill to the `implement-backlog-task`
  agent. (The shared file is the single source of truth, so the work is identical either
  way; only the context differs.)
- Do not commit. Leave the changes staged for the user to review and commit.
