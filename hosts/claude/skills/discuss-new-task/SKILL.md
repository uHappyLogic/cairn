---
name: discuss-new-task
description: Clarify a rough or ambiguous issue into one or more well-defined, task-sized pieces ready to add to the current milestone's task list.
---

# discuss-new-task

Facilitates a short, focused conversation that turns a half-formed issue — the kind that surfaces mid-flight — into a description concrete enough to become a task. This skill is the conversational front-end for `/submit-task`: it clarifies just enough, then proposes the handoff. It never creates or edits any files, including the task list — producing the task(s) is `submit-task`'s job.

Most issues are a single task. But some are a bigger chunk of work that only makes sense as **several** tasks — the user may flag this up front ("this might be a few entries"), or it may become apparent mid-discussion that one "issue" is really two or three independent pieces. When that happens, this skill helps draw the boundaries and produces an ordered set of task-sized descriptions, then hands each off in turn.

The bar to clear is **conceptual clarity**, not full design detail. For each task that comes out of the discussion, three things must be unambiguous:

1. **Which system** the issue touches (a file, component, section, or requirement).
2. **What the desired behavior is** — what should be true after the fix that isn't true now.
3. **Roughly how you'd verify it** — what you'd look at to confirm it's done.

When the work splits into several tasks, one more thing must be clear: **where the boundaries are** — each piece should be independently completable, and their order (what depends on what) should be evident.

Once those are clear, `submit-task` takes over — keep what you produce high-level. Don't push the conversation, or the descriptions you write, past conceptual clarity.

## Usage

```
/discuss-new-task <issue description>
```

- `<issue description>`: a free-form, possibly rough description of a problem, gap, or idea surfaced mid-flight. May be a single issue or a larger "we need to create X" that spans several pieces.

**Example (single task):**
```
/discuss-new-task the setup section's steps are out of order, feels confusing
```

**Example (likely several tasks):**
```
/discuss-new-task I think we need a proper glossary — this is probably a few tasks, not one
```

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Gather context

Read in parallel to ground the discussion in the real project state rather than guessing:

- `<MILESTONE_DIR>/requirements.md` — the goal, constraints, and decisions the issue must fit within.
- `<MILESTONE_DIR>/TASKS_TODO.md` — pending tasks, to spot overlap and dependencies.
- `<MILESTONE_DIR>/TASKS_DONE.md` — completed work, to catch issues already addressed.
- `CLAUDE.md` — the project's conventions and context, so the discussion uses the project's real terms.

If relevant project files are named or implied by the issue, read them too. Concrete grounding makes for sharper questions.

### 2. Triage before discussing

Before asking anything, check two things:

- **Already covered?** If existing tasks in `TASKS_TODO.md` or `TASKS_DONE.md` already address this, say so and name them instead of starting a discussion. For a larger chunk, part of it may already be tracked — point out what's covered and focus the discussion on the genuinely new remainder.
- **Already clear?** If the issue is *already* conceptually clear and is plainly a single task (affected system, desired behavior, and verification all evident), skip straight to step 5 and propose the handoff. Don't ask questions for their own sake.

### 3. Size the work: one task or several?

Decide whether the issue is a single task or a chunk that needs several. The anchor is the same one the task list uses: **a task should be completable in a single `/complete-task` invocation.** "Do X and Y" is two tasks when X and Y can be completed and verified independently.

Treat it as several tasks when any of these hold:
- The user flagged it as a bigger chunk or "a few entries."
- The work spans multiple systems, or mixes an immediate fix with follow-on improvements.
- There are parts that could be completed and verified on their own, in sequence.

Lean toward a single task when in doubt — splitting has a cost. Don't manufacture extra tasks to look thorough.

If it's several, sketch a **provisional** breakdown into atomic, ordered pieces — just a working title or one-line gist per piece. You're finding the task boundaries here, not writing the tasks; resist any detail that belongs to `submit-task`.

### 4. Clarify the ambiguities

Open with a one-sentence restatement of the issue as you understand it. If you're treating it as several tasks, follow that with your provisional breakdown so the user can react to the shape early.

Then surface only the ambiguities that actually block writing the task(s). Anchor each question to the readiness checks — affected system, desired behavior, verification — and, for a multi-task chunk, to the **boundaries and order** between pieces (is this really one task or two? does A have to land before B?).

Format as:

**Understood issue:** one sentence.

**Proposed breakdown (if several):**
1. <piece — one line>
2. <piece — one line>

**Questions:**
1. ...
2. ...
3. (optional) ...

Continue the conversation: after each answer, either ask the next question that matters most or confirm things are clear enough. Keep replies short and move fast. Favor judgment over completeness — listing every conceivable edge case wastes the user's time. The breakdown is allowed to shift as you learn: pieces may merge, split, or drop.

Reach for `/discuss-open-question` instead if the ambiguity is really an open design decision about the milestone's direction (a trade-off to deliberate and record in `requirements.md`), not a concrete issue to queue up.

### 5. Propose the handoff

When the readiness checks are satisfied, synthesize what you've learned into refined, self-contained issue description(s) — each at the high level `submit-task` expects as input, **not** a fleshed-out task. Naming the affected system, the desired behavior, and how to verify it is enough.

**If it's a single task**, propose one handoff:

**Refined issue:**
> <2–4 sentences naming the affected system, the desired behavior, and how to verify it.>

Then offer to invoke `/submit-task "<refined issue>"`.

**If it's several tasks**, present the ordered list for sign-off before submitting anything:

**Proposed tasks (in order):**
1. **<short title>** — <1–3 sentence high-level description: system, desired behavior, verification.>
2. **<short title>** — <...>

Confirm the breakdown reads right — number, ordering, and scope of the pieces. On the user's confirmation, invoke `/submit-task "<description>"` **once per task, in dependency order (prerequisites first)**. After all are submitted, give a one-line summary of what was added.

In either case, if the user wants to adjust wording, ordering, or the split, incorporate the change and re-offer before handing off.
