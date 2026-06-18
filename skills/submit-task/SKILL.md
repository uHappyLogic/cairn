---
name: submit-task
description: Add a single implementation issue (surfaced during development) to the current milestone's TASKS_TODO.md as a properly formatted task. Use when the user reports a concrete bug, gap, or "we should also..." that is already clear enough to queue. Triages for duplicates, decides where the task belongs, then authors and inserts the task inline.
---

# submit-task

Turns a single, already-clear issue into an implementation-ready task in the current
milestone's `TASKS_TODO.md`. This skill is the user-facing entry point
(`/submit-task`) and the handoff target for `/discuss-new-task`.

It does two things the agent can't: the triage and positioning that need the **whole
task list in view** — checking for duplicates and deciding where the task belongs — and then
it authors and inserts the task **inline, in this conversation**. Running the authoring
inline is deliberate: the contract surface, notes, and success criteria you just wrote stay
in context, so the user can immediately ask why a choice was made or request a tweak. For
bulk authoring, `derive-tasks` instead spawns the `submit-task` **agent**, which
runs the same shared procedure in isolation so N tasks' reasoning never lands in its
context. If the issue is still vague or might be several tasks, use
`/discuss-new-task` first.

## Invocation

```
/submit-task <issue description>
```

`<issue description>` is a free-form description of a problem or gap discovered during
development, specific enough that the affected system, desired behavior, and how to verify
it are clear.

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Read context for triage

Read in parallel:
- `<MILESTONE_DIR>/requirements.md` — to confirm the issue fits the milestone's scope.
- `<MILESTONE_DIR>/TASKS_TODO.md` — existing pending tasks, for duplicate-detection and positioning.
- `<MILESTONE_DIR>/TASKS_DONE.md` — completed work, to catch issues already addressed.

### 2. Triage

- **Duplicate?** If an existing pending task or a completed task already covers this issue, stop and tell the user which task covers it. Do not add a duplicate.
- **In scope?** If the issue clearly belongs to a different milestone or is really an open design decision, say so and point to the better tool (`/discuss-open-question`) instead of queuing it.

### 3. Decide the position

You hold the whole task list, so you decide where the task goes:
- If the task is a prerequisite for an existing task, position it **before** that task: `before: <Task Title>`.
- If it depends on an existing task, position it **after** that task: `after: <Task Title>`.
- Otherwise, `append`.

### 4. Author and insert the task inline

Run the shared procedure at `${CLAUDE_PLUGIN_ROOT}/shared/submit-procedure.md` **yourself,
in this conversation** (run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path),
with the issue as the BRIEF and the POSITION you chose in step 3. It owns the task template,
the authoring guidelines, and the insertion logic — follow it exactly.

Do **not** spawn the `submit-task` agent — that would discard the authoring context
this skill exists to keep. (You already read `requirements.md` and `TASKS_TODO.md` in
step 1, so reuse them rather than re-reading.)

### 5. Confirm

Report the task title and where it was inserted (e.g. `Added "Fix Wall Collision Sweep" —
appended (task #4 of 4).`), then stay available: the user may now ask why you scoped it that
way or request a tweak, with the authoring context still in hand. If the procedure's
atomic-scope rule left a second buildable piece unauthored, mention it and offer to queue it
as a follow-up task. If you could not author a concrete task — typically because the issue
was too vague — say so and suggest `/discuss-new-task` to sharpen it first.

## Rules

- Triage and position from the whole-task-list view (that is the skill's job), then author and
  insert via the shared procedure — never delegate this skill to the `submit-task`
  agent. (The shared file is the single source of truth, so the authored task is identical
  either way; only the context differs.)
- Never queue a duplicate of an existing pending or completed task.
- For vague issues or ones that may span several tasks, route through `/discuss-new-task` first.
