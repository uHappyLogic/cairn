# TASKS TODO

## Fold Decision Before Removing Question Block

Reorder the recording core in `shared/answer-procedure.md` so the decision is folded into `## Decisions` (currently step 5) before the matched `<open-question>` block is removed (currently step 4), keeping the cascade step last and the three edits separate, and update the step references in `shared/answer-with-recommendation-procedure.md` and the `CLAUDE.md` invariant that narrate the locate → remove → fold → cascade order. Today a failure or interruption between the removal and the fold leaves the block gone and the decision unrecorded, so the next sweep no longer gathers the question and it is silently lost; folding first leaves a harmless superset state instead. Verified by reading the procedure to confirm the fold precedes the removal, confirming no runtime or invariant text still states remove-then-fold, and regenerating the Antigravity tree with `uv run scripts/migrate_skills_to_agy.py` so `.agents/plugins/cairn/` stays byte-identical to the source.

---
