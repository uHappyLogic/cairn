---
name: finish-milestone
description: Finish a milestone by removing its directory in one commit whose body summarizes its accomplishments, updating AGENTS.md for lasting changes.
---

# finish-milestone

Wraps up the milestone named by `--milestone` — verifies that no open question stands and all tasks are done, composes a summary of what the milestone accomplished, and records it as the body of one `Milestone-finish: <MILESTONE_DIR>` commit that removes `<MILESTONE_DIR>` from the project, together with an update to `AGENTS.md` only if the milestone introduced lasting changes to the project's environment context. A milestone is finished exactly when its directory is gone: its files stand at the finish commit's parent, the plugin's milestones tool's `summary` and `record` queries print the commit's body back as the milestone's summary, and reverting the finish commit makes the milestone live again. It writes nothing to `milestones/README.md`, touches no pointer, and never invokes `/capture-milestone-principle-updates`. Run this when every open question is answered and all tasks are complete.

## Usage

```
/finish-milestone --milestone <path>
```

The required leading `--milestone <path>` names the milestone by its repo-relative path, exactly as the definition tool printed it, trailing slash included, e.g. `milestones/user-guide/`.

## Workflow

### 1. Resolve the milestone

Follow `~/.gemini/config/plugins/cairn/shared/resolve-milestone.md` to resolve `<MILESTONE_DIR>` from the required leading `--milestone <path>`. A call naming no milestone, or one that does not match, ends on that procedure's stop, its fixed line opening the report.

### 2. Read milestone content

In parallel, as two independent tool calls:
- Read `<MILESTONE_DIR>/requirements.md` — to extract the milestone's title, its **Goal**, and its key decisions. The title is the text of the file's top-level `# ` heading with any legacy `Milestone <N>: ` prefix stripped (e.g. `# Milestone 21: Public Release Preparation` and `# Public Release Preparation` both give the title `Public Release Preparation`).
- Run the plugin's milestones tool, to list what was concretely built:

  ```
  python3 ~/.gemini/config/plugins/cairn/tools/milestones.py tasks <MILESTONE_DIR> --with-body
  ```

  It prints, newest first, one tab-separated line per task completed in the milestone (the commit's abbreviated hash, its date, the milestone directory, and the task title), with the task's verified bar indented beneath it, and prints nothing when no task has been completed, which is no failure.

If the call fails, stop and report it, writing and committing nothing: the fixed line `Cannot finish the milestone: the completed-task read failed.` first, then its one `Error: <reason>` line from stderr verbatim below it.

### 3. Verify the milestone is done

First check that no open question stands. Run

```
python3 ~/.gemini/config/plugins/cairn/tools/open_questions.py list <MILESTONE_DIR>
```

It prints the Short Title of every `<open-question>` block still in `<MILESTONE_DIR>/open_questions.xml`, one per line. If it prints nothing, proceed. If it prints anything, stop immediately, writing and committing nothing whatever tasks step 2's `tasks` call listed, and output, with the printed lines as the bullets verbatim:

```
Cannot finish the milestone: the following open questions must be resolved first:
- <Short Title>
- ...

Run /answer-open-question for each one, then re-run /finish-milestone.
```

If the call fails, stop and report it: the fixed line `Cannot finish the milestone: the open-question check failed.` first, then its one `Error: <reason>` line from stderr verbatim below it. This `list` call is the whole check — never read `open_questions.xml` to make it yourself.

Then check that `<MILESTONE_DIR>/TASKS_TODO.md` contains no `##` sections. If tasks remain, stop: print the fixed line `Cannot finish the milestone: tasks remain to be completed.` first, then below it the advice to complete them first (or move them to another milestone).

### 4. Compose the completion summary

Write a short summary (3–8 bullet points) of what was accomplished. Draw from:
- The Goal section of `requirements.md`
- The completed tasks step 2's `tasks` call listed, each with its verified bar
- Any significant decisions recorded in `requirements.md`

Keep each bullet to one sentence, factual and grounded in the requirements and completed tasks — never an invented accomplishment. Focus on what now exists in the project, not on process.

Then compose the finish commit's body from it, in exactly this shape: the title from step 2 on the first line, one blank line, then the bullets, one `- ` line each.

```
<title>

- <accomplishment bullet>
- <accomplishment bullet>
- ...
```

The body is the milestone's record, which the milestones tool prints back, so it holds nothing else: no heading marker, number, date, or path. A trailing trailer block (one paragraph of `Token: value` lines, such as a `Co-Authored-By:` line) is allowed after the bullets, separated from them by one blank line; the milestones tool leaves it out of what it prints.

### 5. Update AGENTS.md only for lasting environment-context changes

Scan the completed tasks and requirements for changes that affect how future milestones are worked — new tools now available, new working conventions adopted, new documentation locations, or structural changes to how the project is organized. If any such changes exist, update the relevant section of `AGENTS.md`. Do **not** add a milestone history section or accomplishment bullets to `AGENTS.md`.

If nothing in the milestone changes the project's environment context or structure, skip this step entirely.

### 6. Commit the finish

Read and follow the shared commit procedure at `~/.gemini/config/plugins/cairn/shared/commit-procedure.md`, running its one commit-tool command yourself as this step's one git tool call. Supply it these four inputs:

- **REMOVALS** — `<MILESTONE_DIR>`, exactly as resolved, trailing slash included: the commit tool removes the milestone's directory and records the removal in the same commit.
- **PATHS** — `AGENTS.md` **only on passes where step 5 actually edited it**, and otherwise none, the commit then recording the removal alone. This conditional inclusion is keyed on whether this skill's step 5 edited the file — decided as the edit is (or is not) made, never by diffing or inspecting content.
- **SUBJECT** — `Milestone-finish: <MILESTONE_DIR>`, the path exactly as resolved, trailing slash included.
- **BODY** — the body step 4 composed.

The commit tool runs the dirty-own-path guard, the removal, the path-scoped staging, and the commit; nothing else is removed, edited, or committed.

### 7. Confirm

On the success path, print exactly one fixed terse status line and nothing else:

```
Milestone finished.
```

Do not restate the milestone name, the tasks-completed count, the accomplishment bullets written into the commit body, the removal, any `AGENTS.md` sections touched, or the commit. Do not print any next-step or handoff pointer.

If step 6's commit tool printed `Nothing committed — none of the paths changed.` (the pass changed no files, so nothing was committed), do not print the terse success line. Instead print this one fixed no-op line and nothing else:

```
Nothing to finish — no changes to commit.
```
