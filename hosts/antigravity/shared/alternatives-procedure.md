# Alternatives procedure (shared core)

This is the single source of truth for enumerating the honest alternatives of one open
question in the current milestone. It is followed inline by the `discuss-open-question`
skill when the question it is deliberating carries no alternatives yet, and once per question
by the read-only `provide-alternatives-to-open-question` subagent during the alternatives
sweep. The caller supplies the one input below and renders the result; this file describes
only the analytical work itself — ground, then enumerate. Picking one of the alternatives is
a separate unit of work, run later by a different runner over the set this procedure
produces, and lives in `.agents/plugins/cairn/shared/recommend-procedure.md`; nothing here forms a
preference.

## Inputs

This procedure produces the alternative set for one question the caller supplies:

- **QUESTION** — the resolved question to reason about (its Short Title and text). The
  caller has already selected it; enumerating the realistic options for it is this
  procedure's job.

## Procedure

### 1. Ground in the real project state

Before listing any option, read the context that bears on the question: the milestone's
`requirements.md` (its goal, relevant starting state, and recorded decisions — a decision
recorded there already closes any option it rules out) and the actual project artifacts the
question turns on. Prefer reading the live project over reasoning from memory — the point is
to ground each option in what the project actually is, not what you recall it to be. All of
this reading is read-only; enumerating alternatives changes nothing.

The milestone's sibling questions — the other open questions standing beside this one —
bound it: they mark where this question ends and another begins, so an option that really
answers a sibling is left to that sibling. They supply scope and nothing more: no sibling has
settled on anything while its alternatives are being enumerated, so no option here presumes
how a sibling will settle.

### 2. Enumerate the alternatives

List the genuinely realistic options — typically two to four. Include no strawmen and no
padding: an option listed only to look thorough wastes the reader's time, and a question
with only one viable path should say so rather than invent rivals. For each option state
three things:

- **What it is** — one sentence.
- **Key advantage** — the strongest reason to choose it.
- **Key drawback** — the main cost or risk it carries.

Each option stands on its own terms. Its three fields describe the option against the
question and the project as they are now — never against an outcome assumed for a sibling
question, which the enumeration has no basis to assume; where an option's merit genuinely
turns on how a sibling settles, say so in its drawback as a condition, without naming the
outcome you expect. The set you enumerate is the option set every later pick over this
question chooses from, and it outlives the decisions that follow it, so it must be complete
now: an option left out cannot be recommended later, and an option the set carries stays
available to a later pick even after a decision elsewhere has narrowed the field.

The alternatives together form one contiguous, self-contained unit that stays attached to
the question they answer — it reads as a single coherent block about that one question, not
scattered commentary.
