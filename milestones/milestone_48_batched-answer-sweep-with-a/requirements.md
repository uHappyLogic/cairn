# Milestone 48: Batched answer sweep with a fold tool

## Goal

Make the inline answer sweep (`answer-all-open-questions-with-recommendation`) record a whole run in one fixed batched shell call, shown in full and run as shown: for each walked question in `walk` order it lifts the pick, folds the decision under its `## Decisions` subsection through a new shell-callable fold command for `requirements.md`, removes the block with its option, and commits one `Recommendation-answer:` commit with the lifted line as body, skipping a failed lift silently and stopping on the first failure after a fold with the tree resumable. The sweep's setup collapses to its fixed-call floor, reading `requirements.md` whole and a compact view of the question document (id, question text, lifted pick) instead of the whole XML, dropping the per-answer `locate`, and retiring the `=====` separator that fails in zsh. The fold command is used by the sweep only and is not the sole writer of `## Decisions`; the three single-question answer skills keep their Edit-based fold; the rewritten sweep is hands-on checked in Claude Code only, with the Antigravity and Codex trees rendered and reviewed.

## Relevant starting state

## Decisions

## Out of Scope

