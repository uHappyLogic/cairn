# Answer-with-recommendation procedure (shared core)

This is the single source of truth for recording one open question's **embedded
recommendation** as its answer in the current milestone's `requirements.md`. It composes
over `shared/answer-procedure.md` (the recording core): it lifts the `<recommendation>`
element the recommend sweep embedded in the question block, then delegates the actual
recording to that core unchanged. It is followed in two ways:

- **Inline**, by the `answer-open-question-with-recommendation` skill, which runs these
  steps directly in the user's conversation so the recording context survives for
  follow-up.
- **In isolation**, by the `answer-open-question-with-recommendation` agent, which runs the
  same steps in a throwaway subagent context for the
  `answer-all-open-questions-with-recommendation` sweep.

The wrappers add their own framing (where the title comes from, how the outcome is
signalled, committing, any follow-up). This file describes only the work itself — resolve,
locate, lift, delegate — and says nothing about how callers obtain their input or wrap the
result.

## Inputs

This procedure records one recommendation-derived answer given one input the caller
supplies:

- **SHORT TITLE** — the resolved handle of an existing `<open-question>` block to answer,
  whether `status="open"` or `status="deferred"` (case-insensitive against the block's
  `id`). The caller has already obtained it; locating the matching block, lifting its
  `<recommendation>` element, and delegating the recording are this procedure's job.

The ANSWER is **not** an input here — this procedure *derives* it by lifting the block's
embedded `<recommendation>` element. That derived ANSWER, together with SHORT TITLE, is what
it hands to `shared/answer-procedure.md`.

## Procedure

### 1. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 2. Locate the question and its embedded recommendation

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
to SHORT TITLE is the match. The matched block spans from its `<open-question …>` opening
boundary line through the next `</open-question>` closing boundary line — one boundary-token
pair per block, shared by open and deferred blocks (they differ only in the `status`
attribute value), so the locate is uniform with no type-specific branch.

**No-`<recommendation>`-element guard.** If no block's `id` case-folds equal to SHORT TITLE,
or the matched block carries no `<recommendation …>` element (the recommend sweep never
annotated it, or the question was added afterward), **stop without changing anything** and
report why. This mirrors `shared/answer-procedure.md`'s clean stop on a Short-Title
mismatch: nothing is recorded.

This locating is a **read** to derive the answer — it is not the recording core's own
locate/remove step, which runs later inside the delegated procedure.

### 3. Lift the `<recommendation>` element into ANSWER

Within the matched block, read the `<recommendation option="...">…</recommendation>` element
as a single-element CLI read: pull its one `option` attribute (by attribute-name-anchored
regex, `option="([^"]*)"`) and its one text node (the rationale between the tags). Do **not**
dereference the `<alternative id="...">` the `option` names — the `option` value doubles as
the readable option label, so no lookup is needed.

Both the `option` value and the rationale text are stored **entity-escaped**, so reverse the
five-predefined-entity substitution on each — replace `&lt;`→`<`, `&gt;`→`>`, `&quot;`→`"`,
`&apos;`→`'`, and `&amp;`→`&` **last** — to recover clean unescaped text. Derive ANSWER by
recombining the un-escaped `option` value with the un-escaped rationale as
"`<option>` — `<rationale>`" (the old anchor form: the option, then a spaced em dash, then
the rationale). That string is the answer text.

### 4. Delegate to the recording core

Hand the resolved **SHORT TITLE** and the derived **ANSWER** to
`${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` and follow it unchanged. That procedure
owns the recording work (locate, analyse, remove, fold, cascade); this procedure only lifts
and delegates.

## Rules

- Title matching is case-insensitive (case-fold both the un-escaped `id` and SHORT TITLE).
- Derive ANSWER only from the block's `<recommendation>` element — its `option` attribute
  recombined with its text as "`<option>` — `<rationale>`" — never from any other element
  (in particular never from a sibling `<applied-principle>`, which keeps the answer
  provenance-free by construction), and never invent answer text.
- The no-`<recommendation>`-element guard is a clean stop: when no block matches or the
  matched block carries no `<recommendation>` element, change nothing and record nothing.
- Do not restate `shared/answer-procedure.md`'s locate/analyse/remove/fold/cascade steps —
  reference it and let it own the recording; this file's job is only lift-then-delegate.
