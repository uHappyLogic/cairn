---
name: derive-tasks
description: Convert the current milestone's requirements.md into a complete, dependency-ordered TASKS_TODO.md of brief-level task sections.
---

# derive-tasks

Reads the current milestone requirements and derives a complete, dependency-ordered list of tasks into `TASKS_TODO.md`, ready for AI-driven completion via `/complete-task`.

Your job here is **decomposition and coverage**. You split the milestone into high-level task briefs, prove that those briefs cover every requirement, order them by dependency, and write them into `TASKS_TODO.md` yourself — you are the single writer on the derivation path, and nothing here is delegated. Keep every task section at brief altitude: a task states *what* is to be achieved, and the completer derives the flow and the formal acceptance bar itself from the description plus `requirements.md`, against the live project.

## Usage

```
/derive-tasks
```

No arguments. The skill always reads from and writes to the current milestone directory.

## Preconditions

- All open questions in the current milestone's `requirements.md` must be resolved (no `<open-question` block with `status="open"` remains; `status="deferred"` blocks may carry forward).
- `TASKS_TODO.md` should be empty or contain only stale tasks from a previous milestone; this skill replaces its contents.

## Workflow

### 0. Find the current milestone

Follow `.agents/plugins/cairn/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Read source documents

Read `CLAUDE.md` at the workspace root for the project's domain context, working conventions, available tools, and how work is verified as done. If it lacks that context, suggest the user run `/init` first, then proceed.

Read `<MILESTONE_DIR>/requirements.md` in full, plus any files referenced in its **Relevant starting state** section, so you understand the exact starting point.

Read the shared task format at `.agents/plugins/cairn/shared/task-format.md`. That file owns the shape of every task section you write in step 7 — its template and authoring guidelines.

### 2. Check for unresolved open questions

Scan `requirements.md` for `<open-question` blocks carrying `status="open"`. If any exist, stop immediately and output:

```
Cannot derive tasks: the following open questions must be resolved first:
- <Short Title>
- ...

Run /answer-open-question for each one, then re-run /derive-tasks.
```

A block with `status="deferred"` does **not** block derivation — deferred questions may carry forward past this point.

### 3. Decompose into high-level task briefs

Break the milestone into discrete, independently-completable task briefs. A **brief** is high-level — it names the affected system, the desired behavior, and how it would be verified. It does **not** spell out the flow, the low-level design, a contract surface, or a structured done-ness section; the completer derives all of that against the live project.

Apply these rules:

- **Atomic scope** — each brief must be completable in a single `/complete-task` invocation, with no mid-task decisions. "Do X and Y" is two briefs when X and Y can be built and verified independently.
- **One area per brief** — group by the natural boundary or area of the work, as defined by the project's organization in `CLAUDE.md`. Do not mix distinct areas unless they are inseparable.
- **No "nice to have" briefs** — only what the spec states. Do not pad the task list.

### 4. Prove coverage (requirement → task matrix)

Re-read `requirements.md` bullet by bullet and build a traceability matrix mapping **every** requirement, constraint, and behavioral detail to at least one brief:

```
| Requirement (quote/paraphrase) | Covered by brief |
|--------------------------------|------------------|
| ...                            | <brief title>    |
```

- Every requirement must map to ≥1 brief. If a requirement maps to none, you have a gap — add a brief (or note why it's already satisfied by the project's existing state per the **Relevant starting state**).
- If a requirement is already satisfied by what already exists — or by work already recorded in `<MILESTONE_DIR>/TASKS_DONE.md` — mark it so and do not create a brief for it; note it in the report instead.
- Do not invent requirements that aren't in the spec.

Do not proceed until the matrix has no unexplained gaps.

### 5. Order the briefs by dependency

Order briefs so each one's prerequisites come first: a brief that produces something other briefs build on or refer to must precede any brief that depends on it. The top of `TASKS_TODO.md` is the highest priority / done first.

### 6. Present the plan, then initialize the file

Show the user the ordered brief list and the coverage matrix (or a short summary of it, flagging anything already-satisfied or any residual gap). This is the cheap moment to correct ordering or scope — before writing N tasks. Then proceed (the user can interrupt to adjust).

Initialize `<MILESTONE_DIR>/TASKS_TODO.md` to a clean header:

```markdown
# TASKS TODO
```

### 7. Write the briefs into the task list, in order

Write each brief into `<MILESTONE_DIR>/TASKS_TODO.md` as one task section, **in dependency order**, appending each after the last so the finished file reads top-to-bottom in that order.

Use the template and the authoring guidelines from `.agents/plugins/cairn/shared/task-format.md` exactly. The brief you decomposed in step 3 *is* the task body; writing it down is a transcription into that format, not a second authoring pass that adds detail.

### 8. Verify coverage and report

Re-read the finished `<MILESTONE_DIR>/TASKS_TODO.md` and confirm every brief from the matrix produced a task section.

On the success path, print exactly one fixed terse status line for the whole run — `Tasks derived.` — with no list of the ordered task titles and no next-step pointer. **Alongside** that terse line, keep the one git-absent advisory this step owns: explicitly flag any requirement you could not trace to a task (flag as a gap — never silently omit).

If the run derived nothing — `TASKS_TODO.md` gained no task section, so step 9's dirty-own-path no-op guard will fire and nothing is committed — do not print the terse success line; instead print a distinct one-line message stating that nothing changed and why (no tasks were derived).

### 9. Commit the derived task list

You commit **once at the end of the run** — here, after every brief has been written (step 7) and coverage is verified (step 8), never after each individual task section. Read and follow the shared commit procedure at `.agents/plugins/cairn/shared/commit-procedure.md`, carrying out its steps yourself. Supply it these two inputs:

- **PATHS** — this run's own change set: `<MILESTONE_DIR>/TASKS_TODO.md` (the file this skill initialized in step 6 and wrote into in step 7).
- **SUBJECT** — `Task-derivation: <milestone_id>`.

The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard (a run that derived nothing into `TASKS_TODO.md` stages and commits nothing), and the commit.
