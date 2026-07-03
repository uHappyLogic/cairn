---
name: recommend-all-open-questions
description: Non-interactively sweep the current milestone's requirements for open and deferred questions and annotate each one with an embedded recommendation — alternatives plus a single recommended option — produced by dispatching one read-only recommend-open-question subagent per question. Use this to batch the per-question /discuss-open-question deliberation across every question at once, typically right after a /review-milestone-requirements pass, so the questions arrive at /answer-open-question-with-recommendation with a recommendation ready to record. Trigger it whenever the user says things like "recommend on the open questions", "sweep recommendations", "run the recommend sweep", "annotate every question with a recommendation", or "give me a recommendation for each open question". Records no decisions and requires no clean working tree — it only annotates and leaves its edit staged.
---

# recommend-all-open-questions

This is the non-interactive batch path for producing recommendations on open questions. It
walks every open and deferred question in the current milestone and, per question, dispatches
a read-only subagent — the non-interactive twin of `/discuss-open-question` — that returns
**Alternatives + a single Recommendation**. The orchestrator is the **sole document mutator**:
it embeds each returned sub-block directly beneath the **unchanged one-line question header**,
so the header stays a one-line, greppable blockquote and the recommendation lives beneath it.

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
nothing and is later consumed (lifted and removed) by the `/answer-open-question-with-recommendation`
skill/agent pair (or the `/answer-all-open-questions-with-recommendation` batch sweep).

## Usage

```
/recommend-all-open-questions
```

Takes no arguments — it sweeps every `Open question` and `Deferred` entry in the current
milestone's `requirements.md`.

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`.
Never use a hardcoded path.

### 1. Gather the questions once

Read `<MILESTONE_DIR>/requirements.md` in full. Gather **every** `> **Open question — <Short Title>`
and `> **Deferred — <Short Title>` entry, in document order — no reordering. If there are none,
say so and stop.

You gather this set **once** and walk it straight through (step 3). There is **no**
gather-order and **no** outer re-gather loop: because the sweep records no decisions and
triggers no cascades, the question set never shrinks under it, so the gathered list stays valid
for the whole run.

### 2. Skip already-recommended blocks (re-run idempotency)

For each gathered question, inspect its block — the contiguous run of `>`-prefixed lines that
starts at the one-line question header and continues until the first non-`>` line (the blank
line that separates entries). A block already carries a recommendation when that contiguous
`>` run contains a `> **Recommendation:**` anchor line.

- **Skip** any block that already carries a `> **Recommendation:**` anchor — do not dispatch a
  subagent and do not re-annotate it. This makes the sweep idempotent and cheap and preserves
  any hand-edits to an existing recommendation.
- **Annotate only** blocks that lack one. The primary re-run motive — questions newly surfaced
  by a later `/review-milestone-requirements` pass — is exactly this un-annotated set.

**Escape hatch for a stale recommendation:** to force a fresh recommendation on a block whose
recommendation has gone stale, the user **deletes that block's recommendation sub-block**
(leaving the one-line question header intact) and re-runs. The block now lacks a
`> **Recommendation:**` anchor, so skip regenerates it. There is deliberately **no**
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
<the question's full Open question / Deferred block, plus relevant surrounding requirements>
```

The subagent is **read-only** — it reads `requirements.md` and the live code to ground its
alternatives but mutates nothing. It returns a ready-to-embed recommendation sub-block as its
final message (an empty `>` line, `> **Alternatives:**` with one `>`-bullet per option, an
empty `>` line, then a `> **Recommendation:** <chosen option> — <rationale>` anchor line). The
orchestrator does **all** the writing.

### 4. Embed each returned sub-block

The orchestrator is the sole mutator. Embed each returned sub-block **directly beneath the
unchanged one-line question header** — insert its `>`-prefixed lines immediately after the
header line with **no** blank line between, so the whole entry stays **one contiguous `>` run**
with empty-`>` internal separation (never bare blank lines). The one-line
`> **Open question — …` / `> **Deferred — …` header must stay unchanged and greppable as the
block's first line.

The block after embedding looks like:

```
> **Open question — <Short Title>:** <question text>
>
> **Alternatives:**
> - **<Option A>** — what it is. *Advantage:* … *Drawback:* …
> - **<Option B>** — what it is. *Advantage:* … *Drawback:* …
>
> **Recommendation:** <chosen option> — <one-line rationale>
```

### 5. Stage the edit (do not commit)

After writing all the sub-blocks, stage **only** this skill's own edit — path-scoped, **never**
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
- **Which questions were skipped** (already carried a `> **Recommendation:**` anchor).
- Point the user at the consumer: run `/answer-open-question-with-recommendation <Short Title>`
  to lift a single block's embedded recommendation as the recorded answer, or
  `/answer-all-open-questions-with-recommendation` to record every recommendation-bearing
  question's answer in one batch sweep.

If there were no open/deferred questions at all, say so and stop (step 1) — nothing to report.

## Rules

- Takes **no arguments** — sweeps every `Open question` / `Deferred` entry. Add no
  `refresh`/selectable mode.
- Gather the questions **once** and walk straight through: **no** gather-order, **no** outer
  re-gather loop, **no** per-question live-re-check/skip against the document. The set never
  shrinks under this sweep.
- **Skip** any block that already carries a `> **Recommendation:**` anchor; annotate **only**
  blocks that lack one.
- Dispatch **one** read-only `recommend-open-question` subagent per surviving question; treat it
  as read-only (it returns the sub-block, the orchestrator does all writing). The dispatches are
  independent — never feed one question's recommendation into another.
- The orchestrator is the **sole document mutator**: embed each sub-block beneath the unchanged
  one-line header, keeping one contiguous `>` run with empty-`>` separation and the header
  greppable on line 1.
- **Mutate but do not commit**: stage path-scoped `git add <MILESTONE_DIR>/requirements.md`
  only, never `git add -A`, and stop. Require **no** clean working tree.
