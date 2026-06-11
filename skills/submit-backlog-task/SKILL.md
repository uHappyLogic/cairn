---
name: submit-backlog-task
description: Add a single implementation issue (surfaced during development) to the current milestone's TASKS_TODO.md as a properly formatted task. Use when the user reports a concrete bug, gap, or "we should also..." that is already clear enough to queue. Triages for duplicates, decides where the task belongs, and delegates the detailed authoring to the submit-backlog-task agent.
---

# submit-backlog-task

Turns a single, already-clear issue into an implementation-ready task in the current milestone's `TASKS_TODO.md`. This skill is the user-facing entry point (`/submit-backlog-task`) and the handoff target for `/discuss-new-backlog-task`.

It is deliberately thin: it does the two things that need the **whole backlog in view** — checking for duplicates and deciding where the new task belongs — then hands the actual task authoring (the contract surface, notes, success criteria) to the `submit-backlog-task` **agent**. The agent owns the task template and does its technical reasoning in a clean context, so that reasoning never lands in this conversation. If the issue is still vague or might be several tasks, use `/discuss-new-backlog-task` first.

## Invocation

```
/submit-backlog-task <issue description>
```

`<issue description>` is a free-form description of a problem or gap discovered during implementation, specific enough that the affected system, desired behavior, and how to verify it are clear.

## Workflow

### 0. Find the current milestone

Read `CLAUDE.md` and extract the path from the `## Current Milestone` section (shown in backticks, e.g. `milestones/milestone_11_tbd/`). Use this as `<MILESTONE_DIR>`.

### 1. Read context for triage

Read in parallel:
- `<MILESTONE_DIR>/requirements.md` — to confirm the issue fits the milestone's scope.
- `<MILESTONE_DIR>/TASKS_TODO.md` — existing pending tasks, for duplicate-detection and positioning.
- `<MILESTONE_DIR>/TASKS_DONE.md` — completed work, to catch issues already addressed.

### 2. Triage

- **Duplicate?** If an existing pending task or a completed task already covers this issue, stop and tell the user which task covers it. Do not add a duplicate.
- **In scope?** If the issue clearly belongs to a different milestone or is really an open design decision, say so and point to the better tool (`/discuss-open-question`) instead of queuing it.

### 3. Decide the position

You hold the whole backlog, so you decide where the task goes — the agent will not re-derive this:
- If the task is a prerequisite for an existing task, position it **before** that task: `before: <Task Title>`.
- If it depends on an existing task, position it **after** that task: `after: <Task Title>`.
- Otherwise, `append`.

### 4. Delegate authoring to the agent

Spawn the `submit-backlog-task` agent with the `Agent` tool (`subagent_type: "submit-backlog-task"`), passing the issue as the brief and the position you chose:

```
Author and insert one backlog task.

BRIEF:
<the issue description, plus any clarifying context you gathered>

POSITION: <append | before: <Task Title> | after: <Task Title>>
```

Wait for it to return.

### 5. Confirm

Relay the agent's result: the task title and where it was inserted (e.g. `Added "Fix Wall Collision Sweep" — appended (task #4 of 4).`). If the agent returned `FAILED: <reason>`, report that reason — typically the issue was too vague, in which case suggest `/discuss-new-backlog-task` to sharpen it first.

## Rules

- This skill triages and positions; it does not author task bodies or edit `TASKS_TODO.md` directly — the agent does that, so the task format stays defined in exactly one place.
- Never queue a duplicate of an existing pending or completed task.
- Decide position from the whole-backlog view and pass it to the agent; don't make the agent guess.
- For vague issues or ones that may span several tasks, route through `/discuss-new-backlog-task` first.
