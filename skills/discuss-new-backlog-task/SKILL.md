---
name: discuss-new-backlog-task
description: Clarify a rough or ambiguous implementation issue discovered during development into one or more clear backlog tasks, then hand off to /submit-backlog-task. Use this whenever the user reports a bug, gap, or "we should also..." idea mid-implementation but the description is too vague to act on, or whenever they want to talk through an issue before adding it to the milestone backlog. Also use it when the user flags that something is a bigger chunk of work that may need several task entries, or when a single reported issue turns out to be too large for one task — this skill will break it into an ordered set of task-sized pieces before handing each off. Prefer this over jumping straight to /submit-backlog-task when the affected system, desired behavior, or how to verify the fix is unclear, or when the right number of tasks isn't obvious yet.
---

# discuss-new-backlog-task

Facilitates a short, focused conversation that turns a half-formed issue — the kind that surfaces while building — into a description concrete enough to become a backlog task. This skill is the conversational front-end for `/submit-backlog-task`: it clarifies just enough, then proposes the handoff. It never writes to the backlog itself.

Most issues are a single task. But some are a bigger chunk of work that only makes sense as **several** tasks — the user may flag this up front ("this might be a few entries"), or it may become apparent mid-discussion that one "issue" is really two or three independent pieces. When that happens, this skill helps draw the boundaries and produces an ordered set of task-sized descriptions, then hands each off in turn.

The bar to clear is **conceptual clarity**, not full implementation detail. For each task that comes out of the discussion, three things must be unambiguous:

1. **Which system** the issue touches (a file, component, mechanic, or requirement).
2. **What the desired behavior is** — what should be true after the fix that isn't true now.
3. **Roughly how you'd verify it** — what you'd look at to confirm it's done.

When the work splits into several tasks, one more thing must be clear: **where the boundaries are** — each piece should be independently implementable, and their order (what depends on what) should be evident.

Once those are clear, `submit-backlog-task` fills in the file-, method-, and step-level specifics for each task. That is its job, not yours — keep what you produce high-level. Don't push the conversation, or the descriptions you write, past conceptual clarity.

## Usage

```
/discuss-new-backlog-task <issue description>
```

- `<issue description>`: a free-form, possibly rough description of a problem, gap, or idea discovered during development. May be a single bug or a larger "we need to build X" that spans several pieces.

**Example (single task):**
```
/discuss-new-backlog-task enemies sometimes walk through walls, feels broken
```

**Example (likely several tasks):**
```
/discuss-new-backlog-task I think we need a proper save system — this is probably a few tasks, not one
```

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded backlog path.

### 1. Gather context

Read in parallel to ground the discussion in the real project state rather than guessing:

- `<MILESTONE_DIR>/requirements.md` — the goal, constraints, and decisions the issue must fit within.
- `<MILESTONE_DIR>/TASKS_TODO.md` — pending tasks, to spot overlap and dependencies.
- `<MILESTONE_DIR>/TASKS_DONE.md` — completed work, to catch issues already addressed.
- `CLAUDE.md` — the stack and conventions, so the discussion uses the project's real terms.

If relevant source files are named or implied by the issue, read them too. Concrete grounding makes for sharper questions.

### 2. Triage before discussing

Before asking anything, check two things:

- **Already covered?** If existing tasks in `TASKS_TODO.md` or `TASKS_DONE.md` already address this, say so and name them instead of starting a discussion. For a larger chunk, part of it may already be tracked — point out what's covered and focus the discussion on the genuinely new remainder.
- **Already clear?** If the issue is *already* conceptually clear and is plainly a single task (affected system, desired behavior, and verification all evident), skip straight to step 5 and propose the handoff. Don't ask questions for their own sake.

### 3. Size the work: one task or several?

Decide whether the issue is a single task or a chunk that needs several. The anchor is the same one the backlog uses: **a task should be completable in a single `/implement-backlog-task` invocation.** "Implement X and Y" is two tasks when X and Y can be built and verified independently.

Treat it as several tasks when any of these hold:
- The user flagged it as a bigger chunk or "a few entries."
- The work spans multiple systems, or mixes an immediate fix with follow-on improvements.
- There are parts that could be implemented and verified on their own, in sequence.

Lean toward a single task when in doubt — splitting has a cost, and `submit-backlog-task` can still position a lone task correctly. Don't manufacture extra tasks to look thorough.

If it's several, sketch a **provisional** breakdown into atomic, ordered pieces — just a working title or one-line gist per piece. You're finding the task boundaries here, not writing the tasks; resist any detail (file paths, contract surface, method names) that belongs to `submit-backlog-task`.

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

Reach for `/discuss-open-question` instead if the ambiguity is really an open design decision about the milestone's direction (a trade-off to deliberate and record in `requirements.md`), not a concrete implementation issue to queue up.

### 5. Propose the handoff

When the readiness checks are satisfied, synthesize what you've learned into refined, self-contained issue description(s) — each at the high level `submit-backlog-task` expects as input, **not** a fleshed-out task. Naming the affected system, the desired behavior, and how to verify it is enough; leave the contract surface, file paths, and success criteria to `submit-backlog-task`.

**If it's a single task**, propose one handoff:

**Refined issue:**
> <2–4 sentences naming the affected system, the desired behavior, and how to verify it.>

Then offer to invoke `/submit-backlog-task "<refined issue>"`.

**If it's several tasks**, present the ordered list for sign-off before submitting anything:

**Proposed tasks (in order):**
1. **<short title>** — <1–3 sentence high-level description: system, desired behavior, verification.>
2. **<short title>** — <...>

Confirm the breakdown reads right — number, ordering, and scope of the pieces. On the user's confirmation, invoke `/submit-backlog-task "<description>"` **once per task, in dependency order (prerequisites first)**. Submitting in order lets each task be positioned correctly relative to the ones already inserted. After all are submitted, give a one-line summary of what was added.

In either case, if the user wants to adjust wording, ordering, or the split, incorporate the change and re-offer before handing off.

## Rules

- Do not create or edit any files, and do not write to the backlog. Producing the task(s) is `submit-backlog-task`'s job; this skill only clarifies and hands off.
- Keep your output high-level. The refined description(s) you pass to `submit-backlog-task` should name the system, behavior, and verification — and stop there. Don't write the contract surface, file paths, or success criteria; duplicating that work slows the user down and steps on `submit-backlog-task`.
- Don't over-interrogate, and don't over-split. Stop at conceptual clarity, and prefer fewer tasks when a split isn't clearly warranted — each task should be independently implementable in a single `/implement-backlog-task` invocation.
- For a multi-task chunk, confirm the ordered breakdown with the user before submitting, then hand off one task at a time in dependency order.
- Ground questions in the files you read, not in assumptions. Prefer the project's real names for systems and files.
- If the issue (or part of it) duplicates tracked work, stop and point to it rather than starting a discussion.
- Keep each response tight after the opening restatement; this should feel like a quick clarifying exchange, not an interview.
