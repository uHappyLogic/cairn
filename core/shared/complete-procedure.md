# Complete-task procedure (shared core)

This is the single source of truth for completing one named task from the named
milestone's task list: the `complete-task` skill follows these steps inline, the
`complete-task` agent follows them in isolation. The wrappers add their own framing; this
file describes only the work itself. If a step fails, diagnose the root cause with the
available tools, fix it, and retry — never skip a step or record partial work as done.

## The task shape

A task section in `TASKS_TODO.md` is **brief-level** — the format
`{{PLUGIN_ROOT}}/shared/task-format.md` defines: a `##` title heading, a 1–3 sentence
description of what is to be achieved, why the milestone needs it, and how it would be
verified, then a trailing `---` separator. That is the whole task.

Two things follow, and they shape this entire procedure:

- **The task carries no acceptance criteria.** You derive the formal acceptance bar
  yourself, from the task description plus the milestone's `requirements.md` (step 2), and
  that derived bar — not anything authored in the task — is what step 4 verifies against
  and what step 5 hands on as the task's record.
- **The task carries no forward contract.** Tasks run in order, so whatever an earlier task
  was to produce already exists: resolve every cross-task reference by reading that prior
  task's **live deliverable** in the project, never by trusting a name the task list
  promised.

Read the whole section body as ordinary description. Whatever a given section happens to
contain — including a heading, label, or bullet list left over from an older task list — is
prose feeding the bar you derive; no part of a task body gets privileged parsing.

## Project context

The project being worked on documents its environment in the workspace root `{{CONTEXT_FILE}}`
(and `README.md`): the project's domain context, working conventions, available tools, and
how work is verified as done. This procedure reads that file; it never assumes a particular
kind of work.

## Procedure

### 1. Find and read the task

When your runner supplies an already-resolved milestone directory, take it as given as
`<MILESTONE_DIR>`, with no resolution of your own. Only when none is supplied, the inline
`complete-task` skill's case, follow `{{PLUGIN_ROOT}}/shared/resolve-milestone.md` to
resolve `<MILESTONE_DIR>`, with the `--milestone <path>` value the runner holds as that
procedure's input.

Read `<MILESTONE_DIR>/TASKS_TODO.md`. Locate the `##` section whose heading matches the
given task name (case-insensitive, partial match is fine). If no section matches, **stop
without changing anything** and report it with the fixed line `No task matches the given name.`
first, then the available `##` headings below it, one per line, so the caller can retry. Do
not carry out anything that is not a task in `TASKS_TODO.md`.

Read the located section in full, from its `##` heading to its trailing `---`, and hold its
full heading text: it is the `<Task Title>` step 5 passes to the removal. Its description is the
statement of intent — what is to be achieved, why, and how it would be verified — and every
sentence of it is input to the acceptance bar you derive next.

### 2. Load the work environment and derive the acceptance bar

Read the workspace root `{{CONTEXT_FILE}}` and hold in context:

- The project's domain context — what the project is and the material it works with.
- Working conventions — the practices to follow while doing and finishing the work.
- Available tools — what tools exist and what they are for.
- How work is verified as done — the checks that confirm a deliverable meets its bar.

Read `<MILESTONE_DIR>/requirements.md` and hold in context the milestone's goal, its
relevant starting state, and its recorded decisions. This is what tells you what "done"
means for this task beyond the brief's own sentences — a decision recorded there is binding
on the work, and any value, name, or threshold it fixes is authoritative.

**The past-work read.** Why an existing file is the way it is stands in the project's completed
tasks, read with `python3 {{PLUGIN_ROOT}}/tools/milestones.py tasks <path> --with-body` run from
the workspace root, `<path>` the file's path, its whole print taken whatever its length, and
followed where a printed task bears by `python3 {{PLUGIN_ROOT}}/tools/milestones.py show <milestone path>`
for that milestone's decisions in their own words — every milestones-tool call this read makes,
the `tasks` call on each file it is taken for and each `show` follow-up alike, written out in
full on every call, never through a variable, alias, or function of your own defined to stand
for the command or any part of it. `tasks` prints, newest first, one tab-separated line per task
commit that changed the file — its abbreviated hash, date, milestone path, and title — with that
task's verified bar indented beneath it, and `show` takes the milestone path exactly as that
line's third field prints it. Take the read for each file the task edits rather than creates
whose shape you judge `requirements.md` does not explain, only this milestone's goal, relevant
starting state, and recorded decisions counting as an explanation and never what
`{{CONTEXT_FILE}}` says about the file, however fully it gives the reason. Deleting, renaming,
or moving a file that already exists counts as editing it, and the read on it is taken on the
path the file has before the task, since the history follows no rename. Take it here for the
files the task names up front: what it surfaces is input to the bar you derive next and may fix
a criterion. Step 3 takes it for the rest.

Then **derive the task's acceptance bar**: turn the task description plus what
`requirements.md` binds for it into an explicit list of concrete, checkable criteria. Each
criterion must be an observable property of a deliverable — something you can confirm by
reading an artifact, running a named command, or inspecting the project — not a restatement
of the intent. Cover what the description asks for and nothing wider: the bar is the task's
definition of done, so it must not import scope the task did not ask for, and it must not
drop a "how it would be verified" clause the description states. Where the bar depends on
something a prior task produced, read that live deliverable now and let what it actually
contains — its real names, structure, and values — fix the criterion.

Hold that derived bar in context verbatim. It is the gate step 4 checks against and the
record step 5 hands to your runner, so it must not drift between here and there.

### 3. Carry out the task

**Uncommitted changes already in the tree may be a previous run's partial work or another
run's live work.** A run of this procedure can be resuming an earlier one that failed or was
interrupted part-way, which leaves its partial work uncommitted in the working tree, and it
can share the tree with other runs still in progress, whose edits stay uncommitted until
each commits its own. Before editing anything, inspect what is already uncommitted. In
either case, whatever bears on this task is work already done — read it, continue from it,
and carry its paths in the running list below — rather than redoing or reverting it, and
uncommitted changes that do not bear on this task are not yours to touch: leave them exactly
as they stand and keep their paths out of your running list.

**The task gives you the goal, not a procedure — you own the design.**
Derive the flow yourself from the task's description and the acceptance bar you derived in
step 2, then translate it into concrete edits: the exact files and where within them the
work lands, the precise wording, the structure. Ground every decision in the live material
you are changing (read the real artifacts you are touching) and in the conventions from
`{{CONTEXT_FILE}}`, not in assumptions.

Resolve anything a sibling task was to provide the same way — by reading that task's live
deliverable in the project and building against what is really there. Since tasks run in
order, the deliverable is the contract; a name recalled from another task's description is
not.

**Take the past-work read before an edit step 2 did not take it for.** When your edits reach an
existing file beyond those the task names up front — to edit, delete, rename, or move it — and
`requirements.md` does not explain its shape, take the past-work read on it, as step 2 states
it, before you change it. What it surfaces shapes how you make the edit only: the acceptance bar
stays exactly as step 2 derived it and is never re-derived on it.

If the goal leaves genuine ambiguity, resolve it the way the description, the derived
acceptance bar, and `requirements.md` most plausibly intend — the derived bar is your
target; whatever satisfies it faithfully is correct. Do not pause to widen scope or invent
requirements the task did not ask for.

**After creating or modifying any file**, follow the finishing conventions documented in
`{{CONTEXT_FILE}}`. At minimum, apply the project's way of verifying the change and fix any
problems before continuing.

**Record the paths you touch.** As you create or edit each file while carrying out the
task, keep an explicit running list of those paths — recorded as each edit is made, never
reconstructed afterwards by diffing the working tree. This recorded set is the task's real
change set.

**Tool patterns:**
- Read or edit a file: `Read` then `Edit`.
- Run a shell command: `Bash`.
- MCP-based operations: use the MCP tool documented in `{{CONTEXT_FILE}}` that matches the goal.

### 4. Verify against the derived acceptance bar

Take the acceptance bar you derived in step 2 and verify the deliverable against it,
criterion by criterion, however the project's conventions define done. If `{{CONTEXT_FILE}}`
documents a done-verification convention (a check, review, or command that confirms work is
complete), apply it. When it defines no such convention, fall back to direct inspection of
the deliverable against the derived bar, checking it criterion-by-criterion using whatever
means each criterion itself names — read the artifact, or run a command only where a
criterion specifies one.

For each criterion:

- Deliverable-content criteria: check the artifact's contents with `Read`.
- Command-output criteria: run the specified command via `Bash` and check the output.
- Structural criteria: use `find` or `Bash` to confirm the expected artifacts exist where expected.
- MCP-based criteria: use the relevant MCP tool documented in `{{CONTEXT_FILE}}`.

Do not proceed to step 5 until every criterion passes.

### 5. Remove the task from the list and hand on its bar

The finished task's record is the brief its section held together with the bar the work was
actually verified against. The section leaves `TASKS_TODO.md` through the plugin's task-list
tool, the sole writer of that file, which removes the located section — its heading, body,
and `---` — and nothing else:

```
python3 {{PLUGIN_ROOT}}/tools/task_list.py remove <MILESTONE_DIR> "<Task Title>"
```

`<Task Title>` is the full heading step 1 located. The tool reads no bar, prints nothing on
success, and on any failure prints one `Error: <reason>` line on stderr with a non-zero exit
and `TASKS_TODO.md` left byte-for-byte unchanged.

The bar this procedure hands to your runner takes one form: the derived acceptance bar as one
`- ` bullet per criterion, in the order you verified them, written as they stood when they
passed in step 4 — the same bar, neither re-derived nor summarized into prose, with no label,
brief, or other line beside it. It reaches the record your runner's own file writes through
the one shell call that file shows, which runs this command and carries the bar with it.
