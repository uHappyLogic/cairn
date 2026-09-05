---
name: recommend-all-open-questions
description: Annotate every open and deferred question in the current milestone's requirements with alternatives and a single recommended option.
---

# recommend-all-open-questions

This is the non-interactive batch path for producing recommendations on open questions. It
walks every open and deferred question in the current milestone and, per question, dispatches
a read-only subagent — the non-interactive twin of `/discuss-open-question` — that returns
**alternatives + a single recommendation** as the `<open-question>` block's XML sub-elements.
The orchestrator is the **sole document mutator**: it embeds each returned set of sub-elements
inside the existing `<open-question>` block, leaving the block's `<open-question …>` /
`</open-question>` boundary tags and its `<question>` element untouched. It is **argument-free**,
records **no decisions**, and triggers **no cascades** — it only annotates. Each embedded
recommendation is consumed later, when it is recorded as an answer, by
`/answer-open-question-with-recommendation` or the
`/answer-all-open-questions-with-recommendation` sweep.

## Usage

```
/recommend-all-open-questions
```

Takes no arguments — it sweeps every `<open-question>` block (both `status="open"` and
`status="deferred"`) in the current milestone's `requirements.md`.

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`.
Never use a hardcoded path.

### 1. Gather the questions once

Fetch the open/deferred set with the line-oriented boundary-line CLI. Every `<open-question>`
block lives under the single `## Open questions` section of `<MILESTONE_DIR>/requirements.md`,
so that section is the one bounded region the CLI slices deterministically. Using `awk`/`sed`/`grep`
keyed on the `<open-question …>` opening and `</open-question>` closing **boundary lines** — never
a real XML processor (`xmllint`) — enumerate every block in document order and, for each, extract
its `id` and `status` (by attribute-name-anchored regex like `id="([^"]*)"` and `status="([^"]*)"`,
so extraction is independent of attribute order) and its `<question>` text. Open and deferred
blocks share one `<open-question …>` / `</open-question>` boundary-token pair distinguished only by
`status`, so the gather ignores type — it lists them all. If there are none, say so and stop.

Keep the full text of each gathered block (from this same pass) in hand — the embed step (step 4)
rewrites the whole block via an exact-string Edit and needs the block's current text as the match
target.

Gather this set **once** and walk it straight through (step 3): **no** gather-order, **no**
per-question live-re-check/skip against the document, and **no** outer re-gather loop. The
gathered list stays valid for the whole run.

### 2. Skip already-recommended blocks (re-run idempotency)

A block already carries a recommendation when it **contains a `<recommendation>` element**. Inspect
each gathered block for one:

- **Skip** any block that already contains a `<recommendation>` element — do not dispatch a
  subagent and do not re-annotate it.
- **Annotate only** blocks that lack one.

**Escape hatch for a stale recommendation:** to force a fresh recommendation on a block whose
recommendation has gone stale, the user **deletes that block's embedded sub-elements** — the
`<alternative>` / `<applied-principle>` / `<recommendation>` children — leaving the
`<open-question>` wrapper and its `<question>` element intact, and re-runs. The block now lacks a
`<recommendation>` element, so skip regenerates it.

### 3. Dispatch the read-only subagent per surviving question

For each **surviving** question (gathered, not skipped), dispatch one read-only subagent. These
dispatches are **independent**: **never feed one question's recommendation into another.** Because
they are independent, they may be run in parallel.

Use the `Agent` tool with `subagent_type: "recommend-open-question"` (singular — the
per-question subagent), one dispatch per surviving question. Pass it that question's **Short
Title** and full block plus surrounding context so it can enumerate honest alternatives:

```
Recommend on this single open question.

Short Title: <Short Title>

Context:
<the question's full <open-question> block, plus relevant surrounding requirements>
```

The subagent is **read-only** — it mutates nothing. It returns the ready-to-embed XML sub-elements
as its final message — one `<alternative id="...">` element per option (each with child
`<advantage>` and `<drawback>`), zero or more sibling `<applied-principle>` elements, and one
`<recommendation option="...">` element — and **only** those child elements, never the
`<open-question>` wrapper or the `<question>` element. The orchestrator does **all** the writing.

**Check the shape of every return before it can be embedded.** A return is usable only when it
is that bare sub-element set: its first non-whitespace text **starts with `<alternative`** and
its last non-whitespace text **ends with `</recommendation>`**. Two returns fail here — one
whose final line is `FAILED: <reason>`, and any return that fails the shape check (prose, a
partial or explanatory reply, an `<open-question>` wrapper, commentary before or after the
elements). Either one is a **skip of that question alone, never a run stop**: embed nothing for
it, leave its `<open-question>` block byte-for-byte untouched, note its Short Title with the
reason (the text after `FAILED:`, or what the shape check rejected) for the step-6 advisory,
and carry on with the other questions. A return that fails this check never reaches step 4's
Edit, so a prose or partial reply cannot be spliced into `requirements.md` as XML.

### 4. Embed each returned set of sub-elements

The orchestrator is the sole mutator. Only returns that passed step 3's shape check reach this
step. Embed each such return's sub-elements **inside the existing `<open-question>` block**, as
children of its wrapper. Do this by **whole-block replacement**, not a line-oriented CLI splice:
locate the target
`<open-question id="...">…</open-question>` in the block text the sweep already holds from its
single gather pass, and replace it whole with an exact-string structural `Edit` — the `old_string`
is the block as it stands (the `<open-question …>` boundary tag, its `<question>` element, and the
`</open-question>` boundary tag), and the `new_string` is that same block with the subagent's
returned children inserted between the `<question>` element and the closing `</open-question>`
tag. Insert the children at a **2-space indent per nesting level** relative to the block's base
column, matching the depth of the existing `<question>` child, so the wrapper's boundary tags and
`<question>` element stay byte-for-byte unchanged.

The block after embedding looks like:

```
<open-question id="Short Title" status="open">
  <question>Question text here.</question>
  <alternative id="Option A">
    what it is
    <advantage>the strongest reason to choose it</advantage>
    <drawback>the main cost or risk it carries</drawback>
  </alternative>
  <alternative id="Option B">
    what it is
    <advantage>…</advantage>
    <drawback>…</drawback>
  </alternative>
  <applied-principle>Short Title</applied-principle>
  <recommendation option="Option A">one-line rationale</recommendation>
</open-question>
```

(The `<applied-principle>` element appears once per bearing principle, or not at all when none
bore; there are one or more `<alternative>` elements and exactly one `<recommendation>`.)

### 5. Commit the annotations

You are the orchestrator, so you commit **once at the end of the run** — here, after every
per-question subagent (step 3) has returned and all their sub-elements are embedded (step 4),
never inside the dispatch loop. Read and follow the shared commit procedure at
`${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you need
to resolve the path), carrying out its steps yourself. Supply it these two inputs:

- **PATHS** — this run's own change set: `<MILESTONE_DIR>/requirements.md` (the file this sweep
  embedded the sub-elements into in step 4).
- **SUBJECT** — `Recommendation-annotation: <milestone_id>`.

The shared procedure owns the path-scoped staging (never `git add -A`), the dirty-own-path no-op
guard, and the commit. Because that guard is dirty-own-path, a sweep that annotated nothing — every
gathered block already carried a `<recommendation>` element, or every dispatched question was
skipped in step 3, so step 4 changed no bytes — stages and commits nothing. This sweep requires **no** clean working tree.

### 6. Report

On the success path, print exactly one fixed terse status line for the whole run —
`Recommendations embedded.` — and nothing more: no annotated-vs-skipped breakdown, no per-question
listing, and no consumer pointer to the `/answer-open-question-with-recommendation` /
`/answer-all-open-questions-with-recommendation` skills.

Alongside that line, if step 3 skipped any question (a `FAILED:` return or one that failed the
shape check), print the skipped questions as an advisory — each one's Short Title with its
reason, one per line. This survives the terse-reporting rule because nothing else records it:
the commit and the annotated `requirements.md` show only the questions that *were* annotated, so
a question left un-annotated is git-absent and the console must carry it. Re-running the sweep
retries exactly those blocks, since they still lack a `<recommendation>` element.

If the sweep committed nothing — its step-5 dirty-own-path no-op guard fired because step 4
changed no bytes — do not print the terse success line; instead print a distinct one-line message
stating that nothing changed and why (every gathered block already carried a `<recommendation>`
element, or every dispatched question was skipped in step 3), still followed by the skipped-question
advisory when there was one.

If there were no open/deferred questions at all, say so and stop (step 1) — nothing to report.
