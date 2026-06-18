# Submit-task procedure (shared core)

This is the single source of truth for authoring one backlog task and inserting it into
the current milestone's `TASKS_TODO.md`. It is followed in two ways:

- **Inline**, by the `submit-task` skill, which runs these steps directly in the
  user's conversation (after its own triage) so the authoring context survives for
  follow-up tweaks.
- **In isolation**, by the `submit-task` agent, which runs the same steps in a
  throwaway subagent context for `derive-tasks` (bulk) so per-task technical reasoning
  never pollutes the caller's memory.

The wrappers add their own framing (where the inputs come from, the return protocol,
follow-up). This file describes only the work itself — author and insert — and says
nothing about how the outcome is signalled.

## Inputs

This procedure authors and inserts one task given two inputs the caller supplies:

- **BRIEF** — a high-level description naming the affected system, the desired behavior,
  and how to verify it. It is *not* fleshed out; fleshing it out is this procedure's job.
- **POSITION** — where to insert the authored task. One of:
  - `append` — add at the end of the file (the default; used when the caller feeds tasks
    in dependency order).
  - `before: <Task Title>` — insert immediately before that existing task section.
  - `after: <Task Title>` — insert immediately after that existing task section (and its
    `---`).

If POSITION is missing, treat it as `append`. This procedure inserts at the POSITION it is
given and never decides global ordering — the caller owns that, because the caller holds
the whole-milestone view.

## What a task is

**A task is a contract, not a script.** You are defining *what* the task achieves and the
surface other tasks will build on — not transcribing the code that achieves it. The
line-by-line "how" is the implementer's job, decided fresh against the live codebase by
the `implement-backlog-task` agent.

**State only what cannot be re-derived at implementation time.** The implementer
reconstructs the flow itself from the goal and the real code — so a numbered list of steps
is wasted tokens and re-decides things it is better placed to decide. What it *cannot*
re-derive is (a) the goal and its acceptance bar, and (b) the named surface and gotchas.
So write the task to serve two readers, with one section each for what only they can't
reconstruct:

1. **The implementer** — needs the goal (`Description`), the acceptance bar (`Success`),
   and any *non-obvious fact* that would otherwise cost it a discovery round (`Notes`). It
   does **not** need the flow spelled out; give it the freedom to write the code
   organically.
2. **The author of the *next* task** — sibling tasks are written before this one is built,
   so the names and behaviors others will reference can't yet be read from the code. Pin
   them down in `Provides` (its public surface), even while leaving the internals open.

## Procedure

### 1. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded backlog path.

### 2. Load context

Read in parallel (skip any file you already hold in context from earlier triage):

- `CLAUDE.md` — the project's tech stack, file organization, available MCP tools,
  build/test commands, and conventions. Ground every step and success criterion in this
  real environment.
- `<MILESTONE_DIR>/requirements.md` — the goal, constraints, and decisions the task must
  fit within. Pull exact file paths, names, numeric values, and thresholds from here
  rather than paraphrasing.
- `<MILESTONE_DIR>/TASKS_TODO.md` — existing task titles, to avoid title collisions and to
  locate the POSITION anchor.

If the brief names or implies specific source files, read them too — concrete grounding
produces a sharper contract and sharper notes.

### 3. Author the task

Use this exact template — it is the single source of truth for backlog task format:

```markdown
## <Task Title>

<1–3 sentence description of what this task does and why it is needed in this milestone.>

**Provides:** (omit this section entirely if the task introduces no new shared surface)
- <A named structure other tasks will reference: new class/singleton/scene/method/field/endpoint, with its threshold or signature.>
- <...>

**Notes:** (omit this section entirely if nothing about the task is non-obvious)
- <A non-obvious fact that would otherwise cost the implementer a round of discovery — a surprising behavior, an ordering constraint, a gotcha.>

**Success:**
- <Verifiable criterion observable in the Editor, Console, build output, or other automated checks.>
- <...>

---
```

There is no `Steps` section: the implementer derives the flow itself from `Description` +
`Success` against the live codebase. Do not reintroduce a step-by-step narration under any
heading.

Authoring guidelines:

- **Title**: 4–8 words, title-cased, unique within the file. If it would collide with an
  existing title, distinguish it.
- **`Provides` is the forward contract — binding on sibling tasks.** Name only the things
  *other tasks will reference* — the new file, method/class/field/singleton/scene being
  introduced, the public API, the threshold values — because sibling tasks are authored
  against those names before this task is built. The implementer treats these as fixed.
  Don't list private fields, exact statements, or message strings that nothing else
  depends on. If the task creates no new shared surface (e.g. a pure bugfix), omit the
  section rather than padding it.
- **`Notes` is advisory — implementer-only, and only the non-obvious.** If a behavior
  would surprise the implementer or cost it a round of discovery — e.g. "with no `Creep`
  objects in the test scene, `RegisterWaveStart()` makes `AllCreepsDead()` return true
  immediately, so Day2 fires on the next tick" — state it as a short note. This is
  high-value content precisely because it can't be cheaply re-derived. Do not use `Notes`
  to smuggle in a flow; if there's nothing non-obvious, omit it.
- **Quote numeric values, durations, thresholds, and configuration values** directly from
  the requirements doc — do not paraphrase them.
- **Atomic scope**: the task must be completable in a single `/implement-backlog-task`
  invocation, with no decisions left to make mid-task. If the brief secretly contains two
  independently-buildable pieces, author the one that matches the brief's primary intent
  and surface the leftover to the caller so it can decide — do not silently split or merge.
- **No open decisions.** Decide *which* approach (traceable to the requirements) — never
  "choose the appropriate approach". That is a different thing from spelling out the code:
  pick the strategy, leave the implementation.
- **`Success` is verification-only — never a back door for steps.** Each criterion must be
  checkable without human judgement: prefer "Build command exits with code 0", "File X
  exists at path Y", "Function Z is exported from W", Inspector/Console state. Avoid "looks
  correct" or "feels smooth", and avoid restating the procedure as a checklist of
  actions — criteria are *observable outcomes*, not moves.
- **No rationale or design discussion** — that belongs in `requirements.md`. Tasks are
  instructions, not explanations.

### 4. Insert at the specified position

`Read` the current `<MILESTONE_DIR>/TASKS_TODO.md`, then `Edit` it to insert your authored
section (including its trailing `---`).

- `append`: add the section at the end of the file.
- `before: <Title>`: insert immediately before that section's `##` heading line.
- `after: <Title>`: insert immediately after that section's trailing `---`.
- If a named anchor is not found, append at the end instead and note that you did.

The `---` separator after every task section is mandatory — `/implement-backlog-task`
parses sections by it. Never modify or reorder existing task sections; only insert your
new one.

## Rules

- Author exactly one task. Do not invent requirements not traceable to the brief or
  `requirements.md`.
- Do not modify, reorder, or delete any existing task section — insert only.
- Insert at the POSITION you were given; do not decide global ordering — the caller owns it.
- The `---` separator is mandatory; never omit it.
