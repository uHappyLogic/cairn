# Milestones

This file tracks milestone progress. It is the source of truth for which milestone is current.

Each milestone lives at `milestones/milestone_<N>_<slug>/` and contains:

- `requirements.md` — goal, relevant starting state, decisions, open questions
- `TASKS_TODO.md` — pending tasks ordered by priority (highest first)
- `TASKS_DONE.md` — completed tasks

## Current Milestone

Current milestone: `milestones/milestone_07_answer-all-with-recommendation/`

## Milestone History

### Milestone 6 — Recommend Open Questions

- Added the `recommend-all-open-questions` orchestrator skill: a non-interactive, argument-free batch path that sweeps the current milestone's open/deferred questions and embeds an alternatives+recommendation sub-block beneath each unchanged one-line question header.
- Added its read-only `recommend-open-question` subagent — the non-interactive twin of `discuss-open-question` — dispatched once per question, which grounds in the live project and returns the recommendation sub-block for the orchestrator to embed (mutating nothing itself).
- Extracted the "alternatives + recommendation for one question" analytical core into the new execution-neutral `shared/recommend-procedure.md`, now referenced (never restated) by both `discuss-open-question` and the `recommend-open-question` agent.
- Made the recommend sweep mutate-but-do-not-commit (path-scoped `git add`, no clean-tree precondition) and idempotent — it skips any block already carrying a `> **Recommendation:**` anchor, with a delete-the-sub-block-and-re-run escape hatch instead of a refresh mode.
- Gave `answer-open-question` a record-recommendation mode: the reserved sentinel answer text `record the recommendation` (exact whole-string match) lifts a block's embedded recommendation as the answer, and stops without changes when no recommendation is present.
- Generalized `shared/answer-procedure.md`'s block-removal step to clear the entire contiguous blockquote run (header plus any embedded recommendation), with the bare one-line header as the degenerate case.
- Synced `README.md` and `CLAUDE.md` to the new recommend-sweep path (skill reference, requirements-loop diagram, layout, pipeline block, and invariants).

### Milestone 5 — Milestone-finish Principle Capture

- Moved answering-principle capture off the per-answer path to an optional, recommended end-of-milestone step.
- `/answer-open-question` now commits its own `requirements.md` edit (path-scoped `git add`, subject `Manual-answer: <Short Title>`, rationale in the body, no `Answer-Principle:` trailer) instead of leaving it staged and chaining to capture — a deliberate, documented exception to the "individual skills never commit" invariant.
- Added the new finish-time skill `capture-milestone-principle-updates` (authored via `/skill-creator:skill-creator`) that distills principles from a milestone's `Manual-answer:` commits into the principle store via a two-phase flow (internal cross-candidate dedup, then strongest-first per-candidate revise-vs-add against the live store); it is now the sole writer of `milestones/answer_decision_principles.md`.
- Made `/finish-current-milestone` recommend (never auto-run) `/capture-milestone-principle-updates` in its step 8, ordered before `/define-milestone-goal`.
- Retired the `try-capture-answer-principle` skill (on-demand per-answer capture) and the `reject-auto-answer` skill (its correction role replaced by the uniform "revert the auto-answer commit, then `/answer-open-question` to re-answer, principle reconciled at finish" flow), scrubbing every live cross-reference.
- Synced `CLAUDE.md` and `README.md` (including the per-phase Mermaid diagrams and the answer-principle-learning-loop prose) to the new capture model.

### Milestone 4 — README Pipeline Diagrams

- Replaced the single oversized Workflow pipeline Mermaid diagram in `README.md` with six smaller per-phase `flowchart TD` diagrams (setup, milestone init, requirements loop, automated derivation/completion, follow-up, ending), each in its own `###` subsection with short flow prose.
- Chained the per-phase diagrams via the shared parallelogram state seam nodes `D0`–`D5`, each internal seam node appearing in its two adjacent diagrams, with the cross-phase "next milestone" loop hosted on the receiving *Initializing a milestone* diagram.
- Trimmed every skill node to its bare skill name (no inline descriptions or `(optional)`/`(auto)` qualifiers), keeping the `## Skill reference` section as the single home for full descriptions.
- Retained per-diagram phase-colour styling for cross-diagram identity, kept the amber `state` styling and parallelogram shape on the seam nodes, flattened the former hexagon nodes to plain boxes, and dropped the stale `linkStyle` line tied to the old monolith's edge indices.
- Fixed the stale `## Self-dogfooding` reference from `milestone_01_public-release-prep` to the current `milestone_04_readme-pipeline-diagrams` — the milestone's single mandated polish edit.

### Milestone 3 — Generic Naming Refactor

- Retired coding-flavored vocabulary across the whole plugin so Cairn reads as a generic idea-to-done workflow, in a clean break with no aliases.
- Renamed the task-execution machinery from "implement" to "complete": `complete-all-tasks` (orchestrator), `complete-task` (skill + agent), and `shared/complete-procedure.md`, with the dispatch type-string updated to match.
- Dropped the redundant "backlog" noun: `submit-backlog-task` → `submit-task` (skill + agent), `discuss-new-backlog-task` → `discuss-new-task`, and renamed `populate-backlog` → `derive-tasks` to name that tasks derive from the requirements.
- Applied the fan-out naming grammar `<verb>-all-<plural-object>`, renaming the answer sweep `try-answer-questions-by-principle` → `try-answer-all-questions-by-principle` while keeping its read-only subagent singular.
- Renamed the `requirements.md` template headings `## Relevant implementation state` → `## Relevant starting state` (and its writer skill to `specify-milestone-starting-state`) and `## Implementation decisions` → `## Decisions`, updating every reader and writer.
- Swept residual generic "implementation"/"implement" prose out of the authoring, clarification, and open-questions skills, and re-synced `README.md` and `CLAUDE.md` with the new vocabulary.
- Added the manually-run `migrate-workspace` skill that upgrades an existing consuming workspace's `milestones/` artifacts to current conventions, with an extension point for future migrations.

### Milestone 2 — Answer Principle Learning Loop

- Added the project-wide answering-principle store `milestones/answer_decision_principles.md` (at the `milestones/` root, shared across all milestones) as the accumulating basis for autonomous question resolution.
- Extracted the answer-recording core into `shared/answer-procedure.md`, now the single source of truth referenced (never restated) by both `answer-open-question` and the sweep orchestrator.
- Added the `try-capture-answer-principle` skill, which extracts and user-confirms reusable answering principles after each manual answer and is the sole writer of the principle store.
- Renamed `answer-obvious-open-questions` → `try-answer-questions-by-principle`: an orchestrator that resolves open questions by candidate elimination against confirmed principles, committing one auto-answer per commit with the applied principle named in an `Answer-Principle:` trailer.
- Added the read-only `try-answer-question-by-principle` subagent that performs per-question candidate elimination and returns a structured verdict, leaving all document mutation and committing to the orchestrator.
- Added the `reject-auto-answer` skill to revert a bad auto-answer commit, reopen its question, and direct the user to re-capture the offending principle.
- Synced `README.md` (Mermaid workflow + per-skill reference) and `CLAUDE.md` (layout, skills overview, invariants) with the new principle-learning loop.

### Milestone 1 — Public Release Preparation

- Renamed the plugin from `workflow` to **Cairn** across the manifest and `CLAUDE.md`, with the tagline "Mark the path from idea to shipped."
- Moved the current-milestone pointer out of `CLAUDE.md` into a single grep-able `Current milestone:` line in `milestones/README.md`, now the sole source of truth.
- Added `shared/get-current-milestone.md` as the one shared snippet all readers use to resolve `<MILESTONE_DIR>`, and migrated every reader and writer skill/agent onto it.
- Adopted zero-padded two-digit milestone numbering (`milestone_01_…`) with the next number derived by scanning `milestones/`.
- Added an MIT `LICENSE` and `.claude-plugin/marketplace.json`, making the repo installable via `/plugin marketplace add uHappyLogic/cairn`.
- Rewrote `README.md` as a public, adoption-focused landing page with a Mermaid workflow flowchart and a banner image concept.

## Completed Milestones

| # | Title | Path |
|---|-------|------|
| 1 | Public Release Preparation | `milestones/milestone_01_public-release-prep/` |
| 2 | Answer Principle Learning Loop | `milestones/milestone_02_answer-principle-learning/` |
| 3 | Generic Naming Refactor | `milestones/milestone_03_generic-naming-refactor/` |
| 4 | README Pipeline Diagrams | `milestones/milestone_04_readme-pipeline-diagrams/` |
| 5 | Milestone-finish Principle Capture | `milestones/milestone_05_milestone-finish-principle-capture/` |
| 6 | Recommend Open Questions | `milestones/milestone_06_recommend-open-questions/` |
