---
name: submit-task
description: Add a single issue (surfaced during development) to the current milestone's TASKS_TODO.md as a brief-level task section. Use when the user reports a concrete bug, gap, or "we should also..." that is already clear enough to queue. Triages for duplicates, decides where the task belongs, then authors and inserts the task inline.
---

# submit-task

Turns a single, already-clear issue into a brief-level task section in the current
milestone's `TASKS_TODO.md`. This skill is the user-facing entry point
(`/submit-task`) and the handoff target for `/discuss-new-task`.

It owns the triage and positioning that need the **whole task list in view** — checking for
duplicates and deciding where the task belongs — and then it authors and inserts the task
**inline, in this conversation**. Authoring inline is deliberate: the task you just wrote
and the reasoning behind it stay in context, so the user can immediately ask why a choice
was made or request a tweak. If the issue is still vague or might be several tasks, use
`/discuss-new-task` first.

A task section states *what* is to be achieved, not how — the completer derives the flow and
the formal acceptance bar itself from the description plus `requirements.md`, against the
live project. Keep what you author at that altitude.

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

### 4. Author the task section inline

Read the shared task format at `${CLAUDE_PLUGIN_ROOT}/shared/task-format.md` (run
`echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path) and write the task section
**yourself, in this conversation**, following its template and authoring guidelines exactly.
That file is the single source of truth for the shape of a task section — the `##` title
heading, the 1–3 sentence description with the "how it would be verified" clause folded in
as prose, and the mandatory trailing `---` separator, and nothing else. Do not restate or
re-derive that format here, and do not add a steps, contract, notes, or done-ness section
under any name.

The issue as the user described it, sharpened against the milestone's scope, *is* the task
body; writing it down is a transcription into that format, not a second authoring pass that
adds detail.

(You already read `requirements.md` and `TASKS_TODO.md` in step 1, so reuse them rather
than re-reading.)

### 5. Insert the section at the chosen position

Insert the authored section into `<MILESTONE_DIR>/TASKS_TODO.md` at the position you decided
in step 3:

- **`append`** — add the section at the end of the file.
- **`before: <Task Title>`** — insert it immediately before that section's `##` heading line.
- **`after: <Task Title>`** — insert it immediately after that section's trailing `---` separator.

If a `before:`/`after:` anchor title matches no existing section, append the task at the end
instead and say so — never guess at a different anchor. That fallback is a one-line advisory
printed alongside step 7's status line, since nothing in the file records the anchor miss.

Never modify or reorder the existing sections; the insert only adds. Always end the inserted
section with its trailing `---` separator — that separator is mandatory, because
`shared/complete-procedure.md` parses task sections by it.

### 6. Commit the inserted task

Read and follow the shared commit procedure at `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path), carrying out its steps yourself. Supply it these two inputs:

- **PATHS** — this skill's own change set: `<MILESTONE_DIR>/TASKS_TODO.md` (the file it just inserted the task into).
- **SUBJECT** — `Task-submission: <task title>`.

The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit; do not restate those mechanics here.

### 7. Confirm

On the success path — the task was authored, inserted, and committed — print exactly one
fixed terse status line and nothing else:

`Task submitted.`

Carry no task title, insert position, or commit subject, and print no next-step or follow-up
pointer. (The authoring context stays in hand for follow-up exactly as before; only the
printed summary goes — the committed diff and git log are the durable record.)

If step 6's dirty-own-path guard fired because the insert authored nothing — no file
changed, so nothing was committed — print instead a distinct one-line no-op message stating
that nothing was submitted and briefly why (e.g. `No task submitted — nothing was authored.`),
not the terse success line.

If you could not author a concrete task — typically because the issue was too vague — say so
and suggest `/discuss-new-task` to sharpen it first.

## Rules

- Triage and position from the whole-task-list view (that is the skill's job), then author the
  section in the shared brief-level format and insert it yourself.
- Never queue a duplicate of an existing pending or completed task.
- For vague issues or ones that may span several tasks, route through `/discuss-new-task` first.
