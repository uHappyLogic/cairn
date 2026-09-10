# Recommendation procedure (shared core)

This is the single source of truth for producing alternatives and a recommendation for one
open question in the current milestone. It is followed inline by the `discuss-open-question`
skill as the analytical spine of an interactive deliberation, and once per question by the
read-only `recommend-open-question` subagent during a sweep. The caller supplies the one
input below and renders the result; this file describes only the analytical work itself —
ground, enumerate honest alternatives, recommend one.

## Inputs

This procedure produces a recommendation for one question the caller supplies:

- **QUESTION** — the resolved open or deferred question to reason about (its Short Title and
  text). The caller has already selected it; forming the alternatives and the single
  recommendation for it is this procedure's job.

## Procedure

### 1. Ground in the real project state

Before forming any view, read the context that bears on the question: the milestone's
`requirements.md` and the actual project artifacts the question turns on. Prefer reading the
live project over reasoning from memory — the point is to ground the recommendation in what
the project actually is, not what you recall it to be. All of this reading is read-only;
forming a recommendation changes nothing.

Part of that grounding is the project-wide answering-principle store
`milestones/answer_decision_principles.md` — a fixed path at the `milestones/` root, above
any one milestone. Read it in place and note any confirmed principle that bears on this
question. Presence of a principle in that file means it is user-confirmed.

Reading `requirements.md` also surfaces the sibling questions, and a recommendation already
attached to a sibling that is itself still unanswered (open or deferred) is legitimate input
to this one. Whenever the recommendation you form leans on such a sibling's recommendation,
disclose that dependency: name the sibling (its Short Title) and the option you assumed it
will settle on. The caller decides how that disclosure is rendered.

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
that one question, not scattered commentary.
