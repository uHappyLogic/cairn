---
name: init-milestone-base-workflow
description: Bootstrap the milestone workflow in a project by creating the milestones/ directory and milestones/README.md, and ensuring CLAUDE.md carries the workflow guidance.
---

# init-milestone-base-workflow

Bootstraps the milestone-driven workflow inside a project. It first checks the one runtime prerequisite of the workflow skills — a Python 3.9 or later interpreter answering as `python3` — and stops before writing anything when none does. It then creates the `milestones/` directory and `milestones/README.md` (with the grep-able `Current milestone:` pointer line), and ensures `CLAUDE.md` contains the `## Milestone Workflow` guidance. Run this **once** per project, before any other workflow skill.

This skill is additive and idempotent: it creates missing scaffolding and inserts missing sections into existing files, but never overwrites or rewrites content that is already there. It does not commit — staging is left to the user.

## Usage

```
/init-milestone-base-workflow
```

No arguments.

## Workflow

### 1. Check the Python prerequisite

The workflow skills drive the plugin's open-question tool as `python3 .agents/plugins/cairn/tools/open_questions.py`, so every project this skill bootstraps needs a Python 3.9 or later interpreter reachable as `python3`. Check it here, before the state detection and on every invocation — a re-run on an already-bootstrapped project gets the same check.

Run `python3 --version`. If it prints a version of 3.9 or later, the check passes: continue to step 2. Compare the version numerically, minor by minor — `3.10` and `3.13` are later than `3.9`, `3.8` is not.

Otherwise — `python3` is not found, or it reports a version below 3.9 — run `python --version` as well. Its result decides nothing about passing; it only makes the message below precise. Then **stop before any write**: create and edit nothing, and print one full message that states, in order:

- **What it looked for** — a Python 3.9 or later interpreter answering as `python3`, and failing that as `python`.
- **What it found** — for each of the two names, that it was not found or the exact version it reported.
- **The remedy** — when `python` reported 3.9 or later, that interpreter exists under the other name and must be exposed as `python3` (a `python3` symlink or alias on the PATH, or the platform's equivalent); otherwise install Python 3.9 or later so that `python3` resolves to it.
- **That a re-run completes the bootstrap** — once `python3 --version` reports 3.9 or later, run `/init-milestone-base-workflow` again; it picks up with nothing to undo, since this stop wrote nothing.

### 2. Detect existing state

Probe the workspace root in parallel and record what already exists:

- Does `milestones/` exist?
- Does `milestones/README.md` exist? If so, does it contain a `Current milestone:` line?
- Does `CLAUDE.md` exist? If so, read it and note whether it already contains a `## Milestone Workflow` section.

Use these findings to decide which steps below are no-ops. If **all** of the following are already present — `milestones/`, `milestones/README.md`, and a `Current milestone:` line in `milestones/README.md` — the project is already initialized: report that and stop without changing anything.

### 3. Create the milestones/ directory

If `milestones/` does not exist, create it. Create no `milestone_<N>_<slug>/` directory inside it — that is `/define-milestone-goal`'s job.

### 4. Create milestones/README.md

If `milestones/README.md` does **not** exist, create it with this exact structure:

```markdown
# Milestones

This file is the source of truth for which milestone is current.

Each milestone lives at `milestones/milestone_<N>_<slug>/` and contains:

- `requirements.md` — goal, relevant starting state, decisions, out of scope
- `open_questions.xml` — the open questions, one `<open-question>` block each under a single `<open-questions>` root, written only by the plugin's open-question tool
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

### 5. Ensure CLAUDE.md carries the workflow guidance

**If `CLAUDE.md` does not exist**, create it with this minimal content:

```markdown
# CLAUDE.md

This file provides guidance to the coding agent working in this repository.

## Milestone Workflow

This project uses the milestone-driven workflow. Each milestone lives at
`milestones/milestone_<N>_<slug>/` with `requirements.md`, `open_questions.xml`,
`TASKS_TODO.md`, and `TASKS_DONE.md`. `milestones/README.md` is the source of truth for
which milestone is current. Never advance the pointer without first running
`/finish-current-milestone`.
```

After creating it, suggest the user run `/init` to document the project in `CLAUDE.md` — its domain context, working conventions, available tools, and how work is verified as done. The workflow skills read this environment context from `CLAUDE.md`.

**If `CLAUDE.md` already exists**, update it without disturbing existing content:

- If it has **no** `## Milestone Workflow` section, append the `## Milestone Workflow` section (the paragraph shown above) to the end of the file.
- If the section already exists, leave it exactly as-is — do not rewrite or re-template it.

Never write a current-milestone pointer into `CLAUDE.md`; the pointer lives only in `milestones/README.md`. Never document the project's environment context in `CLAUDE.md` yourself either — recommending `/init` is as far as this skill goes.

### 6. Confirm

Report:
- Which items were created (`milestones/`, `milestones/README.md`, `CLAUDE.md` sections) vs. already present and left untouched.
- The current-milestone pointer in `milestones/README.md` is initialized to `none`.
- Suggested next steps, in order:
  1. `/init` — document the project in `CLAUDE.md`: its domain context, working conventions, available tools, and how work is verified as done (run once, if not already documented).
  2. `/define-milestone-goal <goal>` — define the first milestone.
