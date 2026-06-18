---
name: init-milestone-base-workflow
description: One-time bootstrap for the milestone workflow in a project — creates the milestones/ directory and milestones/README.md with the Current Milestone pointer, and ensures CLAUDE.md carries the Milestone Workflow guidance. Safe to run on an existing project; never overwrites existing files.
---

# init-milestone-base-workflow

Bootstraps the milestone-driven workflow inside a project. It creates the `milestones/` directory and `milestones/README.md` (with the grep-able `Current milestone:` pointer line), and ensures `CLAUDE.md` contains the `## Milestone Workflow` guidance. Run this **once** per project, before any other workflow skill.

This skill is additive and idempotent: it creates missing scaffolding and inserts missing sections into existing files, but never overwrites or rewrites content that is already there.

## Usage

```
/init-milestone-base-workflow
```

No arguments.

## Workflow

### 1. Detect existing state

Probe the workspace root in parallel and record what already exists:

- Does `milestones/` exist?
- Does `milestones/README.md` exist? If so, does it contain a `Current milestone:` line?
- Does `CLAUDE.md` exist? If so, read it and note whether it already contains a `## Milestone Workflow` section.

Use these findings to decide which steps below are no-ops. If **all** of the following are already present — `milestones/`, `milestones/README.md`, and a `Current milestone:` line in `milestones/README.md` — the project is already initialized: report that and stop without changing anything.

### 2. Create the milestones/ directory

If `milestones/` does not exist, create it.

### 3. Create milestones/README.md

If `milestones/README.md` does **not** exist, create it with this exact structure:

```markdown
# Milestones

This file is the source of truth for which milestone is current.

Each milestone lives at `milestones/milestone_<N>_<slug>/` and contains:

- `requirements.md` — goal, relevant starting state, implementation decisions, open questions
- `TASKS_TODO.md` — pending tasks ordered by priority (highest first)
- `TASKS_DONE.md` — completed tasks

## Current Milestone

Current milestone: none

## Milestone History

_No milestones completed yet._

## Completed Milestones

| # | Title | Path |
|---|-------|------|
```

If `milestones/README.md` **already exists**, do not overwrite it. Instead, ensure it contains a `## Current Milestone` section with a `Current milestone:` line; if either is missing, insert the section (with `Current milestone: none`) after the file's top-level heading, and leave the rest of the file untouched. Report that the file was preserved.

> The README intentionally carries both a `## Milestone History` section (written by `/finish-current-milestone`) and a `## Completed Milestones` table (written by `/goto-next-milestone`). Keep both so neither skill fails.

### 4. Ensure CLAUDE.md carries the workflow guidance

**If `CLAUDE.md` does not exist**, create it with this minimal content:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Milestone Workflow

This project uses the milestone-driven workflow. Each milestone lives at
`milestones/milestone_<N>_<slug>/` with `requirements.md`, `TASKS_TODO.md`, and
`TASKS_DONE.md`. `milestones/README.md` is the source of truth for which milestone
is current. Never advance the pointer without first running `/finish-current-milestone`.
```

After creating it, suggest the user run `/init` to enrich `CLAUDE.md` with full codebase documentation — tech stack, build/test commands, file organization, and conventions. The workflow skills read this environment context from `CLAUDE.md`.

**If `CLAUDE.md` already exists**, update it without disturbing existing content:

- If it has **no** `## Milestone Workflow` section, append the `## Milestone Workflow` section (the paragraph shown above) to the end of the file.
- If the section already exists, leave it exactly as-is — do not rewrite or re-template it.

### 5. Confirm

Report:
- Which items were created (`milestones/`, `milestones/README.md`, `CLAUDE.md` sections) vs. already present and left untouched.
- The current-milestone pointer in `milestones/README.md` is initialized to `none`.
- Suggested next steps, in order:
  1. `/init` — enrich `CLAUDE.md` with the project's tech stack, tooling, and conventions (run once, if not already documented).
  2. `/define-milestone-goal <goal>` — define the first milestone.

## Rules

- Run once per project. If the project is already initialized (presence of `milestones/` and `milestones/README.md` with a `Current milestone:` line is sufficient), stop and report — do not re-scaffold.
- Never overwrite or rewrite an existing `milestones/README.md` or `CLAUDE.md` — only create missing files and append missing sections.
- The current-milestone pointer lives only in `milestones/README.md`; do not write a pointer into `CLAUDE.md`.
- Do not create any `milestone_<N>_<slug>/` directory — that is `/define-milestone-goal`'s job.
- Do not document the tech stack or conventions in `CLAUDE.md` — that is `/init`'s job; only recommend it.
- Do not commit — leave staging to the user.
