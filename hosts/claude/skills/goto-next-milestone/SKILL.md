---
name: goto-next-milestone
description: Activate an already-defined milestone by pointing milestones/README.md at it as the current milestone.
---

# goto-next-milestone

Activates an already-defined milestone by updating `milestones/README.md` to point to it as the current milestone. The milestone directory must already exist (created by `/define-milestone-goal`); this skill creates no files or directories. Run this after `/finish-current-milestone` has cleared the current pointer to "none".

## Usage

```
/goto-next-milestone
```

No arguments. The milestone to activate is discovered automatically.

## Workflow

### 1. Check prerequisites

Read `milestones/README.md` and find the line whose prefix is `Current milestone:`. If that line is not `Current milestone: none` (i.e. it still points to an active milestone path), stop and tell the user to run `/finish-current-milestone` first.

### 2. Pick the lowest candidate

A milestone directory is a directory under `milestones/` whose name matches `milestone_<digits>_<slug>`. Its number is read by stripping leading zeros from `<digits>` and is compared as an integer (e.g. `milestone_01_foo` → number `1`). A `milestone_*` directory whose prefix is not all digits does not match and is silently left out of the candidate set.

Read `milestones/README.md` and collect the done numbers: the integer N parsed from each `### Milestone N — Title` heading under `## Milestone History`. Never consult the `## Completed Milestones` table for this.

The **candidates** are the milestone directories in `milestones/` whose number matches no done number.

If there are no candidates, stop and tell the user to run `/define-milestone-goal` first to create a milestone. Otherwise activate the candidate with the lowest number, without asking the user anything.

### 3. Update milestones/README.md

In `milestones/README.md`, overwrite the `Current milestone:` line with:

```
Current milestone: `milestones/milestone_<number>_<slug>/`
```

Leave the `## Current Milestone` heading, the `## Milestone History` section, and all other content unchanged; update `milestones/README.md` only — never write the pointer into `CLAUDE.md`.

### 4. Commit the activation

Read and follow the shared commit procedure at `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`, carrying out its steps yourself. Supply it these two inputs:

- **PATHS** — this skill's own change set: `milestones/README.md` (the file whose `Current milestone:` pointer it just overwrote).
- **SUBJECT** — `Milestone-activation: milestone_<number>_<slug>`.

The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit.

### 5. Confirm

On the success path — the commit in step 4 recorded the activation — print exactly one fixed terse status line and nothing else:

```
Milestone activated.
```

Do not add the activated milestone's path or title, or a next-step pointer.

If instead the step-4 dirty-own-path guard fired (the `Current milestone:` pointer was unchanged, so nothing was committed), do not print the terse line — print a single concise line stating that nothing changed and briefly why, e.g. `No change — the pointer line already matched the last commit; nothing committed.`
