---
name: submit-task
description: Add a single already-clear issue to the current milestone's TASKS_TODO.md as a brief-level task section.
---

# submit-task

Turns a single, already-clear issue into a brief-level task section in the current
milestone's `TASKS_TODO.md`. This skill is the user-facing entry point
(`/submit-task`) and the handoff target for `/discuss-new-task`.

It owns the triage and positioning that need the **whole task list in view** — checking for
duplicates and deciding where the task belongs — and then it authors and inserts the task
**inline, in this conversation**. If the issue is still vague or might be several tasks,
use `/discuss-new-task` first.

## Invocation

```
/submit-task [--milestone <milestone_id>] <issue description>
```

`<issue description>` is a free-form description of a problem or gap discovered during
development, specific enough that the affected system, desired behavior, and how to verify
it are clear. The optional leading `--milestone <milestone_id>` names the milestone by its
exact directory name under `milestones/`, e.g. `milestone_12_user-guide`, in place of the
current-milestone pointer.

## Workflow

### 0. Find the current milestone

First strip a leading `--milestone <milestone_id>` from the invocation text by the rule in `${PLUGIN_ROOT}/shared/get-current-milestone.md`, reading only the rest as the issue description. Follow `${PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Read context for triage

Read in parallel:
- `<MILESTONE_DIR>/requirements.md` — to confirm the issue fits the milestone's scope.
- `<MILESTONE_DIR>/TASKS_TODO.md` — existing pending tasks, for duplicate-detection and positioning.
- `<MILESTONE_DIR>/TASKS_DONE.md` — completed work, to catch issues already addressed.

### 2. Triage

- **Duplicate?** If an existing pending task or a completed task already covers this issue, stop: print the fixed line `Task not submitted — an existing task already covers it.` first, then below it which task covers it. Do not add a duplicate.
- **In scope?** If the issue clearly belongs to a different milestone or is really an open design decision, stop instead of queuing it: print the fixed line `Task not submitted — the issue is not a task for this milestone.` first, then below it why, pointing to the better tool (`/discuss-open-question`).

### 3. Decide the position

You hold the whole task list, so you decide where the task goes:
- If the task is a prerequisite for an existing task, position it **before** that task: `before: <Task Title>`.
- If it depends on an existing task, position it **after** that task: `after: <Task Title>`.
- Otherwise, `append`.

### 4. Author the task section inline

Read the shared task format at `${PLUGIN_ROOT}/shared/task-format.md` and write the task section
**yourself, in this conversation**, following its template and authoring guidelines exactly.
That file owns the shape of a task section.

The issue as the user described it, sharpened against the milestone's scope, *is* the task
body; writing it down is a transcription into that format, not a second authoring pass that
adds detail.

(You already read `requirements.md` and `TASKS_TODO.md` in step 1, so reuse them rather
than re-reading.)

### 5. Insert and commit the section in one shell call

Split the section you authored in step 4 along `task-format.md`'s template: the text of its
`##` heading is the title, and the description between the heading and the `---` is the
body. The tool writes the `##` line and the `---` itself, so neither goes into the call. Map
the position step 3 decided onto exactly one flag:

- **`append`** — `--end`.
- **`before: <Task Title>`** — `--before "<Task Title>"`.
- **`after: <Task Title>`** — `--after "<Task Title>"`.

Then run this one fixed shell call, written out in full exactly as shown, with only
`<MILESTONE_DIR>`, `<New Task Title>`, `<position flag>`, and the body replaced:

```
python3 ${PLUGIN_ROOT}/tools/task_list.py insert <MILESTONE_DIR> "<New Task Title>" <position flag> <<'EOF' &&
<the 1–3 sentence description>
EOF
out="$(python3 ${PLUGIN_ROOT}/tools/commit.py --subject "Task-submission: <New Task Title>" -- <MILESTONE_DIR>/TASKS_TODO.md)" &&
if [ -z "$out" ]; then
  echo 'submission commit landed'
fi
```

Every title in the call (the new title in both places, and any anchor) is written inside
double quotes, with any `"`, `$`, `` ` ``, or `\` it holds escaped by a backslash. After the
`&&` the call runs the one command of the shared commit procedure at
`${PLUGIN_ROOT}/shared/commit-procedure.md`, the plugin's commit tool, with
`Task-submission: <New Task Title>` as its subject, no body, and this skill's own change set,
`<MILESTONE_DIR>/TASKS_TODO.md`, as its one path, written out on the command line and never
held in a shell variable. The tool runs the dirty-own-path guard over the file, stages exactly
it, and commits it with it as the commit's pathspec, so nothing else the index holds — a change
another run has staged included — rides in the submission's commit, and it repeats a git write
another process's lock refused before giving up. Its stdout is captured in `out`: empty when
the commit landed, its fixed no-op line when the file did not change, so
`submission commit landed` is printed only when `out` is empty and a no-op commits and prints
nothing. `out` is one quoted value set and used within this one call, never a tool command or
a path list.

What the call prints is the whole outcome: `submission commit landed` when the commit landed;
nothing when the commit tool found the file unchanged; otherwise one `Error:` line — the
task-list tool's, with `TASKS_TODO.md` unchanged and nothing committed, or, once the insert
has landed, the commit tool's, naming the git command that failed and carrying git's own
message, with nothing committed.

On the task-list tool's `Error:` line — an anchor naming no section, or a title
`TASKS_TODO.md` already holds — insert nothing, commit nothing, and stop: never re-run the
call with another position or insert the task any other way. Report the failure with the
fixed line `Task not submitted — the task-list tool refused the insert.` first, then below it
the `Error:` line quoted verbatim, so the user can re-run with a correct anchor or a distinct
title.

### 6. Confirm

On the success path — the task was authored, inserted, and committed, the call printing
`submission commit landed` — print exactly one fixed terse status line and nothing else:

`Task submitted.`

Carry no task title, insert position, or commit subject, and print no next-step or follow-up
pointer.

If step 5's commit tool found `TASKS_TODO.md` unchanged — nothing was committed — print
instead this one fixed no-op line, not the terse success line:

```
Task not submitted — the task file was unchanged.
```

If you could not author a concrete task — typically because the issue was too vague — stop:
print the fixed line `Task not submitted — the issue is too vague to author.` first, then
below it a suggestion to run `/discuss-new-task` to sharpen it first.
