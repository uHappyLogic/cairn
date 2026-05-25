---
name: populate-backlog
description: Convert the current milestone's requirements.md into implementation-ready tasks in TASKS_TODO.md, ordered by dependency and sized for agentic execution.
---

# populate-backlog

Reads the current milestone requirements and populates `TASKS_TODO.md` with a complete, dependency-ordered list of implementation tasks ready for AI-driven execution via `/implement-backlog-task`.

## Usage

```
/populate-backlog
```

No arguments. The skill always reads from and writes to the current milestone directory.

## Preconditions

Before running this skill:
- All open questions in the current milestone's `requirements.md` must be resolved (no `> **Open question` blocks remain). If any are found, stop and tell the user to run `/answer-open-question` for each one first.
- `TASKS_TODO.md` should be empty or contain only tasks from a previous milestone that are now stale.

## Workflow

### 0. Find the current milestone

Read `CLAUDE.md` and extract the path from the `## Current Milestone` section (shown in backticks, e.g. `milestones/milestone_11_tbd/`). Use this as `<MILESTONE_DIR>` throughout this workflow.

### 1. Read source documents

Read `<MILESTONE_DIR>/requirements.md` in full. Also read any referenced scripts or assets mentioned in the **Relevant implementation state** section so you understand the exact starting point.

### 2. Check for unresolved open questions

Scan `<MILESTONE_DIR>/requirements.md` for any `> **Open question` blocks. If any exist, stop immediately and output:

```
Cannot populate backlog: the following open questions must be resolved first:
- <Short Title>
- ...

Run /answer-open-question for each one, then re-run /populate-backlog.
```

### 3. Decompose requirements into tasks

Break the milestone into discrete, independently-implementable tasks. Apply these decomposition rules:

**Atomic scope** — each task should be completable in a single `/implement-backlog-task` invocation without requiring decisions from the user mid-task. A task that says "implement X and Y" is two tasks if X and Y can be done independently.

**One system per task** — group by Unity system: one task for script changes, one for material/shader changes, one for scene hierarchy changes, one for prefab changes. Do not mix systems unless they are inseparable (e.g., creating a script and attaching it to a specific GameObject in the same operation).

**Dependency ordering** — place tasks in `TASKS_TODO.md` in the order they should be executed (top = highest priority, done first). A task that creates a script must appear before any task that attaches that script as a component. A task that adds a Unity layer must appear before any task that assigns GameObjects to that layer.

**No open decisions** — all implementation choices must be resolved in the task description itself or traceable to the requirements document. A task must never say "choose the appropriate approach" — it must say exactly which approach.

**Completeness** — every requirement, constraint, and behavioral detail from the spec must be traceable to at least one task. After decomposing, do a gap check: re-read each bullet point in the requirements and confirm it appears in a task.

### 4. Write each task

Use this template for each task section:

```markdown
## <Task Title>

<1–3 sentence description of what this task does and why it is needed in this milestone.>

**Steps:**
1. <Concrete, tool-actionable step.>
2. <...>

**Success:**
- <Verifiable criterion — ideally observable in the Editor or Console without running the game.>
- <...>

---
```

Guidelines for writing tasks suited for AI-agent execution:

- **Steps must be imperative and concrete.** "Open `Assets/Scripts/RailCameraSnapper.cs` and add a coroutine `SwingCameraArc`" is good. "Update the camera script" is not.
- **Reference exact file paths, class names, method names, and field names** as given in the requirements or discoverable from the current codebase.
- **Quote numeric values, durations, easing functions, and thresholds** directly from the requirements doc — do not paraphrase.
- **Success criteria must be checkable without human judgement.** Prefer: "Console shows no errors after compilation", "Component X is visible in the Inspector on GameObject Y", "Field Z reads value W in the Inspector". Avoid: "looks correct", "feels smooth".
- **Do not include rationale or design discussion** — that belongs in the requirements doc. Tasks are instructions, not explanations.

### 5. Write TASKS_TODO.md

Replace the content of `<MILESTONE_DIR>/TASKS_TODO.md` entirely with the generated task list. Use this file structure:

```markdown
# TASKS TODO

## <Task 1 Title>

...

---

## <Task 2 Title>

...

---
```

Preserve the `---` separator between tasks so `/implement-backlog-task` can reliably parse sections.

### 6. Report

After writing the file, output a brief summary, and flag any requirement from the spec that you could not trace to a task (flag as a gap, do not silently omit)

## Rules

- Never invent requirements not present in the spec — tasks must be traceable to the document.
- Never omit a requirement — if it is in the spec it must appear in a task.
- Do not add "nice to have" polish tasks unless explicitly stated in the spec.
- Do not create tasks for work already present in `TASKS_DONE.md`.
- If the requirements doc references a current implementation that already satisfies a requirement, skip that task and note it in the report.
- Tasks must be ordered so that each task's dependencies (scripts, layers, materials) are satisfied by earlier tasks in the list.
- Keep task titles short (4–8 words), title-cased, and unique within the file.
