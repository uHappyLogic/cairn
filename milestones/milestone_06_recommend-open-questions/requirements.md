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

### Recommendation sub-block format

The embedded recommendation lives inside the **same blockquote** as the one-line question header: a single contiguous run of `>`-prefixed lines, with the header unchanged as line 1, internal gaps rendered as empty `>` lines (never bare blank lines), and the whole block bounded by the blank lines that already separate entries. Beneath the header the fixed shape is: an empty `>` line, then `> **Alternatives:**` followed by one `> - **<Option>** — what it is. *Advantage:* … *Drawback:* …` bullet per option, an empty `>` line, then a stable `> **Recommendation:** <chosen option> — <one-line rationale>` anchor line.

This keeps the header a one-line greppable blockquote (grep for `> **Open question` still hits line 1), makes `shared/answer-procedure.md` step 4 a natural generalization of today's single-line removal ("remove the contiguous blockquote run containing this header"), and gives `answer-open-question`'s record-recommendation mode an unambiguous anchor (the `> **Recommendation:** …` line) to lift as the answer text. The internal-separation discipline — empty `>` lines, never bare blank lines — must be stated in the shared extraction file and the subagent's return protocol so the contiguous-run boundary stays intact. This is also the exact shape the read-only subagent returns for the orchestrator to embed.

### Sweep write model

The recommend-sweep orchestrator is a **mutate-but-do-not-commit** skill, not a committing one. It writes every recommendation sub-block, stages only its own edit (`git add <MILESTONE_DIR>/requirements.md`, path-scoped, never `git add -A`, mirroring the `complete-task` skill and `capture-milestone-principle-updates`), and stops — leaving the staged edits for the user to review and commit or discard. It requires **no** clean working tree.

This follows from the sweep recording **no decisions** and triggering **no cascades** — it only annotates. The `try-answer-all-questions-by-principle` twin commits one auto-answer per commit, and enforces a clean-tree precondition, precisely because each auto-answer is an autonomous *decision* that must be individually reversible and distinguishable from human decisions in git history; a recommendation is transient scaffolding that decides nothing and is consumed (lifted and removed) by `answer-open-question`'s record-recommendation mode. The durable git record is therefore the eventual `Manual-answer:` commit, not the recommendation.

The corollary follows directly: because the document never shrinks under this sweep, it does **not** adopt the twin's one-commit-per-question model, gather-order (cascade-parent-first proxy), or per-question live-re-check/skip machinery. It gathers the open/deferred questions once and walks straight through.

### Record-recommendation trigger

`answer-open-question`'s recommendation-lifting mode is selected by a reserved sentinel **answer text**: `record the recommendation`. The existing `<Short Title>. <answer>` grammar and first-`.` split stay unchanged; the mode fires when the parsed answer text, trimmed and lowercased, matches this phrase as an **exact whole-string match** (not a substring), so a genuine literal answer that merely contains the words is never hijacked. In that mode the skill lifts the embedded `> **Recommendation:** …` anchor line out of the targeted block and uses it as the answer text, rather than taking the arg's literal answer.

When the targeted block carries **no** embedded recommendation (the recommend sweep never ran, or the question was added afterward), lift-mode **stops without changing anything** and reports — directing the user to run the recommend sweep first, or to answer with literal text via `<Title>. <answer>` — and commits nothing, mirroring how `shared/answer-procedure.md` already stops cleanly on a Short-Title mismatch.

### New artifact names

The orchestrator fan-out skill is named `recommend-all-open-questions` and its singular read-only subagent is named `recommend-open-question`. Both keep the `-open-question(s)` family suffix shared with `discuss-open-question` and `answer-open-question`, and both use the verb `recommend` to match the milestone's fixed "recommendation" vocabulary (the `> **Recommendation:**` anchor line and `answer-open-question`'s `record the recommendation` trigger). The pair is kept internally parallel — both carry `-open-question` — rather than adopting the sweep twin's bare `question` (`try-answer-all-questions-by-principle` / `try-answer-question-by-principle`).

### Shared extraction boundary

The new `shared/` file is **execution-neutral** and holds only the analytical core — the substance plus the logical output shape, never its rendering. It owns: the grounding discipline (read real context/code over memory before forming a view); the **Alternatives** requirement (2–4 genuinely realistic options, no strawmen, no padding), where each option carries three logical fields — *what-it-is / key advantage / key drawback*; and the single **Recommendation** (one preferred option with a brief, direct rationale, no hedging, plus the tie-break rule — if two options are equivalent, say so and name what breaks the tie). These are defined as logical content only; the file never spells out concrete rendering.

Each wrapper owns its own rendering, interaction, and side-effects. `discuss-open-question` keeps the conversational opening/framing, the **"what would change your mind"** section, the invite-pushback / continue-the-conversation loop, and the on-decision follow-up offers (`answer-open-question`, and `modify-milestone-goal` when the goal must shift); it edits nothing. The new read-only subagent keeps its one-shot read-only framing, resolving the target question from its prompt, the literal recommendation sub-block markup (the `>`-prefixed contiguous run, the empty-`>` separation discipline, and the `> **Recommendation:**` anchor line — i.e. how the three shared fields render as a blockquote bullet), and its return protocol (emit the block as its final message for the orchestrator to embed).

Two boundary calls are explicit. First, **"what would change your mind" is a `discuss-open-question`-only layer**, not part of the shared core: the goal names the extract as the "alternatives + recommendation" logic, and the recorded *Recommendation sub-block format* decision already fixes the sub-block as Alternatives + a `> **Recommendation:**` anchor with no WWCYM. Second, **the shared file owns the three option fields as logical content while the subagent's return protocol owns their blockquote rendering** — the `>`-markup stays out of the shared file so the extraction does not re-create the duplication it removes. This mirrors how `shared/answer-procedure.md` is execution-neutral (locate/fold/cascade) while its wrappers own arg-parsing and committing.

## Out of Scope

## Open questions

> **Deferred — Re-run idempotency:** On re-running the sweep, does it skip blocks that already carry a recommendation, overwrite/refresh them, or make that selectable? A reasonable default (skip already-recommended) exists, so settle this while building.

> **Deferred — Recommendation independence:** Is each per-question recommendation formed in isolation, or may the subagent reference sibling questions/recommendations? The principle-sweep twin sees a shrinking set via cascade; this sweep doesn't cascade, so per-question isolation is the low-risk default — confirm during the work.

