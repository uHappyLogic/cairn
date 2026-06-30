# Milestones

This file tracks milestone progress. It is the source of truth for which milestone is current.

Each milestone lives at `milestones/milestone_<N>_<slug>/` and contains:

- `requirements.md` — goal, relevant starting state, decisions, open questions
- `TASKS_TODO.md` — pending tasks ordered by priority (highest first)
- `TASKS_DONE.md` — completed tasks

## Current Milestone

Current milestone: `milestones/milestone_05_milestone-finish-principle-capture/`

## Milestone History

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
