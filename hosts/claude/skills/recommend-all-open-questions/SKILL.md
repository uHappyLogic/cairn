---
name: recommend-all-open-questions
description: Annotate every question in the current milestone's requirements with alternatives and a single recommended option.
---

# recommend-all-open-questions

This is the non-interactive batch path for producing recommendations on open questions. It
walks every question in the current milestone **most-significant-first, strictly one at a
time**, and, per question, dispatches a read-only subagent — the non-interactive twin of
`/discuss-open-question` — that returns **alternatives + a single recommendation** as the
`<open-question>` block's XML sub-elements. The orchestrator is the only party in this sweep
that changes the question document, `<MILESTONE_DIR>/open_questions.xml`, and every read and
write it makes of that document is a call to the plugin's open-question tool — `list` and
`locate` to gather, `embed` to write, `lift` to read back the line each commit records, `sort`
to reorder once at the end — never a direct read or edit. It embeds each accepted return
**before dispatching the next question**, so every later recommendation may build on the
sibling recommendations already embedded and declares each such use as a
`<depends-on question="…" option="…"/>` child of its block, and it commits each annotation the
moment it is embedded — one `Recommendation-annotation: <Short Title>` commit per annotated
question, none for a skipped one. After the last dispatch it sorts the document once — the
annotated blocks first, in the order the answer sweep will walk them, the un-annotated ones
last — and commits that reorder as its own `Question-ordering: <milestone_id>` commit, a fixed
end-of-run step of every run that found questions. It is **argument-free**, records **no
decisions**, and triggers **no cascades** — it only annotates and orders. Each embedded
recommendation is consumed later, when it is recorded as an answer, by
`/answer-open-question-with-recommendation` or the
`/answer-all-open-questions-with-recommendation` sweep.

## Usage

```
/recommend-all-open-questions
```

Takes no arguments — it sweeps every `<open-question>` block in the current milestone's
`open_questions.xml`.

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`.
Never use a hardcoded path.

### 1. Gather the questions once, in three tool calls

**a. Every question.** Run

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py list <MILESTONE_DIR>
```

It prints the `id` (Short Title) of every `<open-question>` block, one per line in document
order. If it prints nothing, the document holds no questions: say so and stop. If it fails, its
one `Error: <reason>` line on stderr is the report: print it and stop.

**b. The un-annotated ones.** Run

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py list --unannotated <MILESTONE_DIR>
```

It prints, in document order, the ids of the blocks carrying no `<recommendation>` element —
the ones this run annotates. Every other block already carries a recommendation and is
**skipped** (step 2). If this call prints nothing, every block is already annotated: there is
nothing to dispatch, so skip **c** and step 3 and go straight to step 4 — the end-of-run sort
runs on every run that found questions, this one included, and step 5 then picks the report
line from what the run committed. Never exit to the no-op line from here.

**c. Their blocks.** Run one `locate` over every id **b** printed, each id quoted as its own
argument:

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py locate <MILESTONE_DIR> "<id 1>" "<id 2>" …
```

It prints each block verbatim — its `<open-question id="…">` wrapper, its `<question>` child, and
its closing tag — consecutively in the order named. Hold these blocks: read once, they are spent
twice — as the **ranking input** in step 3 and as the **block each dispatch prompt carries**.
Nothing is rebuilt from them.

Gather this set **once**: there is **no** per-question live-re-check against the document and
**no** outer re-gather loop. This run only adds children to blocks — it records no decisions
and triggers no cascades — so the question set never shrinks under it and the gathered blocks
stay valid for the whole run. The order in which they are dispatched is decided in step 3.

### 2. Already-annotated blocks are skipped (re-run idempotency)

Step 1's `--unannotated` filter is the whole skip test: a block that already carries a
`<recommendation>` element is never dispatched and never re-annotated, so re-runs are cheap and
an existing recommendation is left as it stands. The primary re-run motive is exactly the
un-annotated set a later `/review-milestone-requirements` pass surfaces.

**Escape hatch for a stale recommendation:** to force a fresh recommendation on a block, run

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py strip <MILESTONE_DIR> "<Short Title>" …
```

(one or more Short Titles), then re-run this skill. `strip` deletes every child of each named
block but its `<question>`, leaving the wrapper and `<question>` intact and every other block
untouched; the block now carries no `<recommendation>`, so the next run's `--unannotated` list
yields it and the sweep regenerates it. That call and a re-run are the whole hatch —
`open_questions.xml` is never edited by hand, since the tool is its sole writer.

When such a regenerated block's new `<recommendation option>` differs from the option that
surviving dependents' `<depends-on question="…" option="…"/>` elements assumed of it, **leave
those dependents exactly as they are**: do not strip or re-dispatch them, do not rewrite their
`option` values, and print no mismatch advisory. A `<depends-on>` records what a dependent
assumed, not a pointer that must track its target's live recommendation; reconciling it against
the option actually recorded is the answer-time cascade's job, never this sweep's. A dependent
the user also wants regenerated is named in the same `strip` call.

### 3. Dispatch the read-only subagent per surviving question, most-significant-first

First **rank the surviving questions most-significant-first** — foundational questions, whose
eventual answer other questions turn on, ahead of the questions that would build on them. Rank
them by judgment over **exactly what step 1's `locate` printed**: each block's `id` and
`<question>` text. Read nothing else to rank them — the subagent, not the orchestrator, is what
grounds in the milestone. The ranking is a best-effort heuristic: a coupling it orders wrongly
is absorbed by the subagent's own rule that a dependency on a sibling not yet annotated is
expressed as prose, never as an element.

Then dispatch one read-only subagent per surviving question, **strictly sequentially in that
order — never in parallel**: dispatch a question, wait for its return, judge it (sub-steps a–c
below, including its one repair attempt), and embed and commit it (sub-step d) — or skip it —
**before dispatching the next question**. Each dispatch therefore reads an `open_questions.xml`
that already carries every earlier question's embedded children, which is what lets a later
recommendation build on those siblings' recommendations and declare each such use as a
`<depends-on question="…" option="…"/>` element.

Use the `Agent` tool with `subagent_type` set to the namespaced registry name of the
`recommend-open-question` agent (singular — the per-question subagent) under this plugin's
namespace, `cairn:recommend-open-question` — one dispatch per surviving question. Pass it that
question's **Short Title**, the `<MILESTONE_DIR>` resolved in step 0, and the question's block
exactly as `locate` printed it in step 1:

```
Recommend on this single open question.

Short Title: <Short Title>

Milestone directory: <MILESTONE_DIR>

Question block:
<the block as locate printed it>
```

The block is the only question text the prompt carries: the subagent reads the milestone's
documents itself, read-only, for whatever surrounding grounding it needs, so the orchestrator
never reads them to assemble context.

The subagent is **read-only** — it mutates nothing. It returns the ready-to-embed XML
sub-elements as its final message — one `<alternative id="...">` element per option (each with
child `<advantage>` and `<drawback>`), zero or more sibling `<applied-principle>` elements, zero
or more self-closing `<depends-on question="..." option="..."/>` elements (one per
already-embedded sibling the recommendation builds on, naming that sibling's `id` and the
`<alternative>` id it assumes), and one `<recommendation option="...">` element — and **only**
those child elements, never the `<open-question>` wrapper or the `<question>` element. The
orchestrator does **all** the writing, through the tool.

**Judge every return in this fixed order — last-line verdict, then `embed`, then a single
repair attempt when `embed` refuses — and commit what embedded.** The stages are **one
per-return pipeline**: as the return arrives, judge it, repair it once if judging failed,
re-judge what comes back, commit the annotation if it embedded (sub-step d), then move on —
all of it before the next question is dispatched.

**a. Last-line verdict.** Read the return's **last non-whitespace line**. If that line begins
with `FAILED:`, the return is an **explicit failure**: skip that question alone — embed nothing,
leave its block untouched, note its Short Title with the reason (the text after `FAILED:`) for
the step-5 advisory — and make no further attempt on it, **never a repair**, even when
`<alternative>`…`</recommendation>` elements sit above that line. Only when the last
non-whitespace line is **not** a `FAILED:` line does judging continue, and a `FAILED:` token
appearing anywhere else in the message is then ordinary text with no special meaning. This
verdict is the only judging the orchestrator does itself; everything else is the tool's.

**b. Pipe the whole message to `embed`.** Run

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py embed <MILESTONE_DIR> "<Short Title>" <<'EOF'
<the agent's whole final message, verbatim>
EOF
```

The message travels on standard input through a **quoted-delimiter heredoc** (`<<'EOF'`, so
nothing inside is expanded; pick a delimiter line the message does not contain), **whole and
unedited** — never trim it, never extract the elements yourself, never reorder, rewrite, or drop
a returned element. The tool slices the fragment from the first `<alternative` line through the
last `</recommendation>` line (a grounding summary above or a closing remark below is discarded,
not a failure), parses and validates it — no `<open-question>` or `<question>` line, no text
outside the elements, at least one `<alternative>`, exactly one `<recommendation>` naming one of
them, every `<depends-on>` resolving to an annotated block and one of its `<alternative>` ids,
no unknown element; child order is not checked — and writes the block re-rendered in canonical
form, so indentation, escaping, and child grouping are the tool's, never the return's or yours.

- **Silent, exit 0** — the question is annotated. It gets no console mention, however its
  return arrived. Commit it now (sub-step **d**), then move on to the next question.
- **One `Error: <reason>` line on stderr, exit 1** — the return could not be embedded and the
  document is unchanged. Hold that line verbatim: it fills the repair template in **c**.

**c. Repair once, immediately.** A return that passed the last-line verdict but was refused by
`embed` gets **exactly one** repair attempt before any skip. Run that repair **immediately, for
this question** — the moment `embed` refuses, and before the next question is dispatched —
never by holding refused returns back and running the repairs as a second phase once the last
first return has landed. The next dispatch waits until this question's repaired return has been
judged and the question embedded or skipped.

Spend at most **one** repair per question: a repaired return that is refused again is not
repaired a second time; it goes straight to the skip below.

Repair by whichever of these two branches the host supports, in this order:

- **Continue the same agent session.** Where the host can continue a finished agent session and
  you still hold that dispatch's handle — a follow-up message addressed to the agent id the
  `Agent` tool returned — send the corrective message below to **that same agent**. Its context
  is intact, so it re-emits from the analysis it already did.
- **Re-dispatch one fresh agent.** Where the host cannot continue a finished agent session, or
  the handle is gone, dispatch **one** fresh `cairn:recommend-open-question` agent for that
  question with the `Agent` tool, passing the **same prompt** as the original dispatch with the
  corrective message below appended to it as a shape reminder. This second dispatch redoes the
  analysis, so it is the fallback branch, never the preferred one.

Both branches send this fixed one-paragraph corrective message, whose single slot is
`<Error line>`:

```
A previous return for this question could not be embedded — <Error line>. Emit the sub-elements —
the `<alternative>` elements, then any `<applied-principle>` elements, then any `<depends-on>`
elements, then the single `<recommendation>` element — as your whole final message, and check
that message against both shape tests before sending it: its first non-whitespace text starts
with `<alternative`, and its last non-whitespace text ends with `</recommendation>`. Send those
sub-elements and nothing else — no grounding summary above them, no closing remark below them.
```

Fill `<Error line>` with the `Error: <reason>` line the refused `embed` call printed in **b**,
verbatim — the same line the skip advisory would carry — so the one attempt is aimed rather than
blind. Never quote the offending prose back to the agent; the tool's line names what failed, and
the template asks for the sub-elements and nothing else.

Judge whatever comes back — the same agent's re-emitted message, or the fresh dispatch's return
— by sub-steps a and b exactly as a first return is judged: the same last-line verdict, the same
whole-message pipe to `embed`. A silent `embed` annotates it like any other, and sub-step **d**
then commits it like any other.

Only a **second** failure — the repaired return's last line begins `FAILED:`, or `embed` refuses
it again — is a **skip of that question alone, never a run stop**: embed nothing for it, commit
nothing for it, leave its block untouched, note its Short Title with that second reason (the
`FAILED:` text or the second `Error:` line) for the step-5 advisory, and carry on with the other
questions.

**d. Commit the annotation, before the next dispatch.** Every silent `embed` — a first return's
or a repaired return's — is followed at once by this question's own commit: you are the
orchestrator, and you commit **per question, inside the dispatch loop**. First run

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py lift <MILESTONE_DIR> "<Short Title>"
```

It prints one line, "`<option>` — `<rationale>`", read from the `<recommendation>` element the
`embed` call just wrote. **Hold that line as this question's commit body.** Then read and follow
the shared commit procedure at `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`, carrying out its
steps yourself. Supply it these three inputs:

- **PATHS** — this question's own change: `<MILESTONE_DIR>/open_questions.xml` (the document the
  `embed` call wrote).
- **SUBJECT** — `Recommendation-annotation: <Short Title>` (the annotated question's handle).
- **BODY** — the "`<option>` — `<rationale>`" line the `lift` call printed, verbatim.

That procedure owns the path-scoped staging (never `git add -A`), the dirty-own-path no-op guard,
and the commit. Commit once per annotated question — the per-question granularity is the point —
and only then dispatch the next question. A **skipped** question commits nothing: a refused
`embed` never writes, so there is nothing to lift and nothing for the guard to stage, and no
commit is made for it. This sweep requires **no** clean working tree: each commit is path-scoped
to the one document, so a dirty tree elsewhere stays out of it.

When the last surviving question has been embedded and committed or skipped, step 3 is over:
go to step 4. A loop whose every question was skipped falls through to the sort exactly as a
loop that embedded every question does — it never exits to step 5's no-op line directly.

### 4. Sort the document once, after the last dispatch

This is a **fixed end-of-run step, reached on every run that found questions**: a run whose
step 1b printed nothing and dispatched no one, a run whose every dispatch ended in a skip, and
a run that embedded every question all arrive here, and none of them exits to step 5's no-op
line without running it. Only a document with no questions at all (step 1a) stops short of it.
Run it **once**, after the last question's own commit has landed (or at once when there was
nothing to dispatch), never inside the dispatch loop:

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py sort <MILESTONE_DIR>
```

It rewrites the document with the `<recommendation>`-bearing blocks first, in exactly the
order the answer sweep's `walk` will dispatch them, and every block still carrying none last in
its prior order — so a reader of the document meets the questions whose answers no dependency
can nullify before the questions that build on them — and it leaves a document already in
that order as it is. A mutator, it prints nothing on success; a failure is one
`Error: <reason>` line on stderr with the document unchanged — print that line and carry on to
step 5 as a run whose sort committed nothing.

Then commit the reorder as this run's own commit. Read and follow the shared commit procedure
at `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`, carrying out its steps yourself. Supply it
these two inputs, and **no BODY**:

- **PATHS** — `<MILESTONE_DIR>/open_questions.xml` (the one document the `sort` call rewrote).
- **SUBJECT** — `Question-ordering: <milestone_id>`.

That procedure owns the path-scoped staging (never `git add -A`), the dirty-own-path no-op
guard, and the commit. Its guard is the sort's **only** no-op test: a document the sort left as
it stood — already in sorted order, the identity — leaves the path unchanged, so the guard
fires and nothing is committed, while a document in which the sort moved a block leaves the
path dirty, so the reorder is committed. Never test the outcome yourself — no `list` before and
after, no diff read — and never fold the reorder into a per-question commit: every
`Recommendation-annotation:` commit of step 3 has already landed by the time the sort runs, so
no annotation rides in the `Question-ordering:` commit and no reorder rides in an annotation
commit — each subject stays true to what its commit holds. Hold whether this commit landed or
the guard fired: step 5 reads it.

### 5. Report

Print exactly one fixed terse status line for the whole run, chosen by **what this run
committed**: test these three in strict order and print the first that holds.

1. **An `embed` wrote** — step 3 reached its sub-step **d** for at least one question, so at
   least one `Recommendation-annotation: <Short Title>` commit landed — print
   `Recommendations embedded.`, whether or not step 4's sort also committed.
2. **Else the sort committed** — no `embed` wrote, but step 4's `Question-ordering:
   <milestone_id>` commit landed because the sort moved a block — print `Questions reordered.`
3. **Else nothing was committed** — no `embed` wrote and step 4's dirty-own-path guard fired —
   print no success line; print instead a distinct one-line message stating that nothing
   changed and why: every block already carried a `<recommendation>` element, or every
   dispatched question was still skipped after its repair attempt in step 3, and the document
   was already in sorted order.

Each line is the whole of its output and names no identifier: no annotated-vs-skipped
breakdown, no moved-block count, no per-question listing, and no consumer pointer to the
`/answer-open-question-with-recommendation` / `/answer-all-open-questions-with-recommendation`
skills. Those three lines are the whole vocabulary, and the strict order is what keeps each
true to the git log: the success line means there are new recommendations to answer, the
reorder line that the document was reordered and nothing else was committed, and the no-op
line that this run left git history untouched.

Alongside whichever line is chosen, print only the questions step 3 **still skipped after the
repair path** — a return whose last non-whitespace line began `FAILED:` (sub-step a), or one
`embed` refused **again** after its one repair attempt (sub-step c). List each as an advisory:
its Short Title with the reason it was skipped on (the second reason where a repair was spent),
one per line.
This survives the terse-reporting rule because nothing else records it: the per-question commits
and the annotated `open_questions.xml` show only the questions that *were* annotated, and the
`Question-ordering:` commit shows only where blocks moved, so a question left un-annotated is
git-absent and the console must carry it. Re-running the sweep retries exactly those blocks,
since they still lack a `<recommendation>` element.

A question that **was** annotated gets **no console mention at all**, however its return reached
the document: whether it arrived clean, whether the tool discarded surrounding text from it, or
whether it was embedded only after the single repair attempt. The embedded block in the diff is
the whole record, so a recovered return is reported exactly like a clean one — no
recovered-or-repaired listing, no count, no note.

If there were no questions at all, say so and stop (step 1a) — nothing to report.
