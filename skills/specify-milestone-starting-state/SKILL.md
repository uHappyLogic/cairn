---
name: specify-milestone-starting-state
description: Analyze the current codebase and fill the "Relevant starting state" section of a milestone's requirements.md with technical context that supports future decisions.
---

# specify-milestone-starting-state

Reads the milestone goal, explores the current project's codebase, and writes a concise technical summary into the `## Relevant starting state` section of `requirements.md`. The output is reference material — not decisions — to ground the `## Decisions` conversation that follows.

## Usage

```
/specify-milestone-starting-state <milestone_id>
```

- `<milestone_id>`: the milestone directory name under `milestones/`, e.g. `milestone_12_player-shooting`.

**Example:**
```
/specify-milestone-starting-state milestone_12_player-shooting
```

## Workflow

### 1. Locate the milestone

Resolve `milestones/<milestone_id>/requirements.md`. If the file does not exist, stop and report that the milestone was not found — suggest running `/define-milestone-goal` first.

### 2. Read the goal

Read `requirements.md` in full. Extract the `## Goal` section. This is the lens for everything that follows — only surface starting state that is directly relevant to achieving or building on that goal.

### 3. Load the environment and explore the codebase

Read `CLAUDE.md` at the workspace root for the project's environment. If it carries no description of the tech stack or file organization, suggest the user run `/init` to enrich it first — richer project context yields a sharper starting-state summary — then proceed with whatever the codebase reveals.

Extract from `CLAUDE.md`:
- File organization / directory layout — the directories that contain meaningful code; use these to anchor all exploration
- Available MCP tools — whether any MCP tools are available for deeper inspection

Using the goal as a filter, investigate the project under the directories documented in `CLAUDE.md`. Focus on:

- **Source files relevant to the goal** — find files, classes, modules, and components whose names or responsibilities overlap with the goal. Read their public API (exported functions/classes/types/interfaces). Skip internal detail.
- **Existing features** — if the goal builds on an existing system, describe its current behavior and exposed integration points.
- **Configuration and data** — note relevant config files, schemas, database models, or data structures that the milestone will likely touch.
- **Known gaps** — if the goal requires something that clearly does not exist yet, state it as a gap.

Do not exhaustively catalog everything — stay goal-relevant. Depth over breadth: a precise description of one related system is more useful than a surface mention of ten.

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

### 6. Confirm

Report:
- Which milestone was updated.
- How many systems/areas were documented.
- Suggest the next step: `/highlight-milestone-requirements-open-questions` to surface gaps and ambiguities before deriving the task list.

## Rules

- Only write what currently exists in the codebase. Do not describe intended behavior or speculate about future state.
- Do not propose decisions — that is for `/highlight-milestone-requirements-open-questions` and `/discuss-open-question`.
- If a system is missing entirely, say so in one sentence and move on. Do not design its replacement here.
- Do not overwrite `## Goal`, `## Decisions`, or `## Out of Scope`.
- Do not commit — leave staging to the user.
