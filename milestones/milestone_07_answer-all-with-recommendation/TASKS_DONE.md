# TASKS DONE

## Add Lift-then-Delegate Shared Procedure

Create the new execution-neutral shared procedure `shared/answer-with-recommendation-procedure.md` — the single source of truth for the "lift a question's embedded recommendation, then delegate to the recording core" logic. It composes over `shared/answer-procedure.md` and will be referenced by both the forthcoming `answer-open-question-with-recommendation` skill and its agent, exactly as `complete-task`/`submit-task` layer their shared procedures. This is the "Lift-procedure placement" decision in `requirements.md`.

**Provides:**
- New file `shared/answer-with-recommendation-procedure.md`: an execution-neutral shared procedure that takes a resolved SHORT TITLE, resolves `<MILESTONE_DIR>` via `shared/get-current-milestone.md`, locates the question's contiguous `>`-blockquote run in `requirements.md`, lifts the `> **Recommendation:**` anchor to derive the ANSWER, and delegates to `shared/answer-procedure.md` with the resolved SHORT TITLE + derived ANSWER. Referenced via `${CLAUDE_PLUGIN_ROOT}` by both the `answer-open-question-with-recommendation` skill and its agent.

**Notes:**
- The lifted anchor line has the exact form `> **Recommendation:** <chosen option> — <one-line rationale>` (embedded by the recommend sweep beneath the unchanged one-line question header); derive ANSWER by stripping the leading `>` and the `**Recommendation:**` label from that line.
- The no-embedded-recommendation guard mirrors `answer-procedure.md`'s clean stop on a Short-Title mismatch: when no block matches the Short Title, or the matched block carries no `> **Recommendation:**` anchor, stop without changing anything.
- Reference — do not restate — `answer-procedure.md`'s locate → analyse → remove-the-whole-contiguous-`>`-run → fold-into-`## Decisions` → cascade recording core; this file only lifts and delegates. Match the style of the existing `shared/answer-procedure.md` and `shared/submit-procedure.md`. See the "Lift-procedure placement" decision in `requirements.md` for the authoritative detail.

**Success:**
- The file `shared/answer-with-recommendation-procedure.md` exists.
- It reads as execution-neutral: contains no arg-parsing, committing, commit-subject, `DONE`/`FAILED` return-protocol, or follow-up language (those belong to the skill/agent wrappers).
- It describes the lift-then-delegate composition — take SHORT TITLE, resolve `<MILESTONE_DIR>`, locate the blockquote run, lift and strip the `> **Recommendation:**` anchor into ANSWER, then delegate to `shared/answer-procedure.md` — without restating that core's locate/remove/fold/cascade steps.
- It includes the no-embedded-recommendation guard (stops without changes when no matching block exists or the matched block carries no `> **Recommendation:**` anchor).

---

