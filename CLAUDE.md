# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Claude Code plugin (`cairn`) that implements a milestone-driven development workflow. It ships as a set of skills and a couple of agents that move a project from a vague idea through discussion, planning, implementation, and archival — one milestone at a time.

## Repository layout

```
.claude-plugin/plugin.json   — plugin manifest (name, version, author)
.claude-plugin/marketplace.json — single-plugin marketplace manifest (installable via /plugin marketplace add uHappyLogic/cairn)
skills/<skill-name>/SKILL.md — one skill per directory; the SKILL.md is the full skill definition
agents/implement-backlog-task.md — implementation subagent invoked by implement-backlog-tasks skill
agents/submit-backlog-task.md — task-authoring subagent invoked by populate-backlog and the submit-backlog-task skill
shared/implement-procedure.md — single source of truth for the implement-one-task procedure, followed inline by the implement-backlog-task skill and in isolation by the implement-backlog-task agent
shared/get-current-milestone.md — single source of truth for resolving <MILESTONE_DIR> from the grep-able pointer line in milestones/README.md
LICENSE                      — MIT license
README.md                    — authoritative workflow documentation and skill reference
```

No build system, no tests, no dependencies. Everything is plain Markdown.

## Skills and the workflow they encode

The skills form a linear pipeline. Each skill's SKILL.md defines its exact behaviour:

```
init-milestone-base-workflow    ← one-time bootstrap: create milestones/ + milestones/README.md
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
implement-backlog-task          ← (skill) user-facing entry for one ad-hoc task: runs shared/implement-procedure.md inline so the work context stays for follow-up
implement-backlog-task          ← (agent, in agents/) single-task implementation subagent: runs shared/implement-procedure.md in isolation, returns DONE/FAILED
finish-current-milestone        ← writes completion summary to milestones/README.md, clears current-milestone pointer to "none" in milestones/README.md, updates CLAUDE.md only for lasting changes
goto-next-milestone             ← activates an already-defined milestone: scans milestones/ for a defined-but-not-yet-active directory, updates milestones/README.md to point to it
```

## Milestone file structure

Each active milestone lives at `milestones/milestone_<N>_<slug>/` and contains exactly:

- `requirements.md` — Goal, Relevant implementation state, implementation decisions, open questions
- `TASKS_TODO.md` — pending tasks ordered by priority (highest first), `##` headings + `---` separators
- `TASKS_DONE.md` — completed tasks appended in the same format

`milestones/README.md` is the source of truth for which milestone is current.

## Invariants to preserve when editing skills

- `init-milestone-base-workflow` is the one-time bootstrap; it is additive and idempotent — it never overwrites an existing `milestones/README.md` or `CLAUDE.md`, only creating missing files and appending missing sections. It must leave `milestones/README.md` with a `Current milestone:` pointer line.
- `answer-open-question` splits its arg on the first `.` — title before, answer after.
- The `implement-backlog-task` agent expects tasks as `##` sections in `TASKS_TODO.md`, each terminated by a `---` separator.
- `implement-backlog-tasks` (orchestrator) commits after each successful task; individual skills never commit — including the `implement-backlog-task` skill, which leaves an ad-hoc task's changes staged for the user.
- `finish-current-milestone` must always run before `goto-next-milestone` — it records the completion and clears the current-milestone pointer to "none". `goto-next-milestone` checks for this "none" state and refuses to run without it.
- Open questions in `requirements.md` must be fully resolved before `populate-backlog` can run.
- `specify-milestone-starting-implementation-state`, `populate-backlog`, and the shared implement procedure (run by both the `implement-backlog-task` skill and agent) read the project's environment context (tech stack, build/test commands, MCP tools, conventions) from `CLAUDE.md`. Run `/init` once at project setup so `CLAUDE.md` documents it.
- `populate-backlog` owns decomposition and coverage only; it must not author task bodies itself. It proves every requirement maps to a brief (traceability matrix), then submits briefs **in dependency order** to the `submit-backlog-task` agent with `POSITION: append`, spawning the agents **sequentially** (they all mutate the same `TASKS_TODO.md`).
- The task body template (`##` title, description, optional **Provides**, optional **Notes**, **Success**, trailing `---`) lives in exactly one place: the `submit-backlog-task` agent. `populate-backlog` and the `submit-backlog-task` skill must not duplicate it. There is deliberately **no** `Steps` section — see the altitude invariant below.
- `submit-backlog-task` exists as both a thin user-facing skill (triage + dedup + positioning) and an agent (authoring). The skill decides the insert position from the whole-backlog view and passes it to the agent; the agent must not re-derive global ordering.
- The implementation procedure — find task, load environment, implement, verify success criteria, move TODO→DONE — lives in exactly one place: `shared/implement-procedure.md`. Neither the `implement-backlog-task` skill nor the agent may duplicate or restate those steps; both reference the shared file via `${CLAUDE_PLUGIN_ROOT}`. The shared file is execution-neutral — it must not mention the `DONE`/`FAILED` return protocol, committing, or follow-up; those belong to the wrappers.
- `implement-backlog-task` exists as both a user-facing skill and an agent, differing only in *where* the shared procedure runs. The **skill runs it inline** in the user's conversation (so the work context survives for follow-up) and must never spawn the agent. The **agent runs it in an isolated subagent context** and adds the `DONE`/`FAILED` return protocol; it is what the `implement-backlog-tasks` orchestrator spawns per task. Choosing inline vs. isolated is the entire reason both exist — keep that the only difference.
- The `submit-backlog-task` agent and the shared implement procedure always resolve `<MILESTONE_DIR>` by reading `milestones/README.md` — they must never use a hardcoded backlog path.
- Task altitude is split, and the dividing line is **what can be re-derived at implementation time**. The `submit-backlog-task` agent authors only what *cannot* be reconstructed from the goal + live code: the `Description` (intent), the `Success` bar, the optional `Provides` (the forward contract — names/thresholds sibling tasks reference before this task is built), and the optional `Notes` (non-obvious gotchas that would cost the implementer a discovery round). The shared implement procedure owns everything re-derivable — the flow itself and the **detailed implementation design** (exact code, insertion points, assertion wording, decided fresh against the live codebase). The agent must **not** author a step-by-step flow under any heading (no `Steps`); `Provides`/`Notes` are omitted entirely when empty. Keep task bodies minimal to save tokens; never push line-by-line implementation detail — or a re-narration of the flow — back into authored tasks.

## Milestone Workflow

This project uses the milestone-driven workflow. Each milestone lives at
`milestones/milestone_<N>_<slug>/` with `requirements.md`, `TASKS_TODO.md`, and
`TASKS_DONE.md`. `milestones/README.md` is the source of truth for which milestone
is current. Never advance the pointer without first running
`/finish-current-milestone`.

