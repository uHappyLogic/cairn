---
name: ask-in-milestone-context
description: Answer an informational question about the current milestone from its goal, decisions, task lists, and live deliverables, without editing anything.
---

# ask-in-milestone-context

Answers an informational question about the current milestone, grounded in the real project state: the milestone's goal and recorded decisions, the tasks done and still pending, the actual deliverables those tasks produced, and, when a question reaches into past work, the project's record of its milestones. The deliverable is **a clear answer** — not a decision, a new task, or an edited document. This skill reads; it never writes — it never creates or edits any file, not `requirements.md`, not `open_questions.xml`, not the task lists, nothing.

Use it to look back ("how did the onboarding section end up covering setup?", "where did we put the troubleshooting steps?"), to take stock ("what's left in this milestone, and why is it ordered that way?", "what has this milestone changed so far?"), or to pull up relevant context on demand before deciding what to do next.

When the answer surfaces a concrete next step, this skill names the right cairn skill and offers to hand off (step 4) — but it stops there, never doing that skill's work here.

## Usage

```
/ask-in-milestone-context --milestone <path> <question>
```

- `--milestone <path>`: required and leading; names the milestone by its repo-relative path, exactly as the definition tool printed it, trailing slash included, e.g. `milestones/user-guide/`.
- `<question>`: a free-form, informational question about the current milestone. Optional — invoked with no question, give a brief orientation to the milestone (goal, what's done, what's left) and invite a specific question.

**Examples:**
```
/ask-in-milestone-context --milestone milestones/user-guide/ how did we end up handling the case where two milestones are active at once?
/ask-in-milestone-context --milestone milestones/user-guide/ what's left in this milestone and what's blocking it?
/ask-in-milestone-context --milestone milestones/user-guide/ what changed in the rename task — which files did it touch?
```

## Workflow

### 0. Find the current milestone

First strip the leading `--milestone <path>` from the invocation text by the rule in `{{PLUGIN_ROOT}}/shared/resolve-milestone.md`, reading only the rest as the question. Follow `{{PLUGIN_ROOT}}/shared/resolve-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path. A call that resolves no milestone stops as that procedure says, with no answer and no fallback: this skill answers only within a named milestone.

### 1. Gather context

In parallel, as independent tool calls, so the answer rests on the real state rather than memory:

- Read `<MILESTONE_DIR>/requirements.md` — the goal, relevant starting state, and recorded decisions.
- Read `<MILESTONE_DIR>/open_questions.xml` — any remaining open questions, each an `<open-question>` block carrying whatever alternatives and recommendation the recommend sweep has embedded. Read it whole with the file-reading tool, exactly as you read `requirements.md`; that whole read is for reasoning only, and a locate, list, or lift of one block is a call to the plugin's open-question tool, `python3 {{PLUGIN_ROOT}}/tools/open_questions.py <subcommand> <MILESTONE_DIR> …`, never a search of your own over the file.
- Run the plugin's milestones tool — completed tasks:

  ```
  python3 {{PLUGIN_ROOT}}/tools/milestones.py tasks <MILESTONE_DIR> --with-body
  ```

  It prints, newest first, one tab-separated line per task completed in the milestone (the commit's abbreviated hash, its date, the milestone directory, and the task title), with the task's verified bar indented beneath it, and prints nothing when no task has been completed, which is no failure. Each task's title and verified bar tell you *what the task was meant to achieve* — the intent behind the deliverable that now exists — and its brief stands in its commit's diff, as the section removed from `TASKS_TODO.md`, which `git show <hash>` pulls up.
- Read `<MILESTONE_DIR>/TASKS_TODO.md` — pending tasks, in priority order. Their ordering explains dependencies ("what's blocking what").
- Read `{{CONTEXT_FILE}}` — the project's domain context, conventions, and real names for its systems and files, so your answer uses the project's vocabulary.
- When the question concerns past work — what an earlier milestone built, when or why something landed, a finished milestone — run the plugin's milestones tool for the project's composed record, at your own discretion and scoped to the question: the path the question concerns (a file or directory), the milestone's scope (the directory holding its `milestones/` container, `.` for one at `milestones/<slug>/`) for the work around this milestone, or `.` for a project-wide question:

  ```
  python3 {{PLUGIN_ROOT}}/tools/milestones.py record <PATH>
  ```

  It prints one tab-separated line at column 0 for each milestone, live or finished, that changed PATH or whose scope overlaps it (`live` or `finished`, the finish date or `-` for a live one, the milestone's path, and its title; the live ones first, then the finished ones newest first), with its summary bullets, or a live one's goal, and its tasks that changed PATH indented beneath it. A finished milestone, its directory removed, resolves under no `--milestone`, so it is answered from this read, scoped as wide as `.` when nothing narrower lists it.

If the `tasks` call or a `record` call fails, tell the user in prose that the completed-task read or the record read failed, quoting its one `Error: <reason>` line from stderr verbatim, and carry on from the other reads and the live deliverables, printing no fixed line.

Read only what the question needs — a "what's left?" question barely touches `requirements.md`; a "how did task X turn out?" question leans hard on the completed tasks the `tasks` call lists and the live deliverables. Don't read everything reflexively.

### 2. Ground the answer in what was actually produced

For a question about *how finished work turned out* ("how did task X handle Y?", "where did Z go?"), the markdown artifacts give you intent — but the truth is in the deliverable. Go look:

- **The live deliverable is primary.** Read the actual artifact the task produced. The task's title and verified bar, as the `tasks` call lists them, tell you what to look for and what "done" meant; the deliverable itself tells you what was actually produced. When they diverge, the deliverable wins — and that divergence is often exactly what the user is asking about.
- **Git history is a supporting lens, not the spine.** Completed tasks are committed and their commits carry the task heading, so searching commit subjects and bodies for the heading text (`git log --grep`) usually finds the commit for a done task and `git show` pulls up its diff — but the task→commit mapping stays best-effort. Use git to enrich an answer ("this landed in commit abc123, touching these files"), never as the sole source — fall back to reading the live files when no clean commit matches.

For a question about *direction or state* (decisions, what's pending and why), the markdown artifacts are usually enough; reach for the deliverables only when the user asks something the documents can't settle.

### 3. Answer directly

Open with the answer, not a recap of the question or a tour of what you read. Be specific and concrete: cite the file and line (`path/to/file.ext:42`), name the task, quote the decision. If the honest answer is "the artifacts don't record this" or "the deliverable and the task description disagree," say that plainly — a grounded "we don't actually know" beats a confident guess.

Keep it tight. A thorough first answer is fine when the question is broad; follow-ups should be short. Continue the conversation as the user probes, re-grounding in the files each time rather than repeating your first reply.

### 4. Hand off when a concrete next action surfaces

Answering often reveals a next step. When it does, name the right skill and offer to invoke it — then let the user decide. The handoff is an offer, not the goal, and **this skill performs none of these actions itself**:

- The question is really an undecided design trade-off to deliberate and record → `/discuss-open-question <title>`.
- The answer exposes a bug, gap, or "we should also…" worth tracking → `/submit-task` if it's already clear, `/discuss-new-task` if it needs shaping first.
- The user wants to reshape what the milestone is even aiming at → `/discuss-milestone-goal`.
- The user decides to actually do a pending task → `/complete-task <name>`.

If no clear next action emerged, don't manufacture one. Plenty of questions just want an answer.
