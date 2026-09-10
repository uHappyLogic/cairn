# Answer-recording procedure (shared core)

This is the single source of truth for recording an answer to one open question in the
current milestone's `requirements.md`. It is followed inline by the `answer-open-question`
skill and once per resolved question by an orchestrator sweeping several. The caller
supplies the inputs below and wraps the result; this file describes only the recording
work itself — locate, analyse, fold, remove, cascade.

## Inputs

This procedure records one decision given three inputs the caller supplies, the third
optional:

- **SHORT TITLE** — the resolved handle of an existing `<open-question>` block to answer,
  whether `status="open"` or `status="deferred"` (case-insensitive against the block's
  `id`). The caller has already obtained it; locating the matching block is this
  procedure's job.
- **ANSWER** — the answer text for that question.
- **RECORDED OPTION** *(optional)* — the un-escaped option or alternative id the caller
  lifted as the decision, when it lifted one: the block's `<recommendation option="…">`
  value or the chosen `<alternative id="…">` value, with entity escapes already reversed.
  Its presence is the comparison-mode discriminator for step 6's dependency
  reconciliation: supplied, the recorded option is compared to each dependent's assumed
  option as an exact id; absent, the procedure judges whether ANSWER invalidates that
  assumed option. The caller either passes it or passes nothing — this procedure never
  derives it by parsing ANSWER, whose form is the caller's own convention.

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
to SHORT TITLE is the match.

The matched block spans from its `<open-question …>` opening boundary line through the next
`</open-question>` closing boundary line — one boundary-token pair per block, shared by open
and deferred blocks alike.

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
the document. Do not invent implications the answer text does not directly support, and if
the answer is ambiguous or incomplete, remove what is clearly resolved and surface the rest
rather than guessing — never add a brand-new question block to the document.

### 4. Fold the decision into `## Decisions`

Add a concise statement under `## Decisions` — in the relevant existing
subsection, or a new subsection if none fits — capturing what was decided and any
constraint it imposes. Write it as **clean prose with no citation marker**: the document
records the decision itself, not where it came from. Match the live document's section
names.

Write this edit **before** removing the answered block in step 5; the recorded decision
always lands first.

### 5. Remove the answered block

Delete the block located in step 2 from the document — from its `<open-question …>` opening
boundary line through and including its `</open-question>` closing boundary line. The step 4
fold has shifted the line numbers step 2 reported, so re-run that same boundary-line query
first to get the block's current opening and closing lines, then delete that span. This is a
deterministic line-range removal, so drive it with the line-oriented CLI (delete the
opening-through-closing line span), not by hand-matching prose.

The same opening-through-closing removal clears the whole block whether or not it carries
embedded `<alternative>` / `<applied-principle>` / `<depends-on>` / `<recommendation>`
children.

### 6. Cascade to mooted entries and reconcile dependents

If the decision moots another open or deferred entry or forces its answer, fold any implied
constraint into `## Decisions` the same way and remove that entry too.

Then reconcile dependency declarations. The recommend sweep may have embedded in any block
a self-closing `<depends-on question="…" option="…"/>` child recording that the block's
recommendation assumed a sibling's option. Once the answered block and every mooted entry
are removed, collect the `id`s of those removed blocks and query every surviving block under
`## Open questions` for `<depends-on` lines whose `question` attribute — pulled by
attribute-name-anchored regex, entity-unescaped, and case-folded exactly as step 2 matches
`id` — names one of them. Each such dependent takes one of two outcomes, decided by holding
its tag's un-escaped `option` value against what was actually recorded:

- **Agreeing — remove the tag only.** The target is the answered block and the dependent's
  assumed option is the recorded one: with RECORDED OPTION supplied, the two un-escaped,
  case-folded ids are equal; without it, the ANSWER prose plainly leaves the assumed
  option standing. Delete that one `<depends-on …/>` line and nothing else in the block —
  its alternatives, citations, and recommendation stand.
- **Disagreeing — strip the children.** Everything else: the ids differ, the judgment is
  inconclusive, or the target was removed as a mooted entry (no option was recorded for
  it, so there is nothing to agree with). Delete every child line between the block's
  `<question>` element and its `</open-question>` closing line — all its `<alternative>`,
  `<applied-principle>`, `<depends-on>`, and `<recommendation>` children — leaving the bare
  `<open-question …>` wrapper and `<question>` element for the next recommend sweep to
  regenerate. Strip on doubt: whenever the agreeing case cannot be affirmed, this branch
  applies.

Stripping is **transitive**: a stripped block's own dependents assumed a recommendation
that no longer exists, so every surviving block whose `<depends-on question="…">` names a
stripped block is stripped the same way, repeating until no `<depends-on>` names a block
removed or stripped in this run. A stripped block records no decision and is never removed,
and this reconciliation produces no report of its own — the edited document is its record.

Then the document is left in the now-updated state for any further work.

Make steps 4–6 as separate, targeted edits — one per logical change (fold, removal,
cascade, reconciliation) — rather than one large rewrite of a long file, and do not otherwise
rewrite or restructure existing content: only remove the answered entry and any it moots,
add the decisions they produce, and delete the dependency tags or embedded children this
step reconciles.
