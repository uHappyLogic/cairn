# Answer-recording procedure (shared core)

This is the single source of truth for recording an answer to one open question in the
current milestone's `requirements.md`. It is followed in two ways:

- **Inline**, by the `answer-open-question` skill, which runs these steps directly in the
  user's conversation so the recording context survives for follow-up.
- **By an orchestrator**, `try-answer-all-questions-by-principle`, which runs the same steps
  once per question it resolves during a sweep.

The wrappers add their own framing (where the title and answer come from, how the outcome
is signalled, any follow-up). This file describes only the recording work itself —
locate, analyse, remove, fold, cascade — and says nothing about how callers obtain their
inputs or wrap the result.

## Inputs

This procedure records one decision given two inputs the caller supplies:

- **SHORT TITLE** — the resolved handle of an existing `Open question` or `Deferred`
  entry to answer (case-insensitive). The caller has already obtained it; locating the
  matching block is this procedure's job.
- **ANSWER** — the answer text for that question.

Locating the block by its Short Title and cascading to mooted entries are shared work
here; obtaining the title and answer is the caller's job.

## Procedure

### 1. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded backlog path.

### 2. Locate the question

Read `<MILESTONE_DIR>/requirements.md`. Find the `Open question — <Short Title>` or
`Deferred — <Short Title>` entry whose title matches SHORT TITLE (case-insensitive). If no
match is found, **stop without changing anything** and report the mismatch, listing all
available titles so the caller can retry.

### 3. Analyse the answer

Before editing, reason about the answer's implications:

- Does it resolve the question completely, or leave a sub-question open?
- Does it introduce a concrete constraint that belongs under `## Implementation decisions`?
- Does it make any other open or deferred entry moot, or force a specific answer to one?
- Does it contradict or supersede anything already written in the document?

This analysis is how you reach the right edits in steps 4–6; it is not itself written into
the document.

### 4. Remove the matched block

Remove the located `Open question` / `Deferred` block from the document entirely.

### 5. Fold the decision into `## Implementation decisions`

Add a concise statement under `## Implementation decisions` — in the relevant existing
subsection, or a new subsection if none fits — capturing what was decided and any
constraint it imposes. Write it as **clean prose with no citation marker**: the document
records the decision itself, not where it came from. Match the live document's section
names.

### 6. Cascade to mooted entries

If the decision moots another open or deferred entry or forces its answer, remove that
entry too and fold any implied constraint into `## Implementation decisions` the same way.
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
