# TASKS DONE

## Extract Shared Recommend Procedure File

Create the new execution-neutral shared file `shared/recommend-procedure.md`, extracting the "alternatives + recommendation for one question" analytical core currently embedded in `skills/discuss-open-question/SKILL.md` step 3. This single source is referenced (never restated) by `discuss-open-question` and the new read-only `recommend-open-question` subagent so the alternatives/recommendation logic lives in exactly one place. Model its tone and structure on the sibling `shared/answer-procedure.md`.

**Provides:**
- `shared/recommend-procedure.md` — the execution-neutral single-source-of-truth procedure for producing one question's alternatives + recommendation, referenced by wrappers via `${CLAUDE_PLUGIN_ROOT}`. It owns exactly three pieces of logical content and nothing else: (1) the **grounding discipline** — read the real context / live code (read-only) before forming a view, over reasoning from memory; (2) the **Alternatives** requirement — enumerate 2–4 genuinely realistic options (no strawmen, no padding), each carrying three logical fields: what-it-is / key advantage / key drawback; (3) a single **Recommendation** — one preferred option with a brief, direct, hedge-free rationale, plus the tie-break rule (if two options are genuinely equivalent, say so and name what breaks the tie).

**Notes:**
- Two Decisions in `requirements.md` collide on the surface; resolve for the *Shared extraction boundary* decision (the controlling one). The *Recommendation sub-block format* decision says the empty-`>` separation discipline "must be stated in the shared extraction file", but empty `>` lines are themselves `>`-markup, which the boundary decision keeps out of the shared file. So state the attachment concept in **prose only** — a recommendation forms one contiguous, self-contained unit that stays attached to its question — and defer ALL literal `>`-blockquote markup, the `> **Recommendation:**` anchor text, and separation/rendering to the subagent's return protocol. Put no `>`-as-markup characters in this file.
- Do NOT extract "what would change your mind" from step 3. It is a `discuss-open-question`-only layer (per the *Shared extraction boundary* decision), not part of the shared core — the shared file is alternatives + recommendation only.
- Encode the *Recommendation independence* distinction as it bears on grounding: "isolation" constrains the orchestrator (it never feeds one question's recommendation into another), not the analyst's grounding. The analyst still reads `requirements.md` and the live code read-only to enumerate honest alternatives (and incidentally sees the one-line sibling question headers); what it must never do is treat another question's recommendation as an input.
- Keep it execution-neutral like `shared/answer-procedure.md`: no arg-parsing, no committing, no return protocol, no `DONE`/`FAILED`, no milestone resolution or `<MILESTONE_DIR>` handling. It describes only the core analytical work on already-resolved inputs.

**Success:**
- `shared/recommend-procedure.md` exists.
- It specifies the three-field Alternatives requirement (2–4 realistic options; what-it-is / key advantage / key drawback per option), the single Recommendation with the tie-break rule, and the grounding discipline.
- It states the prose-only contiguity / self-contained-unit concept and the isolation-vs-grounding distinction.
- It contains no literal `>` blockquote markup and no rendering/anchor text (e.g. no `> **Recommendation:**` anchor).
- It contains no "what would change your mind" section.
- It reads as execution-neutral: no arg-parsing, no committing, no return protocol, no milestone/`<MILESTONE_DIR>` resolution.

---

## Read-Only Recommend-Open-Question Subagent

Create the new read-only subagent `agents/recommend-open-question.md` — the non-interactive twin of `discuss-open-question`, dispatched once per question by the `recommend-all-open-questions` orchestrator (a later task). Model its YAML frontmatter and section structure (inputs / how-to-produce / Return protocol) on the sibling read-only agent `agents/try-answer-question-by-principle.md`.

**Provides:**
- `agents/recommend-open-question.md` — a read-only single-question subagent (YAML frontmatter: `name: recommend-open-question`, plus a `description` and a `color`) dispatched once per question by `recommend-all-open-questions`; it resolves its target question from its own prompt (the question's Short Title + full block/context) and decides no global ordering.
- Its return-protocol contract — the recommendation sub-block the orchestrator embeds verbatim beneath the unchanged one-line question header, and that `answer-open-question`'s record-recommendation mode later lifts from. It is rendered per the *Recommendation sub-block format* decision in `requirements.md`; its stable, lift-able anchor is the `> **Recommendation:** <chosen option> — <one-line rationale>` line.

**Notes:**
- Unlike the sibling `try-answer-question-by-principle` (whose analytical core is inline in-body), this subagent's how-to-produce section must **reference** `${CLAUDE_PLUGIN_ROOT}/shared/recommend-procedure.md` for the alternatives+recommendation core and never restate it — the reference-a-shared-procedure pattern to mirror is the `complete-task` / `submit-task` agents, not `try-answer-question-by-principle`.
- The shared `recommend-procedure.md` deliberately keeps **all** `>`-blockquote markup out (it is execution-neutral, logical content only). So this subagent **owns** the literal blockquote rendering: the empty-`>` separation discipline (internal gaps are empty `>` lines, never bare blank lines, so the whole thing stays one contiguous `>`-prefixed run) and the `> **Recommendation:**` anchor text. That markup lives here, not in the shared file.

**Success:**
- `agents/recommend-open-question.md` exists with YAML frontmatter carrying `name: recommend-open-question` (plus a `description` and a `color`).
- Its how-to-produce section references `${CLAUDE_PLUGIN_ROOT}/shared/recommend-procedure.md` for the alternatives+recommendation core and does not restate that core.
- It specifies the exact recommendation sub-block shape: beneath the unchanged one-line question header, an empty `>` line, then `> **Alternatives:**` followed by one `> - **<Option>** — what it is. *Advantage:* … *Drawback:* …` bullet per option, an empty `>` line, then the stable `> **Recommendation:** …` anchor line — with every internal gap rendered as an empty `>` line, never a bare blank line.
- It states it is read-only — it mutates nothing (never edits `requirements.md`); the orchestrator owns all document mutation and embedding.
- Its Return protocol emits **only** the sub-block lines placed beneath the header (starting with the leading empty `>` attach line, not the header itself) as its final message, for the orchestrator to embed verbatim.
- It states the *Recommendation independence* distinction: "isolation" is an orchestrator constraint (never feed one question's recommendation into another) and does **not** forbid this subagent from reading `requirements.md` and live code read-only to enumerate honest alternatives (incidentally seeing sibling one-line question headers) — what it must never do is treat another question's recommendation as an input.

---

