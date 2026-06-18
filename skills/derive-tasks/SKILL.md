---
name: derive-tasks
description: Convert the current milestone's requirements.md into a complete, dependency-ordered TASKS_TODO.md. Decomposes the milestone into high-level task briefs, proves every requirement is covered, then delegates the detailed authoring of each task to the submit-task agent.
---

# derive-tasks

Reads the current milestone requirements and derives a complete, dependency-ordered list of tasks into `TASKS_TODO.md`, ready for AI-driven completion via `/complete-task`.

Your job here is **decomposition and coverage**, not task authoring. You split the milestone into high-level task briefs and prove that those briefs cover every requirement — that whole-milestone view is the thing most likely to break if you get lost in file-paths and method names. The detailed, per-task technical authoring (the contract surface, notes, exact paths, success criteria) is delegated, one task at a time, to the `submit-task` agent. That keeps each task's technical reasoning out of your context so your attention stays on completeness and ordering.

This mirrors the completion side: `complete-all-tasks` orchestrates and `complete-task` does the per-task work in a clean context. Here, you orchestrate and `submit-task` (the agent) does the per-task authoring.

## Usage

```
/derive-tasks
```

No arguments. The skill always reads from and writes to the current milestone directory.

## Preconditions

- All open questions in the current milestone's `requirements.md` must be resolved (no `> **Open question` blocks remain).
- `TASKS_TODO.md` should be empty or contain only stale tasks from a previous milestone; this skill replaces its contents.

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded backlog path.

### 1. Read source documents

Read `CLAUDE.md` at the workspace root for the project's tech stack, file organization, and conventions. If it carries no such description, suggest the user run `/init` first — decomposition is sharper when grounded in the real environment — then proceed.

Read `<MILESTONE_DIR>/requirements.md` in full, plus any files referenced in its **Relevant starting state** section, so you understand the exact starting point.

### 2. Check for unresolved open questions

Scan `requirements.md` for any `> **Open question` blocks. If any exist, stop immediately and output:

```
Cannot derive tasks: the following open questions must be resolved first:
- <Short Title>
- ...

Run /answer-open-question for each one, then re-run /derive-tasks.
```

### 3. Decompose into high-level task briefs

Break the milestone into discrete, independently-implementable task briefs. A **brief** is high-level — it names the affected system, the desired behavior, and how it would be verified. It does **not** contain file paths, method names, contract surface, or success criteria; that detail is the agent's job. Keeping briefs high-level is deliberate: it lets you hold many more of them in mind at once and reason about whether they cover everything.

Apply these rules:

- **Atomic scope** — each brief must be completable in a single `/complete-task` invocation, with no mid-task decisions. "Do X and Y" is two briefs when X and Y can be built and verified independently.
- **One system per brief** — group by the technology boundary or layer it touches, as defined by the file organization in `CLAUDE.md` (e.g. backend API / frontend component / DB schema; or for Unity: scripts / prefabs / scene hierarchy). Do not mix layers unless they are inseparable.
- **No "nice to have" briefs** — only what the spec states. Do not pad the task list.

### 4. Prove coverage (requirement → task matrix)

This is the step that most directly fixes "the task list missed something." Re-read `requirements.md` bullet by bullet and build a traceability matrix mapping **every** requirement, constraint, and behavioral detail to at least one brief:

```
| Requirement (quote/paraphrase) | Covered by brief |
|--------------------------------|------------------|
| ...                            | <brief title>    |
```

- Every requirement must map to ≥1 brief. If a requirement maps to none, you have a gap — add a brief (or note why it's already satisfied by existing code per the **Relevant starting state**).
- If a requirement is already satisfied by the current implementation, mark it so and do not create a brief for it.
- Do not invent requirements that aren't in the spec.

Do not proceed until the matrix has no unexplained gaps.

### 5. Order the briefs by dependency

Order briefs so each one's prerequisites come first: a brief that creates a module, schema, or shared utility must precede any brief that imports or references it. The top of `TASKS_TODO.md` is the highest priority / done first.

### 6. Present the plan, then initialize the file

Show the user the ordered brief list and the coverage matrix (or a short summary of it, flagging anything already-satisfied or any residual gap). This is the cheap moment to correct ordering or scope — before authoring N tasks. Then proceed (the user can interrupt to adjust).

Initialize `<MILESTONE_DIR>/TASKS_TODO.md` to a clean header so the agent has an empty file to append into:

```markdown
# TASKS TODO
```

### 7. Delegate authoring, one brief at a time, in order

For each brief, **in dependency order**, spawn the `submit-task` agent with the `Agent` tool (`subagent_type: "submit-task"`). Send the brief and `POSITION: append` — because you submit in dependency order, appending each task yields the correct final order, and the agent never has to re-derive ordering:

```
Author and insert one task.

BRIEF:
<the high-level brief: affected system, desired behavior, how to verify>

POSITION: append
```

**Run these sequentially, never in parallel** — every agent mutates the same `TASKS_TODO.md`, so concurrent runs would clobber each other. Wait for each agent to return before spawning the next.

- If an agent returns `FAILED: <reason>`, stop, report which brief failed and why, and do not continue. Never author the task yourself as a fallback.
- If an agent's final line flags a leftover piece (it judged the brief to contain two tasks), decide whether to spawn a follow-up agent for the remainder or fold it in, then continue.

### 8. Verify coverage and report

Re-read the finished `<MILESTONE_DIR>/TASKS_TODO.md`. Confirm every brief from the matrix produced a task section. Output a brief summary: the ordered task titles, and explicitly flag any requirement you could not trace to a task (flag as a gap — never silently omit).

## Rules

- Your output is briefs + ordering + coverage. Do not write task bodies — the contract surface, notes, file paths, or success criteria — yourself; that is the agent's job, and duplicating it both pollutes your context and risks diverging from the shared task template the agent uses.
- Never invent requirements not present in the spec; never omit one that is.
- Do not create tasks for work already in `TASKS_DONE.md`, or for requirements already satisfied by the current implementation (note these in the report instead).
- Submit briefs in dependency order with `POSITION: append`; let the agent own task wording and the caller (you) own order.
- Spawn authoring agents sequentially, one at a time. Stop on the first `FAILED`.
