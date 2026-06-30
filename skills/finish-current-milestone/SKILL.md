---
name: finish-current-milestone
description: Mark the current milestone as done — records accomplishments in milestones/README.md, clears the current-milestone pointer to "none" in milestones/README.md, and updates CLAUDE.md only for lasting tech-stack or structural changes.
---

# finish-current-milestone

Wraps up the current milestone — verifies all tasks are done, records accomplishments in `milestones/README.md`, clears the current-milestone pointer to "none" in `milestones/README.md`, and updates `CLAUDE.md` only if the milestone introduced lasting technical changes. Run this when all tasks are complete. After this, run `/define-milestone-goal` to define the next milestone, then `/goto-next-milestone` to activate it.

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

Keep each bullet to one sentence. Focus on what now exists in the game/codebase, not on process.

### 5. Update milestones/README.md — history

In `milestones/README.md`, add the finished milestone to the `## Milestone History` section. Prepend a new entry using this format:

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

Append the row in ascending milestone-number order (after any existing rows). If the `## Completed Milestones` section or its table header does not exist, create it after `## Milestone History`.

### 6. Clear the current milestone pointer

In `milestones/README.md`, overwrite the `Current milestone:` line with the literal:

```
Current milestone: none
```

Leave the `## Current Milestone` heading and all other content in `milestones/README.md` unchanged.

### 7. Update CLAUDE.md only for lasting technical changes

Scan the completed tasks and requirements for changes that affect how future milestones are developed — new packages added to the tech stack, new MCP servers integrated, new documentation locations, or structural changes to the repository layout. If any such changes exist, update the relevant section of `CLAUDE.md` (e.g. `## Tech Stack`, `## Repository Layout`). Do **not** add a milestone history section or accomplishment bullets to `CLAUDE.md`.

If nothing in the milestone changes the tech stack, tooling, or project structure, skip this step entirely.

### 8. Confirm

Report: the milestone name, the number of tasks completed, the bullet list written into `milestones/README.md`, and that the current-milestone pointer has been cleared to "none". Note any `CLAUDE.md` sections updated (or confirm none were needed).

Suggest the next steps, in this order:

1. Optional: run `/capture-milestone-principle-updates` to distill reusable answering principles from this milestone's recorded decisions into the principle store. (Recommended now that the milestone has just closed and its row was appended to the `## Completed Milestones` table — but never auto-run.)
2. `/define-milestone-goal` to start planning the next milestone.

## Rules

- Do not mark the milestone done if `TASKS_TODO.md` still has tasks with `##` headings.
- Do not rewrite existing `## Milestone History` entries — only prepend the new one. Likewise only append the new row to the `## Completed Milestones` table; do not alter existing rows.
- Keep the summary factual and grounded in the requirements and tasks — do not invent accomplishments.
- Do not create or modify any files in `<MILESTONE_DIR>/`.
- Clear the current-milestone pointer only in `milestones/README.md` — overwrite the `Current milestone:` line to `Current milestone: none`. Do not modify `CLAUDE.md`'s pointer section.
- `/finish-current-milestone` only *suggests* `/capture-milestone-principle-updates` — it never invokes it and never commits. Step 8 adds the recommendation as suggestion text only.
