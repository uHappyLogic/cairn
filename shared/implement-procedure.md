# Implement-backlog-task procedure (shared core)

This is the single source of truth for implementing one named task from the current
milestone's backlog. It is followed in two ways:

- **Inline**, by the `implement-backlog-task` skill, which runs these steps directly in
  the user's conversation so the implementation context survives for follow-up.
- **In isolation**, by the `implement-backlog-task` agent, which runs the same steps in a
  throwaway subagent context for the `implement-backlog-tasks` orchestrator.

The wrappers add their own framing (return protocol, follow-up, committing). This file
describes only the work itself; it says nothing about how the outcome is signalled.

## Project context

The project being worked on documents its environment in the workspace root `CLAUDE.md`
(and `README.md`): tech stack, available MCP tools, build/test commands, and conventions.
This procedure reads that file; it never assumes a stack.

## Procedure

### 1. Find and read the task

Read the workspace root `CLAUDE.md` and extract the path from the `## Current Milestone`
section (shown in backticks, e.g. `milestones/milestone_11_tbd/`). Use this as
`<MILESTONE_DIR>`. Never use a hardcoded backlog path.

Read `<MILESTONE_DIR>/TASKS_TODO.md`. Locate the `##` section whose heading matches the
given task name (case-insensitive, partial match is fine). If no section matches, **stop
without changing anything** and report that no matching task was found, listing the
available `##` headings so the caller can retry. Do not implement anything that is not a
task in `TASKS_TODO.md`.

Parse the full task body: description, numbered steps, and the **Success** section.

### 2. Load the implementation environment

Read the workspace root `CLAUDE.md` and hold in context:

- Available MCP tools — what tools exist and what they are for.
- Build & test commands — how to verify changes after editing.
- Conventions — post-edit verification steps to always follow.

### 3. Implement the task

**The task steps are intentionally high-level — they describe *what* to achieve, not the
exact code.** You own the implementation design. Translate each step into concrete edits
yourself: the exact files and insertion points, the precise statements, the assertion
wording, the helper structure. Ground every decision in the live codebase (read the real
source you are touching) and in the conventions from `CLAUDE.md`, not in assumptions.
Where the task names a specific file, method, class, field, or threshold, treat that as a
fixed contract other tasks depend on — honor those names exactly; design everything around
them freely.

If a step leaves genuine ambiguity, resolve it the way the task's description, the
**Success** criteria, and `requirements.md` most plausibly intend — the success criteria
are your target; whatever satisfies them faithfully is correct. Do not pause to widen
scope or invent requirements the task did not ask for.

Execute the steps in order.

**After creating or modifying any source file**, follow the post-edit conventions
documented in `CLAUDE.md`. At minimum, run the relevant verification command and fix any
errors before continuing.

**Tool patterns:**
- Read or edit a file: `Read` then `Edit`.
- Run a shell command: `Bash`.
- MCP-based operations: use the MCP tool documented in `CLAUDE.md` that matches the goal.

### 4. Verify success criteria

Re-read the task's **Success** section. For each criterion:

- Source-file criteria: check the file contents with `Read`.
- Command-output criteria: run the specified command via `Bash` and check the output.
- Structural criteria: use `find` or `Bash` to confirm files or exports exist where expected.
- MCP-based criteria: use the relevant MCP tool documented in `CLAUDE.md`.

Do not proceed to step 5 until every criterion passes.

### 5. Move the task TODO → DONE

1. `Read` `<MILESTONE_DIR>/TASKS_TODO.md`.
2. `Edit` it to remove the completed `##` section and its trailing `---` separator. The
   section starts at the `##` heading line and ends at (and includes) the next `---` line.
3. `Read` `<MILESTONE_DIR>/TASKS_DONE.md`.
4. `Edit` it to append the completed section, preserving existing content:
   append `\n## <heading>\n\n<body>\n\n---\n` at the end.

## Rules

- Always follow the conventions from `CLAUDE.md` — never skip post-edit verification.
- Never treat a task as done until every success criterion is confirmed (step 4).
- Never move a task to `TASKS_DONE.md` until step 4 passes completely.
- Never implement a task that is not present in `<MILESTONE_DIR>/TASKS_TODO.md`.
- If a step fails, diagnose the root cause with the available tools, fix it, and retry. Do
  not skip steps or mark partial work as done.
