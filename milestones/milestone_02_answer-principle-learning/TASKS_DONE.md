# TASKS DONE

## Create Answer-Recording Shared Procedure

Create a new `shared/answer-procedure.md` — peer to `shared/submit-procedure.md` and `shared/implement-procedure.md` — as the single source of truth for recording an answer to an open question. It documents the `locate → analyse → remove → fold → cascade` core: resolve `<MILESTONE_DIR>` via `shared/get-current-milestone.md`, locate the question block by its Short Title, analyse the answer's implications, remove the matched block, fold the decision into `## Implementation decisions` as clean prose (no citation marker), and cascade to any entry the answer moots. This extracts the recording steps currently duplicated in prose across `answer-open-question` (steps 3–4) and `answer-obvious-open-questions` (step 2c). This task creates only the new shared file; rewiring the callers to reference it is a separate downstream task.

**Provides:**
- `shared/answer-procedure.md` — the shared answer-recording procedure, referenced by callers via the `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` idiom (matching how the other shared procedures are referenced).
- Its input contract: a **resolved Short Title** plus the **answer text** (locating-by-title and cascading are shared; obtaining the title/answer is the caller's job).

**Notes:**
- Model the file's shape on `shared/submit-procedure.md` (intro framing → Inputs → the procedure phases → Rules).
- The file MUST be execution-neutral, exactly as `submit-procedure.md` never mentions the `DONE`/`FAILED` protocol. It must NOT mention: arg-parsing (e.g. splitting on the first `.`), committing, the `Answer-Principle:` trailer, the `Principle-based-answer:` subject, or the `try-capture-answer-principle` chain. That neutrality is what lets one file serve both the staged-edit `answer-open-question` skill and the commit-per-answer orchestrator — pulling any of it in would defeat the file's purpose.
- Name the `locate → analyse → remove → fold → cascade` sequence as the content the file must cover; do not expand it into per-step implementation narration beyond what the existing skill prose already carries.

**Success:**
- `shared/answer-procedure.md` exists at the repo root's `shared/` directory.
- It covers all five phases: locate the question by Short Title, analyse implications, remove the matched block, fold the decision into `## Implementation decisions` as clean prose, and cascade to mooted entries.
- It resolves `<MILESTONE_DIR>` by following `shared/get-current-milestone.md` (not a hardcoded path).
- It names its inputs as a resolved Short Title + answer text.
- It contains zero references to committing, trailers (`Answer-Principle:`/`Principle-based-answer:`), arg-parsing, or principle capture.

---

