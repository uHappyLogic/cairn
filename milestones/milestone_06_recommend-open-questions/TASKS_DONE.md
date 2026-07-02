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

