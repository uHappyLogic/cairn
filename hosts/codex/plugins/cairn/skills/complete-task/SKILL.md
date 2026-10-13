---
name: complete-task
description: Complete a single named task from the current milestone's TASKS_TODO.md inline in this conversation and move it to TASKS_DONE.md.
---

# complete-task

Completes one named ad-hoc task **inline, in the current conversation** — not in a subagent
— so the work context stays in hand for follow-up.

For completing the whole task list unattended, use `/complete-all-tasks` instead.

## Invocation

```
/complete-task <task name>
```

`<task name>` is the full or partial text of a `##` heading in the current milestone's
`TASKS_TODO.md`.

## Workflow

### 1. Run the shared procedure inline

Read and follow the shared procedure at
`${PLUGIN_ROOT}/shared/complete-procedure.md`, carrying out every step **yourself, in this conversation**,
its step 5 move run as the one shell call step 2 shows. Never spawn the `complete-task` agent.

### 2. Move and commit the completion in one shell call

Run the procedure's step 5 move as this one fixed shell call, written out in full exactly as
shown, with only `<MILESTONE_DIR>`, `<Task Title>`, the bar's bullets, and the paths replaced:

```
python3 ${PLUGIN_ROOT}/tools/task_list.py move <MILESTONE_DIR> "<Task Title>" <<'EOF' &&
- <criterion 1, as verified>
- <criterion 2, as verified>
EOF
if [ -n "$(git status --porcelain -- <recorded path 1> <recorded path 2> <MILESTONE_DIR>/TASKS_TODO.md <MILESTONE_DIR>/TASKS_DONE.md)" ]; then
  git add <recorded path 1> <recorded path 2> <MILESTONE_DIR>/TASKS_TODO.md <MILESTONE_DIR>/TASKS_DONE.md && git commit -q -m "Task-completion: <Task Title>" && echo 'completion commit landed'
fi
```

The move command and its heredoc are exactly the ones the procedure's step 5 shows. After the
`&&` the call carries out the three steps of the shared commit procedure at
`${PLUGIN_ROOT}/shared/commit-procedure.md` itself — its dirty-own-path guard, the
path-scoped `git add`, and the subject-only commit under `Task-completion: <Task Title>`, the
full `##` heading the procedure located — over this skill's own change set: the exact paths
the completion procedure recorded as it created or edited files while carrying out the task,
plus the two milestone task-list files `<MILESTONE_DIR>/TASKS_TODO.md` (the task left it) and
`<MILESTONE_DIR>/TASKS_DONE.md` (the task joined it). The guard and the `git add` name the
same paths, every path written out on the command line as its own argument and none held in
a shell variable — never `git add -A`. Git's success output is silenced.

What the call prints is the whole outcome: `completion commit landed` when the commit landed;
nothing when the guard found none of the paths changed; otherwise the move's one `Error:` line
(both task files unchanged, nothing staged or committed — diagnose it, fix it, and run the call
again) or git's message for a commit it refused.

### 3. Hand back

On the success path — the task was completed, verified, moved to `TASKS_DONE.md`, and
committed, the call printing `completion commit landed` — print exactly one fixed terse
status line and nothing else:

`Task completed.`

Carry no task heading, verification detail, or commit subject, and print no follow-up
pointer.

If nothing was committed because the completion was abandoned before it changed any file —
step 2's call never ran, or its guard found no path changed — print instead a distinct
one-line no-op message stating that nothing was completed and briefly why (e.g. `No task completed — no file
changed.`), not the terse success line.
