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
agents/submit-backlog-task.md — task-authoring subagent invoked by populate-backlog (bulk)
agents/try-answer-question-by-principle.md — read-only candidate-elimination subagent invoked by the try-answer-all-questions-by-principle orchestrator; returns a verdict only, never edits documents
shared/implement-procedure.md — single source of truth for the implement-one-task procedure, followed inline by the implement-backlog-task skill and in isolation by the implement-backlog-task agent
shared/submit-procedure.md — single source of truth for the author-and-insert-one-task procedure, followed inline by the submit-backlog-task skill and in isolation by the submit-backlog-task agent
shared/answer-procedure.md — single source of truth for recording an answer (locate question block by Short Title → fold decision into ## Implementation decisions → cascade), referenced by answer-open-question and the try-answer-all-questions-by-principle orchestrator
shared/get-current-milestone.md — single source of truth for resolving <MILESTONE_DIR> from the grep-able pointer line in milestones/README.md
milestones/answer_decision_principles.md — project-wide answering-principle store at the milestones/ root, shared across all milestones (above any <MILESTONE_DIR>); the loop's one fixed-path artifact
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
try-answer-all-questions-by-principle ← orchestrator: sweeps open/deferred questions, auto-answers only those a confirmed principle resolves, one commit per answer; run after highlight
try-answer-question-by-principle ← (agent, in agents/) read-only candidate-elimination subagent: returns a verdict (unique survivor + cited principles), never edits documents
discuss-open-question           ← structured conversation about one open question
answer-open-question            ← records the decision in requirements.md, then chains to try-capture-answer-principle
try-capture-answer-principle    ← records/revises a confirmed answering principle (user-confirmed); chained from answer-open-question
reject-auto-answer              ← reverts one bad auto-answer commit and reopens its question; revert left staged
populate-backlog                ← decomposes requirements.md into ordered briefs, proves coverage, spawns submit-backlog-task agent per brief
submit-backlog-task             ← (skill) user-facing entry for a single ad-hoc issue: triages + positions, then runs shared/submit-procedure.md inline so the authoring context stays for follow-up
submit-backlog-task             ← (agent, in agents/) bulk per-task authoring for populate-backlog: runs shared/submit-procedure.md in isolation, returns DONE/FAILED
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
- `try-answer-all-questions-by-principle` (renamed from the old `answer-obvious` sweep) is the autonomous sweep run after `highlight-milestone-requirements-open-questions`: it processes Open/Deferred entries **sequentially against the live document** (so cascades apply) and auto-answers a question **only** when a confirmed principle from `milestones/answer_decision_principles.md` resolves it — questions no principle covers are left untouched. The answer-recording mechanism (locate the question block by Short Title → fold the decision into `## Implementation decisions` as clean prose → cascade to mooted entries) lives in exactly one place: `shared/answer-procedure.md`. Both `answer-open-question` and this orchestrator reference it via `${CLAUDE_PLUGIN_ROOT}` and never restate the steps — superseding the prior state where the steps were duplicated in prose between the two. That shared file is **execution-neutral** — it takes a resolved Short Title + answer and never mentions arg-parsing, committing, the `Answer-Principle:` trailer, or the capture chain.
- The `try-answer-all-questions-by-principle` orchestrator owns **all** document mutation and the commit; its `try-answer-question-by-principle` subagent (one dispatch per question) is **read-only on `requirements.md` and the principle store** and returns a verdict only (unique-survivor yes/no, the answer, the cited load-bearing principles, the candidate set considered). The subagent does the candidate elimination; the orchestrator records and commits. This is a deliberate divergence from the file-editing `implement-backlog-task` agent — cascades plus one-commit-per-answer require all mutation serialized in the single sequential orchestrator, while the context-heavy elimination is what's worth isolating.
- `answer-open-question` unconditionally chains to `try-capture-answer-principle` after recording a decision (capture analyses the conversation, not a payload, and engages the user only on a real generalizable principle). The `try-answer-all-questions-by-principle` orchestrator **never** chains to capture — the auto-answer was itself derived from a confirmed principle, so capturing would be circular.
- `reject-auto-answer` reverts exactly one auto-answer commit (`git revert --no-commit`) and leaves the revert **staged** (per the no-commit invariant). It validates the target first — the commit must touch **only `requirements.md`** and carry **≥1 `Answer-Principle:` trailer** — and refuses otherwise; the revert simultaneously restores the question block and removes the folded decision, so the revert *is* the reopen. It **never edits the principle store** — it surfaces the cited principle(s) and directs the user to re-capture to close the loop.
- The `implement-backlog-task` agent expects tasks as `##` sections in `TASKS_TODO.md`, each terminated by a `---` separator.
- Two orchestrators commit; individual skills never commit — including the `implement-backlog-task` skill, which leaves an ad-hoc task's changes staged for the user. `implement-backlog-tasks` commits after each successful task. `try-answer-all-questions-by-principle` commits exactly **one auto-answer per commit** — subject `Principle-based-answer: <Short Title>` (the answered question's handle), with one repeated `Answer-Principle: <Short Title>` trailer line per load-bearing principle.
- `finish-current-milestone` must always run before `goto-next-milestone` — it records the completion and clears the current-milestone pointer to "none". `goto-next-milestone` checks for this "none" state and refuses to run without it.
- Open questions in `requirements.md` must be fully resolved before `populate-backlog` can run.
- `specify-milestone-starting-implementation-state`, `populate-backlog`, and the shared implement procedure (run by both the `implement-backlog-task` skill and agent) read the project's environment context (tech stack, build/test commands, MCP tools, conventions) from `CLAUDE.md`. Run `/init` once at project setup so `CLAUDE.md` documents it.
- `populate-backlog` owns decomposition and coverage only; it must not author task bodies itself. It proves every requirement maps to a brief (traceability matrix), then submits briefs **in dependency order** to the `submit-backlog-task` agent with `POSITION: append`, spawning the agents **sequentially** (they all mutate the same `TASKS_TODO.md`).
- The task body template (`##` title, description, optional **Provides**, optional **Notes**, **Success**, trailing `---`) lives in exactly one place: `shared/submit-procedure.md`. The `submit-backlog-task` skill, the `submit-backlog-task` agent, and `populate-backlog` must not duplicate it. There is deliberately **no** `Steps` section — see the altitude invariant below.
- The author-and-insert procedure — find milestone, load context, author the task (template + authoring guidelines), insert at the given POSITION — lives in exactly one place: `shared/submit-procedure.md`. Neither the `submit-backlog-task` skill nor the agent may duplicate or restate those steps; both reference the shared file via `${CLAUDE_PLUGIN_ROOT}`. The shared file is execution-neutral — it takes BRIEF + POSITION, inserts at the POSITION it is given, and never decides global ordering, mentions the `DONE`/`FAILED` return protocol, triages, or follows up; those belong to the wrappers.
- `submit-backlog-task` exists as both a user-facing skill and an agent, differing in *where* the shared procedure runs **and** in what surrounds it. The **skill runs it inline** in the user's conversation (so the authoring context survives for follow-up) and must never spawn the agent; the skill additionally owns the triage (dedup + scope) and the position decision, because those need the whole-backlog view that `populate-backlog` does not delegate. The **agent runs it in an isolated subagent context** (taking BRIEF + POSITION from its prompt) and adds the `DONE`/`FAILED` return protocol; it is what `populate-backlog` spawns per brief in bulk. Neither may decide global ordering — the caller owns it.
- The implementation procedure — find task, load environment, implement, verify success criteria, move TODO→DONE — lives in exactly one place: `shared/implement-procedure.md`. Neither the `implement-backlog-task` skill nor the agent may duplicate or restate those steps; both reference the shared file via `${CLAUDE_PLUGIN_ROOT}`. The shared file is execution-neutral — it must not mention the `DONE`/`FAILED` return protocol, committing, or follow-up; those belong to the wrappers.
- `implement-backlog-task` exists as both a user-facing skill and an agent, differing only in *where* the shared procedure runs. The **skill runs it inline** in the user's conversation (so the work context survives for follow-up) and must never spawn the agent. The **agent runs it in an isolated subagent context** and adds the `DONE`/`FAILED` return protocol; it is what the `implement-backlog-tasks` orchestrator spawns per task. Choosing inline vs. isolated is the entire reason both exist — keep that the only difference.
- Both shared procedures (`shared/submit-procedure.md` and `shared/implement-procedure.md`) always resolve `<MILESTONE_DIR>` by following `shared/get-current-milestone.md` (which reads `milestones/README.md`) — they must never use a hardcoded backlog path.
- Task altitude is split, and the dividing line is **what can be re-derived at implementation time**. The shared submit procedure authors only what *cannot* be reconstructed from the goal + live code: the `Description` (intent), the `Success` bar, the optional `Provides` (the forward contract — names/thresholds sibling tasks reference before this task is built), and the optional `Notes` (non-obvious gotchas that would cost the implementer a discovery round). The shared implement procedure owns everything re-derivable — the flow itself and the **detailed implementation design** (exact code, insertion points, assertion wording, decided fresh against the live codebase). The submit procedure must **not** author a step-by-step flow under any heading (no `Steps`); `Provides`/`Notes` are omitted entirely when empty. Keep task bodies minimal to save tokens; never push line-by-line implementation detail — or a re-narration of the flow — back into authored tasks.

## Milestone Workflow

This project uses the milestone-driven workflow. Each milestone lives at
`milestones/milestone_<N>_<slug>/` with `requirements.md`, `TASKS_TODO.md`, and
`TASKS_DONE.md`. `milestones/README.md` is the source of truth for which milestone
is current. Never advance the pointer without first running
`/finish-current-milestone`.

