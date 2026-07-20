# Milestone 12: Work-Type-Agnostic Sweep

## Goal

Complete Cairn's transformation into a fully work-type-agnostic workflow by removing every remaining assumption that the work is software engineering — finishing what the Generic Naming Refactor (milestone 3) began. Sweep all behavior files (skills/, agents/, shared/) plus the plugin's own README.md and CLAUDE.md, neutralizing three layers: (1) language — the "You are a Software Engineer" personas, "the code/codebase," "insertion points," "assertions," "exports," and the "tech stack, build/test commands, MCP tools" environment-context wording; (2) the verification mechanism — reframe "build & test / run the verification command" so a task is verified against its Success criteria however the project defines done, deferring to project conventions rather than assuming a build; and (3) examples — replace all software/Unity illustrations (the Creep tower-defense worked example, RailCameraSnapper, "Arc drive technique") with work-type-neutral ones. Stay domain-silent — add no "declare your work type" machinery, since a well-maintained project's CLAUDE.md already supplies domain context. migrate-workspace's references to Cairn's own retired vocabulary stay out of scope (they describe the plugin's history, not the user's work type). Success is proven by a final independent re-audit of the whole plugin returning zero software-engineer-specific findings.

## Relevant starting state

The "project" this milestone changes is the Cairn plugin itself (self-dogfooding): the deliverables are the plugin's own Markdown files under `skills/`, `agents/`, `shared/`, plus root `README.md` and `CLAUDE.md`. There is no build system, no tests, no code — everything is plain Markdown. An audit run at the start of this milestone found software-engineer assumptions in ~16 files across four layers, described below (line references are indicative, not pinned).

### The two shared task cores (deepest SE concentration)

`shared/complete-procedure.md` and `shared/submit-procedure.md` are the single-source-of-truth procedures that drive all task authoring and completion (run inline by the `submit-task`/`complete-task` skills and in isolation by their agents, and by `derive-tasks`). They are the most SE-saturated files: `complete-procedure.md` speaks of "insertion points," "assertion wording," "the live codebase," "source files," "exports," "build/test commands," and "post-edit verification steps"; `submit-procedure.md` frames the deliverable as code ("write the code organically," "read from the code," "the public API"), documents its environment read as "tech stack, MCP tools, build/test commands," and carries a worked Unity tower-defense example (`Creep`, `RegisterWaveStart()`, `AllCreepsDead()`) plus success-criterion models like "Build command exits with code 0" and "Function Z is exported from W." These two files also encode the **verification mechanism** the goal wants reframed — "run the verification command / build & test" — not just vocabulary.

### Agent personas

`agents/submit-task.md` and `agents/complete-task.md` each open with "You are a **Software Engineer** …" (the two cases the user originally spotted). These are one-line persona statements, the shallowest layer.

### "The code / the codebase" framing skills

Several skills treat the deliverable as code and the project as a codebase throughout: `skills/ask-in-milestone-context/SKILL.md` (grounds finished-work answers in "the code those tasks shipped," "the truth is in the code," "live source"), `skills/specify-milestone-starting-state/SKILL.md` (this very skill — "Analyze the current codebase," "meaningful code," "exported functions/classes/types/interfaces," "schemas, database models"), and `skills/derive-tasks/SKILL.md` ("technology boundary or layer … backend API / frontend component / DB schema; or for Unity: scripts / prefabs / scene hierarchy," "existing code," "module, schema, or shared utility"). `agents/recommend-open-question.md`, `shared/recommend-procedure.md`, `skills/discuss-open-question/SKILL.md`, `skills/discuss-new-task/SKILL.md`, and `skills/recommend-all-open-questions/SKILL.md` carry lighter "live code / source files / bug / during development / build X" phrasing.

### Environment-context reading pattern

A recurring instruction to read the project's environment from `CLAUDE.md` as "**tech stack, build/test commands, MCP tools, conventions**" appears in `shared/complete-procedure.md`, `shared/submit-procedure.md`, `skills/derive-tasks/SKILL.md`, `skills/specify-milestone-starting-state/SKILL.md`, `skills/init-milestone-base-workflow/SKILL.md`, `skills/discuss-milestone-goal/SKILL.md`, and `skills/finish-current-milestone/SKILL.md` (the last also updates `CLAUDE.md` only for "tech-stack or structural changes," referencing `## Tech Stack` / `## Repository Layout` and "game/codebase"). A `CLAUDE.md` invariant documents this pattern explicitly as the environment-context contract those readers follow.

### Work-type-specific examples

Beyond the `submit-procedure.md` Unity example, illustrative content assumes software/game work in `skills/answer-open-question/SKILL.md` and `skills/discuss-open-question/SKILL.md` (Cinemachine virtual cameras, `RailCameraSnapper`, `ForceCameraPosition`; recurring example question titles "Arc drive technique" and "Player input during swing") and `skills/review-milestone-requirements/SKILL.md` (same game-mechanics example titles). The goal is to replace all such examples with work-type-neutral ones.

### The plugin's own docs

`README.md` (the public, adoption-focused landing page) and `CLAUDE.md` (the invariants Claude itself acts on) both carry SE framing — `CLAUDE.md`'s invariants restate the "tech stack, build/test commands, MCP tools" environment contract and describe skills in code terms; `README.md` pitches the workflow and diagrams to adopters. Both are in scope this milestone. `CLAUDE.md` also carries the full invariant set that any language/mechanism change here must be reconciled against.

### Prior art and the out-of-scope boundary

Milestone 3 ("Generic Naming Refactor") already retired coding-flavored *vocabulary* (implement→complete, backlog drop, heading renames) in a clean break — this milestone finishes the job it started, extending to personas, the verification mechanism, examples, and the docs. `skills/migrate-workspace/SKILL.md` references "implementation state/decisions" and the plugin's own past "refactors," but those describe Cairn's *own* retired artifact vocabulary (migration history), not an assumption about the user's work type, and are out of scope by the goal's explicit exclusion.

## Decisions

## Out of Scope

## Open questions

<open-question id="Replacement example strategy" status="open">
  <question>Which replacement strategy should the neutralized examples use: one canonical work-type-neutral worked example reused consistently across all files (replacing the Creep tower-defense example, RailCameraSnapper, and the recurring Arc-drive/swing question titles), a varied set of examples drawn from different non-software domains, or fully abstract placeholders — and may a rewritten example name a concrete domain (e.g. cooking, event planning) at all, or does that conflict with the goal&apos;s domain-silent stance?</question>
</open-question>

<open-question id="SE-assumption audit boundary" status="open">
  <question>What counts as a software-engineer-specific finding for the sweep and the final re-audit — in particular, are Cairn&apos;s own operating mechanics (git commits and git-log greps, path-scoped staging, the CLAUDE.md and README.md file names, the consuming project being a git repository) exempt plugin infrastructure or findings to neutralize? Without a decided boundary the &quot;zero findings&quot; success bar is unmeasurable.</question>
</open-question>

<open-question id="Environment-context replacement wording" status="open">
  <question>What neutral formula replaces the recurring &quot;tech stack, build/test commands, MCP tools, conventions&quot; environment-context phrase across its seven reader files and the corresponding CLAUDE.md invariant — i.e. what is a work-type-agnostic project&apos;s CLAUDE.md expected to supply (domain context, working conventions, how done is verified?), and does the &quot;run /init once at project setup&quot; pointer survive for non-software projects?</question>
</open-question>

<open-question id="Verification fallback without conventions" status="deferred">
  <question>When a consuming project&apos;s CLAUDE.md defines no done-verification convention, what should the reframed completion procedure fall back to — direct inspection of the deliverable against the task&apos;s Success criteria, or something stronger?</question>
</open-question>

<open-question id="Re-audit execution form" status="deferred">
  <question>How is the final independent re-audit executed so it is genuinely independent of the sweep (e.g. a fresh-context agent auditing the whole plugin against the decided finding criteria), and in what form does it report its findings?</question>
</open-question>
