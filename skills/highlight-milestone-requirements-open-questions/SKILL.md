---
name: highlight-milestone-requirements-open-questions
description: Highlight remaining open questions around milestone requirements.
---

# highlight-milestone-requirements-open-questions

The current "work in progress" requirements for the planned milestone are described in the current milestone's `requirements.md`.
The overall goal is to make that file ready enough for the work to begin. It's ok to leave some decisions to settle while doing the work if they are better solved there.

## highlight-milestone-requirements-open-questions

```
/highlight-milestone-requirements-open-questions
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

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Read the milestone requirements

Read `<MILESTONE_DIR>/requirements.md` in full. Identify every stated requirement, constraint, and assumption.

### 2. Identify open questions and gaps

For each requirement, ask:
- Is the expected behavior fully specified, or does it leave choices ambiguous?
- Are there edge cases not addressed?
- Are there dependencies on systems not yet described (e.g., input handling, animation state, physics)?
- Are there performance or architectural constraints implied but not stated?

### 3. Categorise findings

Group your findings into two categories:

**Blocking** — questions that, if left unanswered, would force a wrong approach or require a rewrite. These must be resolved before the work begins.

**Deferred** — decisions that are better made while doing the work (e.g., tuning a lerp speed, choosing a specific easing curve). Note these explicitly so they are not forgotten, but do not block on them.

### 4. Annotate and update the document

Edit `<MILESTONE_DIR>/requirements.md` to add the open questions inline, close to the relevant requirement. Use a clearly marked block:

```
> **Open question — <Short Title>:** <question text>
```

The `<Short Title>` is a 2–5 word phrase that uniquely identifies this question within the document (e.g., "Arc drive technique", "Player input during swing"). It acts as a stable reference handle so questions can be cited by name in conversation and task files. Titles must be unique across all open questions and deferred entries in the document.

For deferred decisions, use:

```
> **Deferred — <Short Title>:** <what will be decided while doing the work>
```

Do not restructure or rewrite the existing content — only add annotations.

## Rules

- Do not invent requirements — only annotate gaps relative to what is already written.
- Do not mark something as blocking if a reasonable choice exists that is low-risk to reverse.
- Do not resolve open questions yourself — surface them for the user to decide.
- Keep annotations brief and question-shaped; avoid writing design proposals inside the document.
- If the requirements are already complete enough for the work to begin, say so explicitly and add no annotations.
