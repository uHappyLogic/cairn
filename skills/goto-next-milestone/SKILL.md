---
name: goto-next-milestone
description: Activate an already-defined milestone — scans milestones/ for a defined-but-not-yet-active directory and updates milestones/README.md to point to it as the current milestone. Requires finish-current-milestone to have been run first (current pointer must be "none").
---

# goto-next-milestone

Activates an already-defined milestone by updating `milestones/README.md` to point to it as the current milestone. The milestone directory must already exist (created by `/define-milestone-goal`). Run this after `/finish-current-milestone` has cleared the current pointer to "none".

## Usage

```
/goto-next-milestone
```

No arguments. The milestone to activate is discovered automatically.

## Workflow

### 1. Check prerequisites

Read `milestones/README.md` and find the line whose prefix is `Current milestone:`. If that line is not `Current milestone: none` (i.e. it still points to an active milestone path), stop and tell the user to run `/finish-current-milestone` first.

### 2. Find the candidate milestone

Read `milestones/README.md` and scan `milestones/` to collect:
- All directories matching `milestone_<N>_<slug>/`
- All milestone dirs already listed in the `## Milestone History` section (these are completed)

The **candidates** are directories that exist in `milestones/` but do not appear in `## Milestone History`.

- **Zero candidates**: stop. Tell the user to run `/define-milestone-goal` first to create a milestone.
- **One candidate**: confirm the path and title with the user, then proceed.
- **Multiple candidates**: list them (number, slug, path) and ask the user which one to activate before proceeding. When deriving the number from the directory slug, strip leading zeros and treat it as an integer (e.g. `milestone_01_foo` → number `1`).

### 3. Update milestones/README.md

In `milestones/README.md`, overwrite the `Current milestone:` line with:

```
Current milestone: `milestones/milestone_<number>_<slug>/`
```

Leave the `## Current Milestone` heading, the `## Milestone History` section, and all other content unchanged.

### 4. Confirm

Report:
- The milestone activated: path and title
- `milestones/README.md` updated to point to it
- Suggest the next step: `/specify-milestone-starting-state` to fill in the implementation context

## Rules

- Do not run if the `Current milestone:` line in `milestones/README.md` is not `none` — always require `/finish-current-milestone` to have been run first.
- Do not create any files or directories — the milestone directory must already exist.
- Update `milestones/README.md` only — do not write the pointer into `CLAUDE.md`.
- Do not commit — leave staging to the user.
