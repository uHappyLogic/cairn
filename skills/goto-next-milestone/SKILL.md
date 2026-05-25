---
name: goto-next-milestone
description: Advance the project to a new milestone — creates the milestone directory and updates all current-milestone references in CLAUDE.md and milestones/README.md.
---

# goto-next-milestone

Creates a new milestone directory with empty starter files, then updates `CLAUDE.md` and `milestones/README.md` to point to the new milestone as the current one. Run this after `/finish-milestone` has recorded the previous milestone's accomplishments.

## Usage

```
/goto-next-milestone <number> <title>
```

- `<number>`: the milestone number (integer, e.g. `5`)
- `<title>`: a short human-readable title (e.g. `player-shooting`)

The directory slug is derived by converting `<title>` to lowercase kebab-case.

**Example:**
```
/goto-next-milestone 7 WebGL Demo on GitHub Pages
```
Creates `milestones/milestone_7_webgl-demo-on-github-pages/`.

## Workflow

### 1. Parse the input

Split the args: the first token is `<number>`, the rest is `<title>`. Derive `<slug>` by lowercasing `<title>` and replacing spaces with hyphens. The full directory name is `milestone_<number>_<slug>`.

If `<number>` or `<title>` is missing, report the expected format and stop.

### 2. Check for conflicts

Verify that `milestones/milestone_<number>_<slug>/` does not already exist. If it does, stop and report the conflict.

### 3. Find the current milestone

Read `CLAUDE.md` and extract the current milestone path and title from `## Current Milestone`. Use this as `<PREV_MILESTONE_DIR>` and `<PREV_MILESTONE_TITLE>`.

### 4. Create the new milestone directory

Create `milestones/milestone_<number>_<slug>/` with three starter files:

**`requirements.md`:**
```markdown
# Milestone <number>: <title>

## Goal

## Relevant implementation state

## Implementation decisions

## Open questions

```

**`TASKS_TODO.md`:**
```markdown
# TASKS TODO

```

**`TASKS_DONE.md`:**
```markdown
# TASKS DONE

```

### 5. Update milestones/README.md

Read the current `milestones/README.md` and make two edits:

**a. Replace the Current Milestone section** with the new milestone:

```markdown
## Current Milestone

**Milestone <number> — <title>** (`milestones/milestone_<number>_<slug>/`)

```

**b. Add the previous milestone to the Completed Milestones table** as the first data row (after the header):

```
| <prev_number> | <prev_title> | `milestones/<prev_dir>/` |
```

Extract `<prev_number>` and `<prev_title>` from the old Current Milestone section.

### 6. Update CLAUDE.md

Replace the `## Current Milestone` section content with:

```markdown
**Milestone <number> — <title>** (`milestones/milestone_<number>_<slug>/`)

See `milestones/README.md` for the full milestone history.
```

### 7. Confirm

Report:
- New milestone directory created: `milestones/milestone_<number>_<slug>/`
- Previous milestone moved to completed in `milestones/README.md`
- `CLAUDE.md` updated to reference the new milestone

## Rules

- Never overwrite an existing milestone directory.
- Do not populate `requirements.md` beyond the template — defining the milestone goal is the user's job.
- Always update both `milestones/README.md` and `CLAUDE.md` — leaving either stale breaks every skill that reads the current milestone path.
- Do not commit — leave staging to the user.
