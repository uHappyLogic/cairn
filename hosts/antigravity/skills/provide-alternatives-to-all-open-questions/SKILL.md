---
name: provide-alternatives-to-all-open-questions
description: Annotate every open question in the current milestone lacking alternatives with a set of alternatives, dispatching one subagent per question.
---

# provide-alternatives-to-all-open-questions

This is the first of the two annotating passes over a milestone's open questions: it gives
every `<open-question>` block that carries no `<alternative>` children yet an honest set of
alternatives, and the recommendation pass, `/recommend-all-open-questions`, later picks one of
them per block against that frozen set. Per question it dispatches a read-only subagent that
returns the `<alternative>` elements as the block's XML sub-elements, and the orchestrator is
the only party in this pass that changes the question document,
`<MILESTONE_DIR>/open_questions.xml` — every read and write it makes of that document is a
call to the plugin's open-question tool, `list` and `locate` to gather and `embed` to write,
never a direct read or edit. Alternatives are enumerated per question against the siblings as
scope only, so the dispatches are independent: they run together where the host allows it, each
return is judged and embedded as it lands, and each embedded return is committed the moment it
is written — one `Alternatives-annotation: <Short Title>` commit per annotated question, none for
a skipped one. It is **argument-free**, records **no decisions**, triggers **no cascades**, and
writes no `<recommendation>` — it only supplies the alternatives the recommendation pass reads.

## Usage

```
/provide-alternatives-to-all-open-questions
```

Takes no arguments — it sweeps every `<open-question>` block in the current milestone's
`open_questions.xml`.

## Workflow

### 0. Find the current milestone

Follow `.agents/plugins/cairn/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`.
Never use a hardcoded path.

### 1. Gather the questions once, in three tool calls

**a. Every question.** Run

```
python3 .agents/plugins/cairn/tools/open_questions.py list <MILESTONE_DIR>
```

It prints the `id` (Short Title) of every `<open-question>` block, one per line in document
order. If it prints nothing, the document holds no questions: say so and stop. If it fails, its
one `Error: <reason>` line on stderr is the report: print it and stop.

**b. The ones without alternatives.** Run

```
python3 .agents/plugins/cairn/tools/open_questions.py list --without-alternatives <MILESTONE_DIR>
```

It prints, in document order, the ids of the blocks carrying no `<alternative>` element — the
ones this run annotates. Every other block already carries its alternatives and is **skipped**
(step 2). If this call prints nothing, every block already carries alternatives: there is
nothing to dispatch, so skip **c** and step 3 and go straight to step 4's no-op line.

**c. Their blocks.** Run one `locate` over every id **b** printed, each id quoted as its own
argument:

```
python3 .agents/plugins/cairn/tools/open_questions.py locate <MILESTONE_DIR> "<id 1>" "<id 2>" …
```

It prints each block verbatim — its `<open-question id="…">` wrapper, its `<question>` child, and
its closing tag — consecutively in the order named. Hold these blocks: each is the block its
question's dispatch prompt carries, and nothing is rebuilt from them.

Gather this set **once**: there is **no** per-question live-re-check against the document and
**no** outer re-gather loop. This run only adds children to blocks — it records no decisions
and triggers no cascades — so the question set never shrinks under it and the gathered blocks
stay valid for the whole run.

### 2. Blocks already carrying alternatives are skipped (re-run idempotency)

Step 1's `--without-alternatives` filter is the whole skip test: a block that already carries
an `<alternative>` element is never dispatched and never re-annotated, so re-runs are cheap and
an existing alternative set is left as it stands — that set is frozen for the recommendation
pass, which picks against it. The primary re-run motive is exactly the bare set a later
`/review-milestone-requirements` pass surfaces.

**Escape hatch for a stale alternative set:** to force a fresh set on a block, run

```
python3 .agents/plugins/cairn/tools/open_questions.py strip <MILESTONE_DIR> "<Short Title>" …
```

(one or more Short Titles), then re-run this skill. The bare `strip` deletes every child of
each named block but its `<question>` — its alternatives and, with them, any recommendation
picked against them — leaving the wrapper and `<question>` intact and every other block
untouched; the block now carries no `<alternative>`, so the next run's `--without-alternatives`
list yields it and this pass regenerates it, and the recommendation pass then re-picks on its
next run. That call and a re-run are the whole hatch — `open_questions.xml` is never edited by
hand, since the tool is its sole writer.

When such a regenerated block's new alternative ids differ from the options that surviving
dependents' `<depends-on question="…" option="…"/>` elements assumed of it, **leave those
dependents exactly as they are**: do not strip or re-dispatch them, do not rewrite their
`option` values, and print no mismatch advisory. A `<depends-on>` records what a dependent
assumed, not a pointer that must track its target; reconciling it against the option actually
recorded is the answer-time cascade's job, never this pass's. A dependent the user also wants
regenerated is named in the same `strip` call.

### 3. Dispatch the read-only subagent per surviving question

Dispatch one read-only subagent per question step 1b printed, **all of them together where the
host can run several agent dispatches at once and one after another where it cannot** — with no
cap beyond one dispatch per surviving question — and run the per-return pipeline below on each
return **as it lands**, in either arm. No ranking or ordering precedes the dispatches: an
alternative set is enumerated against the sibling questions as scope only, never against how a
sibling will settle, so no dispatch reads what another wrote and their order changes nothing.
Both arms write the same blocks and land the same commits; the sequential arm differs only in
wall-clock time.

Use the `Agent` tool with `subagent_type` set to the namespaced registry name of the
`provide-alternatives-to-open-question` agent (singular — the per-question subagent) under this
plugin's namespace, `cairn:provide-alternatives-to-open-question` — one dispatch per surviving
question. Pass it that question's **Short Title**, the `<MILESTONE_DIR>` resolved in step 0, and
the question's block exactly as `locate` printed it in step 1:

```
Enumerate the alternatives for this single open question.

Short Title: <Short Title>

Milestone directory: <MILESTONE_DIR>

Question block:
<the block as locate printed it>
```

The block is the only question text the prompt carries: the subagent reads the milestone's
documents itself, read-only, for whatever surrounding grounding it needs, so the orchestrator
never reads them to assemble context.

The subagent is **read-only** — it mutates nothing. It returns the ready-to-embed XML
sub-elements as its final message — one `<alternative id="...">` element per option, each with
its what-it-is text and child `<advantage>` and `<drawback>` elements — and **only** those
child elements, never the `<open-question>` wrapper, the `<question>` element, a
`<recommendation>`, an `<applied-principle>`, or a `<depends-on>` element. The orchestrator does
**all** the writing, through the tool.

**Judge every return in this fixed order — last-line verdict, then `embed`, then a single
repair attempt when `embed` refuses — and commit what embedded.** The stages are **one
per-return pipeline**, run the moment a return lands: judge it, repair it once if judging
failed, re-judge what comes back, commit the annotation if it embedded (sub-step d), then turn
to the next return that has landed. Returns are judged one at a time as they arrive, so the
`embed` and commit of one question never interleave with another's, however many dispatches are
still in flight.

**a. Last-line verdict.** Read the return's **last non-whitespace line**. If that line begins
with `FAILED:`, the return is an **explicit failure**: skip that question alone — embed nothing,
leave its block untouched, note its Short Title with the reason (the text after `FAILED:`) for
the step-4 advisory — and make no further attempt on it, **never a repair**, even when
`<alternative>`…`</alternative>` elements sit above that line. Only when the last
non-whitespace line is **not** a `FAILED:` line does judging continue, and a `FAILED:` token
appearing anywhere else in the message is then ordinary text with no special meaning. This
verdict is the only judging the orchestrator does itself; everything else is the tool's.

**b. Pipe the whole message to `embed --alternatives`.** Run

```
python3 .agents/plugins/cairn/tools/open_questions.py embed --alternatives <MILESTONE_DIR> "<Short Title>" <<'EOF'
<the agent's whole final message, verbatim>
EOF
```

The message travels on standard input through a **quoted-delimiter heredoc** (`<<'EOF'`, so
nothing inside is expanded; pick a delimiter line the message does not contain), **whole and
unedited** — never trim it, never extract the elements yourself, never reorder, rewrite, or drop
a returned element. The tool slices the fragment from the first `<alternative` line through the
last `</alternative>` line (a grounding summary above or a closing remark below is discarded,
not a failure), parses and validates it — no `<open-question>` or `<question>` line, no text
outside the elements, at least one `<alternative>`, no element of the recommendation half, no
unknown element, a target block carrying no `<alternative>` yet — and writes those elements
into the existing block re-rendered in canonical form, so indentation, escaping, and child
grouping are the tool's, never the return's or yours.

- **Silent, exit 0** — the question is annotated. It gets no console mention, however its
  return arrived. Commit it now (sub-step **d**), then turn to the next return.
- **One `Error: <reason>` line on stderr, exit 1** — the return could not be embedded and the
  document is unchanged. Hold that line verbatim: it fills the repair template in **c**.

**c. Repair once, immediately.** A return that passed the last-line verdict but was refused by
`embed` gets **exactly one** repair attempt before any skip. Run that repair **immediately, for
this question** — the moment `embed` refuses — never by holding refused returns back and
running the repairs as a second phase once the last first return has landed. Other dispatches
still in flight are unaffected; their returns are judged as they land.

Spend at most **one** repair per question: a repaired return that is refused again is not
repaired a second time; it goes straight to the skip below.

Repair by whichever of these two branches the host supports, in this order:

- **Continue the same agent session.** Where the host can continue a finished agent session and
  you still hold that dispatch's handle — a follow-up message addressed to the agent id the
  `Agent` tool returned — send the corrective message below to **that same agent**. Its context
  is intact, so it re-emits from the analysis it already did.
- **Re-dispatch one fresh agent.** Where the host cannot continue a finished agent session, or
  the handle is gone, dispatch **one** fresh `cairn:provide-alternatives-to-open-question` agent
  for that question with the `Agent` tool, passing the **same prompt** as the original dispatch
  with the corrective message below appended to it as a shape reminder. This second dispatch
  redoes the analysis, so it is the fallback branch, never the preferred one.

Both branches send this fixed one-paragraph corrective message, whose single slot is
`<Error line>`:

```
A previous return for this question could not be embedded — <Error line>. Emit the `<alternative>`
elements — each with its what-it-is text and its child `<advantage>` and `<drawback>` elements —
as your whole final message, and check that message against both shape tests before sending it:
its first non-whitespace text starts with `<alternative`, and its last non-whitespace text ends
with `</alternative>`. Send those `<alternative>` elements and nothing else — no grounding summary
above them, no closing remark below them, and no `<recommendation>`, `<applied-principle>`, or
`<depends-on>` element among them.
```

Fill `<Error line>` with the `Error: <reason>` line the refused `embed` call printed in **b**,
verbatim — the same line the skip advisory would carry — so the one attempt is aimed rather than
blind. Never quote the offending prose back to the agent; the tool's line names what failed, and
the template asks for the sub-elements and nothing else.

Judge whatever comes back — the same agent's re-emitted message, or the fresh dispatch's return
— by sub-steps a and b exactly as a first return is judged: the same last-line verdict, the same
whole-message pipe to `embed --alternatives`. A silent `embed` annotates it like any other, and
sub-step **d** then commits it like any other.

Only a **second** failure — the repaired return's last line begins `FAILED:`, or `embed` refuses
it again — is a **skip of that question alone, never a run stop**: embed nothing for it, commit
nothing for it, leave its block untouched, note its Short Title with that second reason (the
`FAILED:` text or the second `Error:` line) for the step-4 advisory, and carry on with the other
returns.

**d. Commit the annotation, as soon as it is embedded.** Every silent `embed` — a first return's
or a repaired return's — is followed at once by this question's own commit: you are the
orchestrator, and you commit **per question, inside the return pipeline**. Read and follow the
shared commit procedure at `.agents/plugins/cairn/shared/commit-procedure.md`, carrying out its steps
yourself. Supply it these two inputs, and **no BODY**:

- **PATHS** — this question's own change: `<MILESTONE_DIR>/open_questions.xml` (the document the
  `embed` call wrote).
- **SUBJECT** — `Alternatives-annotation: <Short Title>` (the annotated question's handle).

That procedure owns the path-scoped staging (never `git add -A`), the dirty-own-path no-op guard,
and the subject-only commit. Commit once per annotated question — the per-question granularity
is the point — and only then judge the next landed return. A **skipped** question commits
nothing: a refused `embed` never writes, so there is nothing for the guard to stage, and no
commit is made for it. This pass requires **no** clean working tree: each commit is path-scoped
to the one document, so a dirty tree elsewhere stays out of it.

When the last dispatched question has been embedded and committed or skipped, step 3 is over:
go to step 4.

### 4. Report

Print exactly one fixed terse status line for the whole run, chosen by **what this run
committed**:

1. **An `embed` wrote** — step 3 reached its sub-step **d** for at least one question, so at
   least one `Alternatives-annotation: <Short Title>` commit landed — print
   `Alternatives embedded.`
2. **Else nothing was committed** — no `embed` wrote — print no success line; print instead a
   distinct one-line message stating that nothing changed and why: every block already carried
   `<alternative>` elements (step 1b printed nothing), or every dispatched question was still
   skipped after its repair attempt in step 3.

Each line is the whole of its output and names no identifier: no annotated-vs-skipped
breakdown, no per-question listing, and no next-step pointer to `/recommend-all-open-questions`.
The success line means there are new alternative sets for the recommendation pass to pick
against, and the no-op line that this run left git history untouched.

Alongside whichever line is chosen, print only the questions step 3 **still skipped after the
repair path** — a return whose last non-whitespace line began `FAILED:` (sub-step a), or one
`embed` refused **again** after its one repair attempt (sub-step c). List each as an advisory:
its Short Title with the reason it was skipped on (the second reason where a repair was spent),
one per line. This survives the terse-reporting rule because nothing else records it: the
per-question commits and the annotated `open_questions.xml` show only the questions that *were*
annotated, so a question left without alternatives is git-absent and the console must carry it —
and until it is annotated, the recommendation pass stops on it. Re-running this skill retries
exactly those blocks, since they still lack an `<alternative>` element.

A question that **was** annotated gets **no console mention at all**, however its return reached
the document: whether it arrived clean, whether the tool discarded surrounding text from it, or
whether it was embedded only after the single repair attempt. The embedded block in the diff is
the whole record, so a recovered return is reported exactly like a clean one — no
recovered-or-repaired listing, no count, no note.

If there were no questions at all, say so and stop (step 1a) — nothing to report.
