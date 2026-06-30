# TASKS DONE

## Commit Manual Answers, Drop Capture Chain

Make the `/answer-open-question` skill wrapper (`skills/answer-open-question/SKILL.md`) commit its own manual-answer edit instead of leaving it staged, and sever its unconditional chain into `/try-capture-answer-principle`. After the shared answer-recording procedure folds the decision into `## Decisions`, the skill stages only its own `requirements.md` edit and commits it with a recognizable subject and the rationale in the body — establishing the `Manual-answer:` commit convention that the later finish-time capture skill walks. Only the skill wrapper changes; `shared/answer-procedure.md` is not touched.

**Provides:**
- The manual-answer commit convention that `/capture-milestone-principle-updates` (a later task) greps for: subject line exactly `Manual-answer: <Short Title>` (colon then space — it is matched by `git log --grep='^Manual-answer: '`), the decision rationale in the commit **body**, and **no** `Answer-Principle:` trailer (its absence is the discriminator between a manual answer and a sweep auto-answer that `reject-auto-answer`'s gate relies on).

**Notes:**
- Staging is path-scoped: `git add <MILESTONE_DIR>/requirements.md` only — never `git add -A` — so the commit touches only `requirements.md` and never sweeps in unrelated working-tree changes (per the "Answer commit scope" decision; this also preserves the sweep's clean-tree precondition).
- Cold-answer body rule (per "Cold-answer commit body"): record only rationale that genuinely exists in conversation context — never prompt the user for a rationale and never fabricate one. On a cold answer the body is the answer text recorded verbatim (including any inline "because" clause); when no reasoning was stated the body holds the bare decision. The answer string is itself the cold path's rationale affordance — do not add a separate rationale prompt.
- The commit fires only when the recording actually changed `requirements.md`. The existing no-op paths — a parse error (no `.` separator) and a Short-Title mismatch (the shared procedure stops without changes) — must still produce no commit.
- This skill committing is a deliberate, documented exception to the project's "individual skills never commit" invariant; note it as such in the skill text. Reconciling the CLAUDE.md / README invariant prose is a separate downstream doc-sync task — do not edit those here.
- Do not touch `shared/answer-procedure.md`: it is shared verbatim by the autonomous sweep and must stay commit-free.

**Success:**
- `skills/answer-open-question/SKILL.md` instructs a path-scoped `git add <MILESTONE_DIR>/requirements.md` (and explicitly not `git add -A`) followed by a commit whose subject is `Manual-answer: <Short Title>`, with the decision rationale in the commit body and no `Answer-Principle:` trailer.
- `skills/answer-open-question/SKILL.md` no longer contains any reference to `try-capture-answer-principle` or any "Capture any reusable principle" step, and no longer contains the "Do not commit / leave staged" rule; surrounding text reflects that the skill now commits.
- `git diff` shows `shared/answer-procedure.md` unchanged by this task.

---

