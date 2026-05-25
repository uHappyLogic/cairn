# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Claude Code plugin (`workflow`) that implements a milestone-driven development workflow. It ships as a set of skills and one agent that move a project from a vague idea through discussion, planning, implementation, and archival — one milestone at a time.

## Repository layout

```
.claude-plugin/plugin.json   — plugin manifest (name, version, author)
skills/<skill-name>/SKILL.md — one skill per directory; the SKILL.md is the full skill definition
agents/implement-backlog-task.md — subagent invoked by implement-backlog-tasks skill
README.md                    — authoritative workflow documentation and skill reference
```

No build system, no tests, no dependencies. Everything is plain Markdown.

## Skills and the workflow they encode

The skills form a linear pipeline. Each skill's SKILL.md defines its exact behaviour:

```
define-implementation-environment ← one-time project setup: write IMPLEMENTATION_ENVIRONMENT.md
update-implementation-environment ← update environment file when stack changes
discuss-milestone-goal          ← optional sharpening conversation, creates no files
define-milestone-goal           ← creates milestones/milestone_<N>_<slug>/ with requirements.md, TASKS_TODO.md, TASKS_DONE.md
specify-milestone-starting-implementation-state ← fills "Relevant implementation state" in requirements.md
highlight-milestone-requirements-open-questions ← surfaces ambiguities; run repeatedly
discuss-open-question           ← structured conversation about one open question
answer-open-question            ← records the decision in requirements.md
populate-backlog                ← converts requirements.md → ordered TASKS_TODO.md
implement-backlog-tasks         ← orchestrator: spawns implement-backlog-task agent per task, commits after each
implement-backlog-task          ← single-task subagent (also in agents/)
finish-current-milestone        ← writes completion summary to milestones/README.md, updates CLAUDE.md only for lasting changes
goto-next-milestone             ← advances the current-milestone pointer in CLAUDE.md and milestones/README.md
```

## Milestone file structure

Each active milestone lives at `milestones/milestone_<N>_<slug>/` and contains exactly:

- `requirements.md` — Goal, Relevant implementation state, implementation decisions, open questions
- `TASKS_TODO.md` — pending tasks ordered by priority (highest first), `##` headings + `---` separators
- `TASKS_DONE.md` — completed tasks appended in the same format

`CLAUDE.md` (this file) and `milestones/README.md` are the source of truth for which milestone is current. The current milestone path is shown under `## Current Milestone` in backticks.

## Invariants to preserve when editing skills

- `answer-open-question` splits its arg on the first `.` — title before, answer after.
- `implement-backlog-task` expects tasks as `##` sections in `TASKS_TODO.md`, each terminated by a `---` separator.
- `implement-backlog-tasks` (orchestrator) commits after each successful task; individual skills never commit.
- `finish-current-milestone` must always run before `goto-next-milestone` — the pointer must never be advanced without a completion record.
- Open questions in `requirements.md` must be fully resolved before `populate-backlog` can run.
- `specify-milestone-starting-implementation-state`, `populate-backlog`, and `implement-backlog-task` (skill and agent) all require `IMPLEMENTATION_ENVIRONMENT.md` to exist. Run `define-implementation-environment` once at project setup to create it.
- The `implement-backlog-task` agent always resolves `<MILESTONE_DIR>` by reading `CLAUDE.md` — it must never use a hardcoded backlog path.

## Current Milestone

_(none yet — run `/define-implementation-environment` then `/define-milestone-goal` to start the first milestone)_
