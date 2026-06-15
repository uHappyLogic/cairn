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

## Create Try-Answer-Question-By-Principle Subagent

Create `agents/try-answer-question-by-principle.md` — the read-only, single-question candidate-elimination subagent the `try-answer-questions-by-principle` orchestrator dispatches once per Open/Deferred question. Given one question (its Short Title plus context), it reads the project-wide principle store, enumerates the realistic candidate answers, keeps only those each supportable by at least one confirmed principle, and returns a structured verdict naming the unique survivor (if any) and the principles that kept it alive. It mutates nothing — it is read-only on both `requirements.md` and the principle store; the orchestrator owns all document mutation and committing.

**Provides:**
- `agents/try-answer-question-by-principle.md` — the per-question elimination subagent, dispatched by the orchestrator.
- Its input contract: one question's **Short Title + context** (supplied by the orchestrator).
- Its verdict return contract (the orchestrator parses this to emit one `Answer-Principle:` trailer line per load-bearing principle): (a) whether exactly one candidate survives (unique-survivor yes/no); (b) the surviving answer; (c) the **full** set of load-bearing principles supporting the survivor, by `### <Short Title>` handle — every principle that genuinely kept the survivor alive, **not** a curated "most important" subset; (d) the candidate set considered. Auto-answer is warranted only when exactly one candidate survives; two-or-more survivors (including the conflicting-principles case, where different principles imply different answers) or zero survivors both yield a "no unique survivor" verdict.

**Notes:**
- The principle store is `milestones/answer_decision_principles.md` at the `milestones/` **root** — above any `<MILESTONE_DIR>`, shared across all milestones. It is the one file the loop reads at a fixed root path and is **not** resolved via `shared/get-current-milestone.md` (every other reader resolves relative to `<MILESTONE_DIR>` — do not default to that here).
- If the principle store is **absent or empty**, treat it as no principles → nothing is supportable → every candidate is eliminated → the verdict is always "no unique survivor". This must be stated in the agent because the behavior lives in the still-open `Deferred — Missing principle file` block, not in `## Implementation decisions`.
- The candidate set must be the realistic alternatives — the same bar `discuss-open-question` uses when enumerating options. The gate is only as strong as the candidate set, so an impoverished set defeats it.
- The "supportable" test must be a genuine fit, not a rationalization. Apply each principle's **statement**, not its optional `*Origin:*` line.
- Model the agent's shape on `agents/implement-backlog-task.md`, but it is **READ-ONLY** and returns the structured verdict as its final message in place of that agent's `DONE`/`FAILED` protocol. There is no strength-gate / judgment-based answering (the removed `answer-obvious` logic): a confirmed principle is the sole basis for keeping a candidate.

**Success:**
- `agents/try-answer-question-by-principle.md` exists with valid agent frontmatter (e.g. `name`, `description`).
- The body describes reading the principle store at the `milestones/` root, enumerating realistic candidate answers, keeping only those supportable by ≥1 confirmed principle, and returning a structured verdict reporting unique-survivor yes/no, the surviving answer, all load-bearing principles, and the candidate set considered.
- It explicitly states the subagent never edits `requirements.md` or the principle store.
- It explicitly states that an absent or empty principle store yields a "no unique survivor" verdict.

---

