# Recommendation procedure (shared core)

This is the single source of truth for picking one recommendation over an
already-enumerated alternative set for an open question in the current milestone. It is
followed inline by the `recommend-all-open-questions` skill over every question its run
annotates, held in view together as one whole-set judgment, and inline by the
`discuss-open-question` skill for the one question it is deliberating. The caller supplies
the two inputs below and renders the result; this file describes only the analytical work
itself — ground, then recommend one. Enumerating the alternatives is a separate unit of work,
run earlier by a different runner, and lives in
`${CLAUDE_PLUGIN_ROOT}/shared/alternatives-procedure.md`; this procedure takes its output as
given.

## Inputs

This procedure produces one recommendation for each question the caller supplies:

- **QUESTION** — the resolved question to reason about (its Short Title and text). The
  caller has already selected it; forming the single recommendation for it is this
  procedure's job.
- **ALTERNATIVES** — the question's alternative set, each option carrying its label, what it
  is, its key advantage, and its key drawback. The set is taken as given: the recommendation
  names one of its options by that option's label, and this procedure never adds an option
  to the set or drops one from it — a caller that widens the set does so before running this
  procedure, and the recommendation then names an option of the widened set.

A caller holding several questions may run the procedure over all of them in one pass,
keeping every question's set in view while it reasons; the contract below is per question,
and each question still gets one recommendation of its own.

## Procedure

### 1. Ground in the real project state

Before forming any view, read the context that bears on the question: the milestone's
`requirements.md`, its `open_questions.xml`, and the actual project artifacts the question
turns on. Prefer reading the live project over reasoning from memory — the point is to ground
the recommendation in what the project actually is, not what you recall it to be. All of this
reading is read-only; forming a recommendation changes nothing.

Part of that grounding is the project-wide answering-principle store
`milestones/answer_decision_principles.md` — a fixed path at the `milestones/` root, above
any one milestone. Read it in place and note any confirmed principle that bears on this
question. Presence of a principle in that file means it is user-confirmed.

Reading `<MILESTONE_DIR>/open_questions.xml` whole — with the file-reading tool, exactly as
`requirements.md` is read beside it — surfaces the sibling questions with their own
alternative sets, and a recommendation already attached to a sibling that is itself still
unanswered, or the one you are forming for it in the same pass, is legitimate input to this
one. Whenever the recommendation you form leans on a sibling settling on a particular one of
its alternatives, disclose that dependency: name the sibling (its Short Title) and the option
you assumed it will settle on, by that option's label in the sibling's own set. The caller
decides how that disclosure is rendered. That whole read is for reasoning only: every locate,
list, or lift of a block is a call to the plugin's open-question tool,
`python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py <subcommand> <MILESTONE_DIR> …`, never a
search over the file.

### 2. Recommend one

State a single preferred option from ALTERNATIVES with a brief, direct rationale. Do not
hedge. If two options are genuinely equivalent, say so plainly and name the one thing that
should break the tie rather than pretending a winner exists.

A confirmed principle that bears on this question (found while grounding, step 1) is a
**weighted advisory factor** in the recommendation, not a binding filter: it is a strong
default in favor of the option it supports. Merit may override a bearing principle, but only
for a specific reason you state — a bearing principle never vetoes a candidate outright and
never removes it from consideration. Whenever a confirmed principle influenced the
recommended pick, cite it: the recommendation must name the principle it leaned on, and when
more than one bore on the pick it names each of them. When no confirmed principle bears on
the question, form the recommendation exactly as you otherwise would — the
single-recommendation contract is unchanged from a project with no principles at all.

The set may have aged since it was enumerated: a decision recorded since — under
`## Decisions` of `requirements.md`, or the answer to a sibling question — can have closed
one of its options. When it has, recommend the best option still viable and state in the
rationale which option that decision closed and why, so the pick reads as a choice among what
survives rather than a silent narrowing. Only when no option of the set survives at all is
there nothing to recommend: say so plainly, naming the decision that closed the set, and
form no pick — what follows from that is the caller's.

The recommendation reads as attached to the question it answers and to the alternative set
it chose from — one coherent statement about that one question, not scattered commentary.
