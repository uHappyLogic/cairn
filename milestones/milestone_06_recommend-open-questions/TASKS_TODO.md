# TASKS TODO

## Recommend-All-Open-Questions Sweep Orchestrator

Create the new orchestrator skill `skills/recommend-all-open-questions/SKILL.md` — the non-interactive batch path that sweeps the current milestone's open/deferred questions and annotates each one with an embedded recommendation. It is the argument-free twin of `try-answer-all-questions-by-principle` (model its structure and tone on `skills/try-answer-all-questions-by-principle/SKILL.md`) but is deliberately simpler because it records no decisions and triggers no cascades. It dispatches one `recommend-open-question` subagent per un-annotated question and is the sole document mutator, embedding each returned sub-block beneath the unchanged one-line question header.

**Provides:**
- `skills/recommend-all-open-questions/SKILL.md` — the orchestrator skill (YAML frontmatter `name: recommend-all-open-questions`), argument-free, that sweeps every `> **Open question — <Short Title>` / `> **Deferred — <Short Title>` entry in `<MILESTONE_DIR>/requirements.md`, dispatches `subagent_type: "recommend-open-question"` per surviving question, and is the sole mutator that embeds the returned recommendation sub-block beneath the unchanged one-line header. It is a **mutate-but-do-not-commit** skill: it stages only its own path-scoped `git add <MILESTONE_DIR>/requirements.md` edit and stops. Its named consumer is `answer-open-question`'s record-recommendation mode.

**Notes:**
- Model on the twin but **deliberately drop** four pieces of its machinery, per the *Sweep write model* and *Recommendation independence* decisions: no gather-order (the twin's most-significant→least cascade-parent-first proxy), no per-question live-re-check/skip against a mutating document, no outer re-gather loop, and no clean-working-tree precondition. Gather the open/deferred entries **once** and walk straight through — because the sweep records no decisions and triggers no cascades, the question set never shrinks under it.
- Re-run idempotency (*Re-run idempotency* decision): **skip** any question block that already carries a recommendation sub-block — detect by the presence of the `> **Recommendation:**` anchor line within the block's contiguous `>` run — and dispatch/annotate **only** blocks that lack one. Document the escape hatch: to force a fresh recommendation on a stale block the user deletes that block's recommendation sub-block (leaving the one-line question header intact) and re-runs, whereupon skip regenerates it. Add **no** `refresh`/selectable mode — keep the skill argument-free like its twin.
- The per-question dispatches are **independent** and may be parallelized (*Recommendation independence*): never feed one question's recommendation into another. Embedding keeps the whole entry one contiguous `>` run with empty-`>` internal separation (never bare blank lines), and the one-line `> **Open question — …` / `> **Deferred — …` header must stay greppable on line 1.
- Write model (*Sweep write model* decision): after writing all sub-blocks, stage **only** its own edit with a path-scoped `git add <MILESTONE_DIR>/requirements.md` (**never** `git add -A`) and stop, leaving the staged edit for the user to review and commit or discard. State briefly *why* it neither commits nor requires a clean tree: it records no decisions and triggers no cascades, so it needs neither the one-commit-per-question model nor the clean-tree precondition — the durable git record is the eventual `Manual-answer:` commit, not the transient recommendation scaffolding.

**Success:**
- `skills/recommend-all-open-questions/SKILL.md` exists with YAML frontmatter carrying `name: recommend-all-open-questions`, and takes no arguments.
- It resolves `<MILESTONE_DIR>` by following `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` (no hardcoded path), gathers every `Open question`/`Deferred` entry **once**, and walks straight through with no re-gather loop, no gather-order, and no live-re-check/skip; it says so and stops when there are no open/deferred questions.
- It skips blocks that already carry a `> **Recommendation:**` anchor and annotates only those lacking one, and documents the delete-the-sub-block-and-re-run escape hatch; it adds no `refresh`/selectable mode.
- It dispatches `subagent_type: "recommend-open-question"` (singular) via the `Agent` tool once per surviving question, passing that question's Short Title and full block/context, and treats the subagent as read-only (returns the sub-block; the orchestrator does all writing).
- It embeds each returned sub-block directly beneath the unchanged one-line header, keeping one contiguous `>` run with empty-`>` separation and the header greppable on line 1.
- It stages a path-scoped `git add <MILESTONE_DIR>/requirements.md` and does **not** commit, and requires no clean working tree.
- It reports which questions were annotated and which were skipped, and points the user at `answer-open-question`'s record-recommendation mode as the consumer.

---

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
