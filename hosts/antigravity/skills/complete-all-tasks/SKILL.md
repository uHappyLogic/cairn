---
name: complete-all-tasks
description: Complete every task in the current milestone's TASKS_TODO.md one by one, moving each to TASKS_DONE.md.
---

# complete-all-tasks

Pure orchestrator. Reads the current milestone's task list and spawns one isolated subagent per task, each with a clean context and exactly one task to complete, then commits each finished task from the path file its subagent wrote. Never complete a task directly here, even as a fallback when a subagent fails.

## Invocation

```
/complete-all-tasks [--milestone <milestone_id>]
```

With no argument the skill completes the current milestone's tasks. The optional leading `--milestone <milestone_id>` names another milestone by its exact directory name under `milestones/`, e.g. `milestone_12_user-guide`, in place of the current-milestone pointer.

## Workflow

### 0. Find the current milestone

Follow `~/.gemini/config/plugins/cairn/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Read the task list

Read `<MILESTONE_DIR>/TASKS_TODO.md` and confirm it has at least one `##` section. If the file is empty or has no `##` sections, print this one fixed no-op line and stop:

```
No tasks to complete — the task list is empty.
```

### 2. For each task (top to bottom)

Before the first dispatch, create the run's scratch directory: run

```
mktemp -d
```

once and hold the path it prints as `<scratch dir>`: a fresh, uniquely named directory under the system temp location, outside the repository, that belongs to this run alone, so no other run's path file can reach it. Every agent writes its path file into it, and every later command names it by that path, written out in full, never held in a shell variable. You delete nothing in it at any point in the run — no path file, no `processed` subdirectory, not the directory itself; the system's own temp handling reclaims it.

Then repeat the following loop until no tasks remain:

#### 2a. Identify the next task

Re-read `<MILESTONE_DIR>/TASKS_TODO.md` to get the current top task — the first `##` heading in the file. Do not cache the task list across iterations, since each completed task is removed.

#### 2b. Spawn a subagent to complete the task

Use the `invoke_subagent` tool with one entry in its `Subagents` array whose `TypeName` is the name this plugin registers the `complete-task` agent under, `complete-task`, whose `Role` is `Task completer`, and whose `Prompt` carries the task name, the milestone directory, and the scratch directory and nothing else, substituting `<TASK_NAME>` with the exact `##` heading text (without the `##` prefix), `<MILESTONE_DIR>` with the directory resolved in step 0, and `<scratch dir>` with the directory created at the start of step 2. The call returns at once, and the agent's final message reaches you as a message from it once it ends; that message is its return:

```
Complete the task named: "<TASK_NAME>"

Milestone directory: <MILESTONE_DIR>

Scratch directory: <scratch dir>
```

Every dispatch carries the `Milestone directory:` line, holding the `<MILESTONE_DIR>` step 0 resolved, whether from an override or from the pointer, so each agent works in the milestone this run commits for, and the `Scratch directory:` line, holding the one `<scratch dir>` created at the start of this step, the same directory on every dispatch, so each agent writes its path file where 2c reads it.

Wait for the agent to return.

- If the agent reports FAILED, stop the loop and end the run: print the fixed line `Task run stopped — a task failed.` first, then below it the task name and the failure reason. Do not proceed to 2c.
- If the agent returns without an explicit DONE or FAILED status (e.g. it returned early, produced no output, or gave an ambiguous result), treat this as FAILED: stop the loop, print the fixed line `Task run stopped — a task agent returned no status.` first, then below it the task name and what was returned, and do not proceed to 2c. **Never attempt to complete the task yourself as a fallback.**
- On `DONE`, the agent has written its task's change set — the paths it created or edited, plus the two milestone task-list files — to the path file `<scratch dir>/paths.txt`, one path per line, and has staged and committed nothing. You commit the task from that file in 2c; you name no path and stage nothing yourself, and the agent's message carries nothing to collect.

#### 2c. Commit the task from its path file

After the subagent returns `DONE`, commit its task from the path file in this one fixed shell call, written out in full exactly as shown, with only `<scratch dir>` and `<TASK_NAME>` replaced, `<TASK_NAME>` being the exact `##` heading text step 2b already holds:

```
if [ ! -e "<scratch dir>/paths.txt" ]; then
  echo 'path file absent'
else
  if ! grep -q . "<scratch dir>/paths.txt"; then
    echo 'path file empty'
  elif out="$(python3 ~/.gemini/config/plugins/cairn/tools/commit.py --subject "Task-completion: <TASK_NAME>" --path-file "<scratch dir>/paths.txt")" && [ -z "$out" ]; then
    echo 'completion commit landed'
  fi
  mkdir -p "<scratch dir>/processed" &&
    mv "<scratch dir>/paths.txt" "$(mktemp "<scratch dir>/processed/paths.XXXXXX")"
fi
```

The call first tests the path file: absent (no file under the fixed name) or empty (no line of it naming a path) commits nothing. Otherwise it runs the one command of the shared commit procedure at `~/.gemini/config/plugins/cairn/shared/commit-procedure.md`, the plugin's commit tool, with `Task-completion: <TASK_NAME>` as its subject, no body, and the path file as its only pathspec, given as `--path-file`: the tool reads the file line-exact, one path per line, each line taken whole, runs the dirty-own-path guard over those paths, stages exactly them (never `git add -A`), and commits them with them as the commit's pathspec, so nothing else the index holds — a change another run has staged included — rides in the task's commit, and it repeats a git write another process's lock refused before giving up. The call names no path itself and holds no path list: the file is the task's whole change set. Run no git command of your own beside it — no status check, no `git add`, no `git commit`, and no `--allow-empty`. The tool's stdout is captured in `out`: empty when the commit landed, its fixed no-op line when none of the paths changed, so `completion commit landed` is printed only when `out` is empty. Once the file has been read, whatever the commit's outcome, the call moves it into the scratch directory's `processed` subdirectory under a name `mktemp` makes unique there, so the fixed name is absent when the next agent starts and no path file is ever read twice; it deletes nothing. `out` is one quoted value set and used within this one call, never a tool command or a path list.

What the call prints is the whole outcome:

- **`completion commit landed`** — the task's `Task-completion: <TASK_NAME>` commit landed. Go on to 2d.
- **Nothing** — the commit tool found none of the paths changed, so nothing was committed and no empty commit made: skip the task silently and go on to 2d.
- **Anything else** — `path file absent`, `path file empty`, the commit tool's one `Error:` line (naming the git command that failed and carrying git's own message, nothing committed), or a failed move's own message. Stop the loop and end the run: print the fixed line `Task run stopped — a completed task could not be committed.` first, then below it the task name and what the call printed, verbatim, which for an absent or empty path file is the line saying which. Commit and stage nothing yourself and touch nothing in the tree: the agent's move and edits stay uncommitted, exactly as it left them, for a later run to resume.

Commit once per task.

#### 2d. Continue

Go back to 2a and process the next task.

### 3. Report completion

On the success path, when `<MILESTONE_DIR>/TASKS_TODO.md` contains no more `##` sections, print exactly one fixed terse status line for the whole run — `All tasks completed.` — and nothing more: no list of the tasks that were completed and no next-step pointer. This is the line whatever the per-task commits found: a task whose commit tool found none of its paths changed was skipped silently in 2c, and a run whose every task returned `DONE` and was committed or skipped has no other line.
