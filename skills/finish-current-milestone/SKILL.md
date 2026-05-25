---
name: finish-current-milestone
description: Mark the current milestone as done — records accomplishments in milestones/README.md and updates CLAUDE.md only for lasting tech-stack or structural changes.
---

# finish-current-milestone

Wraps up the current milestone — verifies all tasks are done, records accomplishments in `milestones/README.md`, and updates `CLAUDE.md` only if the milestone introduced lasting technical changes. Run this when all tasks are complete, before running `/goto-next-milestone`.

## Usage

```
/finish-current-milestone
```

No arguments.

## Workflow

### 1. Find the current milestone

Read `CLAUDE.md` and extract:
- The path from the `## Current Milestone` section (shown in backticks, e.g. `milestones/milestone_11_tbd/`). Use as `<MILESTONE_DIR>`.
- The milestone title shown in the same section (e.g. "Milestone 11 — TBD").

### 2. Read milestone content

Read in parallel:
- `<MILESTONE_DIR>/requirements.md` — to extract the milestone **Goal** and key implementation decisions.
- `<MILESTONE_DIR>/TASKS_DONE.md` — to list what was concretely built.

### 3. Verify the milestone is done

Check that `<MILESTONE_DIR>/TASKS_TODO.md` contains no `##` sections. If tasks remain, stop and tell the user to complete them first (or move them to the next milestone).

### 4. Compose the completion summary

Write a short summary (3–8 bullet points) of what was accomplished. Draw from:
- The Goal section of `requirements.md`
- The completed tasks in `TASKS_DONE.md`
- Any significant implementation decisions recorded in `requirements.md`

Keep each bullet to one sentence. Focus on what now exists in the game/codebase, not on process.

### 5. Update milestones/README.md

In `milestones/README.md`, add the finished milestone to the `## Milestone History` section. Prepend a new entry using this format:

```markdown
### Milestone N — Title

- <accomplishment bullet>
- <accomplishment bullet>
- ...
```

If the `## Milestone History` section does not exist, create it after the `## Current Milestone` section. Do **not** change the `## Current Milestone` section — that is done by `/goto-next-milestone`.

### 6. Update CLAUDE.md only for lasting technical changes

Scan the completed tasks and requirements for changes that affect how future milestones are developed — new packages added to the tech stack, new MCP servers integrated, new documentation locations, or structural changes to the repository layout. If any such changes exist, update the relevant section of `CLAUDE.md` (e.g. `## Tech Stack`, `## Repository Layout`). Do **not** add a milestone history section or accomplishment bullets to `CLAUDE.md`.

If nothing in the milestone changes the tech stack, tooling, or project structure, skip this step entirely.

### 7. Confirm

Report: the milestone name, the number of tasks completed, and the bullet list written into `milestones/README.md`. Note any `CLAUDE.md` sections updated (or confirm none were needed).

## Rules

- Do not mark the milestone done if `TASKS_TODO.md` still has tasks with `##` headings.
- Do not rewrite existing `## Milestone History` entries — only prepend the new one.
- Keep the summary factual and grounded in the requirements and tasks — do not invent accomplishments.
- Do not create or modify any files in `<MILESTONE_DIR>/`.
- Do not touch the `## Current Milestone` section in either `CLAUDE.md` or `milestones/README.md` — `/goto-next-milestone` owns that.
