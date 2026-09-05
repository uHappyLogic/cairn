# Answer-with-recommendation procedure (shared core)

This is the single source of truth for recording one open question's **embedded
recommendation** as its answer in the current milestone's `requirements.md`. It composes
over `shared/answer-procedure.md` (the recording core): it lifts the `<recommendation>`
element the recommend sweep embedded in the question block, then delegates the actual
recording to that core unchanged. It is followed inline by the
`answer-open-question-with-recommendation` skill and in isolation by the
`answer-open-question-with-recommendation` agent. The caller supplies the one input below
and wraps the result; this file describes only the work itself — resolve, locate, lift,
delegate.

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

Follow `.agents/plugins/cairn/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 2. Locate the question and its embedded recommendation

Locate the block whose `id` case-folds equal to SHORT TITLE exactly as
`.agents/plugins/cairn/shared/answer-procedure.md` step 2 specifies: the line-oriented CLI
(`awk`/`sed`/`grep`) keyed on the `<open-question …>` / `</open-question>` boundary lines
within the single `## Open questions` section of `<MILESTONE_DIR>/requirements.md`, the `id`
attribute pulled by attribute-name-anchored regex, entity-unescaped, and case-folded against
SHORT TITLE. The matched block spans its opening boundary line through the next
`</open-question>` closing boundary line.

**No-`<recommendation>`-element guard.** If no block's `id` case-folds equal to SHORT TITLE,
or the matched block carries no `<recommendation …>` element (the recommend sweep never
annotated it, or the question was added afterward), **stop without changing anything** and
report why: nothing is recorded.

### 3. Lift the `<recommendation>` element into ANSWER

Within the matched block, read the `<recommendation option="...">…</recommendation>` element
as a single-element CLI read: pull its one `option` attribute (by attribute-name-anchored
regex, `option="([^"]*)"`) and its one text node (the rationale between the tags). Do **not**
dereference the `<alternative id="...">` the `option` names — the `option` value doubles as
the readable option label, so no lookup is needed. Derive ANSWER only from this element,
never from any other (in particular never from a sibling `<applied-principle>`, which keeps
the answer provenance-free by construction), and never invent answer text.

Both the `option` value and the rationale text are stored **entity-escaped**, so reverse the
five-predefined-entity substitution on each — replace `&lt;`→`<`, `&gt;`→`>`, `&quot;`→`"`,
`&apos;`→`'`, and `&amp;`→`&` **last** — to recover clean unescaped text. Derive ANSWER by
recombining the un-escaped `option` value with the un-escaped rationale as
"`<option>` — `<rationale>`" (the old anchor form: the option, then a spaced em dash, then
the rationale). That string is the answer text.

### 4. Delegate to the recording core

Hand the resolved **SHORT TITLE** and the derived **ANSWER** to
`.agents/plugins/cairn/shared/answer-procedure.md` and follow it unchanged. That procedure
owns the recording work (locate, analyse, fold, remove, cascade); this procedure only lifts
and delegates.
