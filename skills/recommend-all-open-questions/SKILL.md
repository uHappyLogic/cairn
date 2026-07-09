---
name: recommend-all-open-questions
description: Non-interactively sweep the current milestone's requirements for open and deferred questions and annotate each one with an embedded recommendation — alternatives plus a single recommended option — produced by dispatching one read-only recommend-open-question subagent per question. Use this to batch the per-question /discuss-open-question deliberation across every question at once, typically right after a /review-milestone-requirements pass, so the questions arrive at /answer-open-question-with-recommendation with a recommendation ready to record. Trigger it whenever the user says things like "recommend on the open questions", "sweep recommendations", "run the recommend sweep", "annotate every question with a recommendation", or "give me a recommendation for each open question". Records no decisions and requires no clean working tree — it only annotates and leaves its edit staged.
---

# recommend-all-open-questions

This is the non-interactive batch path for producing recommendations on open questions. It
walks every open and deferred question in the current milestone and, per question, dispatches
a read-only subagent — the non-interactive twin of `/discuss-open-question` — that returns
**alternatives + a single recommendation** as the `<open-question>` block's XML sub-elements.
The orchestrator is the **sole document mutator**: it embeds each returned set of sub-elements
inside the existing `<open-question>` block, leaving the block's `<open-question …>` /
`</open-question>` boundary tags and its `<question>` element untouched.

It is **argument-free** and **deliberately simple**, because it records **no decisions** and
triggers **no cascades** — it only annotates. Because the question set never shrinks under it,
four pieces of machinery a decision-recording sweep would need are all unnecessary here:

- **No gather-order.** Ordering questions most-significant → least is a cascade-parent-first
  proxy; there are no cascades here, so ordering buys nothing. Gather once, walk straight through.
- **No per-question live-re-check / skip against a mutating document.** A decision-recording sweep
  re-reads the document before each question because a prior answer's cascade may have removed it.
  Nothing removes a question here, so the gathered set stays valid start to finish.
- **No outer re-gather loop.** Nothing adds or removes questions mid-sweep, so a single pass
  is the fixed point.
- **No clean-working-tree precondition.** A sweep that commits needs one to keep "one commit = one
  answer"; this skill commits nothing, so it needs no clean tree.

The durable git record is the eventual `Recommendation-answer:` commit produced when a
recommendation is recorded — the recommendation itself is transient scaffolding that decides
nothing and is later consumed (the `<recommendation>` element is lifted and its block removed) by
the `/answer-open-question-with-recommendation` skill/agent pair (or the
`/answer-all-open-questions-with-recommendation` batch sweep).

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

You gather this set **once** and walk it straight through (step 3). There is **no**
gather-order and **no** outer re-gather loop: because the sweep records no decisions and
triggers no cascades, the question set never shrinks under it, so the gathered list stays valid
for the whole run.

### 2. Skip already-recommended blocks (re-run idempotency)

A block already carries a recommendation when it **contains a `<recommendation>` element**. Inspect
each gathered block for one:

- **Skip** any block that already contains a `<recommendation>` element — do not dispatch a
  subagent and do not re-annotate it. This makes the sweep idempotent and cheap and preserves
  any hand-edits to an existing recommendation.
- **Annotate only** blocks that lack one. The primary re-run motive — questions newly surfaced
  by a later `/review-milestone-requirements` pass — is exactly this un-annotated set.

**Escape hatch for a stale recommendation:** to force a fresh recommendation on a block whose
recommendation has gone stale, the user **deletes that block's embedded sub-elements** — the
`<alternative>` / `<applied-principle>` / `<recommendation>` children — leaving the
`<open-question>` wrapper and its `<question>` element intact, and re-runs. The block now lacks a
`<recommendation>` element, so skip regenerates it. There is deliberately **no**
`refresh`/selectable mode — this delete-and-re-run hatch covers staleness and keeps the skill
argument-free.

### 3. Dispatch the read-only subagent per surviving question

For each **surviving** question (gathered, not skipped), dispatch one read-only subagent. These
dispatches are **independent** — a recommendation decides nothing, so nothing may build on one.
**Never feed one question's recommendation into another.** Because they are independent, they
may be run in parallel.

Use the `Agent` tool with `subagent_type: "recommend-open-question"` (singular — the
per-question subagent), one dispatch per surviving question. Pass it that question's **Short
Title** and full block plus surrounding context so it can enumerate honest alternatives:

```
Recommend on this single open question.

Short Title: <Short Title>

Context:
<the question's full <open-question> block, plus relevant surrounding requirements>
```

The subagent is **read-only** — it reads `requirements.md` and the live code to ground its
alternatives but mutates nothing. It returns the ready-to-embed XML sub-elements as its final
message — one `<alternative id="...">` element per option (each with child `<advantage>` and
`<drawback>`), zero or more sibling `<applied-principle>` elements, and one
`<recommendation option="...">` element — and **only** those child elements, never the
`<open-question>` wrapper or the `<question>` element. The orchestrator does **all** the writing.

### 4. Embed each returned set of sub-elements

The orchestrator is the sole mutator. Embed each returned set of sub-elements **inside the
existing `<open-question>` block**, as children of its wrapper. Do this by **whole-block
replacement**, not a line-oriented CLI splice: locate the target
`<open-question id="...">…</open-question>` in the block text the sweep already holds from its
single gather pass, and replace it whole with an exact-string structural `Edit` — the `old_string`
is the block as it stands (the `<open-question …>` boundary tag, its `<question>` element, and the
`</open-question>` boundary tag), and the `new_string` is that same block with the subagent's
returned children inserted between the `<question>` element and the closing `</open-question>`
tag. Insert the children at a **2-space indent per nesting level** relative to the block's base
column, matching the depth of the existing `<question>` child, so the wrapper's boundary tags and
`<question>` element stay byte-for-byte unchanged.

The CLI is deliberately scoped to locate/extract (step 1) and never used to splice mid-block:
constructing correctly-indented nested children is structural construction the read-whole Edit
idiom handles cleanly, where escaping-heavy line-oriented insertion is weakest.

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

### 5. Stage the edit (do not commit)

After writing all the sub-elements, stage **only** this skill's own edit — path-scoped, **never**
`git add -A`:

```
git add <MILESTONE_DIR>/requirements.md
```

Then **stop**, leaving the staged edit for the user to review and commit or discard. This skill
**does not commit** and requires **no** clean working tree. It records no decisions and triggers
no cascades, so it needs neither a one-commit-per-question model nor a clean-tree
precondition — the durable git record is the eventual `Recommendation-answer:` commit, not the
transient recommendation scaffolding.

### 6. Report

Report once:

- **Which questions were annotated** (dispatched and embedded this run).
- **Which questions were skipped** (already contained a `<recommendation>` element).
- Point the user at the consumer: run `/answer-open-question-with-recommendation <Short Title>`
  to lift a single block's embedded recommendation as the recorded answer, or
  `/answer-all-open-questions-with-recommendation` to record every recommendation-bearing
  question's answer in one batch sweep.

If there were no open/deferred questions at all, say so and stop (step 1) — nothing to report.

## Rules

- Takes **no arguments** — sweeps every `<open-question>` block (`status="open"` and
  `status="deferred"`). Add no `refresh`/selectable mode.
- Gather the questions **once** via the boundary-line CLI and walk straight through: **no**
  gather-order, **no** outer re-gather loop, **no** per-question live-re-check/skip against the
  document. The set never shrinks under this sweep.
- **Skip** any block that already contains a `<recommendation>` element; annotate **only** blocks
  that lack one.
- Dispatch **one** read-only `recommend-open-question` subagent per surviving question; treat it
  as read-only (it returns the XML sub-elements, the orchestrator does all writing). The dispatches
  are independent — never feed one question's recommendation into another.
- The orchestrator is the **sole document mutator**: embed each returned set of sub-elements inside
  the existing `<open-question>` block by whole-block-replacement `Edit` (not a CLI splice),
  inserting the children at 2-space-per-level indent and leaving the `<open-question …>` /
  `</open-question>` boundary tags and the `<question>` element unchanged.
- **Mutate but do not commit**: stage path-scoped `git add <MILESTONE_DIR>/requirements.md`
  only, never `git add -A`, and stop. Require **no** clean working tree.
