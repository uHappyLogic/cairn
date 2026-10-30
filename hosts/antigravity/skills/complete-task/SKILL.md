---
name: complete-task
description: Complete a single named task from the named milestone's TASKS_TODO.md inline in this conversation and commit it with its verified bar.
---

# complete-task

Completes one named ad-hoc task **inline, in the current conversation** — not in a subagent
— so the work context stays in hand for follow-up.

For completing the whole task list unattended, use `/complete-all-tasks` instead.

## Invocation

```
/complete-task --milestone <path> <task name>
```

`<task name>` is the full or partial text of a `##` heading in the named milestone's
`TASKS_TODO.md`. The required leading `--milestone <path>` names the milestone by its
repo-relative path, exactly as the definition tool printed it, trailing slash included, e.g.
`milestones/user-guide/`.

## Workflow

### 1. Run the shared procedure inline

First strip the leading `--milestone <path>` from the invocation text by the rule in
`~/.gemini/config/plugins/cairn/shared/resolve-milestone.md`, holding its value as the input of the
procedure's milestone resolution and reading only the rest as the task name. Read and follow
the shared procedure at
`~/.gemini/config/plugins/cairn/shared/complete-procedure.md`, carrying out every step **yourself, in this conversation**,
its step 5 removal run as the one shell call step 2 shows. Never spawn the `complete-task` agent.

### 2. Remove and commit the completion in one shell call

Run the procedure's step 5 removal as this one fixed shell call, written out in full exactly
as shown, with only `<MILESTONE_DIR>`, `<Task Title>`, the bar's bullets, and the paths
replaced:

```
{ bar="$(cat)"; } <<'EOF' &&
- <criterion 1, as verified>
- <criterion 2, as verified>
EOF
if ! printf '%s\n' "$bar" | grep -q '[^[:space:]]'; then
  echo 'acceptance bar empty'
  false
fi &&
python3 ~/.gemini/config/plugins/cairn/tools/task_list.py remove <MILESTONE_DIR> "<Task Title>" &&
out="$(python3 ~/.gemini/config/plugins/cairn/tools/commit.py --subject "Task-completion: <Task Title>" --body "$bar" -- <recorded path 1> <recorded path 2> <MILESTONE_DIR>/TASKS_TODO.md)" &&
if [ -z "$out" ]; then
  echo 'completion commit landed'
fi
```

The call opens by capturing the acceptance bar, in the form the procedure's step 5 states,
from the quoted heredoc into `bar`: the heredoc feeds the `{ … }` group rather than sitting
inside the `$( )`, the form every shell parses alike whatever apostrophes or parentheses the
bar holds, and the delimiter is quoted so nothing inside is expanded (pick a delimiter line
the bar does not contain). The test that follows refuses a bar holding no non-blank line: it
prints `acceptance bar empty` and ends the call before anything is removed or committed. The
removal command is exactly the one the procedure's step 5 shows. After its `&&` the call runs
the one command of the shared commit procedure at `~/.gemini/config/plugins/cairn/shared/commit-procedure.md`,
the plugin's commit tool, with `Task-completion: <Task Title>`, the full `##` heading the
procedure located, as its subject, the bar as its body, and this skill's own change set as
its paths: the exact paths the completion procedure recorded as it created or edited files
while carrying out the task, plus the milestone's task list `<MILESTONE_DIR>/TASKS_TODO.md`
(the task left it), every path written out on the command line after `--` as its own argument
and none held in a shell variable. The tool runs the dirty-own-path guard over those paths,
stages exactly them (never `git add -A`), and commits them with them as the commit's
pathspec, so nothing else the index holds — a change another run has staged included — rides
in the completion's commit, and it repeats a git write another process's lock refused before
giving up. Its stdout is captured in `out`: empty when the commit landed, its fixed no-op line
when none of the paths changed, so `completion commit landed` is printed only when `out` is
empty and a no-op commits and prints nothing. `bar` and `out` are each one quoted value set
and used within this one call, never a tool command or a path list.

What the call prints is the whole outcome: `completion commit landed` when the commit landed;
nothing when the commit tool found none of the paths changed; otherwise `acceptance bar
empty` (nothing removed or committed — write the bar's bullets into the heredoc and run the
call again), the removal's one `Error:` line (`TASKS_TODO.md` unchanged, nothing staged or
committed — diagnose it, fix it, and run the call again), or, once the removal has landed, the
commit tool's one `Error:` line, naming the git command that failed and carrying git's own
message, with nothing committed.

### 3. Hand back

On the success path — the task was completed, verified, removed from `TASKS_TODO.md`, and
committed with its bar, the call printing `completion commit landed` — print exactly one
fixed terse status line and nothing else:

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
