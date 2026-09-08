# Milestone 20: Recommend Agent Return Robustness

## Goal

Make the `recommend-all-open-questions` sweep robust to a `recommend-open-question` agent return that wraps otherwise well-formed XML sub-elements in surrounding text, so that no valid recommendation is ever dropped: the orchestrator first extracts the sub-element region (first `<alternative` through last `</recommendation>`) from the raw return and runs the existing shape check on that, and when extraction fails it continues the *same* agent session once with a corrective re-emit prompt (never a fresh re-dispatch, which would redo the analysis), falling back to today's skip-with-advisory only when the repair attempt also fails. Rewrite the agent's return contract from the ground up — replacing the accumulated prohibition list with a draft → self-check against the two shape tests → emit final step — and apply the same extraction/repair pattern to another dispatched agent only where it duplicates this exact failure, never as a general audit. Claude Code is the target host and the Antigravity build degrades gracefully where session continuation is unavailable; this deliberately reverses the "discarded whole, never salvaged" invariant.

## Relevant starting state

## Decisions

## Out of Scope

