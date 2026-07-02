# TASKS TODO

## Add Record-Recommendation Mode To Answer-Open-Question

Extend `skills/answer-open-question/SKILL.md` with a record-recommendation mode: instead of taking literal answer text, the skill lifts the recommendation the recommend-sweep embedded beneath a question header and records THAT as the answer. Selected by the reserved sentinel answer text `record the recommendation`; per the *Record-recommendation trigger* decision in `requirements.md`, the existing grammar, first-`.` split, literal-answer path, and `Manual-answer:` commit rules all stay unchanged.

**Provides:**
- The reserved sentinel answer text `record the recommendation` as the public trigger for record-recommendation mode — the named consumer of the recommendation sub-blocks that `recommend-all-open-questions` embeds.

**Notes:**
- Mode selection is exact: the sentinel fires only when the parsed answer text, after trim + lowercase, equals `record the recommendation` as a **whole-string** match — never a substring — so a genuine literal answer that merely contains those words is never hijacked. Any answer text that is not the exact sentinel routes through the unchanged literal-answer path.
- Lifting the recommendation is *answer-derivation*, which is the wrapper's job — so in sentinel mode the skill must itself locate the targeted block and read its `> **Recommendation:** <chosen option> — <rationale>` anchor line, then pass that anchor's content as the `ANSWER` to `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` in place of the arg's literal text. This read-locate is distinct from — and must not restate — the shared procedure's recording locate/remove/fold/cascade mechanism, which per the CLAUDE.md invariant lives only in `answer-procedure.md` (the shared procedure re-locates and removes the whole run itself, unchanged). To do its own locate the skill resolves `<MILESTONE_DIR>` via `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` (no hardcoded path).
- No-recommendation guard: when the targeted block carries no embedded `> **Recommendation:**` anchor (the recommend sweep never ran, or the question was added afterward), lift-mode **stops without changing anything**, reports — pointing the user to run the recommend sweep (`/recommend-all-open-questions`) first, or to answer with literal text via `<Title>. <answer>` — and commits nothing. This mirrors how the shared procedure already stops cleanly (and produces no commit) on a Short-Title mismatch, which remains the other no-commit sub-case in sentinel mode.
- The `> **Recommendation:** …` anchor shape and the contiguous-run block format come from the *Recommendation sub-block format* decision; the whole-run removal on answering is owned by the separate "Generalize Answer-Procedure Block Removal" task — do not author removal logic here.

**Success:**
- `skills/answer-open-question/SKILL.md` documents record-recommendation mode selected by the sentinel answer text `record the recommendation`, matched as an exact whole-string comparison after trim + lowercase, explicitly stated as not a substring match.
- It specifies that in this mode the skill lifts the embedded `> **Recommendation:** …` anchor line's content as the answer text passed to `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md`, then proceeds through the unchanged record + `Manual-answer:` commit path.
- It documents the no-embedded-recommendation case: lift-mode stops without changes, reports (pointing to `/recommend-all-open-questions` or the literal `<Title>. <answer>` form), and commits nothing.
- The existing first-`.` split (Short Title before, answer text after), the literal-answer path for any non-sentinel answer text, and the commit rules (path-scoped `git add <MILESTONE_DIR>/requirements.md`, subject `Manual-answer: <Short Title>`, rationale in body, no `Answer-Principle:` trailer) remain intact.

---
