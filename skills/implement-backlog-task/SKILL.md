---
name: implement-backlog-task
description: Implement a single named task from the current milestone's TASKS_TODO.md, then move it to TASKS_DONE.md. Thin user-facing entry point that delegates the work to the implement-backlog-task agent.
---

# implement-backlog-task

Thin wrapper. Implements one ad-hoc named task by spawning the `implement-backlog-task` agent, which owns the full implementation procedure (find task → load environment → implement → verify success criteria → move TODO→DONE). Keeping the procedure in a single place — the agent — means the `implement-backlog-tasks` orchestrator and this single-task entry point can never drift apart.

## Invocation

```
/implement-backlog-task <task name>
```

`<task name>` is the full or partial text of a `##` heading in the current milestone's `TASKS_TODO.md`. The agent resolves the current milestone itself (from `CLAUDE.md`), so nothing needs to be looked up here first.

## Workflow

### 1. Spawn the implementation agent

Use the `Agent` tool with `subagent_type: "implement-backlog-task"` and a prompt containing only the task name:

```
Implement the task named: "<task name>"
```

Wait for the agent to return. It runs in an isolated context and ends with `DONE` or `FAILED: <reason>`.

### 2. Relay the result

- If the agent reports `DONE`, tell the user the task was implemented and moved to `TASKS_DONE.md`.
- If the agent reports `FAILED` (including the no-matching-task case), relay the failure reason to the user. If no task matched, point them at the available headings the agent reported so they can retry with a correct name.
- If the agent returns without an explicit `DONE` or `FAILED`, treat it as a failure: report what came back and stop. **Never implement the task yourself as a fallback.**

## Rules

- This skill only spawns the agent and relays its result — it never implements tasks directly, even when the agent fails.
- Do not commit. Committing belongs to the `implement-backlog-tasks` orchestrator alone; an ad-hoc single-task run leaves the changes staged for the user to review and commit.
