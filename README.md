# Workflow Claude Plugin

A milestone-driven development workflow plugin for Claude Code. It moves an idea from a vague goal through discussion, planning, implementation, and archival — one milestone at a time.

## How it works

Each milestone lives in `milestones/milestone_<N>_<slug>/` and contains three files:

- `requirements.md` — goal, relevant implementation state, and implementation decisions
- `TASKS_TODO.md` — pending tasks ordered by priority (highest first)
- `TASKS_DONE.md` — completed tasks

The plugin provides skills that operate on the current milestone's files. `CLAUDE.md` and `milestones/README.md` are the source of truth for which milestone is current.

Before starting the first milestone, run `/init` so `CLAUDE.md` documents the project's tech stack, available tooling, and file organization. Skills read this environment context from `CLAUDE.md` instead of assuming any particular environment.

## Workflow overview

```
init-milestone-base-workflow    ← one-time bootstrap: create milestones/ + README, seed CLAUDE.md pointer
         ↓
/init                           ← one-time project setup: document tech stack/tooling in CLAUDE.md
         ↓
discuss-milestone-goal          ← optional: sharpen a vague idea before defining
         ↓
define-milestone-goal           ← create the milestone directory and seed requirements.md
         ↓
specify-milestone-starting-implementation-state ← fill "Relevant implementation state" from the codebase
         ↓
┌─────────────────────────────────────────────────────────────────┐
│  highlight-milestone-requirements-open-questions                │  ← repeat to surface more gaps
│           ↓                                                     │
│  discuss-open-question  ← explore one question (optional)      │
│           ↓                                                     │
│  answer-open-question   ← record the decision                  │
└──────────────────────────────── repeat until satisfied ─────────┘
         ↓
populate-backlog                ← convert requirements.md → ordered TASKS_TODO.md
         ↓
implement-backlog-tasks         ← execute all tasks, committing after each one
         ↓
finish-current-milestone        ← record accomplishments; update CLAUDE.md if needed
         ↓
goto-next-milestone             ← advance the current-milestone pointer
```

Run `highlight-milestone-requirements-open-questions` as many times as needed — each pass may surface questions that earlier answers opened up. Once no open questions remain, proceed to `populate-backlog`.

## Skills

### `init-milestone-base-workflow`

One-time bootstrap for a project. Creates the `milestones/` directory and `milestones/README.md`, and ensures `CLAUDE.md` carries the `## Milestone Workflow` guidance and the `## Current Milestone` pointer that every other skill reads. Additive and idempotent — it creates missing scaffolding and inserts missing sections into existing files, but never overwrites content that is already there. Run this before any other workflow skill.

### `discuss-milestone-goal <overall_goal_description>`

Facilitates a structured conversation to sharpen a vague goal into a clear, actionable statement. Produces a refined goal description ready for `/define-milestone-goal`. Creates no files.

### `define-milestone-goal <overall_goal_description>`

Creates a new `milestones/milestone_<N>_<slug>/` directory with `requirements.md` (Goal section filled), plus empty `TASKS_TODO.md` and `TASKS_DONE.md`. Does **not** activate the milestone or update `CLAUDE.md`.

### `specify-milestone-starting-implementation-state <milestone_id>`

Reads the milestone goal, explores the project using the file organization documented in `CLAUDE.md`, and writes a concise technical summary into the `## Relevant implementation state` section of `requirements.md`. Sets up the context needed to make implementation decisions.

### `highlight-milestone-requirements-open-questions`

Scans the current milestone's `requirements.md` and surfaces remaining ambiguities or decisions that need to be made before the backlog can be populated. Run it multiple times — earlier answers often open new questions, and repeated passes catch gaps that weren't visible before.

### `discuss-open-question <question_name>`

Opens a structured conversation about a named open question in `requirements.md`. Surfaces alternatives, trade-offs, and a recommendation to help the user reach a decision.

### `answer-open-question <question_name>`

Records the resolution of a named open question in `requirements.md`, updating the document to reflect the decision and its downstream implications.

### `populate-backlog`

Converts the current milestone's `requirements.md` into `TASKS_TODO.md` — a complete, dependency-ordered list of atomic, AI-executable tasks. It decomposes the milestone into high-level task briefs, proves every requirement is covered with a requirement→task matrix, then delegates the detailed authoring of each task to the `submit-backlog-task` agent (one brief at a time, in dependency order). Requires all open questions to be resolved first.

### `discuss-new-backlog-task <issue description>`

Clarifies a rough or oversized issue discovered mid-implementation into one or more clear, task-sized briefs through a short conversation, then hands each off to `/submit-backlog-task`. Writes nothing itself. Use it when the affected system, desired behavior, or verification isn't yet clear, or when one issue is really several tasks.

### `submit-backlog-task <issue description>`

Adds a single, already-clear issue to `TASKS_TODO.md`. The skill triages for duplicates and decides where the task belongs, then delegates the detailed authoring to the `submit-backlog-task` agent. For vague or multi-task issues, route through `/discuss-new-backlog-task` first.

### `implement-backlog-tasks`

Orchestrator: executes all tasks in `TASKS_TODO.md` top to bottom, spawning one subagent per task and committing after each success. Stops on first failure.

### `implement-backlog-task <task_name>`

Implements a single named task from the current milestone's `TASKS_TODO.md` **inline, in the current conversation** — it follows `shared/implement-procedure.md` directly rather than spawning a subagent. Running inline keeps the implementation context (what changed, why, how it was verified) in the conversation, so you can ask follow-up questions or request tweaks right after. The changes are left staged for the user — unlike `/implement-backlog-tasks`, it does not commit. For implementing the whole backlog unattended, use `/implement-backlog-tasks`, which runs each task in an isolated subagent instead.

### `finish-current-milestone`

Verifies all tasks are done, writes a completion summary to `milestones/README.md`, and updates `CLAUDE.md` only for lasting tech-stack or structural changes. Does **not** update the current milestone pointer — run `/goto-next-milestone` after.

### `goto-next-milestone <number> <title>`

Creates the next milestone directory with empty starter files and updates the current-milestone pointer in both `CLAUDE.md` and `milestones/README.md`. Only runnable after `/finish-current-milestone` has been called.

## Agents

Two subagents do per-task work in a clean context so detailed technical reasoning never pollutes the orchestrating skill's memory. They are spawned by skills, not invoked directly:

- **`submit-backlog-task`** — authors one well-scoped task from a high-level brief and inserts it into `TASKS_TODO.md` at a caller-given position. Keeps the task at contract altitude: *what* to achieve plus the names and thresholds sibling tasks depend on, not the line-by-line code. Spawned by `populate-backlog` (bulk) and the `submit-backlog-task` skill (ad-hoc). Owns the task-body template.
- **`implement-backlog-task`** — implements one named task, verifies its success criteria, and moves it to `TASKS_DONE.md`, following the shared `shared/implement-procedure.md` in an isolated context. That procedure owns the **detailed implementation design** — turning the task's high-level steps into concrete code against the live codebase. Spawned by the `implement-backlog-tasks` orchestrator for bulk runs. (The ad-hoc `implement-backlog-task` skill follows the *same* procedure, but inline rather than via this agent, so its work context survives for follow-up.)

## Rules

- Run `/init-milestone-base-workflow` once before anything else — it creates `milestones/` and the current-milestone pointer the other skills depend on.
- Run `/init` once before starting the first milestone so `CLAUDE.md` documents the tech stack, tooling, and conventions. Skills that explore or implement code read this environment context from `CLAUDE.md`.
- Never skip `/finish-current-milestone` before `/goto-next-milestone` — the pointer in `CLAUDE.md` must always reflect the active milestone.
- Open questions in `requirements.md` must be resolved before running `/populate-backlog`.
- Skills never commit — staging and committing is always left to the user (except `/implement-backlog-tasks`, which commits after each task).
