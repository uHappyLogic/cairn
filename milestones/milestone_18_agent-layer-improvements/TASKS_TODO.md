# TASKS TODO

## Agent Stages Own Change Set Before Return

Change the two file-editing agents so each path-scoped `git add`s its own change set and returns only `DONE` or `FAILED: <reason>` with no hand-back payload: `agents/complete-task.md` stages the paths recorded while carrying out the task plus `<MILESTONE_DIR>/TASKS_TODO.md` and `<MILESTONE_DIR>/TASKS_DONE.md` (dropping its path hand-back section), and `agents/answer-open-question-with-recommendation.md` stages `<MILESTONE_DIR>/requirements.md` (dropping its lifted-recommendation hand-back), while `skills/complete-all-tasks/SKILL.md` and `skills/answer-all-open-questions-with-recommendation/SKILL.md` commit the already-staged index under their existing subjects, the answer orchestrator lifting the `<recommendation>` text for its commit body from the block during its pre-dispatch re-check rather than from the agent, and the `CLAUDE.md` invariants describing the hand-back are updated to the stage-then-return arrangement, with `shared/commit-procedure.md` and `shared/complete-procedure.md` left execution-neutral. Staging is not committing, so the agents-never-commit rule holds. Verified when neither agent file mentions handing back paths or recommendation text, both orchestrators commit without a hand-back input, and the regenerated `.agents/plugins/cairn/` tree is byte-identical to the source.

---

## Fold Decision Before Removing Question Block

Reorder the recording core in `shared/answer-procedure.md` so the decision is folded into `## Decisions` (currently step 5) before the matched `<open-question>` block is removed (currently step 4), keeping the cascade step last and the three edits separate, and update the step references in `shared/answer-with-recommendation-procedure.md` and the `CLAUDE.md` invariant that narrate the locate → remove → fold → cascade order. Today a failure or interruption between the removal and the fold leaves the block gone and the decision unrecorded, so the next sweep no longer gathers the question and it is silently lost; folding first leaves a harmless superset state instead. Verified by reading the procedure to confirm the fold precedes the removal, confirming no runtime or invariant text still states remove-then-fold, and regenerating the Antigravity tree with `uv run scripts/migrate_skills_to_agy.py` so `.agents/plugins/cairn/` stays byte-identical to the source.

---
