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
/complete-task [--milestone <milestone_id>] <task name>
```

`<task name>` is the full or partial text of a `##` heading in the current milestone's
`TASKS_TODO.md`. The optional leading `--milestone <milestone_id>` names the milestone by its
exact directory name under `milestones/`, e.g. `milestone_12_user-guide`, in place of the
current-milestone pointer.

## Workflow

### 1. Run the shared procedure inline

First strip a leading `--milestone <milestone_id>` from the invocation text by the rule in
`{{PLUGIN_ROOT}}/shared/get-current-milestone.md`, holding any override as the input of the
procedure's milestone resolution and reading only the rest as the task name. Read and follow
the shared procedure at
`{{PLUGIN_ROOT}}/shared/complete-procedure.md`, carrying out every step **yourself, in this conversation**,
its step 5 move run as the one shell call step 2 shows. Never spawn the `complete-task` agent.

### 2. Move and commit the completion in one shell call

Run the procedure's step 5 move as this one fixed shell call, written out in full exactly as
shown, with only `<MILESTONE_DIR>`, `<Task Title>`, the bar's bullets, and the paths replaced:

```
python3 {{PLUGIN_ROOT}}/tools/task_list.py move <MILESTONE_DIR> "<Task Title>" <<'EOF' &&
- <criterion 1, as verified>
- <criterion 2, as verified>
EOF
out="$(python3 {{PLUGIN_ROOT}}/tools/commit.py --subject "Task-completion: <Task Title>" -- <recorded path 1> <recorded path 2> <MILESTONE_DIR>/TASKS_TODO.md <MILESTONE_DIR>/TASKS_DONE.md)" &&
if [ -z "$out" ]; then
  echo 'completion commit landed'
fi
```

The move command and its heredoc are exactly the ones the procedure's step 5 shows. After the
`&&` the call runs the one command of the shared commit procedure at
`{{PLUGIN_ROOT}}/shared/commit-procedure.md`, the plugin's commit tool, with
`Task-completion: <Task Title>`, the full `##` heading the procedure located, as its subject,
no body, and this skill's own change set as its paths: the exact paths the completion
procedure recorded as it created or edited files while carrying out the task, plus the two
milestone task-list files `<MILESTONE_DIR>/TASKS_TODO.md` (the task left it) and
`<MILESTONE_DIR>/TASKS_DONE.md` (the task joined it), every path written out on the command
line after `--` as its own argument and none held in a shell variable. The tool runs the
dirty-own-path guard over those paths, stages exactly them (never `git add -A`), and commits
them with them as the commit's pathspec, so nothing else the index holds — a change another
run has staged included — rides in the completion's commit, and it repeats a git write another
process's lock refused before giving up. Its stdout is captured in `out`: empty when the commit
landed, its fixed no-op line when none of the paths changed, so `completion commit landed` is
printed only when `out` is empty and a no-op commits and prints nothing. `out` is one quoted
value set and used within this one call, never a tool command or a path list.

What the call prints is the whole outcome: `completion commit landed` when the commit landed;
nothing when the commit tool found none of the paths changed; otherwise the move's one
`Error:` line (both task files unchanged, nothing staged or committed — diagnose it, fix it,
and run the call again) or, once the move has landed, the commit tool's one `Error:` line,
naming the git command that failed and carrying git's own message, with nothing committed.

### 3. Hand back

On the success path — the task was completed, verified, moved to `TASKS_DONE.md`, and
committed, the call printing `completion commit landed` — print exactly one fixed terse
status line and nothing else:

`Task completed.`

Carry no task heading, verification detail, or commit subject, and print no follow-up
pointer.

If nothing was committed because the completion was abandoned before it changed any file —
step 2's call never ran, or its commit tool found no path changed — print instead this one
fixed no-op line, not the terse success line:

```
No task completed — no file changed.
```

A task name matching no section is the procedure's own stop: its fixed line and the
available headings are the whole report.
