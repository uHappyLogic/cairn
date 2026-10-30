---
name: init-milestone-base-workflow
description: Bootstrap the milestone workflow in a project by ensuring CLAUDE.md carries the path-addressed milestone workflow guidance.
---

# init-milestone-base-workflow

Bootstraps the milestone-driven workflow inside a project. Its whole duty is `CLAUDE.md`: it ensures that file carries the `## Milestone Workflow` guidance, which tells anyone working in the project where milestones live and how each is named and finished. It probes nothing and creates no `milestones/` directory or other scaffold — `/define-milestone-goal` checks the workflow's runtime prerequisites each time it runs and creates a scope's `milestones/` container with the first milestone placed there. Run this **once** per project, before any other workflow skill.

This skill is additive and idempotent: it creates `CLAUDE.md` when it is missing and appends the section when the file lacks it, but never overwrites or rewrites content that is already there. It commits `CLAUDE.md` alone as one path-scoped commit.

## Usage

```
/init-milestone-base-workflow
```

No arguments.

## Workflow

### 1. Detect existing state

Check whether `CLAUDE.md` exists at the workspace root. If it does, read it and note whether it already contains a `## Milestone Workflow` section — any section under that heading, whatever its text says, an older one included.

If the section is present, the project is already bootstrapped: stop without changing anything and committing nothing, and print this one line and nothing else:

```
Workflow already bootstrapped — the guidance section is present.
```

### 2. Write the workflow guidance into CLAUDE.md

**If `CLAUDE.md` does not exist**, create it with this minimal content:

```markdown
# CLAUDE.md

This file provides guidance to the coding agent working in this repository.

## Milestone Workflow

This project uses the milestone-driven workflow. Each milestone lives at
`<scope>/milestones/<slug>/`, under the `milestones/` container of the directory holding the
core of its work, with `requirements.md`, `open_questions.xml`, and `TASKS_TODO.md`. No
milestone is current: every skill working inside one is given its path as
`--milestone <path>`, exactly as `/define-milestone-goal` printed it, trailing slash included.
A milestone directory is removed only by `/finish-milestone`, whose `Milestone-finish: <path>`
commit carries the milestone's record, so the directories standing are the live milestones and
the git log holds the finished ones.
```

**If `CLAUDE.md` exists and lacks the section**, append the `## Milestone Workflow` section — its heading and the paragraph shown above, exactly — to the end of the file, leaving every existing line untouched.

Never write a milestone path into `CLAUDE.md`, and never document the project's environment context in it yourself either.

### 3. Commit the bootstrap

Read and follow the shared commit procedure at `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`, running its one commit-tool command yourself as this step's one git tool call. Supply it these two inputs:

- **PATHS** — this skill's own change set: `CLAUDE.md` alone, which step 2 created or appended the section to.
- **SUBJECT** — `Workflow-bootstrap: milestones`.

Supply no BODY: the commit is subject-only. Hand the path over unchanged — uncommitted changes already present in `CLAUDE.md` before this run (for example a file just written by `/init`) are swept into this commit, with no status probe beforehand, no stop, no confirmation, no hunk-level staging, and no advisory.

The commit tool runs the dirty-own-path guard, the path-scoped staging, and the commit.

### 4. Confirm

On the success path — the commit in step 3 recorded the bootstrap — print exactly one fixed terse status line and nothing else:

```
Workflow bootstrapped.
```

Do not say whether the file was created or appended to, name the commit, or add any next-step or handoff pointer; the commit diff shows what was written.

If instead the step-3 commit tool printed `Nothing committed — none of the paths changed.` (the file already matched the last commit, so nothing was committed), do not print the terse line — print this one fixed line and nothing else:

```
Bootstrap committed nothing — the guidance already matched the last commit.
```
