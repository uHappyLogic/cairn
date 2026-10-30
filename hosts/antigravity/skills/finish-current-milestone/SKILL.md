---
name: finish-current-milestone
description: Mark the current milestone as done, recording its accomplishments in milestones/README.md, clearing the current-milestone pointer, and updating AGENTS.md for lasting changes.
---

# finish-current-milestone

Wraps up the current milestone — verifies that no open question stands and all tasks are done, records accomplishments in `milestones/README.md`, clears the current-milestone pointer to "none" in `milestones/README.md` when it names the finished milestone, and updates `AGENTS.md` only if the milestone introduced lasting changes to the project's environment context. It creates or modifies no files in `<MILESTONE_DIR>/`, and it never invokes `/capture-milestone-principle-updates`. Run this when every open question is answered and all tasks are complete. After this, run `/define-milestone-goal` to define the next milestone, then `/goto-next-milestone` to activate it.

## Usage

```
/finish-current-milestone [--milestone <milestone_id>]
```

With no argument the skill finishes the current milestone. The optional leading `--milestone <milestone_id>` names another milestone by its exact directory name under `milestones/`, e.g. `milestone_12_user-guide`, in place of the current-milestone pointer.

## Workflow

### 1. Find the current milestone

Follow `~/.gemini/config/plugins/cairn/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`, from a leading `--milestone <milestone_id>` override when one is given and from the `Current milestone:` line in `milestones/README.md` otherwise. A matching override is honoured whatever the pointer reads, `none` included. If no override was given and the pointer is `none`, that procedure's stop ends the run, its fixed line opening the report.

Read `<MILESTONE_DIR>/requirements.md` and extract the milestone title from its top-level `# Milestone N: <Title>` heading (e.g. `# Milestone 1: Public Release Preparation` → title "Milestone 1 — Public Release Preparation"). The milestone number N comes from the path slug — strip any leading zeros when parsing it as an integer (e.g. `milestone_01_foo` → N is `1`).

### 2. Read milestone content

In parallel, as two independent tool calls:
- Read `<MILESTONE_DIR>/requirements.md` — to extract the milestone **Goal** and key decisions.
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

Run /answer-open-question for each one, then re-run /finish-current-milestone.
```

If the call fails, stop and report it: the fixed line `Cannot finish the milestone: the open-question check failed.` first, then its one `Error: <reason>` line from stderr verbatim below it. This `list` call is the whole check — never read `open_questions.xml` to make it yourself.

Then check that `<MILESTONE_DIR>/TASKS_TODO.md` contains no `##` sections. If tasks remain, stop: print the fixed line `Cannot finish the milestone: tasks remain to be completed.` first, then below it the advice to complete them first (or move them to the next milestone).

### 4. Compose the completion summary

Write a short summary (3–8 bullet points) of what was accomplished. Draw from:
- The Goal section of `requirements.md`
- The completed tasks step 2's `tasks` call listed, each with its verified bar
- Any significant decisions recorded in `requirements.md`

Keep each bullet to one sentence, factual and grounded in the requirements and completed tasks — never an invented accomplishment. Focus on what now exists in the project, not on process.

### 5. Update milestones/README.md — history

In `milestones/README.md`, add the finished milestone to the `## Milestone History` section. Prepend a new entry using this format, never rewriting existing entries:

```markdown
### Milestone N — Title

- <accomplishment bullet>
- <accomplishment bullet>
- ...
```

If the `## Milestone History` section does not exist, create it after the `## Current Milestone` section.

Then add a one-line index entry to the `## Completed Milestones` table — append a new row with the milestone number N (leading zeros stripped), the Title, and the backticked `<MILESTONE_DIR>` path:

```markdown
| N | Title | `milestones/milestone_<NN>_<slug>/` |
```

Append the row in ascending milestone-number order (after any existing rows), altering no existing row. If the `## Completed Milestones` section or its table header does not exist, create it after `## Milestone History`.

### 6. Clear the current milestone pointer when it names the finished milestone

In `milestones/README.md`, read the `Current milestone:` line. Only when its backtick-quoted path names the finished milestone's directory, `<MILESTONE_DIR>` (always the case when no override was given), overwrite that line with the literal:

```
Current milestone: none
```

When the line reads `none`, leave it `none`. When it names a different milestone, leave it pointing there, untouched. Steps 5 and 8 run as written in every case.

Leave the `## Current Milestone` heading and all other content in `milestones/README.md` unchanged, and do not write the pointer into `AGENTS.md`.

### 7. Update AGENTS.md only for lasting environment-context changes

Scan the completed tasks and requirements for changes that affect how future milestones are worked — new tools now available, new working conventions adopted, new documentation locations, or structural changes to how the project is organized. If any such changes exist, update the relevant section of `AGENTS.md`. Do **not** add a milestone history section or accomplishment bullets to `AGENTS.md`.

If nothing in the milestone changes the project's environment context or structure, skip this step entirely.

### 8. Commit the finish

Read and follow the shared commit procedure at `~/.gemini/config/plugins/cairn/shared/commit-procedure.md`, running its one commit-tool command yourself as this step's one git tool call. Supply it these two inputs:

- **PATHS** — this skill's own change set: **always** `milestones/README.md` (it carries the completion summary from steps 4–5 and, on passes where step 6 cleared it, the `Current milestone: none` pointer, in the same edit), and **additionally** `AGENTS.md` **only on passes where step 7 actually edited it**. If step 7 was skipped, `AGENTS.md` is not in the set and the commit covers `milestones/README.md` alone. This conditional inclusion is keyed on whether this skill's step 7 edited the file — decided as the edit is (or is not) made, never by diffing or inspecting content.
- **SUBJECT** — `Milestone-finish: milestone_<NN>_<slug>`.

The commit tool runs the dirty-own-path guard, the path-scoped staging, and the commit.

### 9. Confirm

On the success path, print exactly one fixed terse status line and nothing else:

```
Milestone finished.
```

Do not restate the milestone name, the tasks-completed count, the accomplishment bullets written into `milestones/README.md`, the pointer clear, any `AGENTS.md` sections touched, or the commit. Do not print any next-step or handoff pointer.

If step 8's commit tool printed `Nothing committed — none of the paths changed.` (the pass changed no files, so nothing was committed), do not print the terse success line. Instead print this one fixed no-op line and nothing else:

```
Nothing to finish — no changes to commit.
```
