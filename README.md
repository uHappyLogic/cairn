# Workflow Claude Plugin

A milestone-driven development workflow plugin for Claude Code. It moves an idea from a vague goal through discussion, planning, implementation, and archival — one milestone at a time.

## How it works

Each milestone lives in `milestones/milestone_<N>_<slug>/` and contains three files:

- `requirements.md` — goal, relevant implementation state, and implementation decisions
- `TASKS_TODO.md` — pending tasks ordered by priority (highest first)
- `TASKS_DONE.md` — completed tasks

The plugin provides skills that operate on the current milestone's files. `CLAUDE.md` and `milestones/README.md` are the source of truth for which milestone is current.

## Workflow overview

```
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

### `discuss-milestone-goal <overall_goal_description>`

Facilitates a structured conversation to sharpen a vague goal into a clear, actionable statement. Produces a refined goal description ready for `/define-milestone-goal`. Creates no files.

### `define-milestone-goal <overall_goal_description>`

Creates a new `milestones/milestone_<N>_<slug>/` directory with `requirements.md` (Goal section filled), plus empty `TASKS_TODO.md` and `TASKS_DONE.md`. Does **not** activate the milestone or update `CLAUDE.md`.

### `specify-milestone-starting-implementation-state <milestone_id>`

Reads the milestone goal, explores the Unity project, and writes a concise technical summary into the `## Relevant implementation state` section of `requirements.md`. Sets up the context needed to make implementation decisions.

### `highlight-milestone-requirements-open-questions`

Scans the current milestone's `requirements.md` and surfaces remaining ambiguities or decisions that need to be made before the backlog can be populated. Run it multiple times — earlier answers often open new questions, and repeated passes catch gaps that weren't visible before.

### `discuss-open-question <question_name>`

Opens a structured conversation about a named open question in `requirements.md`. Surfaces alternatives, trade-offs, and a recommendation to help the user reach a decision.

### `answer-open-question <question_name>`

Records the resolution of a named open question in `requirements.md`, updating the document to reflect the decision and its downstream implications.

### `populate-backlog`

Converts the current milestone's `requirements.md` into `TASKS_TODO.md` — a complete, dependency-ordered list of atomic, AI-executable tasks. Requires all open questions to be resolved first.

### `implement-backlog-tasks`

Orchestrator: executes all tasks in `TASKS_TODO.md` top to bottom, spawning one subagent per task and committing after each success. Stops on first failure.

### `implement-backlog-task <task_name>`

Implements a single named task from the current milestone's `TASKS_TODO.md`, verifies its success criteria, and moves it to `TASKS_DONE.md`.

### `finish-current-milestone`

Verifies all tasks are done, writes a completion summary to `milestones/README.md`, and updates `CLAUDE.md` only for lasting tech-stack or structural changes. Does **not** update the current milestone pointer — run `/goto-next-milestone` after.

### `goto-next-milestone <number> <title>`

Creates the next milestone directory with empty starter files and updates the current-milestone pointer in both `CLAUDE.md` and `milestones/README.md`. Only runnable after `/finish-current-milestone` has been called.

## Rules

- Never skip `/finish-current-milestone` before `/goto-next-milestone` — the pointer in `CLAUDE.md` must always reflect the active milestone.
- Open questions in `requirements.md` must be resolved before running `/populate-backlog`.
- Skills never commit — staging and committing is always left to the user (except `/implement-backlog-tasks`, which commits after each task).
