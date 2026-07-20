---
name: specify-milestone-starting-state
description: Analyze the project's existing state and fill the "Relevant starting state" section of a milestone's requirements.md with context that supports future decisions.
---

# specify-milestone-starting-state

Reads the milestone goal, explores the project's existing state, and writes a concise summary into the `## Relevant starting state` section of `requirements.md`. The output is reference material — not decisions — to ground the `## Decisions` conversation that follows.

## Usage

```
/specify-milestone-starting-state <milestone_id>
```

- `<milestone_id>`: the milestone directory name under `milestones/`, e.g. `milestone_12_user-guide`.

**Example:**
```
/specify-milestone-starting-state milestone_12_user-guide
```

## Workflow

### 1. Locate the milestone

Resolve `milestones/<milestone_id>/requirements.md`. If the file does not exist, stop and report that the milestone was not found — suggest running `/define-milestone-goal` first.

### 2. Read the goal

Read `requirements.md` in full. Extract the `## Goal` section. This is the lens for everything that follows — only surface starting state that is directly relevant to achieving or building on that goal.

### 3. Load the environment and explore the project

Read `CLAUDE.md` at the workspace root for the project's environment. If it carries no description of the project's domain context or working conventions, suggest the user run `/init` to enrich it first — richer project context yields a sharper starting-state summary — then proceed with whatever the project reveals.

Extract from `CLAUDE.md`:
- The project's domain context — what the project is and how its material is organized; use this to anchor all exploration
- Working conventions — the practices the project follows
- Available tools — whether any tools (including MCP tools) are available for deeper inspection
- How work is verified as done — the project's convention for confirming a deliverable meets its bar

Using the goal as a filter, investigate the areas the project documents in `CLAUDE.md`. Focus on:

- **Existing artifacts relevant to the goal** — find the artifacts, sections, and components whose names or responsibilities overlap with the goal. Read what they expose — their outward-facing surface. Skip internal detail.
- **Existing capabilities** — if the goal builds on something that already exists, describe its current state and how other work connects to it.
- **Supporting materials** — note any settings, reference data, or structures the milestone will likely touch.
- **Known gaps** — if the goal requires something that clearly does not exist yet, state it as a gap.

Do not exhaustively catalog everything — stay goal-relevant. Depth over breadth: a precise description of one related area is more useful than a surface mention of ten.

Use `find`, `grep`, and `Read` for file-based exploration. If MCP tools are documented in `CLAUDE.md` and are relevant to exploration, use them.

### 4. Write the starting state

Draft the `## Relevant starting state` section. Structure it as named subsections, one per relevant system or area:

```markdown
## Relevant starting state

### <System Name>

<2–5 sentences: what exists, where it lives, what it exposes, and any known limitations relevant to the goal.>

### <Another System>

...
```

Keep each subsection tight. The audience is someone who will use this to make decisions — they need facts, not commentary.

### 5. Update the file

Replace the (empty) `## Relevant starting state` section in `requirements.md` with the drafted content. Do not modify any other section.

### 6. Commit the starting state

Read and follow the shared commit procedure at `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path), carrying out its steps yourself. Supply it these two inputs:

- **PATHS** — this skill's own change set: `milestones/<milestone_id>/requirements.md` (the file whose `## Relevant starting state` section it just filled).
- **SUBJECT** — `Starting-state: <milestone_id>`.

The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit; do not restate those mechanics here.

### 7. Confirm

On the success path — the commit in step 6 recorded the filled-in starting state — print exactly one fixed terse status line and nothing else:

```
Starting state recorded.
```

Do not add the milestone id, the count of systems documented, or a next-step pointer; the committed diff and git log are the durable record.

If instead the step-6 dirty-own-path guard fired (`requirements.md` was unchanged, so nothing was committed), do not print the terse line — print a single concise line stating that nothing changed and briefly why, e.g. `No change — the starting state was already up to date; nothing committed.`

## Rules

- Only write what currently exists in the project. Do not describe intended behavior or speculate about future state.
- Do not propose decisions — that is for `/review-milestone-requirements` and `/discuss-open-question`.
- If a system is missing entirely, say so in one sentence and move on. Do not design its replacement here.
- Do not overwrite `## Goal`, `## Decisions`, or `## Out of Scope`.
