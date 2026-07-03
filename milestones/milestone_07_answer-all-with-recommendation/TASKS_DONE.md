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

## Add Answer-With-Recommendation Skill

Create the new user-facing skill `skills/answer-open-question-with-recommendation/SKILL.md` — the inline twin of the `answer-open-question-with-recommendation` agent, completing the SKILL + AGENT wrapper pair (like `complete-task`/`submit-task`). Invoked as `/answer-open-question-with-recommendation <Short Title>`, it runs the shared lift-then-delegate procedure inline to record that one question's embedded recommendation, then commits inline. This is the "Standalone skill commit" decision in `requirements.md`.

**Provides:**
- New file `skills/answer-open-question-with-recommendation/SKILL.md`: a `model: opus` user-facing skill, invoked `/answer-open-question-with-recommendation <Short Title>`, whose description triggers when a user wants to record a single question's embedded recommendation as its answer. It runs `shared/answer-with-recommendation-procedure.md` (referenced via `${CLAUDE_PLUGIN_ROOT}`) **inline** in the user's conversation to lift and record that question's embedded recommendation, then **commits inline** — path-scoped `git add <MILESTONE_DIR>/requirements.md` (never `git add -A`), subject `Recommendation-answer: <Short Title>`, no `Answer-Principle:` trailer.

**Notes:**
- Model the frontmatter and structure on the `complete-task` / `submit-task` **skill** wrappers (the inline half of the SKILL+AGENT pattern: `model: opus`, run the shared procedure inline in the user's conversation so the context survives for follow-up, never spawn the agent twin). The **only** differences from the `answer-open-question-with-recommendation` agent are that this skill runs the procedure inline rather than in isolation, and that it omits the agent's `DONE` / `FAILED` return protocol.
- Unlike `complete-task`/`submit-task`, which leave changes staged, this skill **commits** — because it records a decision, it joins the committing category, mirroring `answer-open-question`, the committing mode this pair is extracted from. Path-scoped staging (`git add <MILESTONE_DIR>/requirements.md`, never `git add -A`) is the mechanism that keeps a dirty tree from contaminating the commit, not an incidental choice.
- On the shared procedure's clean stop (no matching block, or the matched block carries no `> **Recommendation:**` anchor), the skill stops without changing or committing anything — its existing clean-stop-and-point pattern.
- Reference — do not restate — the lift/record steps: point at `shared/answer-with-recommendation-procedure.md` via `${CLAUDE_PLUGIN_ROOT}` and never re-narrate lifting the anchor, folding into `## Decisions`, or cascading (all owned by the shared procedures). See the "Standalone skill commit", "Recommendation-answer commit subject", and "Lift-procedure placement" decisions in `requirements.md` for authoritative detail.

**Success:**
- The file `skills/answer-open-question-with-recommendation/SKILL.md` exists and carries `model: opus` in its frontmatter with a description that triggers on recording a single question's embedded recommendation as its answer.
- It references `shared/answer-with-recommendation-procedure.md` via `${CLAUDE_PLUGIN_ROOT}` and does not restate the lift/record/cascade steps.
- It runs the shared procedure inline and never spawns the `answer-open-question-with-recommendation` agent.
- It instructs the skill to commit inline path-scoped (`git add <MILESTONE_DIR>/requirements.md`, never `git add -A`) under the subject `Recommendation-answer: <Short Title>` with no `Answer-Principle:` trailer.
- It stops without changing or committing anything on the shared procedure's no-embedded-recommendation / missing-block clean stop.

---


## Add Answer-All-With-Recommendation Orchestrator

Create the new orchestrator skill `skills/answer-all-open-questions-with-recommendation/SKILL.md` — the sweep that answers every open question already carrying an embedded recommendation by dispatching the file-editing `answer-open-question-with-recommendation` agent once per question, strictly sequentially. It is structurally modeled on `skills/try-answer-all-questions-by-principle/SKILL.md` but deliberately diverges on one axis: it dispatches a **file-editing** agent, not a read-only subagent, because the recommendation is pre-computed — so only mutation (not reasoning) is isolated. This realizes the milestone's "mutation isolated into a file-editing agent, dispatched strictly sequentially, one commit per answer" divergence plus the "Sweep cascade ordering" and "Sweep commit ownership" decisions in `requirements.md`.

**Provides:**
- New file `skills/answer-all-open-questions-with-recommendation/SKILL.md`: an argument-free orchestrator skill invoked `/answer-all-open-questions-with-recommendation`, whose trigger-rich description fires when the user wants to sweep the milestone and record every open question's embedded recommendation as its answer. It resolves `<MILESTONE_DIR>` via `shared/get-current-milestone.md`, gathers — once, in most-significant-first order — every `Open question` / `Deferred` entry **that carries an embedded `> **Recommendation:**` anchor** (recommendation-less questions are the recommend sweep's job and are never gathered here), walks them exactly once, and for each surviving question dispatches the `answer-open-question-with-recommendation` agent (`Agent` tool, `subagent_type: "answer-open-question-with-recommendation"`) with that question's Short Title, strictly sequentially. It never commits and never edits `requirements.md`.

**Notes:**
- Frontmatter follows the **orchestrator** convention, not the skill+agent-pair convention: mirror `try-answer-all-questions-by-principle`'s frontmatter (`name` + `description` only) — do **not** add `model: opus` (that belongs to the paired skill/agent, not this sweep).
- Mirror the principle sweep's gather/order/re-check machinery (its step 2 for gather-once-most-significant-first, and its step 3a for the per-question live re-read + skip) but invert the read-only-vs-file-editing axis. Gather once most-significant-first (the cascade-parent-first proxy) — restricting the gathered set to questions that carry an embedded `> **Recommendation:**` anchor; before each dispatch re-read `requirements.md` and skip the question when a prior answer's cascade already removed its block. The agent's `shared/answer-procedure.md` step-2 stop-on-missing-block stays as a backstop.
- Dispatch **strictly sequentially — never in parallel** — waiting for each agent to return before dispatching the next, because every dispatch mutates the same `requirements.md`. This is the load-bearing reason this sweep cannot parallelize its dispatches.
- The agent owns **all** mutation and its own path-scoped commit (one commit = one answer, subject `Recommendation-answer: <Short Title>`); the orchestrator purely dispatches and sequences. Do **not** add an orchestrator-side commit or any `requirements.md` edit — that is the "Sweep commit ownership" divergence from `try-answer-all-questions-by-principle`, whose orchestrator (unlike this one) owns the commit.
- Unlike the principle sweep, this orchestrator needs **no** clean-working-tree precondition: the agent stages path-scoped (`git add <MILESTONE_DIR>/requirements.md`, never `git add -A`), so a dirty tree cannot contaminate its commit. The "Sweep cascade ordering" decision adopts only two of the principle sweep's mechanisms (gather-once-ordered + per-question re-read/skip), not its clean-tree gate.
- On an agent `FAILED: <reason>` return, follow the established file-editing-agent sweep convention — check how `complete-all-tasks` (the orchestrator over the file-editing `complete-task` agent) reacts to a `FAILED` dispatch, since `try-answer-all-questions-by-principle`'s read-only subagent never returns `FAILED`; report-and-stop. Because the gather step already filters to questions carrying an embedded recommendation, and the per-dispatch re-read/skip handles cascade-removed blocks, the agent's no-anchor/missing-block clean-stop `FAILED` should fire only on a genuine should-not-happen inconsistency (a block that raced away between gather and dispatch) — treating it as a real failure to report-and-stop on is correct, not a benign skip. Resolve the exact reaction against the live `agents/answer-open-question-with-recommendation.md` return protocol — do not fabricate reason-string parsing.

**Success:**
- The file `skills/answer-all-open-questions-with-recommendation/SKILL.md` exists, with a trigger-rich description (modeled on `try-answer-all-questions-by-principle`'s "Trigger it whenever the user says…" style) for sweeping every open question with an embedded recommendation.
- Its frontmatter carries `name` + `description` only and does **not** include `model: opus`.
- It gathers, once in most-significant-first order, every `Open question` / `Deferred` entry that carries an embedded `> **Recommendation:**` anchor (recommendation-less questions are not gathered), and walks them exactly once (no outer re-gather loop).
- It re-reads `requirements.md` before each dispatch and skips a question whose block a prior answer's cascade already removed.
- It dispatches the `answer-open-question-with-recommendation` agent (`subagent_type: "answer-open-question-with-recommendation"`) strictly sequentially, one dispatch per surviving question, never in parallel.
- It never itself commits and never edits `requirements.md`, and it documents that the agent owns all mutation and its own commit.

---

## Narrow Answer-Open-Question To Literal-Only With Redirect Guard

Now that recommendation-recording is extracted into the `answer-open-question-with-recommendation` pair, narrow `skills/answer-open-question/SKILL.md` to the **literal-answer path only**: remove the record-recommendation mode — the sentinel-gated lift/locate logic that resolved `<MILESTONE_DIR>`, found the question's blockquote run, and lifted its `> **Recommendation:**` anchor as the answer. In its place retain a small **redirect guard** that still recognizes the old sentinel and, instead of recording it, cleanly stops and points the user at `/answer-open-question-with-recommendation`. This is the "answer-open-question redirect after extraction" decision in `requirements.md`.

**Notes:**
- The redirect guard reuses the sentinel-matching discipline of the removed mode exactly: the parsed answer text, **trimmed and lowercased**, compared as an **exact whole-string match** against `record the recommendation` — **never a substring**, so a literal answer that merely contains those words still records literally. On a match the skill **stops without recording or committing anything** and prints a redirect message naming `/answer-open-question-with-recommendation`. This is not a revived feature — it records nothing; it fits the skill's existing clean-stop-and-point pattern (the old no-anchor guard and the shared procedure's Short-Title mismatch).
- The guard must fire **before** delegating to `shared/answer-procedure.md`, at the arg-resolution point where the old sentinel would otherwise flow through as literal text and be committed as a `Manual-answer:` decision recording the phrase itself — that interception is the entire purpose.
- Everything else is unchanged and must stay: the first-`.` arg split (Short Title before, answer text after), the literal-answer path for any non-sentinel text, delegation to `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md`, and the `Manual-answer: <Short Title>` commit (path-scoped `git add <MILESTONE_DIR>/requirements.md`, rationale in the body, no `Answer-Principle:` trailer).
- The current file threads record-recommendation mode through several surfaces beyond the workflow steps — the intro paragraph after Usage, the "record-recommendation mode" example block, step 2 ("Resolve the answer text"), the step 4 commit-body wording that mentions "the lifted `<chosen option>`", and the Rules list. Reconcile all of them to literal-only-plus-redirect so no stale lift/anchor language survives.

**Success:**
- `skills/answer-open-question/SKILL.md` no longer contains any record-recommendation lift/locate logic — no resolving `<MILESTONE_DIR>` to find a block, no reading or stripping a `> **Recommendation:**` anchor, no `/recommend-all-open-questions`-first pointer.
- Any literal answer still records exactly as before and commits under `Manual-answer: <Short Title>` (path-scoped, rationale in body, no `Answer-Principle:` trailer).
- An answer text exactly equal to `record the recommendation` (after trim + lowercase, whole-string) triggers a clean stop that records nothing and commits nothing, and prints a redirect to `/answer-open-question-with-recommendation`.
- The first-`.` split and the literal-answer path are intact and documented; no stale references to record-recommendation mode remain anywhere in the file (Usage intro, examples, workflow steps, or Rules).

---
