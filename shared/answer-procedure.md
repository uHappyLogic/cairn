# Answer-recording procedure (shared core)

This is the single source of truth for recording an answer to one open question in the
current milestone's `requirements.md`. It is followed in two ways:

- **Inline**, by the `answer-open-question` skill, which runs these steps directly in the
  user's conversation so the recording context survives for follow-up.
- **By an orchestrator**, which runs the same steps once per question it resolves during a sweep.

The wrappers add their own framing (where the title and answer come from, how the outcome
is signalled, any follow-up). This file describes only the recording work itself —
locate, analyse, remove, fold, cascade — and says nothing about how callers obtain their
inputs or wrap the result.

## Inputs

This procedure records one decision given two inputs the caller supplies:

- **SHORT TITLE** — the resolved handle of an existing `<open-question>` block to answer,
  whether `status="open"` or `status="deferred"` (case-insensitive against the block's
  `id`). The caller has already obtained it; locating the matching block is this
  procedure's job.
- **ANSWER** — the answer text for that question.

Locating the block by its Short Title and cascading to mooted entries are shared work
here; obtaining the title and answer is the caller's job.

## Procedure

### 1. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 2. Locate the question

Locating a block by its handle is a deterministic lookup, so query it with the line-oriented
CLI (`awk`/`sed`/`grep`) keyed on the `<open-question …>` / `</open-question>` boundary
lines rather than reading the whole file to eyeball a header. Every `<open-question>` block
lives under the single `## Open questions` section of `<MILESTONE_DIR>/requirements.md`, so
those boundary lines within that one section enumerate the entire question set.

For each `<open-question …>` opening boundary line, pull its `id` attribute with an
attribute-name-anchored regex — `id="([^"]*)"` — so the match is independent of attribute
order (`status` may precede or follow `id`). The captured value is stored **entity-escaped**,
so reverse the five-predefined-entity substitution on it before comparing — replace
`&lt;`→`<`, `&gt;`→`>`, `&quot;`→`"`, `&apos;`→`'`, and `&amp;`→`&` **last**. Then case-fold
both that un-escaped `id` and SHORT TITLE and compare: the block whose `id` case-folds equal
to SHORT TITLE is the match. (This preserves the existing case-insensitive locate contract
with zero regression.)

The matched block spans from its `<open-question …>` opening boundary line through the next
`</open-question>` closing boundary line — one boundary-token pair per block. Open and
deferred blocks share that same pair (they differ only in the `status` attribute value), so
the locate is uniform with no type-specific branch.

If no block's `id` case-folds equal to SHORT TITLE, **stop without changing anything** and
report the mismatch, listing all available ids — deterministically enumerable by pulling
`id="([^"]*)"` from every `<open-question …>` boundary line in the `## Open questions`
section — so the caller can retry.

### 3. Analyse the answer

Before editing, reason about the answer's implications:

- Does it resolve the question completely, or leave a sub-question open?
- Does it introduce a concrete constraint that belongs under `## Decisions`?
- Does it make any other open or deferred entry moot, or force a specific answer to one?
- Does it contradict or supersede anything already written in the document?

This analysis is how you reach the right edits in steps 4–6; it is not itself written into
the document.

### 4. Remove the matched block

Delete the located block from the document — from its `<open-question …>` opening boundary
line through and including its `</open-question>` closing boundary line, the boundary-token
pair found in step 2. This is a deterministic line-range removal, so drive it with the
line-oriented CLI (delete the opening-through-closing line span), not by hand-matching prose.

This covers both cases uniformly: an open block and a deferred block share the one
`<open-question …>` / `</open-question>` boundary-token pair — whether or not the block
carries embedded `<alternative>` / `<applied-principle>` / `<recommendation>` children, the
same opening-through-closing removal clears the whole block with no type-specific branch.

### 5. Fold the decision into `## Decisions`

Add a concise statement under `## Decisions` — in the relevant existing
subsection, or a new subsection if none fits — capturing what was decided and any
constraint it imposes. Write it as **clean prose with no citation marker**: the document
records the decision itself, not where it came from. Match the live document's section
names.

### 6. Cascade to mooted entries

If the decision moots another open or deferred entry or forces its answer, remove that
entry too and fold any implied constraint into `## Decisions` the same way.
Then the document is left in the now-updated state for any further work.

Make steps 4–6 as separate, targeted edits — one per logical change (removal, fold,
cascade) — rather than one large rewrite of a long file.

## Rules

- Title matching is case-insensitive.
- The folded decision is clean prose with no citation marker — never annotate it with its
  provenance.
- Do not rewrite or restructure existing content — only remove the answered entry (and any
  it moots) and add the decisions they produce.
- Do not invent implications not directly supported by the answer text.
- If the answer is ambiguous or incomplete, remove what is clearly resolved and surface the
  rest rather than guessing — never add a brand-new question block to the document.
