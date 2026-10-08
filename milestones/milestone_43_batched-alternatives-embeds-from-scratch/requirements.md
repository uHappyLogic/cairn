# Milestone 43: Batched alternatives embeds from scratch files

## Goal

The alternatives pass stops re-typing agent returns and stops spending one orchestrator turn per return. The `provide-alternatives-to-open-question` agent writes its checked `<alternative>` elements to one scratch file outside the repository and ends its session with that file's path as its final message, or `FAILED: <reason>` as before, so a return no longer travels through the orchestrator's context twice. Each time the orchestrator wakes with landed returns, it pipes every landed file into `embed --alternatives` and commits every question that embedded, all in one shell call, keeping one `Alternatives-annotation: <Short Title>` commit per question, the one-repair path (continuation where the host can, one re-dispatch where it cannot) with the repaired return arriving the same way, and the per-question skip. The change is host-neutral: no host slot and no change to the open-question tool, with `CLAUDE.md`, the agent file, the skill, and `docs/` restating the agent's contract as read-only toward the project with that one scratch file as the exception, and the per-return pipeline as a per-wake-up batch.

Out of scope: batching the recommendation pass's embeds, a task-list tool for the completion move, the `complete-task` agent's return contract, the headless chains' model and effort settings in `docs/ways-of-using-cairn.md`, and any change to what the alternatives agent enumerates.

## Relevant starting state

## Decisions

## Out of Scope

