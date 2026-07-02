# Milestone 6: Recommend Open Questions

## Goal

Add a non-interactive batch path for producing recommendations on open questions, so the per-question `/discuss-open-question` deliberation can be swept automatically after `/review-milestone-requirements`.

Introduce an orchestrator skill that walks every `Open question`/`Deferred` entry in the current milestone and, per question, dispatches a new **read-only** subagent — the non-interactive twin of `discuss-open-question` — that returns alternatives + a recommendation. The orchestrator is the **sole document mutator**: it embeds each result as a recommendation sub-block directly beneath the **unchanged one-line question header** (the question header stays a one-line, greppable blockquote).

Extend `answer-open-question` with a mode that, on "record the recommendation", reads the embedded recommendation out of the block instead of taking literal answer text.

Extract the shared "alternatives + recommendation for one question" logic into `shared/` so both `discuss-open-question` and the new subagent reference one source.

This path is **independent of** `try-answer-all-questions-by-principle` (which may be retired later) and sweeps all open/deferred questions.

## Relevant starting state

### Question block format (author: `review-milestone-requirements`)

`skills/review-milestone-requirements/SKILL.md` is the sole author of question blocks. Each is a **one-line blockquote**: `> **Open question — <Short Title>:** <question text>` or `> **Deferred — <Short Title>:** <what will be decided while doing the work>`. The `<Short Title>` is a 2–5 word phrase, unique across all blocks, used as a stable handle for citation and locating. The skill reconciles/surfaces/reports on these blocks but never records decisions. Convergence for `/derive-tasks` = no `> **Open question` blocks remain (Deferred may carry forward). This milestone must keep the header a one-line, greppable blockquote and add the recommendation *beneath* it.

### `discuss-open-question` skill (source of the logic to extract)

`skills/discuss-open-question/SKILL.md` is the interactive, per-question deliberation. Its core output shape (step 3) is **Alternatives** (2–4 realistic options, each with what-it-is / key advantage / key drawback), a single **Recommendation** with rationale, and **What would change your mind** (1–2 conditions). It reads context (grounds in real code over memory), is purely conversational (edits nothing), and on decision *offers* `/answer-open-question` (and `/modify-milestone-goal` when the goal must shift). This "alternatives + recommendation for one question" logic is what the milestone extracts into `shared/` for reuse by the new read-only subagent.

### `answer-open-question` skill + `shared/answer-procedure.md` (to be extended / affected)

`skills/answer-open-question/SKILL.md` parses its arg on the **first `.`** (Short Title before, literal answer text after), then follows `shared/answer-procedure.md` and commits a path-scoped `Manual-answer: <Short Title>` (rationale in body, no `Answer-Principle:` trailer — a deliberate exception to "individual skills never commit"). This milestone adds a mode where "record the recommendation" reads the embedded recommendation out of the block instead of taking literal answer text.

`shared/answer-procedure.md` is the execution-neutral recording core (inputs: SHORT TITLE + ANSWER): locate the block by its `Open question — <Short Title>` / `Deferred — <Short Title>` header (case-insensitive), analyse implications, **remove the matched block** (step 4), fold the decision into `## Decisions` as clean citation-free prose, cascade to mooted entries. Locating keys off the header line (unchanged by this milestone), but step 4's "remove the matched block" currently assumes a single line — it must be extended to also remove the recommendation sub-block beneath the header.

### Orchestrator + read-only subagent twin pattern (the structural template)

The new skill is modeled directly on the existing pair — this milestone is a twin of it (independent of it; it may be retired later):

- `skills/try-answer-all-questions-by-principle/SKILL.md` (orchestrator) — takes no args; requires a clean working tree; gathers every Open/Deferred entry and orders them once (most-significant → least, a cascade-parent-first proxy); walks the order **exactly once** (no outer re-gather loop) with a per-question **live re-check + skip** against the mutating document; dispatches the read-only subagent per surviving question via the `Agent` tool; **owns all document mutation and committing** (one auto-answer per commit). Recording is delegated to `shared/answer-procedure.md`, never restated.
- `agents/try-answer-question-by-principle.md` (subagent) — a `name`/`description`/`color` frontmatter agent, **read-only** (reads `requirements.md` and the principle store, mutates nothing). It enumerates realistic candidates and returns a structured `VERDICT` block as its final message (candidates considered, unique-survivor yes/no, surviving answer, load-bearing principles). The orchestrator parses the verdict and does the writing.

### `shared/` and `agents/` conventions

`shared/*.md` files (`answer-procedure.md`, `complete-procedure.md`, `submit-procedure.md`, `get-current-milestone.md`) are single-source-of-truth procedures referenced (never restated) by their skill/agent wrappers via `${CLAUDE_PLUGIN_ROOT}`, and are **execution-neutral** (they take resolved inputs and describe only the core work — no arg-parsing, committing, or return protocol). All readers resolve `<MILESTONE_DIR>` by following `shared/get-current-milestone.md` (reads `milestones/README.md`). Agents live in `agents/<name>.md` with YAML frontmatter and a return protocol section. The new subagent and the extracted `shared/` file must follow these conventions.

## Decisions

## Out of Scope

## Open questions

> **Open question — Recommendation sub-block format:** What exact markdown structure holds the embedded recommendation *beneath* the unchanged one-line question header? It must keep the header a one-line greppable blockquote, be unambiguously bounded so `answer-open-question` can read it and `shared/answer-procedure.md` step 4 can remove it whole, survive sitting adjacent to the next block, and carry the alternatives + recommendation. This is also the shape the read-only subagent returns for the orchestrator to embed.

> **Open question — Record-recommendation trigger:** How does `answer-open-question`'s new mode get selected, given it currently splits its arg on the first `.` (Short Title before, literal answer after)? Is "record the recommendation" a reserved sentinel answer-text phrase (exact match? case-insensitive?), and what happens when the targeted block carries no embedded recommendation (sweep never run, or question added afterward)?

> **Open question — Sweep write model:** Does the orchestrator **commit** its edits (one per question, like `try-answer-all-questions-by-principle`) or leave them staged/uncommitted — and does it therefore need that twin's clean-working-tree precondition? Note the recommend-sweep records **no decisions** and triggers **no cascades** (it only annotates), so the twin's gather-order + per-question live-re-check machinery may be unnecessary here.

> **Open question — Shared extraction boundary:** What exactly moves into the new `shared/` file? Presumably the execution-neutral "alternatives + recommendation for one question" core, leaving each wrapper its own layer — `discuss-open-question` keeps the conversation, "what would change your mind", and follow-up offers; the new subagent keeps its read-only one-shot framing and structured return protocol. Where is the line drawn (mirroring how `answer-procedure.md` is execution-neutral)?

> **Open question — New artifact names:** What are the names of the new orchestrator skill (fan-out `<verb>-all-<plural>` grammar, e.g. `recommend-all-open-questions`) and the singular read-only subagent (e.g. `recommend-open-question`), given `discuss-open-question` is already taken?

> **Deferred — Re-run idempotency:** On re-running the sweep, does it skip blocks that already carry a recommendation, overwrite/refresh them, or make that selectable? A reasonable default (skip already-recommended) exists, so settle this while building.

> **Deferred — Recommendation independence:** Is each per-question recommendation formed in isolation, or may the subagent reference sibling questions/recommendations? The principle-sweep twin sees a shrinking set via cascade; this sweep doesn't cascade, so per-question isolation is the low-risk default — confirm during the work.

