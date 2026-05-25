---
name: submit-backlog-task
description: Convert an implementation issue (surfaced during development) into a properly formatted task in the current milestone's TASKS_TODO.md, anchored to the current milestone requirements.
---

# submit-backlog-task

Takes a brief issue description and inserts a new, implementation-ready task into the current milestone's `TASKS_TODO.md`.

## Invocation

```
/submit-backlog-task <issue description>
```

`<issue description>` is a free-form description of the problem or gap discovered during implementation. It should be specific enough to write a concrete task from.

## Workflow

### 0. Find the current milestone

Read `CLAUDE.md` and extract the path from the `## Current Milestone` section (shown in backticks, e.g. `milestones/milestone_11_tbd/`). Use this as `<MILESTONE_DIR>` throughout this workflow.

### 1. Read context

Read the following in parallel:
- `<MILESTONE_DIR>/requirements.md` — to understand the relevant requirements and constraints.
- `<MILESTONE_DIR>/TASKS_TODO.md` — to understand existing task scope and avoid duplication.
- `<MILESTONE_DIR>/TASKS_DONE.md` — to confirm the issue is not already addressed by a completed task.

### 2. Understand the issue

Interpret the issue description in light of the milestone requirements. Determine:
- Which requirement or system the issue touches.
- Whether it is a gap (missing implementation) or a correction (wrong implementation).
- Whether it depends on any not-yet-completed tasks in `TASKS_TODO.md`.

If the issue duplicates an existing task, stop and tell the user which task already covers it.

### 3. Write the task

Use this exact template:

```markdown
## <Task Title>

<1–3 sentence description of what the task does and why it is needed.>

**Steps:**
1. <Concrete, tool-actionable step.>
2. <...>

**Success:**
- <Verifiable criterion observable in the Editor or Console without running the game.>
- <...>

---
```

Guidelines:
- **Title**: 4–8 words, title-cased, unique within the file.
- **Steps**: imperative and concrete — reference exact file paths, class names, method names, and field names. Never say "update the script"; say which file and what change.
- **Success**: checkable without human judgement. Prefer Inspector state, Console output, or compilation result over subjective criteria.
- **No rationale or design discussion** — that belongs in the requirements doc.

### 4. Insert the task into TASKS_TODO.md

Determine the correct priority position:
- If the task is a prerequisite for existing tasks, insert it **before** those tasks.
- If the task depends on existing tasks, insert it **after** those tasks.
- Otherwise, append it at the end of the file.

Use the `Edit` tool to insert the new `##` section (including its trailing `---` separator) at the chosen position.

### 5. Confirm

Output a one-line summary: the task title and where it was inserted (e.g., "Added as task #3 of 5").

## Rules

- Never invent requirements not traceable to the issue description or the milestone requirements doc.
- Do not create tasks for work already in `TASKS_DONE.md`.
- Do not modify any existing task — only insert new content.
- The `---` separator after each task section is mandatory; do not omit it.
