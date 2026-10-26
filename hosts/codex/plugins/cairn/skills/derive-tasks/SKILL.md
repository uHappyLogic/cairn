---
name: derive-tasks
description: Convert the current milestone's requirements.md into a complete, dependency-ordered TASKS_TODO.md of brief-level task sections.
---

# derive-tasks

Reads the current milestone requirements and derives a complete, dependency-ordered list of tasks into `TASKS_TODO.md`, ready for AI-driven completion via `/complete-task`.

Your job here is **decomposition and coverage**. You split the milestone into high-level task briefs, prove that those briefs cover every requirement, order them by dependency, and write them into `TASKS_TODO.md` yourself, as one whole list through the plugin's task-list tool — nothing here is delegated. Keep every task section at brief altitude: a task states *what* is to be achieved, and the completer derives the flow and the formal acceptance bar itself from the description plus `requirements.md`, against the live project.

## Usage

```
/derive-tasks
```

No arguments. The skill always reads from and writes to the current milestone directory.

## Preconditions

- All open questions in the current milestone must be resolved: its `open_questions.xml` holds no `<open-question>` block, so the plugin's open-question tool's `list` prints nothing (checked in step 2).
- `TASKS_TODO.md` should be empty or contain only stale tasks from a previous milestone; this skill replaces its contents.

## Workflow

### 0. Find the current milestone

Follow `${PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Read source documents

Read `AGENTS.md` at the workspace root for the project's domain context, working conventions, available tools, and how work is verified as done. If it lacks that context, suggest the user run `/init` first, then proceed.

Read `<MILESTONE_DIR>/requirements.md` in full, plus any files referenced in its **Relevant starting state** section, so you understand the exact starting point.

Read the shared task format at `${PLUGIN_ROOT}/shared/task-format.md`. That file owns the shape of every task section you write in step 7 — its template and authoring guidelines.

### 2. Check for unresolved open questions

Run

```
python3 ${PLUGIN_ROOT}/tools/open_questions.py list <MILESTONE_DIR>
```

It prints the Short Title of every `<open-question>` block still in `<MILESTONE_DIR>/open_questions.xml`, one per line. If it prints nothing, the precondition holds — proceed. If it prints anything, stop immediately and output, with the printed lines as the bullets verbatim:

```
Cannot derive tasks: the following open questions must be resolved first:
- <Short Title>
- ...

Run /answer-open-question for each one, then re-run /derive-tasks.
```

If the call fails, its one `Error: <reason>` line on stderr is the report: print it and stop. This `list` call is the whole check — never read `open_questions.xml` to make it yourself.

### 3. Decompose into high-level task briefs

Break the milestone into discrete, independently-completable task briefs. A **brief** is high-level — it names the affected system, the desired behavior, and how it would be verified. It does **not** spell out the flow, the low-level design, a contract surface, or a structured done-ness section; the completer derives all of that against the live project.

Apply these rules:

- **Atomic scope** — each brief must be completable in a single `/complete-task` invocation, with no mid-task decisions. "Do X and Y" is two briefs when X and Y can be built and verified independently.
- **One area per brief** — group by the natural boundary or area of the work, as defined by the project's organization in `AGENTS.md`. Do not mix distinct areas unless they are inseparable.
- **No "nice to have" briefs** — only what the spec states. Do not pad the task list.

**Conflicting decisions.** Where two `## Decisions` entries cannot both hold as written, the later-recorded entry governs the brief; an entry that only refines, narrows, or extends another is no conflict. Take every pair listed under `## Noted contradictions`, when that section stands, as conflicting as noted, without re-judging it, and resolve any other pair you find conflicting yourself, here or while building step 4's matrix, the same way. To tell which entry is later, find the commit that added each entry's lines by `git blame` or a pickaxe search (`git log -S`), path-scoped to `<MILESTONE_DIR>/requirements.md`: the entry from the newer commit is the later-recorded one (where an entry's lines came from more than one commit, the newest dates it). Never order a pair by its position in the file, and never take the order from the note. Flag nothing for either kind of pair, neither in step 6's plan nor in step 8's report: the brief simply follows the later entry. A noted contradiction never blocks the run, since step 2's `list` call stays the whole precondition.

### 4. Prove coverage (requirement → task matrix)

Re-read `requirements.md` bullet by bullet and build a traceability matrix mapping **every** requirement, constraint, and behavioral detail to at least one brief:

```
| Requirement (quote/paraphrase) | Covered by brief |
|--------------------------------|------------------|
| ...                            | <brief title>    |
```

- Every requirement must map to ≥1 brief. If a requirement maps to none, you have a gap — add a brief (or note why it's already satisfied by the project's existing state per the **Relevant starting state**).
- If a requirement is already satisfied by what already exists — or by work already recorded in `<MILESTONE_DIR>/TASKS_DONE.md` — mark it so and do not create a brief for it; note it in the report instead.
- Where step 3's tie-break let the later-recorded entry of a conflicting pair govern, that entry is the requirement a brief covers; the earlier entry's conflicting text maps to no brief and is no gap, while whatever else of that entry still holds maps as usual.
- Do not invent requirements that aren't in the spec.

Do not proceed until the matrix has no unexplained gaps.

### 5. Order the briefs by dependency

Order briefs so each one's prerequisites come first: a brief that produces something other briefs build on or refer to must precede any brief that depends on it. The top of `TASKS_TODO.md` is the highest priority / done first.

### 6. Present the plan

Show the user the ordered brief list and the coverage matrix (or a short summary of it, flagging anything already-satisfied or any residual gap). This is the cheap moment to correct ordering or scope — before writing N tasks. Then proceed (the user can interrupt to adjust).

If the run derived no brief at all — every requirement is already satisfied — skip step 7: write nothing, commit nothing, and go to step 8.

### 7. Write and commit the task list in one shell call

Write every brief as one task section, using the template and the authoring guidelines from `${PLUGIN_ROOT}/shared/task-format.md` exactly: its `##` title heading, its description, and its trailing `---`. The brief you decomposed in step 3 *is* the task body; writing it down is a transcription into that format, not a second authoring pass that adds detail.

Then run this one fixed shell call, written out in full exactly as shown, with only `<MILESTONE_DIR>`, `<milestone_id>` (the last path component of `<MILESTONE_DIR>`), and the sections replaced — every brief's section in the heredoc, **in dependency order**, so the finished file reads top-to-bottom in that order:

```
python3 ${PLUGIN_ROOT}/tools/task_list.py initialize <MILESTONE_DIR> <<'EOF' &&
## <Task Title 1>

<1–3 sentence description>

---

## <Task Title 2>

<1–3 sentence description>

---
EOF
if [ -n "$(git status --porcelain -- <MILESTONE_DIR>/TASKS_TODO.md)" ]; then
  git add <MILESTONE_DIR>/TASKS_TODO.md && git commit -q -m "Task-derivation: <milestone_id>" && echo 'derivation commit landed'
fi
```

The tool replaces `<MILESTONE_DIR>/TASKS_TODO.md` with its heading followed by the whole list in the order given, or, refusing anything in it, prints one `Error:` line and leaves the file byte-for-byte unchanged. After the `&&` the call carries out the three steps of the shared commit procedure at `${PLUGIN_ROOT}/shared/commit-procedure.md` itself — its dirty-own-path guard, the path-scoped `git add`, and the subject-only commit under `Task-derivation: <milestone_id>` — over this skill's own change set, `<MILESTONE_DIR>/TASKS_TODO.md`, written out on the command line in both places and never held in a shell variable. Git's success output is silenced. Never write the briefs into the file any other way, one at a time or by editing it.

What the call prints is the whole outcome: `derivation commit landed` when the commit landed; nothing when the guard found the file unchanged (the list matched what it already held); otherwise the tool's one `Error:` line, with `TASKS_TODO.md` unchanged and nothing committed, or git's message for a commit it refused.

On the tool's `Error:` line — two briefs whose titles fold to the same title, or a section with an empty title or body — commit nothing and stop: report the failure quoting the `Error:` line verbatim, and print neither status line of step 8.

### 8. Verify coverage and report

Re-read the finished `<MILESTONE_DIR>/TASKS_TODO.md` and confirm every brief from the matrix produced a task section.

On the success path — the call printed `derivation commit landed` — print exactly one fixed terse status line for the whole run — `Tasks derived.` — with no list of the ordered task titles and no next-step pointer. **Alongside** that terse line, keep the one git-absent advisory this step owns: explicitly flag any requirement you could not trace to a task (flag as a gap — never silently omit).

If the run derived nothing — step 6 skipped the call because no brief was derived, or step 7's dirty-own-path guard found `TASKS_TODO.md` unchanged, so nothing is committed — do not print the terse success line; instead print a distinct one-line message stating that nothing changed and why (no tasks were derived, or the derived list matched the file already).
