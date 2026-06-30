# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Claude Code plugin (`cairn`) that provides a milestone-driven development workflow. It ships as a set of skills and a couple of agents that move a project from a vague idea through discussion, planning, completion, and archival — one milestone at a time.

## Repository layout

```
.claude-plugin/plugin.json   — plugin manifest (name, version, author)
.claude-plugin/marketplace.json — single-plugin marketplace manifest (installable via /plugin marketplace add uHappyLogic/cairn)
skills/<skill-name>/SKILL.md — one skill per directory; the SKILL.md is the full skill definition
agents/complete-task.md — task-completion subagent invoked by complete-all-tasks skill
agents/submit-task.md — task-authoring subagent invoked by derive-tasks (bulk)
agents/try-answer-question-by-principle.md — read-only candidate-elimination subagent invoked by the try-answer-all-questions-by-principle orchestrator; returns a verdict only, never edits documents
shared/complete-procedure.md — single source of truth for the complete-one-task procedure, followed inline by the complete-task skill and in isolation by the complete-task agent
shared/submit-procedure.md — single source of truth for the author-and-insert-one-task procedure, followed inline by the submit-task skill and in isolation by the submit-task agent
shared/answer-procedure.md — single source of truth for recording an answer (locate question block by Short Title → fold decision into ## Decisions → cascade), referenced by answer-open-question and the try-answer-all-questions-by-principle orchestrator
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
specify-milestone-starting-state ← fills "Relevant starting state" in requirements.md
review-milestone-requirements   ← repeatable loop engine: each pass reconciles existing questions against recorded decisions, surfaces new gaps, reports convergence; run repeatedly
try-answer-all-questions-by-principle ← orchestrator: sweeps open/deferred questions, auto-answers only those a confirmed principle resolves, one commit per answer; run after a review pass
try-answer-question-by-principle ← (agent, in agents/) read-only candidate-elimination subagent: returns a verdict (unique survivor + cited principles), never edits documents
discuss-open-question           ← structured conversation about one open question; on a decision offers answer-open-question, and if the goal itself must shift also offers modify-milestone-goal — when both apply, modify-milestone-goal runs first so the answer records against the revised goal
answer-open-question            ← records the decision in requirements.md, then chains to try-capture-answer-principle
modify-milestone-goal           ← revises the ## Goal of an already-defined milestone (act-only); edits Goal only, surfaces downstream impact, never cascades; offered by discuss-open-question, invisible to answer-open-question
try-capture-answer-principle    ← records/revises a confirmed answering principle (user-confirmed); chained from answer-open-question
reject-auto-answer              ← reverts one bad auto-answer commit and reopens its question; revert left staged
derive-tasks                    ← decomposes requirements.md into ordered briefs, proves coverage, spawns submit-task agent per brief
submit-task                     ← (skill) user-facing entry for a single ad-hoc issue: triages + positions, then runs shared/submit-procedure.md inline so the authoring context stays for follow-up
submit-task                     ← (agent, in agents/) bulk per-task authoring for derive-tasks: runs shared/submit-procedure.md in isolation, returns DONE/FAILED
discuss-new-task                ← clarifies a vague/large issue into briefs, then hands off to the submit-task skill
complete-all-tasks              ← orchestrator: spawns complete-task agent per task, commits after each
complete-task                   ← (skill) user-facing entry for one ad-hoc task: runs shared/complete-procedure.md inline so the work context stays for follow-up
complete-task                   ← (agent, in agents/) single-task completion subagent: runs shared/complete-procedure.md in isolation, returns DONE/FAILED
ask-in-milestone-context        ← (on-demand, read-only) answers a free-form informational question grounded in the current milestone — goal, decisions, done/pending tasks, and the live code those tasks produced; never edits, offers a handoff when a concrete next action surfaces
finish-current-milestone        ← writes completion summary to milestones/README.md, clears current-milestone pointer to "none" in milestones/README.md, updates CLAUDE.md only for lasting changes
goto-next-milestone             ← activates an already-defined milestone: scans milestones/ for a defined-but-not-yet-active directory, updates milestones/README.md to point to it
```

## Milestone file structure

Each active milestone lives at `milestones/milestone_<N>_<slug>/` and contains exactly:

- `requirements.md` — Goal, Relevant starting state, decisions, open questions
- `TASKS_TODO.md` — pending tasks ordered by priority (highest first), `##` headings + `---` separators
- `TASKS_DONE.md` — completed tasks appended in the same format

`milestones/README.md` is the source of truth for which milestone is current.

## Invariants to preserve when editing skills

- `init-milestone-base-workflow` is the one-time bootstrap; it is additive and idempotent — it never overwrites an existing `milestones/README.md` or `CLAUDE.md`, only creating missing files and appending missing sections. It must leave `milestones/README.md` with a `Current milestone:` pointer line.
- `answer-open-question` splits its arg on the first `.` — title before, answer after.
- `review-milestone-requirements` (renamed from the old `highlight-milestone-requirements-open-questions`) is the repeatable engine of the requirements-iteration loop: each pass **reconciles** the existing `Open question`/`Deferred` blocks against the recorded `## Decisions`, **surfaces** new gaps, and **reports convergence** (no `> **Open question` blocks remaining is exactly `derive-tasks`'s precondition; Deferred blocks may carry forward). It is the **only** skill besides the answer path that may remove a question block, and only as *cleanup of already-recorded state*: it may delete a block solely when it can cite a `## Decisions` entry that already covers it, or dedup an exact repeat — when in doubt it flags ("possibly resolved — confirm") rather than deletes, and every removal is reported. It **never records a decision or answers a question**: folding a decision into `## Decisions` and cascading to mooted siblings stays scoped to `shared/answer-procedure.md` (used by `answer-open-question` and the sweep). This boundary — tidy the questions section vs. record an answer — is the whole reason the two stay separate.
- `try-answer-all-questions-by-principle` (renamed from the old `answer-obvious` sweep) is the autonomous sweep run after a `review-milestone-requirements` pass: it processes Open/Deferred entries **sequentially against the live document** (so cascades apply) and auto-answers a question **only** when a confirmed principle from `milestones/answer_decision_principles.md` resolves it — questions no principle covers are left untouched. The answer-recording mechanism (locate the question block by Short Title → fold the decision into `## Decisions` as clean prose → cascade to mooted entries) lives in exactly one place: `shared/answer-procedure.md`. Both `answer-open-question` and this orchestrator reference it via `${CLAUDE_PLUGIN_ROOT}` and never restate the steps — superseding the prior state where the steps were duplicated in prose between the two. That shared file is **execution-neutral** — it takes a resolved Short Title + answer and never mentions arg-parsing, committing, the `Answer-Principle:` trailer, or the capture chain.
- The `try-answer-all-questions-by-principle` orchestrator owns **all** document mutation and the commit; its `try-answer-question-by-principle` subagent (one dispatch per question) is **read-only on `requirements.md` and the principle store** and returns a verdict only (unique-survivor yes/no, the answer, the cited load-bearing principles, the candidate set considered). The subagent does the candidate elimination; the orchestrator records and commits. This is a deliberate divergence from the file-editing `complete-task` agent — cascades plus one-commit-per-answer require all mutation serialized in the single sequential orchestrator, while the context-heavy elimination is what's worth isolating.
- `answer-open-question` unconditionally chains to `try-capture-answer-principle` after recording a decision (capture analyses the conversation, not a payload, and engages the user only on a real generalizable principle). The `try-answer-all-questions-by-principle` orchestrator **never** chains to capture — the auto-answer was itself derived from a confirmed principle, so capturing would be circular.
- `modify-milestone-goal` is the **only** skill that mutates the `## Goal` of an already-defined milestone (`define-milestone-goal` writes it once at creation; `discuss-milestone-goal` is conversational and pre-creation). It is **act-only**: it edits the `## Goal` section and nothing else — never `## Decisions`, the question blocks, `## Out of Scope`, or the task lists. Because the Goal is the root of the requirements tree, the skill **surfaces but never cascades** the downstream impact (which Decisions/questions/Out-of-Scope/derived tasks the new goal may invalidate) and points the user at `/review-milestone-requirements` to reconcile — folding those consequences in silently would have too large a blast radius. It is offered by `discuss-open-question` (which still edits nothing itself — it proposes the revised goal and the user confirms) and is **deliberately invisible to `answer-open-question`**: recording an answer and reshaping the objective are different acts, and the autonomous answer/principle path must never reach goal mutation. It **never** chains to `try-capture-answer-principle` (a goal change yields no answering principle) and does not commit.
- `reject-auto-answer` reverts exactly one auto-answer commit (`git revert --no-commit`) and leaves the revert **staged** (per the no-commit invariant). It validates the target first — the commit must touch **only `requirements.md`** and carry **≥1 `Answer-Principle:` trailer** — and refuses otherwise; the revert simultaneously restores the question block and removes the folded decision, so the revert *is* the reopen. It **never edits the principle store** — it surfaces the cited principle(s) and directs the user to re-capture to close the loop.
- The `complete-task` agent expects tasks as `##` sections in `TASKS_TODO.md`, each terminated by a `---` separator.
- Two orchestrators commit; individual skills never commit — including the `complete-task` skill, which leaves an ad-hoc task's changes staged for the user. `complete-all-tasks` commits after each successful task. `try-answer-all-questions-by-principle` commits exactly **one auto-answer per commit** — subject `Principle-based-answer: <Short Title>` (the answered question's handle), with one repeated `Answer-Principle: <Short Title>` trailer line per load-bearing principle.
- `finish-current-milestone` must always run before `goto-next-milestone` — it records the completion and clears the current-milestone pointer to "none". `goto-next-milestone` checks for this "none" state and refuses to run without it.
- Open questions in `requirements.md` must be fully resolved before `derive-tasks` can run.
- `ask-in-milestone-context` is the on-demand, **read-only** Q&A skill: it answers an informational question about the current milestone and never mutates any file. It is not a pipeline step — it is usable any time across requirements/automation/follow-up. It grounds answers about finished work in the **live code** (with the `TASKS_DONE.md` entry as intent and `git log`/`git show "<task heading>"` as a supporting lens — the task→commit mapping is best-effort, since ad-hoc `complete-task` runs leave changes staged/uncommitted). When a concrete next action surfaces it **offers** the owning skill (`discuss-open-question` to decide a question, `submit-task`/`discuss-new-task` to file an issue, `discuss-milestone-goal` to reshape the goal, `complete-task` to do a pending task) but performs none of their work itself — the asking/acting split is the whole point.
- `specify-milestone-starting-state`, `derive-tasks`, and the shared completion procedure (run by both the `complete-task` skill and agent) read the project's environment context (tech stack, build/test commands, MCP tools, conventions) from `CLAUDE.md`. Run `/init` once at project setup so `CLAUDE.md` documents it.
- `derive-tasks` owns decomposition and coverage only; it must not author task bodies itself. It proves every requirement maps to a brief (traceability matrix), then submits briefs **in dependency order** to the `submit-task` agent with `POSITION: append`, spawning the agents **sequentially** (they all mutate the same `TASKS_TODO.md`).
- The task body template (`##` title, description, optional **Provides**, optional **Notes**, **Success**, trailing `---`) lives in exactly one place: `shared/submit-procedure.md`. The `submit-task` skill, the `submit-task` agent, and `derive-tasks` must not duplicate it. There is deliberately **no** `Steps` section — see the altitude invariant below.
- The author-and-insert procedure — find milestone, load context, author the task (template + authoring guidelines), insert at the given POSITION — lives in exactly one place: `shared/submit-procedure.md`. Neither the `submit-task` skill nor the agent may duplicate or restate those steps; both reference the shared file via `${CLAUDE_PLUGIN_ROOT}`. The shared file is execution-neutral — it takes BRIEF + POSITION, inserts at the POSITION it is given, and never decides global ordering, mentions the `DONE`/`FAILED` return protocol, triages, or follows up; those belong to the wrappers.
- `submit-task` exists as both a user-facing skill and an agent, differing in *where* the shared procedure runs **and** in what surrounds it. The **skill runs it inline** in the user's conversation (so the authoring context survives for follow-up) and must never spawn the agent; the skill additionally owns the triage (dedup + scope) and the position decision, because those need the whole-task-list view that `derive-tasks` does not delegate. The **agent runs it in an isolated subagent context** (taking BRIEF + POSITION from its prompt) and adds the `DONE`/`FAILED` return protocol; it is what `derive-tasks` spawns per brief in bulk. Neither may decide global ordering — the caller owns it.
- The completion procedure — find task, load environment, carry out, verify success criteria, move TODO→DONE — lives in exactly one place: `shared/complete-procedure.md`. Neither the `complete-task` skill nor the agent may duplicate or restate those steps; both reference the shared file via `${CLAUDE_PLUGIN_ROOT}`. The shared file is execution-neutral — it must not mention the `DONE`/`FAILED` return protocol, committing, or follow-up; those belong to the wrappers.
- `complete-task` exists as both a user-facing skill and an agent, differing only in *where* the shared procedure runs. The **skill runs it inline** in the user's conversation (so the work context survives for follow-up) and must never spawn the agent. The **agent runs it in an isolated subagent context** and adds the `DONE`/`FAILED` return protocol; it is what the `complete-all-tasks` orchestrator spawns per task. Choosing inline vs. isolated is the entire reason both exist — keep that the only difference.
- Both shared procedures (`shared/submit-procedure.md` and `shared/complete-procedure.md`) always resolve `<MILESTONE_DIR>` by following `shared/get-current-milestone.md` (which reads `milestones/README.md`) — they must never use a hardcoded task-list path.
- Task altitude is split, and the dividing line is **what can be re-derived at completion time**. The shared submit procedure authors only what *cannot* be reconstructed from the goal + live code: the `Description` (intent), the `Success` bar, the optional `Provides` (the forward contract — names/thresholds sibling tasks reference before this task is built), and the optional `Notes` (non-obvious gotchas that would cost the completer a discovery round). The shared completion procedure owns everything re-derivable — the flow itself and the **detailed design** (exact code, insertion points, assertion wording, decided fresh against the live codebase). The submit procedure must **not** author a step-by-step flow under any heading (no `Steps`); `Provides`/`Notes` are omitted entirely when empty. Keep task bodies minimal to save tokens; never push line-by-line build detail — or a re-narration of the flow — back into authored tasks.

## Milestone Workflow

This project uses the milestone-driven workflow. Each milestone lives at
`milestones/milestone_<N>_<slug>/` with `requirements.md`, `TASKS_TODO.md`, and
`TASKS_DONE.md`. `milestones/README.md` is the source of truth for which milestone
is current. Never advance the pointer without first running
`/finish-current-milestone`.

