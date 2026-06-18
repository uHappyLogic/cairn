---
name: complete-all-tasks
description: Complete all tasks from the current milestone's TASKS_TODO.md one by one, committing after each completed task.
---

# complete-all-tasks

Pure orchestrator. Reads the current milestone's task list and spawns one isolated subagent per task. Each subagent gets a clean context and completes exactly one task.

## Invocation

```
/complete-all-tasks
```

No arguments required.

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Read the task list

Read `<MILESTONE_DIR>/TASKS_TODO.md` and confirm it has at least one `##` section. If the file is empty or has no `##` sections, report that the task list is empty and stop.

### 2. For each task (top to bottom)

Repeat the following loop until no tasks remain:

#### 2a. Identify the next task

Re-read `<MILESTONE_DIR>/TASKS_TODO.md` to get the current top task — the first `##` heading in the file. Do not cache the task list across iterations, since each completed task is removed.

#### 2b. Spawn a subagent to complete the task

Use the `Agent` tool with `subagent_type: "complete-task"` and a prompt containing only the task name, substituting `<TASK_NAME>` with the exact `##` heading text (without the `##` prefix):

```
Complete the task named: "<TASK_NAME>"
```

Wait for the agent to return.

- If the agent reports FAILED, stop the loop, report the task name and the failure reason to the user, and stop. Do not proceed to 2c.
- If the agent returns without an explicit DONE or FAILED status (e.g. it returned early, produced no output, or gave an ambiguous result), treat this as FAILED. Report what was returned, stop the loop, and do not proceed to 2c. **Never attempt to complete the task yourself as a fallback.**

#### 2c. Commit the changes

After the subagent confirms success and the task has been moved to `<MILESTONE_DIR>/TASKS_DONE.md`, commit:

```
git add -A
git commit -m "<task heading>"
```

Use the task's `##` heading (without the `##` prefix) as the commit message subject.

#### 2d. Continue

Go back to 2a and process the next task.

### 3. Report completion

When `<MILESTONE_DIR>/TASKS_TODO.md` contains no more `##` sections, report that all tasks have been completed and list each task that was completed.

## Rules

- Re-read `TASKS_TODO.md` at the start of every iteration — do not cache the task list across iterations.
- Never commit partial work. Only commit after the subagent has confirmed success and the task has been moved to `TASKS_DONE.md`.
- If any task fails, stop the loop immediately and report which task failed and why.
- This file is the orchestrator only — **never complete tasks directly here, even as a fallback when a subagent fails.**
