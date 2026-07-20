# Complete-task procedure (shared core)

This is the single source of truth for completing one named task from the current
milestone's task list. It is followed in two ways:

- **Inline**, by the `complete-task` skill, which runs these steps directly in
  the user's conversation so the work context survives for follow-up.
- **In isolation**, by the `complete-task` agent, which runs the same steps in a
  throwaway subagent context for the `complete-all-tasks` orchestrator.

The wrappers add their own framing (return protocol, follow-up, committing). This file
describes only the work itself; it says nothing about how the outcome is signalled.

## Project context

The project being worked on documents its environment in the workspace root `CLAUDE.md`
(and `README.md`): the project's domain context, working conventions, available tools, and
how work is verified as done. This procedure reads that file; it never assumes a particular
kind of work.

## Procedure

### 1. Find and read the task

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

Read `<MILESTONE_DIR>/TASKS_TODO.md`. Locate the `##` section whose heading matches the
given task name (case-insensitive, partial match is fine). If no section matches, **stop
without changing anything** and report that no matching task was found, listing the
available `##` headings so the caller can retry. Do not carry out anything that is not a
task in `TASKS_TODO.md`.

Parse the full task body: the description, the optional **Provides** section (the names
other tasks depend on — a fixed contract), the optional **Notes** section (advisory facts),
and the **Success** section. There is no steps section — you derive the flow yourself
(step 3).

### 2. Load the work environment

Read the workspace root `CLAUDE.md` and hold in context:

- The project's domain context — what the project is and the material it works with.
- Working conventions — the practices to follow while doing and finishing the work.
- Available tools — what tools exist and what they are for.
- How work is verified as done — the checks that confirm a deliverable meets its bar.

### 3. Carry out the task

**The task gives you the goal, not a procedure — you own the design.**
Derive the flow yourself from the **Description** and **Success** criteria, then translate
it into concrete edits: the exact files and where within them the work lands, the precise
wording, the structure. Ground every decision in the live material you are changing (read
the real artifacts you are touching) and in the conventions from `CLAUDE.md`, not in
assumptions.

Honor the two optional sections for what they are:
- **Provides** lists the names other tasks depend on — files, sections, named artifacts,
  thresholds. Treat these as a fixed contract: honor the names exactly, design everything
  around them freely.
- **Notes** are advisory facts the author surfaced to save you a discovery round (a
  surprising behavior, an ordering constraint, a gotcha). Use them, but they are not
  acceptance criteria — the **Success** section is.

If the goal leaves genuine ambiguity, resolve it the way the **Description**, the
**Success** criteria, and `requirements.md` most plausibly intend — the success criteria
are your target; whatever satisfies them faithfully is correct. Do not pause to widen
scope or invent requirements the task did not ask for.

**After creating or modifying any file**, follow the finishing conventions documented in
`CLAUDE.md`. At minimum, apply the project's way of verifying the change and fix any
problems before continuing.

**Record the paths you touch.** As you create or edit each file while carrying out the
task, keep an explicit running list of those paths — recorded as each edit is made, never
reconstructed afterwards by diffing the working tree. This recorded set is the task's real
change set; a wrapper reads it from here when it needs to know exactly which files this task
touched. Recording paths as you go is neither committing nor content inspection.

**Tool patterns:**
- Read or edit a file: `Read` then `Edit`.
- Run a shell command: `Bash`.
- MCP-based operations: use the MCP tool documented in `CLAUDE.md` that matches the goal.

### 4. Verify success criteria

Re-read the task's **Success** section and verify the deliverable against it, however the
project's conventions define done. If `CLAUDE.md` documents a done-verification convention
(a check, review, or command that confirms work is complete), apply it. When it defines no
such convention, fall back to direct inspection of the deliverable against the **Success**
section, checking it criterion-by-criterion using whatever means each criterion itself names
— read the artifact, or run a command only where a criterion specifies one.

For each criterion:

- Deliverable-content criteria: check the artifact's contents with `Read`.
- Command-output criteria: run the specified command via `Bash` and check the output.
- Structural criteria: use `find` or `Bash` to confirm the expected artifacts exist where expected.
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

- Always follow the conventions from `CLAUDE.md` — never skip the project's way of verifying the work.
- Never treat a task as done until every success criterion is confirmed (step 4).
- Never move a task to `TASKS_DONE.md` until step 4 passes completely.
- Never carry out a task that is not present in `<MILESTONE_DIR>/TASKS_TODO.md`.
- If a step fails, diagnose the root cause with the available tools, fix it, and retry. Do
  not skip steps or mark partial work as done.
