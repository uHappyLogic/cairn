---
name: finish-current-milestone
description: Mark the current milestone as done, recording its accomplishments in milestones/README.md, clearing the current-milestone pointer, and updating CLAUDE.md for lasting changes.
---

# finish-current-milestone

Wraps up the current milestone — verifies all tasks are done, records accomplishments in `milestones/README.md`, clears the current-milestone pointer to "none" in `milestones/README.md`, and updates `CLAUDE.md` only if the milestone introduced lasting changes to the project's environment context. It creates or modifies no files in `<MILESTONE_DIR>/`, and it never invokes `/capture-milestone-principle-updates`. Run this when all tasks are complete. After this, run `/define-milestone-goal` to define the next milestone, then `/goto-next-milestone` to activate it.

## Usage

```
/finish-current-milestone
```

No arguments.

## Workflow

### 1. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>` from the `Current milestone:` line in `milestones/README.md`. If the pointer is `none`, stop and tell the user there is no active milestone to finish.

Read `<MILESTONE_DIR>/requirements.md` and extract the milestone title from its top-level `# Milestone N: <Title>` heading (e.g. `# Milestone 1: Public Release Preparation` → title "Milestone 1 — Public Release Preparation"). The milestone number N comes from the path slug — strip any leading zeros when parsing it as an integer (e.g. `milestone_01_foo` → N is `1`).

### 2. Read milestone content

Read in parallel:
- `<MILESTONE_DIR>/requirements.md` — to extract the milestone **Goal** and key decisions.
- `<MILESTONE_DIR>/TASKS_DONE.md` — to list what was concretely built.

### 3. Verify the milestone is done

Check that `<MILESTONE_DIR>/TASKS_TODO.md` contains no `##` sections. If tasks remain, stop and tell the user to complete them first (or move them to the next milestone).

### 4. Compose the completion summary

Write a short summary (3–8 bullet points) of what was accomplished. Draw from:
- The Goal section of `requirements.md`
- The completed tasks in `TASKS_DONE.md`
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

### 6. Clear the current milestone pointer

In `milestones/README.md`, overwrite the `Current milestone:` line with the literal:

```
Current milestone: none
```

Leave the `## Current Milestone` heading and all other content in `milestones/README.md` unchanged, and do not write the pointer into `CLAUDE.md`.

### 7. Update CLAUDE.md only for lasting environment-context changes

Scan the completed tasks and requirements for changes that affect how future milestones are worked — new tools now available, new working conventions adopted, new documentation locations, or structural changes to how the project is organized. If any such changes exist, update the relevant section of `CLAUDE.md`. Do **not** add a milestone history section or accomplishment bullets to `CLAUDE.md`.

If nothing in the milestone changes the project's environment context or structure, skip this step entirely.

### 8. Commit the finish

Read and follow the shared commit procedure at `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path), carrying out its steps yourself. Supply it these two inputs:

- **PATHS** — this skill's own change set: **always** `milestones/README.md` (it carries both the completion summary from steps 4–5 and the `Current milestone: none` pointer cleared in step 6, in the same edit), and **additionally** `CLAUDE.md` **only on passes where step 7 actually edited it**. If step 7 was skipped, `CLAUDE.md` is not in the set and the commit covers `milestones/README.md` alone. This conditional inclusion is keyed on whether this skill's step 7 edited the file — decided as the edit is (or is not) made, never by diffing or inspecting content.
- **SUBJECT** — `Milestone-finish: milestone_<NN>_<slug>`.

The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit.

### 9. Confirm

On the success path, print exactly one fixed terse status line and nothing else:

```
Milestone finished.
```

Do not restate the milestone name, the tasks-completed count, the accomplishment bullets written into `milestones/README.md`, the pointer clear, any `CLAUDE.md` sections touched, or the commit. Do not print any next-step or handoff pointer.

If step 8's dirty-own-path no-op guard fired (the pass changed no files, so nothing was committed), do not print the terse success line. Instead print a distinct one-line message stating that nothing changed and briefly why, for example:

```
Nothing to finish — no changes to commit.
```
