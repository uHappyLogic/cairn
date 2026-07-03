# TASKS DONE

## Delete The Auto-Answer-By-Principle Sweep Files

Remove the autonomous auto-answer-by-principle sweep now that Milestone 8 reframes the answering principles as a recommendation advisor rather than an auto-answer engine. Delete both the orchestrator skill and its read-only candidate-elimination subagent so no auto-answer path remains in the plugin.

**Notes:**
- This is a pure two-file deletion. The dead cross-references these files leave behind in other files (the skill roster, the recommend sweep's "argument-free twin" anchors, the retired `Principle-based-answer:`/`Answer-Principle:` provenance vocabulary, capture's exclusion grep, the revert-then-re-answer wording, and the CLAUDE.md/README.md/principle-store docs) are cleaned up by separate downstream tasks — do not touch them here.
- Delete the whole `skills/try-answer-all-questions-by-principle/` directory, not just its `SKILL.md`.

**Success:**
- The directory `skills/try-answer-all-questions-by-principle/` no longer exists.
- The file `agents/try-answer-question-by-principle.md` no longer exists.
- No other file in the plugin is modified by this task (`git status` shows only the two deletions).

---

