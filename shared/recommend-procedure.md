# Recommendation procedure (shared core)

This is the single source of truth for producing alternatives and a recommendation for one
open question in the current milestone. It is followed in two ways:

- **Inline**, by the `discuss-open-question` skill, which runs it directly in the user's
  conversation as the analytical spine of an interactive deliberation.
- **By a read-only subagent**, `recommend-open-question`, which runs the same core once per
  question during a `recommend-all-open-questions` sweep and returns the result for the
  orchestrator to embed.

The wrappers add their own framing (conversation vs. one-shot return, how the result is
rendered, and where it goes). This file describes only the analytical work itself — ground,
enumerate honest alternatives, recommend one — and says nothing about how callers present or
record the result.

## Inputs

This procedure produces a recommendation for one question the caller supplies:

- **QUESTION** — the resolved open or deferred question to reason about (its Short Title and
  text). The caller has already selected it; forming the alternatives and the single
  recommendation for it is this procedure's job.

Rendering the result and any side-effects are the caller's job.

## Procedure

### 1. Ground in the real project state

Before forming any view, read the context that bears on the question: the milestone's
`requirements.md` and the actual project artifacts the question turns on. Prefer reading the
live project over reasoning from memory — the point is to ground the recommendation in what
the project actually is, not what you recall it to be. All of this reading is read-only;
forming a recommendation changes nothing.

Part of that grounding is the project-wide answering-principle store
`milestones/answer_decision_principles.md` — a fixed path at the `milestones/` root, above
any one milestone. Read it in place (name that path directly; the confirmed principles are
not a caller-supplied input alongside QUESTION) and note any confirmed principle that bears
on this question. Presence of a principle in that file means it is user-confirmed. How a
bearing principle shapes the recommendation is covered in step 3.

Grounding is not the same as coupling to other questions. Reading `requirements.md`
incidentally surfaces the sibling questions, but a recommendation for this question is
formed in isolation from any *other* question's recommendation — never treat another
question's recommendation as an input to this one. That isolation is a constraint the caller
enforces across questions; it never narrows the honest grounding you do for the question at
hand.

### 2. Enumerate the alternatives

List the genuinely realistic options — typically two to four. Include no strawmen and no
padding: an option listed only to look thorough wastes the reader's time, and a question
with only one viable path should say so rather than invent rivals. For each option state
three things:

- **What it is** — one sentence.
- **Key advantage** — the strongest reason to choose it.
- **Key drawback** — the main cost or risk it carries.

### 3. Recommend one

State a single preferred option with a brief, direct rationale. Do not hedge. If two options
are genuinely equivalent, say so plainly and name the one thing that should break the tie
rather than pretending a winner exists.

A confirmed principle that bears on this question (found while grounding, step 1) is a
**weighted advisory factor** in the recommendation, not a binding filter: it is a strong
default in favor of the option it supports. Merit may override a bearing principle, but only
for a specific reason you state — a bearing principle never vetoes a candidate outright and
never drops it from the alternatives. Whenever a confirmed principle influenced the
recommended pick, cite it: the recommendation must name the principle it leaned on, and when
more than one bore on the pick it names each of them. When no confirmed principle bears on
the question, form the recommendation exactly as you otherwise would — the alternatives and
single-recommendation contract is unchanged from a project with no principles at all.

The alternatives and the recommendation together form one contiguous, self-contained unit
that stays attached to the question it answers — it reads as a single coherent block about
that one question, not scattered commentary. How that unit is laid out, marked up, and either
shown to the user or handed back for embedding is the wrapper's concern, not this file's.

## Rules

- Ground in the real project state before forming a view — the live project over memory — and read
  the project-wide principle store `milestones/answer_decision_principles.md` in place as
  part of that grounding.
- Two to four alternatives, no strawmen and no padding; each carrying what-it-is / key
  advantage / key drawback.
- Exactly one recommendation, stated directly with no hedging; on a genuine tie, say so and
  name what breaks it.
- A confirmed principle that bears on the question is a weighted advisory default in favor of
  its supported option — overridable only for a stated reason, never a veto that drops a
  candidate — and any principle that influenced the pick must be cited. When no principle
  bears, the recommendation is produced exactly as before.
- Isolation is a cross-question constraint on the caller: never build one question's
  recommendation on another's. It never restricts the read-only grounding you do for the
  question at hand.
- Produce only the alternatives and the recommendation as one contiguous, self-contained
  unit — nothing about how the result is rendered, recorded, or committed.
