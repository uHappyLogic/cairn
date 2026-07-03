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

## Add Answer-With-Recommendation Agent

Create the new file-editing agent `agents/answer-open-question-with-recommendation.md` — the isolated-context twin of the forthcoming `answer-open-question-with-recommendation` skill, dispatched per-question by the forthcoming `/answer-all-open-questions-with-recommendation` sweep. Given a target question's Short Title in its prompt, it runs the shared lift-then-delegate procedure to record that question's embedded recommendation, then commits its own answer. This is the "mutation isolated into a file-editing agent" divergence plus the "Sweep commit ownership" and "Recommendation-answer commit subject" decisions in `requirements.md`.

**Provides:**
- New file `agents/answer-open-question-with-recommendation.md`: a `model: opus` file-editing agent that takes a target question's Short Title from its prompt, runs `shared/answer-with-recommendation-procedure.md` (referenced via `${CLAUDE_PLUGIN_ROOT}`) to lift and record that question's embedded recommendation, and **commits its own answer** — path-scoped `git add <MILESTONE_DIR>/requirements.md`, subject `Recommendation-answer: <Short Title>`, no `Answer-Principle:` trailer.
- Return protocol: `DONE` on a successful recorded-and-committed answer; `FAILED: <reason>` on the shared procedure's clean stop or any error, leaving the tree as it found it (no partial commit). The `/answer-all-open-questions-with-recommendation` orchestrator relies on this contract — because the agent owns the commit, the orchestrator dispatches and sequences only and never commits.

**Notes:**
- Model this agent's frontmatter and structure on `agents/complete-task.md` / `agents/submit-task.md` (the established SKILL+AGENT pattern: `model: opus`, run the shared procedure in isolation, add a return protocol), **but** unlike those two this agent (a) mutates `requirements.md` and (b) commits its own answer. In `complete-task` committing is the orchestrator's job; here it is deliberately the agent's — do not mirror `complete-task`'s stage-and-leave-to-orchestrator behavior. Both reversals are documented decisions ("Sweep commit ownership", plus the mutation-in-agent divergence).
- Path-scoped staging (`git add <MILESTONE_DIR>/requirements.md`, **never** `git add -A`) is what keeps a dirty working tree from contaminating the commit — it is the mechanism behind the "one commit = one answer" guarantee, not an incidental choice.
- The shared procedure's no-anchor / missing-block outcome is a **clean stop**, which this agent surfaces as `FAILED: <reason>` (not `DONE`) with nothing committed — "nothing recorded" is a failure to answer, not a success.
- Reference — do not restate — the lift/record steps: the agent points at `shared/answer-with-recommendation-procedure.md` via `${CLAUDE_PLUGIN_ROOT}` and never re-narrates lifting the anchor, folding into `## Decisions`, or cascading (all owned by the shared procedures). See the "Sweep commit ownership" and "Recommendation-answer commit subject" decisions in `requirements.md` for authoritative detail.

**Success:**
- The file `agents/answer-open-question-with-recommendation.md` exists and carries `model: opus` in its frontmatter.
- It references `shared/answer-with-recommendation-procedure.md` via `${CLAUDE_PLUGIN_ROOT}` and does not restate the lift/record/cascade steps.
- It instructs the agent to commit path-scoped (`git add <MILESTONE_DIR>/requirements.md`, never `git add -A`) under the subject `Recommendation-answer: <Short Title>` with no `Answer-Principle:` trailer.
- It defines the `DONE` / `FAILED: <reason>` return protocol and states that a clean stop or any failure returns `FAILED` and leaves the tree as it found it with no partial commit.

---

