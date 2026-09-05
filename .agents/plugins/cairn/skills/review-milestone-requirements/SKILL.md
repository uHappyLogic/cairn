---
name: review-milestone-requirements
description: Review the current milestone's requirements.md to reconcile its open questions against recorded decisions, surface new gaps, and report whether it has converged.
---

# review-milestone-requirements

The current "work in progress" requirements for the planned milestone live in the current milestone's `requirements.md`. The overall goal is to make that file ready enough for the work to begin — it's fine to leave some decisions to settle while doing the work if they're better solved there.

This skill is the **repeatable engine** of the requirements-iteration loop — run it each time around:

```
review → (discuss) → answer → review → answer → … → converged → derive-tasks
```

Each pass does three jobs: **reconcile** the existing questions against what's now decided, **surface** the new gaps, and report whether the document has **converged**.

## review-milestone-requirements

```
/review-milestone-requirements
```

## Milestone requirements document structure

The structure of `requirements.md` is as follows:
```md
# Milestone <milestone_id>: <name>

## Goal

<description of the goal here>

## Relevant starting state

<description of the Relevant starting state>

## Decisions

<subsections with detailed requirements>

## Open questions

<any open questions, each a `<open-question>` XML block>
```

The `## Goal`, `## Relevant starting state`, `## Decisions`, and `## Out of Scope` sections stay prose Markdown. The `## Open questions` section is different: it holds raw, structured `<open-question>` XML blocks (one per question, never inline next to a requirement), queried by line-oriented CLI (`awk`/`sed`/`grep` on the block boundary lines). All `<open-question>` blocks live under this one section.

## Workflow

### 0. Find the current milestone

Follow `.agents/plugins/cairn/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded path.

### 1. Read the document and take inventory

Read `<MILESTONE_DIR>/requirements.md` in full. Build a mental inventory of three things, because the rest of the pass plays them against each other:

- the **Decisions** already recorded (what's settled),
- the **`<open-question>` blocks** already present under `## Open questions` (what's still flagged) — both `status="open"` and `status="deferred"`,
- every stated requirement, constraint, and assumption.

### 2. Reconcile the existing question set

This is the step that makes the skill loop-aware: the document you're reading has been edited since questions were last raised, so the existing blocks may be stale. Tidy them — but only with evidence, and never by answering:

- **Prune a settled block** — remove an `<open-question>` block **only when you can point to an entry already in `## Decisions` that covers it**. Removing a block means deleting it in full, from its `<open-question …>` opening boundary line through its matching `</open-question>` closing boundary line (inclusive). This is cleanup of cascade-misses and manual drift, not answering. If you can't cite the covering decision, do not remove it.
- **Dedup repeats** — when two blocks ask materially the same thing, keep the clearest one and drop the other (again, deleting the loser in full from `<open-question …>` through `</open-question>`).
- **When in doubt, flag — don't delete.** If a block *looks* answered but no recorded decision clearly covers it, leave it in place and note it in your report as "possibly resolved — confirm". Silently dropping a still-live question destroys tracked state; that's the one outcome to avoid.

You **never** record a decision, fold an answer into `## Decisions`, or otherwise resolve a question here. Recording answers belongs to `/answer-open-question` alone. This step only shapes the *questions* section to match decisions that already exist.

### 3. Surface new gaps

Now look for questions the document doesn't yet capture — paying special attention to gaps the most recent decisions just **exposed** (a settled decision often raises a fresh downstream choice). For each requirement, ask:

- Is the expected behavior fully specified, or does it leave choices ambiguous?
- Are there edge cases not addressed?
- Are there dependencies on systems not yet described?
- Are there constraints implied but not stated?

Add only genuinely new questions — don't re-raise anything already present (you just inventoried them in step 1), and do not invent requirements: only annotate gaps relative to what is already written. Categorise each new finding:

**Blocking** — would force a wrong approach or a rewrite if left unanswered. Must be resolved before the work begins. Do not mark something blocking if a reasonable, low-risk-to-reverse choice exists.

**Deferred** — better decided while doing the work (e.g. tuning a value, choosing a specific curve). Note it so it isn't forgotten, but it does not block.

Author each new finding as an `<open-question>` XML block, appended under the single `## Open questions` section (create that section if it does not yet exist). These blocks are **not** placed inline next to the requirement they concern — they all live together in `## Open questions`. Because a block does not sit next to its originating requirement, **each `<question>` must stand on its own** — write it brief, self-contained, and question-shaped, fully understandable without the surrounding context that inline placement used to supply, never a design proposal.

A block you author has exactly three lines: the opening boundary tag, one `<question>` child, and the closing boundary tag. For a blocking (open) question:

```
<open-question id="Short Title" status="open">
  <question>Question text here.</question>
</open-question>
```

For a deferred decision, only the `status` value and the child text change:

```
<open-question id="Short Title" status="deferred">
  <question>What will be decided while doing the work.</question>
</open-question>
```

Author every block to this exact shape — these conventions are the contract the recommendation and answer skills match against, so hold to them precisely:

- **Single-line opening tag, id first.** The `<open-question …>` opening tag is written on one physical line that never wraps, with attributes in id-first order: `id` then `status`, both double-quoted — `<open-question id="…" status="open">`.
- **Boundary tags at the base column.** The `<open-question …>` and `</open-question>` lines both sit at the section's base column (no leading indent under `## Open questions`).
- **`<question>` indented 2 spaces.** The child is nested one level — 2 spaces — under the opening tag. You author only this one child; the `<alternative>` / `<applied-principle>` / `<recommendation>` children are added later by the recommend path.
- **Entity-escape everything.** Both the element text (inside `<question>`) and the attribute values (`id` and `status`) are XML-escaped using the five predefined entities — `&amp;` for `&`, `&lt;` for `<`, `&gt;` for `>`, `&quot;` for `"`, `&apos;` for `'`. Escape any of these characters wherever they appear in the Short Title or the question text.

The `id` is the **Short Title**: a 2–5 word phrase that uniquely identifies the question within the document (e.g. "Getting-started section order", "Glossary term scope"). It is the stable handle the question is cited by in conversation and located by in the answering and recommendation skills, which match it **case-insensitively** — so keep every Short Title unique across all `<open-question>` blocks even ignoring case.

Do not restructure or rewrite existing content — only append the new `<open-question>` blocks and apply the reconcile edits from step 2.

### 4. Commit the reshaped requirements

Read and follow the shared commit procedure at `.agents/plugins/cairn/shared/commit-procedure.md`, carrying out its steps yourself. Supply it these two inputs:

- **PATHS** — this skill's own change set: `<MILESTONE_DIR>/requirements.md` (the file whose `## Open questions` section it reconciled and surfaced into).
- **SUBJECT** — `Requirements-review: <milestone_id>`.

The shared procedure owns the no-op guard, the path-scoped staging, and the commit. Its dirty-own-path guard covers this skill's no-op case: a pass that reconciled, pruned, and surfaced nothing leaves `requirements.md` unchanged, so nothing is staged and nothing is committed; a pass that reshaped the questions section commits that reshaping.

### 5. Report convergence

On the success path, print exactly one fixed terse status line — `Requirements reviewed.` — carrying no identifier (no milestone id, no count, no commit subject). Do **not** re-narrate what the pass reshaped: there is no "What changed this pass" summary (blocks pruned, repeats merged, new questions raised, "possibly resolved — confirm" flags) and no handoff pointer toward `/discuss-open-question` or `/answer-open-question`.

Follow that terse line with only the two pieces of decision-critical state git never captures, so the user knows whether to loop again or move on:

- **What's still open** — the remaining `status="open"` blocks, by Short Title (`id`). No nudge pointer.
- **Convergence** — `/derive-tasks` requires that **no `status="open"` blocks remain** (`status="deferred"` blocks may carry forward — they're meant to be settled while doing the work). So:
  - If any `status="open"` block remains → the requirements are **not** ready; the next loop step is to answer them, then re-run this skill.
  - If none remain → say explicitly that the requirements look **ready for `/derive-tasks`**, noting any `status="deferred"` blocks that will be settled during the work.

**No-op pass.** When the step-4 dirty-own-path guard fires — this pass reconciled, pruned, and surfaced nothing, so `requirements.md` is unchanged and nothing was committed — do **not** print `Requirements reviewed.` Instead print a single distinct line stating that nothing changed and briefly why (e.g. "No changes — the question set already matched the recorded decisions and no new gaps surfaced."). Still report the still-open list and convergence verdict above, since that state is unchanged but the user still needs it to decide the next loop step.
