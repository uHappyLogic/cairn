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

## Make Recommend Procedure Principle-Aware

Upgrade the execution-neutral analytical core `shared/recommend-procedure.md` so the shared recommendation logic consults the project-wide answering principles, per the milestone's "Recommendation machinery" decision. Both wrappers — the `discuss-open-question` skill (inline) and the read-only `recommend-open-question` agent — inherit this through the shared core, so the store read must live here once and never be duplicated into the wrappers.

**Provides:**
- `shared/recommend-procedure.md`'s grounding step reads the fixed project-wide principle store `milestones/answer_decision_principles.md` directly and in place (naming that path itself, not taking principles as a caller-supplied input alongside QUESTION) as part of grounding.
- The core states, in execution-neutral prose, the requirement that any confirmed principle which influenced the recommended pick be cited — the logical contract the `recommend-open-question` agent renders as its `> **Applied principle:**` line in a separate downstream task.

**Notes:**
- A bearing confirmed principle is a **weighted advisory factor**, not a binding filter: it is a strong default in favor of its supported option, but merit MAY override it — only for a specific stated reason that must be named in the recommendation. It must never veto a candidate outright.
- When no confirmed principle bears on the question, recommendations are produced exactly as today — the existing alternatives/recommendation contract is otherwise unchanged.
- Keep the file execution-neutral: state the citation requirement logically only. Own **no** `>`-blockquote markup and do **not** specify the `> **Applied principle:**` line rendering — that belongs to the `recommend-open-question` agent (a separate task). Do not duplicate the store read into either wrapper.
- The store is a fixed milestone-independent path above any milestone, so reading it in place preserves the only caller-owned path-freedom that matters (`<MILESTONE_DIR>` resolution), which is unaffected.

**Success:**
- `shared/recommend-procedure.md`'s grounding step names and reads `milestones/answer_decision_principles.md`.
- The procedure describes a bearing principle as a weighted advisory default (strong default with merit-override only for a named reason), requires citing any principle that influenced the pick, and states that behavior is unchanged from today when no principle bears.
- The file contains no `>`-blockquote markup and does not restate the agent's `> **Applied principle:**` line rendering.
- The alternatives (2–4, what-it-is / advantage / drawback) and single-recommendation-with-tie-break contract is otherwise unchanged, and the store read appears only in this file (not duplicated into the two wrappers).

---

