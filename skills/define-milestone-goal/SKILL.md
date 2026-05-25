---
name: define-milestone-goal
description: Create a new milestone directory with initialized requirements.md (Goal filled from the provided description) and empty TASKS files.
---

# define-milestone-goal

Creates a new milestone directory under `milestones/` with a `requirements.md` pre-filled with the goal, plus empty `TASKS_TODO.md` and `TASKS_DONE.md`. Does not populate the remaining sections — those are filled by subsequent skills (`/specify-milestone-starting-implementation-state`, `/highlight-milestone-requirements-open-questions`, etc.).

## Usage

```
/define-milestone-goal <overall_goal_description>
```

- `<overall_goal_description>`: a clear description of what the milestone should accomplish. Use `/discuss-milestone-goal` first if the goal is still vague.

**Example:**
```
/define-milestone-goal add a shooting mechanic where the player fires a single projectile at enemies on the same spline segment
```

## Workflow

### 1. Determine the milestone number

Read `milestones/README.md` and `CLAUDE.md` to find the current milestone number. The new milestone number is `<current_number> + 1`.

If the current milestone is already `TBD` (i.e. `/finish-current-milestone` has not been run), stop and tell the user to finish the current milestone first before defining a new one.

### 2. Derive the milestone slug

Convert `<overall_goal_description>` to a short kebab-case slug (3–5 words max) that captures the essence of the goal. The full directory name is `milestone_<number>_<slug>`.

**Example:** "add a shooting mechanic where the player fires a single projectile" → `milestone_12_player-shooting`

### 3. Check for conflicts

Verify that `milestones/milestone_<number>_<slug>/` does not already exist. If a milestone with that number exists under any slug, stop and report the conflict.

### 4. Create the milestone directory

Create `milestones/milestone_<number>_<slug>/` with three files:

**`requirements.md`:**
```markdown
# Milestone <number>: <title>

## Goal

<overall_goal_description>

## Relevant implementation state

## Implementation decisions

## Out of Scope

```

**`TASKS_TODO.md`:**
```markdown
# TASKS TODO

```

**`TASKS_DONE.md`:**
```markdown
# TASKS DONE

```

### 5. Confirm

Report:
- New milestone directory created: `milestones/milestone_<number>_<slug>/`
- The goal written into `requirements.md`
- Suggest the next step: `/specify-milestone-starting-implementation-state milestone_<number>_<slug>` to fill in the implementation state section.

## Rules

- Do not update `CLAUDE.md` or `milestones/README.md` — those are only updated when the milestone becomes the *current* active milestone via `/goto-next-milestone`.
- Do not populate `## Relevant implementation state`, `## Implementation decisions`, or `## Out of Scope` — leave them empty for later skills.
- Do not assign the milestone as current — defining a milestone does not activate it.
- Never overwrite an existing milestone directory.
- Do not commit — leave staging to the user.
