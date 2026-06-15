# Milestones

This file tracks milestone progress. It is the source of truth for which milestone is current.

Each milestone lives at `milestones/milestone_<N>_<slug>/` and contains:

- `requirements.md` — goal, relevant implementation state, implementation decisions, open questions
- `TASKS_TODO.md` — pending tasks ordered by priority (highest first)
- `TASKS_DONE.md` — completed tasks

## Current Milestone

Current milestone: `milestones/milestone_02_answer-principle-learning/`

## Milestone History

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
