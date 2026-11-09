---
name: submit-task
description: Add a single already-clear issue to the named milestone's TASKS_TODO.md as a brief-level task section.
---

# submit-task

Turns a single, already-clear issue into a brief-level task section in the named
milestone's `TASKS_TODO.md`. This skill is the user-facing entry point
(`/submit-task`) and the handoff target for `/discuss-new-task`.

It owns the triage and positioning that need the **whole task list in view** — checking for
duplicates and deciding where the task belongs — and then it authors and inserts the task
**inline, in this conversation**. If the issue is still vague or might be several tasks,
use `/discuss-new-task` first.

## Invocation

```
/submit-task --milestone <path> <issue description>
```

`<issue description>` is a free-form description of a problem or gap discovered during
development, specific enough that the affected system, desired behavior, and how to verify
it are clear. The required leading `--milestone <path>` names the milestone by its
repo-relative path, exactly as the definition tool printed it, trailing slash included, e.g.
`milestones/user-guide/`.

## Workflow

### 0. Find the milestone

First strip the leading `--milestone <path>` from the invocation text by the rule in `~/.gemini/config/plugins/cairn/shared/resolve-milestone.md`, reading only the rest as the issue description. Follow `~/.gemini/config/plugins/cairn/shared/resolve-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Check the scope gate

Directly after resolving the milestone, and before anything else, follow
`~/.gemini/config/plugins/cairn/shared/check-scope-gate.md` for `<MILESTONE_DIR>`. When the gate is closed,
its report is the whole output: read, refresh, insert, and commit nothing, and print no line
of step 9.

### 2. Refresh a stale starting state

Before reading anything for triage, check whether other milestones' work has landed in the
scope since this milestone's starting state was recorded. Run, from the workspace root, the
plugin's milestones tool:

```
python3 ~/.gemini/config/plugins/cairn/tools/milestones.py since <MILESTONE_DIR> --milestones
```

Its first line, when it prints one, is the anchor, the commit that last recorded this
milestone's starting state; every line beneath it is another milestone's task or finish
commit that landed in the scope after it. Read its print as exactly one of three outcomes:

- **No line at all, or the anchor alone** — there is no anchor to measure from, or nothing
  has landed since it: explore nothing, commit nothing, print nothing about the starting
  state, and go on to step 3 with the `## Relevant starting state` section as it stands,
  empty or filled.
- **Anything beyond the anchor** — the ground moved under the section: refresh it before
  authoring anything, as below.
- **The call failed** — any non-zero exit, whatever its `Error:` line says: stop the whole
  run, reading, inserting, and committing nothing. Report the starting-state procedure's
  fixed line `Starting state stopped — a milestones-tool read failed.` first, then below it
  the call's `Error:` line from stderr, verbatim, and print no line of step 9.

To refresh, read and follow the shared starting-state procedure at
`~/.gemini/config/plugins/cairn/shared/starting-state-procedure.md` in place, with `<MILESTONE_DIR>` as its
input; its pick judgment applies here in full, since this milestone's questions may carry
standing picks. It ends in exactly one of three ways:

- **The anchor alone** — its step 1 found the ground unmoved, so it explored, edited, and
  cleared nothing. Make no commit and go on to step 3.
- **A stop** — it stopped on one of its two fixed lines,
  `Starting state stopped — a milestones-tool read failed.` or
  `Starting state stopped — clearing the undermined picks failed.`, with the detail the
  procedure gives beneath it. That report, as the procedure states it, is this run's whole
  output: insert no task, commit nothing, and print no line of step 9.
- **The change handed back** — it ran through its step 7, with `requirements.md` edited or
  left as it stood, and `open_questions.xml` changed exactly when its step 6 cleared a pick.
  Commit it, as below, then go on to step 3.

Commit the handed-back change as a commit of its own, before any read of step 3 and any
authoring, by reading and following the shared commit procedure at
`~/.gemini/config/plugins/cairn/shared/commit-procedure.md`, running its one commit-tool command yourself as
one git tool call, with these two inputs:

- **PATHS** — `<MILESTONE_DIR>/requirements.md`, and `<MILESTONE_DIR>/open_questions.xml`
  beside it only when the procedure's step 6 cleared a pick, so a refresh and the picks it
  cleared are one commit.
- **SUBJECT** — `Starting-state: <MILESTONE_DIR>`, the milestone path exactly as resolved,
  trailing slash included.

The refresh commit prints no line of its own in this run's report: whether it landed (the
commit tool printed nothing) or found nothing to commit (it printed
`Nothing committed — none of the paths changed.`, the exploration having left the section as
it stood), go on to step 3. If the commit tool prints an `Error:` line instead, stop the whole
run, inserting and committing nothing further: report the fixed line
`Task not submitted — the starting-state refresh could not be committed.` first, then the
`Error:` line quoted verbatim below it, and print no line of step 9.

### 3. Read context for triage

In parallel, as independent tool calls:
- Read `<MILESTONE_DIR>/requirements.md` — to confirm the issue fits the milestone's scope.
- Read `<MILESTONE_DIR>/TASKS_TODO.md` — existing pending tasks, for duplicate-detection and positioning.
- Run the plugin's milestones tool — completed work, to catch issues already addressed:

  ```
  python3 ~/.gemini/config/plugins/cairn/tools/milestones.py tasks <MILESTONE_DIR> --with-body
  ```

  It prints, newest first, one tab-separated line per task completed in the milestone (the
  commit's abbreviated hash, its date, the milestone directory, and the task title), with the
  task's verified bar indented beneath it, and prints nothing when no task has been completed,
  which is no failure.

If the call fails, stop, writing and committing nothing: print the fixed line
`Task not submitted — the completed-task read failed.` first, then below it its one
`Error: <reason>` line from stderr verbatim.

### 4. Triage

- **Duplicate?** If an existing pending task or a completed task the `tasks` call listed already covers this issue, stop: print the fixed line `Task not submitted — an existing task already covers it.` first, then below it which task covers it. Do not add a duplicate.
- **In scope?** If the issue clearly belongs to a different milestone or is really an open design decision, stop instead of queuing it: print the fixed line `Task not submitted — the issue is not a task for this milestone.` first, then below it why, pointing to the better tool (`/discuss-open-question`).

### 5. Decide the position

You hold the whole task list, so you decide where the task goes:
- If the task is a prerequisite for an existing task, position it **before** that task: `before: <Task Title>`.
- If it depends on an existing task, position it **after** that task: `after: <Task Title>`.
- Otherwise, `append`.

### 6. Author the task section inline

Read the shared task format at `~/.gemini/config/plugins/cairn/shared/task-format.md` and write the task section
**yourself, in this conversation**, following its template and authoring guidelines exactly.
That file owns the shape of a task section.

The issue as the user described it, sharpened against the milestone's scope, *is* the task
body; writing it down is a transcription into that format, not a second authoring pass that
adds detail.

(You already read `requirements.md` and `TASKS_TODO.md` in step 3, so reuse them rather
than re-reading.)

### 7. Check the scope gate again

Directly ahead of the insert, follow `~/.gemini/config/plugins/cairn/shared/check-scope-gate.md` for
`<MILESTONE_DIR>` a second time, since another milestone may have started in the scope while
this run read, triaged, and authored. When the gate is closed, its report is the whole output:
insert and commit no task, and print no line of step 9. A refresh commit step 2 already landed
stays committed. The call in step 8 checks no gate of its own.

### 8. Insert and commit the section in one shell call

Split the section you authored in step 6 along `task-format.md`'s template: the text of its
`##` heading is the title, and the description between the heading and the `---` is the
body. The tool writes the `##` line and the `---` itself, so neither goes into the call. Map
the position step 5 decided onto exactly one flag:

- **`append`** — `--end`.
- **`before: <Task Title>`** — `--before "<Task Title>"`.
- **`after: <Task Title>`** — `--after "<Task Title>"`.

Then run this one fixed shell call, written out in full exactly as shown, with only
`<MILESTONE_DIR>`, `<New Task Title>`, `<position flag>`, and the body replaced:

```
python3 ~/.gemini/config/plugins/cairn/tools/task_list.py insert <MILESTONE_DIR> "<New Task Title>" <position flag> <<'EOF' &&
<the 1–3 sentence description>
EOF
out="$(python3 ~/.gemini/config/plugins/cairn/tools/commit.py --subject "Task-submission: <New Task Title>" -- <MILESTONE_DIR>/TASKS_TODO.md)" &&
if [ -z "$out" ]; then
  echo 'submission commit landed'
fi
```

Every title in the call (the new title in both places, and any anchor) is written inside
double quotes, with any `"`, `$`, `` ` ``, or `\` it holds escaped by a backslash. After the
`&&` the call runs the one command of the shared commit procedure at
`~/.gemini/config/plugins/cairn/shared/commit-procedure.md`, the plugin's commit tool, with
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

### 9. Confirm

On the success path — the task was authored, inserted, and committed, the call printing
`submission commit landed` — print exactly one fixed terse status line and nothing else:

`Task submitted.`

Carry no task title, insert position, or commit subject, and print no next-step or follow-up
pointer.

If step 8's commit tool found `TASKS_TODO.md` unchanged — nothing was committed — print
instead this one fixed no-op line, not the terse success line:

```
Task not submitted — the task file was unchanged.
```

If you could not author a concrete task — typically because the issue was too vague — stop:
print the fixed line `Task not submitted — the issue is too vague to author.` first, then
below it a suggestion to run `/discuss-new-task` to sharpen it first.
