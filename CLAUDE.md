# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Claude Code plugin (`workflow`) that implements a milestone-driven development workflow. It ships as a set of skills and a couple of agents that move a project from a vague idea through discussion, planning, implementation, and archival — one milestone at a time.

## Repository layout

```
.claude-plugin/plugin.json   — plugin manifest (name, version, author)
skills/<skill-name>/SKILL.md — one skill per directory; the SKILL.md is the full skill definition
agents/implement-backlog-task.md — implementation subagent invoked by implement-backlog-tasks skill
agents/submit-backlog-task.md — task-authoring subagent invoked by populate-backlog and the submit-backlog-task skill
README.md                    — authoritative workflow documentation and skill reference
```

No build system, no tests, no dependencies. Everything is plain Markdown.

## Skills and the workflow they encode

The skills form a linear pipeline. Each skill's SKILL.md defines its exact behaviour:

```
init-milestone-base-workflow    ← one-time bootstrap: create milestones/ + milestones/README.md, seed CLAUDE.md ## Current Milestone pointer
discuss-milestone-goal          ← optional sharpening conversation, creates no files
define-milestone-goal           ← creates milestones/milestone_<N>_<slug>/ with requirements.md, TASKS_TODO.md, TASKS_DONE.md
specify-milestone-starting-implementation-state ← fills "Relevant implementation state" in requirements.md
highlight-milestone-requirements-open-questions ← surfaces ambiguities; run repeatedly
discuss-open-question           ← structured conversation about one open question
answer-open-question            ← records the decision in requirements.md
populate-backlog                ← decomposes requirements.md into ordered briefs, proves coverage, spawns submit-backlog-task agent per brief
submit-backlog-task             ← (skill) user-facing entry for a single ad-hoc issue: triages + positions, then spawns the submit-backlog-task agent
submit-backlog-task             ← (agent, in agents/) authors one task from a brief and inserts it into TASKS_TODO.md at a caller-given position
discuss-new-backlog-task        ← clarifies a vague/large issue into briefs, then hands off to the submit-backlog-task skill
implement-backlog-tasks         ← orchestrator: spawns implement-backlog-task agent per task, commits after each
implement-backlog-task          ← (skill) thin user-facing entry for one ad-hoc task: spawns the implement-backlog-task agent and relays its result
implement-backlog-task          ← (agent, in agents/) single-task implementation subagent that owns the full implement procedure
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

- `init-milestone-base-workflow` is the one-time bootstrap; it is additive and idempotent — it never overwrites an existing `milestones/README.md` or `CLAUDE.md`, only creating missing files and appending missing sections. It must leave both `CLAUDE.md` and `milestones/README.md` with an agreeing `## Current Milestone` section.
- `answer-open-question` splits its arg on the first `.` — title before, answer after.
- The `implement-backlog-task` agent expects tasks as `##` sections in `TASKS_TODO.md`, each terminated by a `---` separator.
- `implement-backlog-tasks` (orchestrator) commits after each successful task; individual skills never commit — including the `implement-backlog-task` skill, which leaves an ad-hoc task's changes staged for the user.
- `finish-current-milestone` must always run before `goto-next-milestone` — the pointer must never be advanced without a completion record.
- Open questions in `requirements.md` must be fully resolved before `populate-backlog` can run.
- `specify-milestone-starting-implementation-state`, `populate-backlog`, and the `implement-backlog-task` agent read the project's environment context (tech stack, build/test commands, MCP tools, conventions) from `CLAUDE.md`. Run `/init` once at project setup so `CLAUDE.md` documents it.
- `populate-backlog` owns decomposition and coverage only; it must not author task bodies itself. It proves every requirement maps to a brief (traceability matrix), then submits briefs **in dependency order** to the `submit-backlog-task` agent with `POSITION: append`, spawning the agents **sequentially** (they all mutate the same `TASKS_TODO.md`).
- The task body template (`##` title, description, **Steps**, **Success**, trailing `---`) lives in exactly one place: the `submit-backlog-task` agent. `populate-backlog` and the `submit-backlog-task` skill must not duplicate it.
- `submit-backlog-task` exists as both a thin user-facing skill (triage + dedup + positioning) and an agent (authoring). The skill decides the insert position from the whole-backlog view and passes it to the agent; the agent must not re-derive global ordering.
- `implement-backlog-task` exists as both a thin user-facing skill (spawn + relay) and an agent (the procedure). The implementation procedure — find task, load environment, implement, verify success criteria, move TODO→DONE — lives in exactly one place: the agent. The skill must not duplicate it; it only spawns the agent and relays `DONE`/`FAILED`. Both the skill and the `implement-backlog-tasks` orchestrator reach the procedure through that single agent.
- The `implement-backlog-task` and `submit-backlog-task` agents always resolve `<MILESTONE_DIR>` by reading `CLAUDE.md` — they must never use a hardcoded backlog path.

## Current Milestone

_(none yet — run `/init` then `/define-milestone-goal` to start the first milestone)_
