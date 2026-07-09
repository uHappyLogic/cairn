# Milestone 9: Open-Question XML Format

## Goal

Convert the open-question representation in requirements.md from the one-line Markdown blockquote (with its embedded `>`-run recommendation sub-block) to a well-formed, indented XML block: `<open-question id="Short Title">` containing a `<question>`, one or more `<alternative id="...">` each with child `<advantage>` and `<drawback>` elements, an optional `<applied-principle>`, and a `<recommendation option="...">`. These question blocks become raw structured data that no longer renders as clean Markdown (the surrounding `## Goal`, `## Relevant starting state`, `## Decisions`, and `## Out of Scope` sections stay prose Markdown), traded for deterministic CLI/awk queryability and future UI-parseability. Re-wire the open-question-handling skills to query the artifact via CLI where it pays — deterministic locate, extract, and block removal — and read the whole document only when the operation reasons across it (cascade analysis, reconciliation): review-milestone-requirements authors the new XML, recommend-open-question renders the alternatives/applied-principle/recommendation as XML sub-elements, answer-procedure and answer-with-recommendation-procedure locate/remove the block and lift `<recommendation>` via CLI, and discuss-open-question / recommend-all-open-questions fetch through it. Scope is the open-question block only — TASKS_TODO.md, the milestone pointer, and the Decisions/Goal prose are untouched; no historical or consuming-workspace migration (migrate-workspace is not modified). All modifications to skills and agents must be made through the skill-creator plugin rather than by editing the SKILL.md/agent files directly. Sync CLAUDE.md and README.md (invariants, skill reference, and the Iterating milestone requirements diagram) to the new format and the query-where-it-pays convention.

## Relevant starting state

### Current open-question representation

An open question in `requirements.md` is today a **one-line Markdown blockquote header** optionally followed by an embedded recommendation sub-block, the whole thing forming **one contiguous run of `>`-prefixed lines** bounded by the blank lines separating entries. The header is `> **Open question — <Short Title>:** <question text>` or `> **Deferred — <Short Title>:** <what will be decided while doing the work>`; the `<Short Title>` is a 2–5 word phrase unique across all blocks and is the stable locating handle. When annotated, the recommendation sub-block sits directly beneath the unchanged header (internal gaps rendered as empty `>` lines, never bare blank lines) and looks like:

```
> **Open question — <Short Title>:** <question text>
>
> **Alternatives:**
> - **<Option A>** — what it is. *Advantage:* … *Drawback:* …
> - **<Option B>** — what it is. *Advantage:* … *Drawback:* …
>
> **Applied principle:** <Short Title>
> **Recommendation:** <chosen option> — <one-line rationale>
```

The `> **Recommendation:** <chosen option> — <one-line rationale>` line is the load-bearing **anchor**: it must stay the last line of the run, and it is lifted *verbatim* as the recorded answer. Any `> **Applied principle:**` citation lines stack immediately above it (one per bearing principle, or none). This is clean-rendering Markdown today — the milestone's goal trades that for XML.

### Authoring path — review-milestone-requirements

`skills/review-milestone-requirements/SKILL.md` is the **sole author** of question blocks. Its step 3 emits the one-line `> **Open question — …` / `> **Deferred — …` blockquote inline next to the relevant requirement. The skill also **reconciles** (prunes a block a `## Decisions` entry now covers, dedups repeats) and **reports convergence** (no `> **Open question` blocks remaining is `/derive-tasks`'s precondition; Deferred may carry forward). It reads the whole `requirements.md` in and reasons over it; it does not query via CLI. It never records decisions.

### Recommendation rendering and embedding

`shared/recommend-procedure.md` is the execution-neutral analytical core (inputs: QUESTION) — it grounds in live code + the principle store `milestones/answer_decision_principles.md`, enumerates 2–4 alternatives (what-it-is / advantage / drawback), and states one recommendation, citing any bearing principle. It carries **no `>`-blockquote markup** by design. Two wrappers add the rendering:

- `agents/recommend-open-question.md` — read-only subagent that runs the shared core and, in its step 3, renders the result as the literal `>`-prefixed sub-block above (the empty-`>` separation, the `> **Applied principle:**` lines, and the final `> **Recommendation:**` anchor). Returns only the sub-block (no header) as its final message; mutates nothing.
- `skills/recommend-all-open-questions/SKILL.md` — orchestrator, the **sole document mutator** of the sweep. Gathers every `> **Open question — …` / `> **Deferred — …` entry once, skips any block already carrying a `> **Recommendation:**` anchor (idempotency), dispatches one `recommend-open-question` subagent per surviving question, and embeds each returned sub-block beneath the unchanged one-line header. Stages path-scoped (`git add <MILESTONE_DIR>/requirements.md`), does not commit.

`skills/discuss-open-question/SKILL.md` is the interactive twin: it reads the whole file, locates the block by header, runs the same `shared/recommend-procedure.md` inline, and adds its own "what would change your mind" layer. It edits nothing.

### Answering path — locate, remove, lift

Two composed shared procedures own recording:

- `shared/answer-procedure.md` — execution-neutral recording core (inputs: SHORT TITLE + ANSWER). It **locates** the block by its `Open question — <Short Title>` / `Deferred — <Short Title>` header (case-insensitive), analyses implications, **removes the entire contiguous `>`-prefixed run** (header + any embedded sub-block; the bare one-line header is the degenerate case), folds the decision into `## Decisions` as clean citation-free prose, and cascades to mooted entries. All locating/removal is done by reading the file and matching the header string, not via CLI.
- `shared/answer-with-recommendation-procedure.md` — composes over the core (input: SHORT TITLE only). It locates the block, finds the `> **Recommendation:** <chosen option> — <rationale>` anchor line, **lifts** it (strips the `> **Recommendation:**` label) into ANSWER — with a no-anchor guard that stops cleanly when the block was never annotated — then delegates to `shared/answer-procedure.md`.

The wrappers over these procedures: `skills/answer-open-question/SKILL.md` (literal answers, splits on first `.`, plus a retired-sentinel redirect guard; commits `Manual-answer: <Short Title>`), the `answer-open-question-with-recommendation` **skill** (inline lift + `Recommendation-answer:` commit) and **agent** (`agents/answer-open-question-with-recommendation.md`, isolated file-editing, returns DONE/FAILED), and the `answer-all-open-questions-with-recommendation` orchestrator (sequential per-question agent dispatch; the agent commits, not the orchestrator). Every one of these reads `requirements.md` whole and locates the block by header string — there is **no CLI/awk/grep query layer** anywhere today.

### Milestone resolution

Every open-question skill/procedure resolves `<MILESTONE_DIR>` by following `shared/get-current-milestone.md`, which reads the `Current milestone:` pointer line in `milestones/README.md`. Scope note from the goal: the pointer, `TASKS_TODO.md`, and the `## Decisions`/`## Goal` prose are untouched by this milestone.

### Authoring constraint and documentation to sync

- **skill-creator plugin** — available as the `skill-creator:skill-creator` skill. The goal mandates that all skill/agent modifications go through it rather than by editing `SKILL.md`/agent files directly.
- **CLAUDE.md** — carries the extensive per-skill/-procedure **invariants** describing today's blockquote format, the contiguous-`>`-run removal, and the verbatim-anchor lift; these must be re-synced to the XML format and the query-where-it-pays convention.
- **README.md** — the "### Iterating milestone requirements" section (around line 102) and the per-skill reference describe the one-line greppable blockquote header and the recommendation anchor; both need syncing, as does the Iterating-requirements Mermaid diagram.
- **No migration** — `migrate-workspace` is explicitly out of scope; no historical `requirements.md` (milestones 01–08) or consuming-workspace conversion is performed.

## Decisions

### CLI query tooling

The "locate / extract / remove" operations over `<open-question>` blocks are implemented with line-oriented `awk`/`sed`/`grep` keyed on the `<open-question …>` / `</open-question>` boundary lines, not a real XML processor (`xmllint --xpath`). It is dependency-free (xmllint is not guaranteed in consuming workspaces), it is the only option compatible with `requirements.md` being a Markdown file that no XML parser can read whole, and it matches the plugin's plain-text no-dependency ethos. Its one cost — a load-bearing block whitespace/indentation and boundary-line contract — is exactly what the Deferred "Block indentation spec" commits to pinning down.

### Open/Deferred encoding

Both `Open question` and `Deferred` entries use a single `<open-question>` element distinguished by an explicit `status="open"|"deferred"` attribute — not a separate `<deferred>` element and not an absence-based boolean marker. This keeps the block boundary uniform (one `<open-question …>` / `</open-question>` token pair) for the locate/extract/remove operations that ignore type, confines the lifecycle distinction to one self-describing attribute the convergence check and gather/filters read, and stays consistent with the goal's fixed `<open-question>` element name. An explicit `status` value is more machine-checkable than testing for the absence of a marker.

### Question-block placement

All `<open-question>` XML blocks live under a single dedicated `## Open questions` section rather than inline next to the requirement each concerns. The goal already frames only Goal / Relevant starting state / Decisions / Out of Scope as prose (omitting Open questions from that list), and the document is already laid out this way. Consolidating quarantines the raw, non-rendering XML into one region — keeping the four prose sections clean Markdown, letting authoring append to one place, and giving the CLI one bounded section to slice deterministically when it extracts the whole set. The lost physical adjacency between a question and its originating requirement is immaterial, since locating keys off Short Title, not position; each `<question>` must simply be self-contained enough to stand alone.

### Applied-principle placement

`<applied-principle>` is a direct child of `<open-question>` and a sibling of `<recommendation>` — never a child of `<recommendation>` — with one `<applied-principle>` element per bearing principle rather than a single multi-id element. Keeping the citations siblings of `<recommendation>` leaves the recommendation lift structurally disjoint from them, so extracting `<recommendation>` alone never touches a citation and recorded decisions stay provenance-free by construction. Repeated single-principle elements are the faithful XML analog of today's atomic, independently-greppable one-line-per-principle stacking.

### Recommendation lift mapping

When the answer path lifts a `<recommendation option="...">…</recommendation>` as the recorded answer, the answer text is the `option` attribute value recombined with the element's text as "`<option>` — `<rationale>`" (the old anchor form), and `option="..."` references the winning `<alternative id="...">` by its id. This reproduces today's clean `## Decisions` prose verbatim, keeps CLI extraction a single-element read (one attribute + one text node, no dereferencing) since Short-Title-style ids double as readable labels, and makes `option` a genuine recommendation→alternative link rather than a duplicated free-text string.

## Open questions

> **Open question — Recommendation embed mechanism:** How does `recommend-all-open-questions` insert the subagent's returned alternatives / applied-principle / recommendation XML sub-elements into an existing `<open-question>` block — read the block and rewrite it whole, or splice via CLI? Embedding is a mutation, not a fetch, so the goal's "fetch through it" wording does not settle it, and this is exactly where the read-whole-vs-CLI line must be drawn deliberately.
>
> **Alternatives:**
> - **Read the block and rewrite it whole** — locate the target `<open-question id="...">…</open-question>` in the whole document the sweep already read to gather questions, and replace that block via an exact-string structural Edit with the subagent's `<alternative>`/`<applied-principle>`/`<recommendation>` children inserted. *Advantage:* robust — constructing correctly-indented nested child elements is a structural edit that whole-block replacement handles cleanly, the full document is already in context from the single gather pass (no extra read), and it sits squarely on the goal's "read the whole document when the operation reasons across it" side. *Drawback:* it does not reuse the boundary-keyed CLI locate machinery the answer/query paths use, so the block gets one mutation idiom (Edit) alongside CLI locate/extract/remove elsewhere.
> - **Splice via CLI** — reuse the same line-oriented CLI chosen for locate/extract/remove to insert the returned sub-elements at the block's `</open-question>` boundary line. *Advantage:* one consistent idiom — every block operation goes through the same boundary-keyed CLI. *Drawback:* fragile — unlike whole-block removal (delete lines between markers), inserting multi-line indented XML mid-file must construct correct nesting and indentation and is escaping-heavy, exactly where line-oriented `awk`/`sed` is weakest, risking malformed blocks.
>
> **Recommendation:** Read the block and rewrite it whole — the sweep already holds the entire document from its one gather pass and embedding nested, correctly-indented children is structural construction (the goal's "reason across / read whole" side), not the deterministic locate/extract/remove that CLI is chosen for.

> **Deferred — XML special-char escaping:** The exact rule for escaping `<`, `>`, `&`, and quotes in question text and in the `id` / `option` attribute values (entity-escaping vs CDATA), plus the round-trip un-escape when the recommendation is lifted back into prose — settled while implementing so blocks stay well-formed.
>
> **Alternatives:**
> - **Uniform XML entity-escaping** — Escape the five predefined entities (`&amp;` `&lt;` `&gt;` `&quot;` `&apos;`) everywhere the data can carry a special char — both element text (`<question>`, `<advantage>`, rationale) and the `id`/`option` attribute values — and reverse the substitution (or let the XML reader decode it) when `<recommendation>` is lifted into `## Decisions` prose. *Advantage:* one rule for text and attributes alike, is exactly what a real XML processor emits and consumes so the round-trip is automatic under `xmllint`, and degrades to a small fixed reverse-substitution table (apply `&amp;` last) for line-oriented tooling. *Drawback:* raw blocks read slightly less cleanly when text is entity-dense, and under awk/sed the un-escape map must be applied in the correct order by hand rather than by a parser.
> - **CDATA for element text, entities for attributes (hybrid)** — Wrap free-form text nodes in `<![CDATA[…]]>` so their content stays verbatim, and entity-escape only the `id`/`option` attribute values (CDATA is illegal in attributes). *Advantage:* element text needs no escaping of `<`/`&` and stays maximally human-readable. *Drawback:* two rules instead of one, entity-escaping is still unavoidable for attributes so CDATA buys only a partial win, and the `]]>` sentinel plus multi-line CDATA spans are awkward for the line-oriented extraction the CLI-tooling question may pick.
> - **Minimal escaping by convention** — Keep Short-Title `id`/`option` values plain-word by authoring convention so they never need escaping, and escape only the genuinely unavoidable `&`/`<` in free text. *Advantage:* least visual noise, ids stay clean. *Drawback:* not well-formed in general — question text and rationale can legitimately contain `<`, `>`, `&`, or quotes, so leaning on convention risks malformed blocks, defeating the "stay well-formed" purpose this very question exists to serve.
>
> **Recommendation:** Uniform XML entity-escaping — because attribute values cannot use CDATA at all, entity-escaping is unavoidable for `id`/`option` regardless, so making it uniform across text too gives one deterministic rule that round-trips for free under a real XML processor and reduces to a fixed reverse-substitution map (un-escape `&amp;` last) for line-oriented tools; as a Deferred item the exact reverse-substitution mechanics can be pinned once the CLI query-tooling question lands, but entity-escaping is the safe default to build against now.

> **Deferred — Block indentation spec:** The precise indent depth and style of the well-formed block — decided during implementation, kept consistent enough for whatever the chosen CLI extraction relies on.
>
> **Alternatives:**
> - **2-space indent per nesting level** — each `<open-question>` child (`<question>`, `<alternative>` and its `<advantage>`/`<drawback>`, `<applied-principle>`, `<recommendation>`) is indented two spaces deeper than its parent, boundary tags at the requirement's base column. *Advantage:* compact and readable at the 3–4 levels of nesting these blocks reach, matching the lightweight nesting the surrounding Markdown already uses, and trivially consistent to author. *Drawback:* deep nesting is visually shallow, so mis-nesting is slightly easier to miss by eye than with a wider indent.
> - **4-space indent per nesting level** — same scheme, four spaces per level. *Advantage:* each level is unmistakable, the most forgiving to read when a block nests `<alternative>` → `<advantage>` several deep. *Drawback:* pushes the innermost text far to the right, wrapping long question/rationale lines awkwardly and costing more horizontal room for no functional gain.
> - **Tab indentation** — one tab per nesting level. *Advantage:* width is reader-configurable and the leading whitespace is unambiguously structural. *Drawback:* mixes with the space-indented Markdown around it, renders inconsistently across viewers, and invites space/tab drift that a whitespace-sensitive line-oriented CLI would be least tolerant of.
>
> **Recommendation:** 2-space indent per nesting level, boundary tags at the requirement's base column, applied consistently — it is the most compact fit for the shallow nesting these blocks reach and matches the document's existing style; since the CLI keys on the `<open-question …>`/`</open-question>` boundary lines (and a real XML parser is whitespace-insensitive anyway), interior depth is a readability choice, so lock in 2-space during implementation once the CLI-tooling question settles.

> **Deferred — id match case-sensitivity:** Whether the CLI `id` lookup preserves today's case-insensitive Short-Title matching or tightens to exact-match — a low-risk default (keep case-insensitive) exists; confirm while wiring the locate.
>
> **Alternatives:**
> - **Keep case-insensitive `id` matching** — the CLI `id` lookup lowercases (or otherwise case-folds) both the queried Short Title and the block's `id` attribute before comparing, preserving today's `shared/answer-procedure.md` behavior. *Advantage:* backward-compatible, so users who type a Short Title with different casing than the stored `id` still resolve the block, and no existing skill's locate semantics change. *Drawback:* case-folding adds a small step to every CLI query and a plain `grep`/`xmllint --xpath` on the raw `id` string won't match by default, so the tooling must wrap the fold explicitly.
> - **Tighten to exact case-sensitive match** — the `id` lookup compares the queried Short Title against the `id` attribute byte-for-byte. *Advantage:* the simplest possible CLI query — a literal string match with no normalization, matching how XML attribute values are natively compared. *Drawback:* a behavior regression versus today's case-insensitive locate, so a user passing a differently-cased Short Title (a common typo) silently fails to match, pushing friction onto every answer/discuss/lift call.
>
> **Recommendation:** Keep case-insensitive `id` matching — it is the question's named low-risk default, preserves the current `answer-procedure.md` locate contract with zero behavior regression, and being a Deferred item the exact case-fold mechanism can be finalized against the chosen CLI while wiring the locate.

## Out of Scope

