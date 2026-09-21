---
name: review-milestone-requirements
description: Review the current milestone's requirements to reconcile its open questions against recorded decisions, surface new gaps, and report whether it has converged.
---

# review-milestone-requirements

The current "work in progress" requirements for the planned milestone live in two documents of the current milestone directory: `requirements.md` (the prose — goal, relevant starting state, decisions, out of scope) and `open_questions.xml` (one `<open-question>` block per question still open). The overall goal is to make that requirements set ready enough for the work to begin.

This skill is the **repeatable engine** of the requirements-iteration loop — run it each time around:

```
review → (discuss) → answer → review → answer → … → converged → derive-tasks
```

Each pass does three jobs: **reconcile** the existing questions against what's now decided, **surface** the new gaps, and report whether the requirements have **converged**.

Every write this skill makes to `open_questions.xml`, and every listing of its blocks, is a call to the plugin's open-question tool, `python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py <subcommand> <MILESTONE_DIR> …` — that file's sole writer, which owns the document's escaping and layout: a mutator prints nothing on success, `list` prints bare ids one per line, and any failure is one `Error: <reason>` line on stderr with a non-zero exit and the document left unchanged. Reading the document whole to reason over it is the one thing done directly, with the file-reading tool. Never edit `open_questions.xml` yourself.

## review-milestone-requirements

```
/review-milestone-requirements
```

## Milestone requirements document structure

`requirements.md` is prose Markdown in four sections:
```md
# Milestone <milestone_id>: <name>

## Goal

<description of the goal here>

## Relevant starting state

<description of the Relevant starting state>

## Decisions

<subsections with detailed requirements>

## Out of Scope

<what the milestone deliberately leaves out>
```

The open questions live beside it in `<MILESTONE_DIR>/open_questions.xml` — one `<open-question id="Short Title">` block per question under a single root, each holding a `<question>` child and, once the recommend sweep has annotated it, `<alternative>`, `<applied-principle>`, `<depends-on>`, and `<recommendation>` children. No question block is ever placed inline in `requirements.md`.

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded path.

### 1. Read the documents and take inventory

Read `<MILESTONE_DIR>/requirements.md` and `<MILESTONE_DIR>/open_questions.xml` in full with the file-reading tool. That whole read is for reasoning only — every listing of the blocks and every change to the question document below is a tool call. Build a mental inventory of three things, because the rest of the pass plays them against each other:

- the **Decisions** already recorded (what's settled),
- the **`<open-question>` blocks** already present (what's still flagged),
- every stated requirement, constraint, and assumption.

### 2. Reconcile the existing question set

This is the step that makes the skill loop-aware: the documents have been edited since questions were last raised, so the existing blocks may be stale. Tidy them — but only with evidence, and never by answering:

- **Prune a settled block** — remove an `<open-question>` block **only when you can point to an entry already in `## Decisions` that covers it**. This is cleanup of cascade-misses and manual drift, not answering. If you can't cite the covering decision, do not remove it.
- **Dedup repeats** — when two blocks ask materially the same thing, keep the clearest one and remove the other.
- **When in doubt, flag — don't delete.** If a block *looks* answered but no recorded decision clearly covers it, leave it in place and note it in your report as "possibly resolved — confirm". Silently dropping a still-live question destroys tracked state; that's the one outcome to avoid.

Each removal, on either path, is one bare call — no `--option`, since a prune or dedup records nothing:

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py remove <MILESTONE_DIR> "<Short Title>"
```

In that one write the tool deletes the block and strips every block whose embedded analysis depended on it — and every block that depended on those in turn — back to its `<question>`, so no `<depends-on>` tag is left naming a removed or stripped block; a stripped block stays in the document as a live question for the next `/recommend-all-open-questions` pass to regenerate. Stripping decides nothing, records nothing under `## Decisions`, and adds nothing to the step-5 report — the committed diff is its record.

You **never** record a decision, fold an answer into `## Decisions`, or otherwise resolve a question here. Recording answers belongs to `/answer-open-question` alone. This step only shapes the question set to match decisions that already exist — removing settled or repeated blocks, and with them the analysis that depended on them.

### 3. Surface new gaps

Now look for questions the documents don't yet capture — paying special attention to gaps the most recent decisions just **exposed** (a settled decision often raises a fresh downstream choice). For each requirement, ask:

- Is the expected behavior fully specified, or does it leave choices ambiguous?
- Are there edge cases not addressed?
- Are there dependencies on systems not yet described?
- Are there constraints implied but not stated?

Add only genuinely new questions — don't re-raise anything already present (you just inventoried them in step 1), and do not invent requirements: only annotate gaps relative to what is already written.

Author each new finding as one `add` call, the question text as its heredoc body:

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py add <MILESTONE_DIR> "<Short Title>" <<'EOF'
<Question text here.>
EOF
```

The tool appends the block after the existing ones and owns its shape — escaping, indentation, and the fold of the text to one line — so you write plain text, no XML and no entities. What you author is the two judgments the block carries:

- **The question text.** Because a block does not sit next to the requirement it concerns, **each question must stand on its own** — brief, self-contained, and question-shaped, fully understandable without the surrounding context, never a design proposal.
- **The Short Title** (the block's `id`): a 2–5 word phrase that uniquely identifies the question within the document (e.g. "Getting-started section order", "Glossary term scope"). It is the stable handle the question is cited by in conversation and located by in the answering and recommendation skills, which match it **case-insensitively** — so keep every Short Title unique across all blocks even ignoring case. The tool refuses an id an existing block already carries (its `Error:` line names it); pick a distinct title and call again.

Do not restructure or rewrite existing content — `requirements.md` is not edited by this pass, and the question document changes only through the `remove` calls of step 2 and the `add` calls here.

### 4. Commit the reshaped requirements

Read and follow the shared commit procedure at `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`, carrying out its steps yourself. Supply it these two inputs:

- **PATHS** — this skill's own change set, the milestone's two requirements documents: `<MILESTONE_DIR>/open_questions.xml` (where every prune, dedup, and new block of this pass landed) and `<MILESTONE_DIR>/requirements.md`.
- **SUBJECT** — `Requirements-review: <milestone_id>`.

The shared procedure owns the no-op guard, the path-scoped staging, and the commit. Its dirty-own-path guard covers this skill's no-op case: a pass that reconciled, pruned, and surfaced nothing leaves both files unchanged, so nothing is staged and nothing is committed; a pass that reshaped the question set commits that reshaping.

### 5. Report convergence

Run

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py list <MILESTONE_DIR>
```

It prints the Short Title of every `<open-question>` block still in the document, one per line in document order; empty output is a converged document. That print — not your recollection of the pass — is what the two items below are read from.

On the success path, print exactly one fixed terse status line — `Requirements reviewed.` — carrying no identifier (no milestone id, no count, no commit subject). Do **not** re-narrate what the pass reshaped: there is no "What changed this pass" summary (blocks pruned, repeats merged, new questions raised, "possibly resolved — confirm" flags) and no handoff pointer toward `/discuss-open-question` or `/answer-open-question`.

Follow that terse line with only the two pieces of decision-critical state git never captures, so the user knows whether to loop again or move on:

- **What's still open** — the Short Titles `list` printed, one per line. No nudge pointer.
- **Convergence** — `/derive-tasks` requires that **no `<open-question>` block remains**, which is exactly an empty `list`. So:
  - If `list` printed anything → the requirements are **not** ready; the next loop step is to answer them, then re-run this skill.
  - If it printed nothing → say explicitly that the requirements look **ready for `/derive-tasks`**.

**No-op pass.** When the step-4 dirty-own-path guard fires — this pass reconciled, pruned, and surfaced nothing, so both files are unchanged and nothing was committed — do **not** print `Requirements reviewed.` Instead print a single distinct line stating that nothing changed and briefly why (e.g. "No changes — the question set already matched the recorded decisions and no new gaps surfaced."). Still report the still-open list and convergence verdict above, since that state is unchanged but the user still needs it to decide the next loop step.
