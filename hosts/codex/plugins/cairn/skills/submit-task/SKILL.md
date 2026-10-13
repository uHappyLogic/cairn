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
/submit-task <issue description>
```

`<issue description>` is a free-form description of a problem or gap discovered during
development, specific enough that the affected system, desired behavior, and how to verify
it are clear.

## Workflow

### 0. Find the current milestone

Follow `${PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Read context for triage

Read in parallel:
- `<MILESTONE_DIR>/requirements.md` — to confirm the issue fits the milestone's scope.
- `<MILESTONE_DIR>/TASKS_TODO.md` — existing pending tasks, for duplicate-detection and positioning.
- `<MILESTONE_DIR>/TASKS_DONE.md` — completed work, to catch issues already addressed.

### 2. Triage

- **Duplicate?** If an existing pending task or a completed task already covers this issue, stop and tell the user which task covers it. Do not add a duplicate.
- **In scope?** If the issue clearly belongs to a different milestone or is really an open design decision, say so and point to the better tool (`/discuss-open-question`) instead of queuing it.

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
if [ -n "$(git status --porcelain -- <MILESTONE_DIR>/TASKS_TODO.md)" ]; then
  git add <MILESTONE_DIR>/TASKS_TODO.md && git commit -q -m "Task-submission: <New Task Title>" && echo 'submission commit landed'
fi
```

Every title in the call (the new title in both places, and any anchor) is written inside
double quotes, with any `"`, `$`, `` ` ``, or `\` it holds escaped by a backslash. After the
`&&` the call carries out the three steps of the shared commit procedure at
`${PLUGIN_ROOT}/shared/commit-procedure.md` itself — its dirty-own-path guard, the
path-scoped `git add`, and the subject-only commit under `Task-submission: <New Task Title>`
— over this skill's own change set, `<MILESTONE_DIR>/TASKS_TODO.md`, written out on the
command line in both places and never held in a shell variable. Git's success output is
silenced.

What the call prints is the whole outcome: `submission commit landed` when the commit landed;
nothing when the guard found the file unchanged; otherwise the tool's one `Error:` line, with
`TASKS_TODO.md` unchanged and nothing committed, or git's message for a commit it refused.

On the tool's `Error:` line — an anchor naming no section, or a title `TASKS_TODO.md` already
holds — insert nothing, commit nothing, and stop: never re-run the call with another position
or insert the task any other way. Report the failure quoting the `Error:` line verbatim, so
the user can re-run with a correct anchor or a distinct title.

### 6. Confirm

On the success path — the task was authored, inserted, and committed, the call printing
`submission commit landed` — print exactly one fixed terse status line and nothing else:

`Task submitted.`

Carry no task title, insert position, or commit subject, and print no next-step or follow-up
pointer.

If step 5's dirty-own-path guard found `TASKS_TODO.md` unchanged — nothing was committed —
print instead a distinct one-line no-op message stating that nothing was submitted and
briefly why (e.g. `No task submitted — nothing was authored.`), not the terse success line.

If you could not author a concrete task — typically because the issue was too vague — say so
and suggest `/discuss-new-task` to sharpen it first.
