# Alternatives procedure (shared core)

This is the single source of truth for enumerating the honest alternatives of one open
question in the current milestone. It is followed inline by the `discuss-open-question`
skill when the question it is deliberating carries no alternatives yet, and once per question
by the read-only `provide-alternatives-to-open-question` subagent during the alternatives
sweep. The caller supplies the one input below and renders the result; this file describes
only the analytical work itself — ground, then enumerate. Picking one of the alternatives is
a separate unit of work, run later by a different runner over the set this procedure
produces, and lives in `${CLAUDE_PLUGIN_ROOT}/shared/recommend-procedure.md`; nothing here forms a
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

**Name the axes first.** Before drafting any option, name the axes the underlying decision
turns on — the decision the question exists to settle, not only the choice its wording
offers. An axis is any dimension on which a real answer can take a different position:

- A choice between approaches is an axis whose values are those approaches.
- A degree or parameter value is an axis like any other. Its values are the points at which
  the key advantage or drawback genuinely changes, a middle of the range included wherever
  it trades differently from both ends; values whose trade-off is the same are one value,
  described by its range.
- Each assumption the question's wording takes for granted is an axis too, with accepting it
  and rejecting it as its values, so rejecting a premise comes out of this same step.
- Every axis also has a none position: not having that element at all, keeping what exists
  as it stands, removing it outright, or leaving it unenforced. It is a value like the
  others wherever it is honestly viable, and it is most easily missed exactly when the
  wording lists only ways of doing the element.

Take the values from the underlying decision, not from the list the wording offers: a
question that names two ways of doing something has not shown that doing it is settled.

An axis a sibling question owns is not this question's to vary: the sibling scope step 1
sets holds here, so no option takes a position on it.

**Weigh not doing the thing.** On every question, apart from the axes above, weigh the
direction of not doing what the question is about. List it as an option when it is honestly
viable and leave it out otherwise, without noting that it was weighed. Postponing the
decision is one form of this direction, not a separate one: the set lists at most one option
for not doing the thing now, and that option says whether it means never or later.

**Build the options as positions on the axes.** Each option is one position on every axis;
on a question with more than one axis it is one combination of values. Weigh every
combination in your reasoning and describe each viable one; a combination that cannot work
is dropped, not listed. Include no strawmen and no padding: an option listed only to look
thorough wastes the reader's time, and a question with only one viable path should say so
rather than invent rivals. How many options the set holds follows from its axes and which of
their combinations are viable, and from nothing else. For each option state three things:

- **What it is** — only what the option is: its position on each axis. Any reason for or
  against it belongs in the next two fields, and its length follows from how many positions
  there are to state.
- **Key advantage** — the strongest reason to choose it.
- **Key drawback** — the main cost or risk it carries. Where the option's viability depends
  on an axis a sibling question owns, name that axis here as a condition, without naming the
  outcome you expect.

**Test the set.** The finished set must pass two tests, and a set that fails either is
reworked until it passes both:

- **Distinct** — every two options differ in substance on at least one axis. Two options
  that differ only in wording, emphasis, or a detail that changes neither trade-off are one
  option.
- **Covering** — the set covers the underlying decision rather than the question's wording:
  every viable position on every axis appears in some option, the none position included,
  every viable combination is described as one option rather than left for the reader to
  assemble from two, and the direction of not doing the thing appears wherever it is
  honestly viable.

Each option stands on its own terms. Its three fields describe the option against the
question and the project as they are now — never against an outcome assumed for a sibling
question, which the enumeration has no basis to assume. The set you enumerate is the option
set every later pick over this question chooses from, and it outlives the decisions that
follow it, so it must be complete now: an option left out cannot be recommended later, and
an option the set carries stays available to a later pick even after a decision elsewhere
has narrowed the field.

The alternatives together form one contiguous, self-contained unit that stays attached to
the question they answer — it reads as a single coherent block about that one question, not
scattered commentary.
