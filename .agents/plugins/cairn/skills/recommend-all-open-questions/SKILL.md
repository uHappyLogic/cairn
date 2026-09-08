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

Follow `.agents/plugins/cairn/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`.
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

Use the `Agent` tool with `subagent_type` set to the namespaced registry name of the
`recommend-open-question` agent (singular — the per-question subagent) under this plugin's
namespace — Claude Code lists it as `cairn:recommend-open-question` — one dispatch per surviving
question. Pass it that question's **Short Title**, the `<MILESTONE_DIR>` resolved in step 0, and
the question's full `<open-question>` block — the block text this sweep already holds from its
single gather pass — so it can enumerate honest alternatives:

```
Recommend on this single open question.

Short Title: <Short Title>

Milestone directory: <MILESTONE_DIR>

Question block:
<the question's full <open-question> block>
```

The block is the only requirements text the prompt carries: the subagent reads
`<MILESTONE_DIR>/requirements.md` itself, read-only, for whatever surrounding grounding it needs,
so the orchestrator never reads the whole file to assemble context.

The subagent is **read-only** — it mutates nothing. It returns the ready-to-embed XML sub-elements
as its final message — one `<alternative id="...">` element per option (each with child
`<advantage>` and `<drawback>`), zero or more sibling `<applied-principle>` elements, and one
`<recommendation option="...">` element — and **only** those child elements, never the
`<open-question>` wrapper or the `<question>` element. The orchestrator does **all** the writing.

**Judge every return before it can be embedded, in this fixed order — last-line verdict, then
extraction, then the acceptance gate, then a single repair attempt when the gate rejects.** Each
stage runs only on what the stage before it passed, and the four stages are **one per-return
pipeline**: as each return arrives, judge it, repair it once if judging failed, re-judge what
comes back, then embed or skip.

**a. Last-line verdict (before any extraction).** Read the return's **last non-whitespace line**
first. If that line begins with `FAILED:`, the return is an **explicit failure**: skip that
question alone — embed nothing, leave its `<open-question>` block byte-for-byte untouched, note
its Short Title with the reason (the text after `FAILED:`) for the step-6 advisory — and make no
further attempt on it, even when an `<alternative>`…`</recommendation>` region sits above that
line. Only when the last non-whitespace line is **not** a `FAILED:` line does judging continue,
and a `FAILED:` token appearing anywhere else in the message is then ordinary text with no
special meaning.

**b. Extract the sub-element region.** Take the region running from the line holding the **first
`<alternative`** through the line holding the **last `</recommendation>`**, inclusive, and discard
everything outside it. Surrounding text — a grounding summary above, a closing remark below — is
stripped here, not a failure in itself. If the return holds no `<alternative` line, or no
`</recommendation>` line, extraction fails with the reason `no <alternative> line to extract from`
or `no </recommendation> line to extract to`.

**c. Acceptance gate over the extracted region.** The region is usable only when it passes **all**
of these, checked in the same line-oriented boundary-line CLI idiom as step 1 (`awk`/`sed`/`grep`
over lines and the boundary tokens on them — never a real XML processor, so the gate needs no XML
parser):

1. The region's **first non-whitespace text starts with `<alternative`** (nothing shares the
   opening line ahead of it).
2. The region's **last non-whitespace text ends with `</recommendation>`** (nothing trails it on
   the closing line).
3. The region contains **no `<open-question>`, `</open-question>`, `<question>`, or `</question>`
   line** — the wrapper and question element are the orchestrator's to write, never the return's.
4. The region contains **exactly one `<recommendation` opening line**.
5. The region contains **at least one `<alternative id` line**.
6. The `<recommendation>`'s **`option` value equals one of those `<alternative>` ids** — compared
   after reversing the XML entity escapes (`&amp;`, `&lt;`, `&gt;`, `&quot;`, `&apos;`) on both
   sides and case-folding them.

**Every miss produces a reason string naming the test that failed** (`text precedes <alternative>
on the region's opening line`, `text trails </recommendation> on the region's closing line`, `the
region contains a <question> line`, `the region contains two <recommendation> opening lines`, `the
region contains no <alternative id> line`, `the option value matches no <alternative> id`). A miss
— boundary or structural — is an **extraction failure**, and an extraction failure is never an
immediate skip: it takes the single repair attempt of sub-step d.

**d. Repair once, on arrival.** A return that passed the last-line verdict but failed extraction
(b) or the acceptance gate (c) gets **exactly one** repair attempt before any skip. Repair it **as
it arrives** — the moment its judging fails, while the other dispatches are still in flight —
never by holding failed returns back and running the repairs as a second phase once the slowest
first return has landed.

Carry a **repair-spent marker per question**: unset when the question is dispatched, set the
moment its repair is issued. Repair only a question whose marker is unset, and set that marker as
you issue the repair — first and repaired returns interleave in arbitrary order, so the marker is
what keeps the one attempt from being spent twice. A failing return for a question whose marker is
already set is not repaired again; it goes straight to the skip below.

Repair by whichever of these two branches the host supports, in this order:

- **Continue the same agent session.** Where the host can continue a finished agent session and
  you still hold that dispatch's handle — under Claude Code, `SendMessage` addressed to the agent
  id the `Agent` tool returned — send the corrective message below to **that same agent**. Its
  context is intact, so it re-emits from the analysis it already did.
- **Re-dispatch one fresh agent.** Where the host offers no session-continuation equivalent (as
  under Antigravity), or the handle is gone, dispatch **one** fresh `cairn:recommend-open-question`
  agent for that question with the `Agent` tool, passing the **same prompt** as the original
  dispatch with the corrective message below appended to it as a shape reminder. This second
  dispatch redoes the analysis, so it is the fallback branch, never the preferred one.

Both branches send this fixed one-paragraph corrective message, whose single slot is
`<failed test>`:

```
A previous return for this question could not be used: <failed test>. Emit the sub-elements — the
`<alternative>` elements, then any `<applied-principle>` elements, then the single
`<recommendation>` element — as your whole final message, and check that message against both
shape tests before sending it: its first non-whitespace text starts with `<alternative`, and its
last non-whitespace text ends with `</recommendation>`. Send those sub-elements and nothing else —
no grounding summary above them, no closing remark below them.
```

Fill `<failed test>` with the reason string the failed test already produced in b or c — the same
string the skip advisory would carry — so the one attempt is aimed rather than blind. Never quote
the offending prose back to the agent; the reason string names the test, and the template asks for
the sub-elements and nothing else.

Judge whatever comes back — the same agent's re-emitted message, or the fresh dispatch's return —
by sub-steps a, b and c exactly as a first return is judged: the same last-line verdict, the same
extraction, the same acceptance gate. An accepted region goes to step 4 like any other.

Only a **second** failure — the repaired return's last line begins `FAILED:`, or it misses
extraction or the gate again — is a **skip of that question alone, never a run stop**: embed
nothing for it, leave its `<open-question>` block byte-for-byte untouched, note its Short Title
with that second reason for the step-6 advisory, and carry on with the other questions.

Only an **accepted region** reaches step 4's Edit — never the raw return — so prose, a partial or
explanatory reply, or a returned `<open-question>` wrapper cannot be spliced into
`requirements.md` as XML.

### 4. Embed each returned set of sub-elements

The orchestrator is the sole mutator. Only the regions step 3's acceptance gate accepted reach
this step. Embed each accepted region's sub-elements **inside the existing `<open-question>`
block**, as children of its wrapper. Do this by **whole-block replacement**, not a
line-oriented CLI splice: locate the target `<open-question id="...">…</open-question>` in the
block text the sweep already holds from its single gather pass, and replace it whole with an
exact-string structural `Edit` — the `old_string` is the block as it stands (the
`<open-question …>` boundary tag, its `<question>` element, and the `</open-question>` boundary
tag), and the `new_string` is that same block with the subagent's returned children inserted
between the `<question>` element and the closing `</open-question>` tag. Insert the children at
a **2-space indent per nesting level** relative to the block's base column, matching the depth
of the existing `<question>` child, so the wrapper's boundary tags and `<question>` element
stay byte-for-byte unchanged.

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
`.agents/plugins/cairn/shared/commit-procedure.md`, carrying out its steps yourself. Supply it these two inputs:

- **PATHS** — this run's own change set: `<MILESTONE_DIR>/requirements.md` (the file this sweep
  embedded the sub-elements into in step 4).
- **SUBJECT** — `Recommendation-annotation: <milestone_id>`.

The shared procedure owns the path-scoped staging (never `git add -A`), the dirty-own-path no-op
guard, and the commit. Because that guard is dirty-own-path, a sweep that annotated nothing — every
gathered block already carried a `<recommendation>` element, or every dispatched question was
**still skipped after its repair attempt** in step 3, so step 4 changed no bytes — stages and
commits nothing. This sweep requires **no** clean working tree.

### 6. Report

On the success path, print exactly one fixed terse status line for the whole run —
`Recommendations embedded.` — and nothing more: no annotated-vs-skipped breakdown, no per-question
listing, and no consumer pointer to the `/answer-open-question-with-recommendation` /
`/answer-all-open-questions-with-recommendation` skills.

Alongside that line, print only the questions step 3 **still skipped after the repair path** — a
return whose last non-whitespace line began `FAILED:` (sub-step a), or one that failed extraction
or the acceptance gate **again** after its one repair attempt (sub-step d). List each as an
advisory: its Short Title with the reason it was skipped on (the second reason where a repair was
spent), one per line. This survives the terse-reporting rule because nothing else records it:
the commit and the annotated `requirements.md` show only the questions that *were* annotated, so
a question left un-annotated is git-absent and the console must carry it. Re-running the sweep
retries exactly those blocks, since they still lack a `<recommendation>` element.

A question that **was** annotated gets **no console mention at all**, however its return reached
step 4: whether it arrived clean, whether extraction stripped surrounding text from it (step 3's
sub-step b), or whether it was accepted only after the single repair attempt (sub-step d). The
embedded block in the diff is the whole record, so a recovered return is reported exactly like a
clean one — no recovered-or-repaired listing, no count, no note.

If the sweep committed nothing — its step-5 dirty-own-path no-op guard fired because step 4
changed no bytes — do not print the terse success line; instead print a distinct one-line message
stating that nothing changed and why (every gathered block already carried a `<recommendation>`
element, or every dispatched question was still skipped after its repair attempt in step 3), still
followed by the still-skipped-question advisory when there was one.

If there were no open/deferred questions at all, say so and stop (step 1) — nothing to report.
