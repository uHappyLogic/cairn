# Milestone 12: Work-Type-Agnostic Sweep

## Goal

Complete Cairn's transformation into a fully work-type-agnostic workflow by removing every remaining assumption that the work is software engineering — finishing what the Generic Naming Refactor (milestone 3) began. Sweep all behavior files (skills/, agents/, shared/) plus the plugin's own README.md and CLAUDE.md, neutralizing three layers: (1) language — the "You are a Software Engineer" personas, "the code/codebase," "insertion points," "assertions," "exports," and the "tech stack, build/test commands, MCP tools" environment-context wording; (2) the verification mechanism — reframe "build & test / run the verification command" so a task is verified against its Success criteria however the project defines done, deferring to project conventions rather than assuming a build; and (3) examples — replace all software/Unity illustrations (the Creep tower-defense worked example, RailCameraSnapper, "Arc drive technique") with work-type-neutral ones. Stay domain-silent — add no "declare your work type" machinery, since a well-maintained project's CLAUDE.md already supplies domain context. migrate-workspace's references to Cairn's own retired vocabulary stay out of scope (they describe the plugin's history, not the user's work type). Success is proven by a final independent re-audit of the whole plugin returning zero software-engineer-specific findings.

## Relevant starting state

## Decisions

## Out of Scope

