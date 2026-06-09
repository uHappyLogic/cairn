---
name: implement-backlog-task
description: Implement a named task from the current milestone's TASKS_TODO.md, then move it to TASKS_DONE.md.
---

# implement-backlog-task

Implement the task whose `##` heading matches the name given in the skill argument.

## Invocation

```
/implement-backlog-task <task name>
```

`<task name>` is the full or partial text of a `##` heading in the current milestone's `TASKS_TODO.md`.

## Workflow

### 0. Find the current milestone

Read `CLAUDE.md` and extract the path from the `## Current Milestone` section (shown in backticks, e.g. `milestones/milestone_11_tbd/`). Use this as `<MILESTONE_DIR>` throughout this workflow.

### 1. Find the task

Read `<MILESTONE_DIR>/TASKS_TODO.md` and locate the `##` section whose heading matches (case-insensitive, partial match is fine). If no match is found, list all available task headings and stop.

### 2. Read and understand the task

Parse the full task description: requirements, steps, success criteria, and any code snippets.

### 3. Load the implementation environment

Read `CLAUDE.md` at the workspace root and hold in context:
- Available MCP tools for this project
- Build & test commands — how to verify changes after editing
- Conventions — post-edit verification steps to always follow

### 4. Implement the task

Execute all steps described in the task.

After any source file creation or modification, follow the post-edit conventions and run the relevant verification command from `CLAUDE.md`. Fix any errors before continuing.

Use the MCP tools documented in `CLAUDE.md` where the task steps call for them. For file edits use `Read` then `Edit`. For shell commands use `Bash`.

### 5. Verify it works

Re-read the task's **Success** section and confirm each criterion is met.

### 6. Update the milestone backlog

Once all success criteria pass:

1. **Remove** the completed `##` section (and its trailing `---` separator) from `<MILESTONE_DIR>/TASKS_TODO.md`.
2. **Append** the same section to `<MILESTONE_DIR>/TASKS_DONE.md` under a `---` separator.

Use the `Edit` tool for both files.

## Rules

- Follow the conventions from `CLAUDE.md` for all post-edit verification — do not skip these steps.
- Do not move the task to TASKS_DONE.md until every success criterion is confirmed.
- If a step fails, diagnose the root cause using available tools and fix before continuing — do not mark partial work as done.
