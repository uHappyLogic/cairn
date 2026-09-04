---
name: complete-all-tasks
description: Complete every task in the current milestone's TASKS_TODO.md one by one, moving each to TASKS_DONE.md.
---

# complete-all-tasks

Pure orchestrator. Reads the current milestone's task list and spawns one isolated subagent per task, each with a clean context and exactly one task to complete. Never complete a task directly here, even as a fallback when a subagent fails.

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
- On `DONE`, the agent also hands back the explicit set of paths it created or edited while carrying out the task (its recorded change set). Collect those paths — you commit them in 2c.

#### 2c. Commit the changes

After the subagent returns `DONE` (success confirmed and the task moved to `<MILESTONE_DIR>/TASKS_DONE.md`), commit that task by reading and following the shared commit procedure at `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path). Supply it these two inputs:

- **PATHS** — this task's exact change set: the created/edited paths the subagent handed back in its `DONE` return, **plus** the two milestone task-list files `<MILESTONE_DIR>/TASKS_TODO.md` (the task left it) and `<MILESTONE_DIR>/TASKS_DONE.md` (the task joined it). Name each path explicitly — never `git add -A`.
- **SUBJECT** — `Tasklist-completion: <descriptor>` (e.g. `Tasklist-completion: complete one milestone task`), the marker naming this orchestrator's task-list-completion function. Put the task's `##` heading text (without the `##` prefix) in the commit **body** (a second `-m`), not in the subject.

The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit itself. Commit once per task.

#### 2d. Continue

Go back to 2a and process the next task.

### 3. Report completion

On the success path, when `<MILESTONE_DIR>/TASKS_TODO.md` contains no more `##` sections, print exactly one fixed terse status line for the whole run — `All tasks completed.` — and nothing more: no list of the tasks that were completed and no next-step pointer.

If the run committed nothing — every per-task commit in step 2c hit its dirty-own-path no-op guard, so no files changed across the whole run — do not print the terse success line; instead print a distinct one-line message stating that nothing changed and why (nothing was committed this run).
