---
name: implement-backlog-task
description: Implement a named task from the current milestone's TASKS_TODO.md using Unity MCP tools, then move it to TASKS_DONE.md.
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

### 3. Verify Unity Editor is ready

Use the `unity-mcp-skill` workflow:
- Read `mcpforunity://editor/state` to confirm Unity is open and not compiling.
- If `is_compiling` is true, wait and poll until it clears before proceeding.

### 4. Implement the task

Execute all steps described in the task (see `unity-mcp-skill` for potential tool usage patterns).

After any script or shader creation, always:
1. Poll `editor/state` until `is_compiling == false`.
2. `read_console(types=["error"], count=20, include_stacktrace=true)` and fix any errors before continuing.

### 5. Verify it works

Re-read the task's **Success** section and confirm each criterion is met.

### 6. Update the milestone backlog

Once all success criteria pass:

1. **Remove** the completed `##` section (and its trailing `---` separator) from `<MILESTONE_DIR>/TASKS_TODO.md`.
2. **Append** the same section to `<MILESTONE_DIR>/TASKS_DONE.md` under a `---` separator.

Use the `Edit` tool for both files.

## Rules

- Do not skip the compilation check — attaching a component from a script that hasn't compiled yet will silently fail.
- Do not move the task to TASKS_DONE.md until every success criterion is confirmed.
- If a step fails, diagnose via `read_console` and fix before continuing — do not mark partial work as done.
- Prefer `batch_execute` when making multiple independent MCP calls (10–100× faster).
