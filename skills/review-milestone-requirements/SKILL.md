---
name: review-milestone-requirements
description: Run a review pass over the current milestone's requirements.md to drive its open-questions loop forward — reconcile the existing question set against what's already been decided (prune blocks an existing decision now covers, dedup repeats), surface genuinely new gaps the latest decisions exposed, and report whether the document has converged enough to derive tasks. This is the repeatable engine of the "iterate the requirements" loop: run it after define/specify to open the questions, and re-run it after every answer or two to clean up, raise what the answers newly exposed, and check for convergence. Use it whenever the user wants to "review the requirements", "check what's still open", "see what questions are left", "tidy up the open questions", or "find out if requirements are ready for /derive-tasks". It never answers questions or records decisions itself — it shapes and reports the open-questions state for the answering skills to resolve.
---

# review-milestone-requirements

The current "work in progress" requirements for the planned milestone live in the current milestone's `requirements.md`. The overall goal is to make that file ready enough for the work to begin — it's fine to leave some decisions to settle while doing the work if they're better solved there.

This skill is the **repeatable engine** of the requirements-iteration loop. You don't run it once; you run it each time around the loop:

```
review → (discuss) → answer → review → answer → … → converged → derive-tasks
```

Answering a question almost always exposes the next one, and folding a decision into the document can leave the open-questions section out of date. So each pass does three jobs: **reconcile** the existing questions against what's now decided, **surface** the new gaps, and report whether the document has **converged**. Run it as many times as the loop takes.

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

<list of open questions around the requirements, if any>
```

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded path.

### 1. Read the document and take inventory

Read `<MILESTONE_DIR>/requirements.md` in full. Build a mental inventory of three things, because the rest of the pass plays them against each other:

- the **Decisions** already recorded (what's settled),
- the **Open question** and **Deferred** blocks already present (what's still flagged),
- every stated requirement, constraint, and assumption.

### 2. Reconcile the existing question set

This is the step that makes the skill loop-aware: the document you're reading has been edited since questions were last raised, so the existing blocks may be stale. Tidy them — but only with evidence, and never by answering:

- **Prune a settled block** — remove an `Open question` / `Deferred` block **only when you can point to an entry already in `## Decisions` that covers it**. This is cleanup of cascade-misses and manual drift, not answering. If you can't cite the covering decision, do not remove it.
- **Dedup repeats** — when two blocks ask materially the same thing, keep the clearest one and drop the other.
- **When in doubt, flag — don't delete.** If a block *looks* answered but no recorded decision clearly covers it, leave it in place and note it in your report as "possibly resolved — confirm". Silently dropping a still-live question destroys tracked state; that's the one outcome to avoid.

You **never** record a decision, fold an answer into `## Decisions`, or otherwise resolve a question here. Recording answers belongs to `/answer-open-question` (and the principle sweep) alone. This step only shapes the *questions* section to match decisions that already exist.

### 3. Surface new gaps

Now look for questions the document doesn't yet capture — paying special attention to gaps the most recent decisions just **exposed** (a settled decision often raises a fresh downstream choice). For each requirement, ask:

- Is the expected behavior fully specified, or does it leave choices ambiguous?
- Are there edge cases not addressed?
- Are there dependencies on systems not yet described?
- Are there constraints implied but not stated?

Add only genuinely new questions — don't re-raise anything already present (you just inventoried them in step 1). Categorise each new finding:

**Blocking** — would force a wrong approach or a rewrite if left unanswered. Must be resolved before the work begins.

**Deferred** — better decided while doing the work (e.g. tuning a value, choosing a specific curve). Note it so it isn't forgotten, but it does not block.

Annotate inline, close to the relevant requirement, using a clearly marked block:

```
> **Open question — <Short Title>:** <question text>
```

For deferred decisions:

```
> **Deferred — <Short Title>:** <what will be decided while doing the work>
```

The `<Short Title>` is a 2–5 word phrase that uniquely identifies the question within the document (e.g. "Arc drive technique", "Player input during swing"). It is a stable handle so the question can be cited by name in conversation and by the answering skills. Titles must be unique across all `Open question` and `Deferred` blocks in the document.

Do not restructure or rewrite existing content — only add annotations and apply the reconcile edits from step 2.

### 4. Report convergence

Close the pass by telling the user where the loop stands, so they know whether to go around again or move on:

- **What changed this pass** — blocks pruned (with the covering decision cited), repeats merged, new questions raised, and anything flagged "possibly resolved — confirm".
- **What's still open** — the remaining `Open question` blocks, by Short Title, with a one-line nudge toward `/discuss-open-question` or `/answer-open-question`.
- **Convergence** — `/derive-tasks` requires that **no `> **Open question` blocks remain** (Deferred blocks may carry forward — they're meant to be settled while doing the work). So:
  - If `Open question` blocks remain → the requirements are **not** ready; the next loop step is to answer them, then re-run this skill.
  - If none remain → say explicitly that the requirements look **ready for `/derive-tasks`**, noting any Deferred decisions that will be settled during the work.

## Rules

- Do not invent requirements — only annotate gaps relative to what is already written.
- Do not mark something as blocking if a reasonable, low-risk-to-reverse choice exists.
- Do not resolve open questions or record decisions yourself — surface and shape them for the answering skills to decide.
- Remove a question block only when a recorded decision covers it (cite it) or it's an exact duplicate; otherwise flag, don't delete.
- Keep annotations brief and question-shaped; avoid writing design proposals inside the document.
- If a pass finds nothing to reconcile and no new gaps, say so — and state whether the document has converged.
