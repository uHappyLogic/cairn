---
name: ask-in-milestone-context
description: Use when the user is asking a question about the current milestone rather than trying to change it.
---

# ask-in-milestone-context

Answers an informational question about the current milestone, grounded in the real project state: the milestone's goal and recorded decisions, the tasks done and still pending, and the actual deliverables those tasks produced. The deliverable is **a clear answer** — not a decision, a new task, or an edited document. This skill reads; it never writes — it never creates or edits any file, not `requirements.md`, not the task lists, nothing.

Use it to look back ("how did the onboarding section end up covering setup?", "where did we put the troubleshooting steps?"), to take stock ("what's left in this milestone, and why is it ordered that way?", "what has this milestone changed so far?"), or to pull up relevant context on demand before deciding what to do next.

When the answer surfaces a concrete next step, this skill names the right cairn skill and offers to hand off (step 4) — but it stops there, never doing that skill's work here.

## Usage

```
/ask-in-milestone-context <question>
```

- `<question>`: a free-form, informational question about the current milestone. Optional — invoked with no question, give a brief orientation to the milestone (goal, what's done, what's left) and invite a specific question.

**Examples:**
```
/ask-in-milestone-context how did we end up handling the case where two milestones are active at once?
/ask-in-milestone-context what's left in this milestone and what's blocking it?
/ask-in-milestone-context what changed in the rename task — which files did it touch?
```

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

If the pointer is `none` (no active milestone), don't dead-end. Tell the user there's no open milestone, then answer from what *is* available — the `## Milestone History` and completed-milestone table in `milestones/README.md` — if the question is about past work. If they're clearly asking about active work that doesn't exist yet, say so and point them at `/define-milestone-goal` (or `/goto-next-milestone` if a milestone is defined but not active).

### 1. Gather context

Read in parallel, so the answer rests on the real state rather than memory:

- `<MILESTONE_DIR>/requirements.md` — the goal, relevant starting state, recorded decisions, and any remaining open questions.
- `<MILESTONE_DIR>/TASKS_DONE.md` — completed tasks. Each entry's description and `**Verified:**` bar tell you *what the task was meant to achieve* — the intent behind the deliverable that now exists.
- `<MILESTONE_DIR>/TASKS_TODO.md` — pending tasks, in priority order. Their ordering explains dependencies ("what's blocking what").
- `CLAUDE.md` — the project's domain context, conventions, and real names for its systems and files, so your answer uses the project's vocabulary.

Read only what the question needs — a "what's left?" question barely touches `requirements.md`; a "how did task X turn out?" question leans hard on `TASKS_DONE.md` and the live deliverables. Don't read everything reflexively.

### 2. Ground the answer in what was actually produced

For a question about *how finished work turned out* ("how did task X handle Y?", "where did Z go?"), the markdown artifacts give you intent — but the truth is in the deliverable. Go look:

- **The live deliverable is primary.** Read the actual artifact the task produced. The `TASKS_DONE.md` entry tells you what to look for and what "done" meant; the deliverable itself tells you what was actually produced. When they diverge, the deliverable wins — and that divergence is often exactly what the user is asking about.
- **Git history is a supporting lens, not the spine.** Completed tasks are committed, so `git log` and `git show` can pull up the diff for a done task — but the task→commit mapping is best-effort, not keyed on the heading in the subject line. Use git to enrich an answer ("this landed in commit abc123, touching these files"), never as the sole source — fall back to reading the live files when no clean commit matches.

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
