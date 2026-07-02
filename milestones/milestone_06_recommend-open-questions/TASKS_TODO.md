# TASKS TODO

## Rewire Discuss-Open-Question To Shared Core

Refactor the existing interactive skill `skills/discuss-open-question/SKILL.md` so its restated "alternatives + recommendation" analytical core (current step 3) becomes a **reference** to `${CLAUDE_PLUGIN_ROOT}/shared/recommend-procedure.md` instead of inline duplication, completing the single-source-of-truth extraction. Net user behavior is unchanged; the only change is that the alternatives+recommendation substance is now sourced from the shared file rather than restated inline. Mirror the reference-a-shared-procedure pattern used by the `complete-task` / `submit-task` skills.

**Notes:**
- Per the *Shared extraction boundary* decision, only the shared analytical core moves out. The skill **keeps** everything that is its own layer and is not in the shared core: the conversational opening/framing (open directly with the substance, no preamble), the **"What would change your mind"** section (explicitly a `discuss-open-question`-only layer, not part of the shared core — do not delete it), the invite-pushback / continue-the-conversation loop, and the on-decision follow-up offers (offer `/answer-open-question`, and `/modify-milestone-goal` when the goal itself must shift, running `/modify-milestone-goal` first when both apply).
- Do **not** duplicate the alternatives/recommendation substance (the 2–4-options-with-what-it-is/advantage/drawback and the single recommendation-with-tie-break) that now lives in the shared file — reference it, do not restate it. `shared/recommend-procedure.md` is created by the "Extract Shared Recommend Procedure File" task, which this task depends on.
- Preserve the existing frontmatter, Usage, and the "find the current milestone" / "locate the question" / "gather context" steps and the Rules section unchanged — only the restated analytical core in step 3 changes to a reference. The skill still edits nothing (purely conversational).

**Success:**
- `skills/discuss-open-question/SKILL.md` no longer restates inline the 2–4-alternatives-with-three-fields (what-it-is / advantage / drawback) and the single-recommendation-with-tie-break substance; instead it references `${CLAUDE_PLUGIN_ROOT}/shared/recommend-procedure.md` for that core.
- The **"What would change your mind"** section, the conversational opening/framing, the continue-the-conversation loop, and the on-decision offers (`/answer-open-question` and `/modify-milestone-goal`, with `/modify-milestone-goal` run first when both apply) all remain present.
- The skill's frontmatter, Usage, and the find-milestone / locate-question / gather-context steps and Rules are preserved.
- The skill still edits no files — it remains purely conversational.

---

## Generalize Answer-Procedure Block Removal

Generalize step 4 ("Remove the matched block") of `shared/answer-procedure.md` so it removes the **entire contiguous blockquote run** containing the located question header — the unchanged one-line header plus any recommendation sub-block the recommend-sweep has embedded beneath it — instead of assuming the block is a single line. Once questions can carry an embedded recommendation, a question block is a contiguous run of `>`-prefixed lines, and answering it must clear the whole run, not just line 1.

**Notes:**
- Per the *Recommendation sub-block format* decision in `requirements.md`, a question block is one contiguous `>`-prefixed run: the one-line header on line 1, then optionally an embedded recommendation sub-block, with internal gaps rendered as empty `>` lines (never bare blank lines). The run is therefore bounded by the blank lines that already separate entries — that boundary is how "the contiguous run containing this header" is delimited.
- This is a targeted edit to step 4's removal semantics only. Do **not** touch step 2 (locating still keys off the unchanged one-line header), steps 3/5/6 (analyse / fold into `## Decisions` / cascade), or the file's execution-neutrality (no arg-parsing, committing, or return protocol).
- The bare one-line header with no sub-block is the degenerate single-line case and must still be removed exactly as today — the new wording is a strict generalization, not a behavior change for that case.

**Success:**
- `shared/answer-procedure.md` step 4 removes the entire contiguous `>`-prefixed run containing the located header (header plus any embedded recommendation sub-block), explicitly covering both the annotated case and the bare single-line header case.
- Step 2's locating still keys off the one-line header, and steps 3, 5, and 6 are unchanged.
- The file stays execution-neutral — no arg-parsing, committing, return protocol, or milestone-resolution added.

---

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
