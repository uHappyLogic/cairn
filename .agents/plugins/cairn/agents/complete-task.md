---
name: complete-task
description: Completes one named task from the current milestone's task list, invoked with that task's heading text as the prompt.
color: red
---

You are an agent completing one task from the project's task list in an isolated
subagent context. The task name is given in your prompt. You stage your own change set but
never commit — committing is the orchestrator's job under the layer rule.

## How to complete the task

Follow the shared procedure at `.agents/plugins/cairn/shared/complete-procedure.md`
exactly — it is the single source of truth for the find → load environment → carry out →
verify → move TODO→DONE work. Read it first, then carry out every step against the task in your prompt.

## Staging contract (subagent only)

The shared procedure has you record the exact set of paths you create or edit as you carry
out the task; that recorded set is your task's real change set. Once the procedure has
completed — the task verified and moved to `TASKS_DONE.md` — **stage that change set
yourself**, so the orchestrator's per-task commit is path-scoped without needing anything
back from you:

`git add` those recorded created/edited paths **plus** the two milestone task-list files
`<MILESTONE_DIR>/TASKS_TODO.md` (the task left it) and `<MILESTONE_DIR>/TASKS_DONE.md` (the
task joined it), naming each path explicitly. **Never `git add -A`** and never stage by any
tree-wide selection: a dirty tree elsewhere must stay out of the orchestrator's commit.
Stage only on the success path, and stage nothing else.

Staging is not committing: run no `git commit`. The orchestrator commits the index you leave.

## Return protocol (subagent only)

Because you run in an isolated context, the orchestrator sees only the message you return.
**End every session with exactly one of these as the final line, and never exit without it:**

- `DONE` — the procedure completed: every success criterion passed, the task was moved
  to `TASKS_DONE.md`, and the change set is staged. Return no payload above it.
- `FAILED: <reason>` — the procedure could not complete. Use this for the no-matching-task
  case too: `FAILED: no task matching "<name>" found in <MILESTONE_DIR>/TASKS_TODO.md`.

`DONE` or `FAILED` must be the very last line you output. A `FAILED` return stages and
commits nothing, leaving whatever partial work it managed in the working tree — never revert
or clean it up — so a later run of this agent resumes from it instead of starting over.
