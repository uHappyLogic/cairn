---
name: recommend-all-open-questions
description: Annotate every open question in the current milestone carrying alternatives with a single recommended option, reasoning over the whole set inline.
---

# recommend-all-open-questions

This is the second of the two annotating passes over a milestone's open questions, and the
non-interactive batch form of `/discuss-open-question`'s pick: the alternatives pass,
`/provide-alternatives-to-all-open-questions`, has already given every `<open-question>` block
its frozen set of `<alternative>` elements, and this pass picks one of them per block. It runs
**inline and dispatches no agents**: you read the question document whole, hold every question
still lacking a `<recommendation>` in view at once, follow the shared pick procedure over that
whole set, and embed each block's `<recommendation>`, its `<depends-on>` declarations, and its
`<applied-principle>` citations yourself, through the plugin's open-question tool. You are the
only party in this pass that changes `<MILESTONE_DIR>/open_questions.xml`, and every write
you make of it is a tool call — `embed` to write, `lift` to read back the lines the commit
records, `sort` to reorder once at the end — never a direct edit; reading the document whole
with the file-reading tool is for reasoning only, and every list, locate, or lift of a block
is the tool's. It commits once per run — one `Recommendation-annotation: <milestone_id>`
commit whose body is one lifted line per annotated question — then sorts the document once,
the annotated blocks first in the order the answer sweep will walk them, and commits that
reorder as its own `Question-ordering: <milestone_id>` commit, a fixed end-of-run step of every
run that found questions. It is **argument-free**, records **no decisions**, triggers **no
cascades**, and never adds, drops, or edits a block's `<alternative>` — it only picks and orders.
Each embedded recommendation is consumed later, when it is recorded as an answer, by
`/answer-open-question-with-recommendation` or the
`/answer-all-open-questions-with-recommendation` sweep.

## Usage

```
/recommend-all-open-questions
```

Takes no arguments — it sweeps every `<open-question>` block in the current milestone's
`open_questions.xml`. `<milestone_id>` below is the last path component of `<MILESTONE_DIR>`
(the directory name under `milestones/`).

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

**b. The ones without alternatives — the stop test.** Run

```
python3 .agents/plugins/cairn/tools/open_questions.py list --without-alternatives <MILESTONE_DIR>
```

It prints, in document order, the ids of the blocks carrying no `<alternative>` element. If it
prints **anything**, this pass cannot run: it picks only against a frozen alternative set, and
a block without one has nothing to pick from. **Stop without changing anything**, print the
ids it listed, and point the user at `/provide-alternatives-to-all-open-questions`, which
supplies those blocks' alternatives — a re-run of this skill afterwards picks for them. Only
when this call prints nothing does the pass continue.

**c. The ones without a recommendation.** Run

```
python3 .agents/plugins/cairn/tools/open_questions.py list --without-recommendation <MILESTONE_DIR>
```

It prints, in document order, the ids of the blocks carrying no `<recommendation>` element —
the ones this run annotates. Every other block already carries a recommendation and is
**skipped** (step 2). If this call prints nothing, every block is already annotated: there is
nothing to pick, so skip steps 3, 4, and 5 and go straight to step 6 — the end-of-run sort
runs on every run that found questions, this one included, and step 7 then picks the report
line from what the run committed. Never exit to the no-op line from here.

Gather this set **once**: there is **no** per-question live re-check against the document and
**no** outer re-gather loop. This run only adds children to blocks — it records no decisions
and triggers no cascades — so the question set never shrinks under it and the ids **c**
printed stay valid for the whole run.

### 2. Blocks already carrying a recommendation are skipped (re-run idempotency)

Step 1's `--without-recommendation` filter is the whole skip test: a block that already
carries a `<recommendation>` element is never re-picked, so re-runs are cheap and a standing
recommendation is left as it stands — the tool's `embed --recommendation` refuses a block
already carrying one, so the rule holds in the tool and not only here. The primary re-run
motive is exactly the recommendation-less set a later `/review-milestone-requirements` pass
surfaces, or that an answer's cascade cleared: a dependent whose pick an answer invalidated
loses its `<recommendation>`, `<depends-on>`, and `<applied-principle>` children and keeps its
`<alternative>` children, so it is this pass's to re-pick on the next run, against the same
frozen set. A standing recommendation on a block this run is not writing is **context**: step
3 reads it as a sibling pick this run's own picks may build on and declare a `<depends-on>`
against, and never revises it.

**Escape hatch for a stale recommendation:** to force a fresh pick on a block, run

```
python3 .agents/plugins/cairn/tools/open_questions.py strip --recommendation <MILESTONE_DIR> "<Short Title>" …
```

(one or more Short Titles), then re-run this skill. `strip --recommendation` deletes only the
`<recommendation>`, `<depends-on>`, and `<applied-principle>` children of each named block,
leaving its `<alternative>` children, its wrapper, and its `<question>` intact and every other
block untouched; the block now carries no `<recommendation>`, so the next run's
`--without-recommendation` list yields it and this pass re-picks it against the same frozen
set. That call and a re-run are the whole hatch — `open_questions.xml` is never edited by
hand, since the tool is its sole writer. Revising the alternative set itself is the
alternatives pass's hatch (the bare `strip`, then that pass), not this one's.

When such a re-picked block's new `<recommendation option>` differs from the option that
surviving dependents' `<depends-on question="…" option="…"/>` elements assumed of it, **leave
those dependents exactly as they are**: do not strip them, do not rewrite their `option`
values, and print no mismatch advisory. A `<depends-on>` records what a dependent assumed, not
a pointer that must track its target's live recommendation; reconciling it against the option
actually recorded is the answer-time cascade's job, never this pass's. A dependent the user also
wants re-picked is named in the same `strip --recommendation` call.

### 3. Pick over the whole set at once

Read `<MILESTONE_DIR>/requirements.md` and `<MILESTONE_DIR>/open_questions.xml` **whole**
with the file-reading tool. The document read gives you, for every id step 1c printed, the
block's `<question>` text and its frozen `<alternative>` set — each option's `id`, what-it-is
text, `<advantage>`, and `<drawback>` — and, for every other block, the `<recommendation>`
already standing on it. That whole read is for reasoning only; it changes nothing and finds
nothing you later write against, since every write names a block by its Short Title.

Then read and follow the shared pick procedure at
`.agents/plugins/cairn/shared/recommend-procedure.md`, carrying out its steps yourself over
**every question step 1c printed, held in view together as one judgment**. For each such
question its QUESTION is the block's Short Title and `<question>` text and its ALTERNATIVES
are the block's own `<alternative>` elements, taken as given — the pick names one of them by
its `id` and never adds to or drops from the set. Ground once for the whole set (the
procedure's grounding step names the live project, the principle store, and the sibling
questions with their alternatives and any standing recommendations), then form one
recommendation per question, keeping every question's set in view while you reason so the
picks cohere with one another and with the recommendations already standing. Decide every
pick before rendering any of them; what follows in step 4 is rendering and writing only.

Two of the procedure's outcomes carry over into this pass as its own rules:

- **A pick that leans on a sibling** settling on one of its alternatives — a sibling with a
  standing recommendation, or one whose pick you are forming in this same pass — is
  disclosed as a `<depends-on question="…" option="…"/>` element of the block (step 4),
  naming the sibling's `id` and one of that sibling's own `<alternative>` ids. Every block
  carries its alternatives by step 1b, so every such sibling is a legitimate target; there is
  no option-less tag form and no guessed option.
- **A stale set** — a decision recorded since the alternatives were enumerated, under
  `## Decisions` of `requirements.md` or as a sibling's answer, has closed one of a block's
  options — still gets a pick: recommend the best option still viable and state in the
  rationale which option that decision closed and why. Only a block **no** option of which
  survives is **skipped**: embed nothing for it, leave its block untouched, and note its Short
  Title with the decision that closed the set for the step-7 advisory, where the remedy is
  named — the bare `strip` on that block followed by a run of
  `/provide-alternatives-to-all-open-questions`, since only a fresh alternative set can give
  it something to pick from. That is the one judged skip this pass has.

### 4. Render each pick as XML and embed it, one `embed` call per block

For every question you picked for in step 3, render the pick as the sub-elements that go
*inside* its `<open-question>` block, each a direct child of it — never the
`<open-question …>` / `</open-question>` wrapper, the `<question>` element, or an
`<alternative>` element, which the document already holds — in exactly this shape:

```
<applied-principle>Short Title</applied-principle>
<depends-on question="Sibling Short Title" option="Option X"/>
<recommendation option="Option A">one-line rationale</recommendation>
```

- One `<applied-principle>` element per confirmed principle that bore on the pick, carrying
  that principle's Short Title as its text — a sibling of `<recommendation>`, never a child
  of it, one element per bearing principle with no list syntax, and **none at all** when no
  principle bore.
- One self-closing `<depends-on question="…" option="…"/>` element per sibling the pick
  leans on (step 3): `question` is that sibling block's `id`, `option` one of that sibling's
  `<alternative id>` values. None when the pick builds on no sibling.
- Exactly one `<recommendation option="…">…</recommendation>` element: its `option` names the
  winning alternative by that alternative's `id`, and its text is the one-line rationale
  alone — the answer path lifts this element by recombining the two as
  "`<option>` — `<rationale>`", so the rationale carries neither a principle citation nor a
  sibling dependency, which live only in their own sibling elements.

The elements must be well-formed XML, since the tool parses them before it writes them — a
literal `&` or `<` in element text or an attribute value is written `&amp;` or `&lt;`. Beyond
that, indentation, escaping, and child order are the tool's: the block is re-rendered in its
canonical form when it is written.

Then write each block with one tool call, the rendered elements travelling on standard
input through a **quoted-delimiter heredoc** (`<<'EOF'`, so nothing inside is expanded; pick a
delimiter line the elements do not contain):

```
python3 .agents/plugins/cairn/tools/open_questions.py embed --recommendation <MILESTONE_DIR> "<Short Title>" <<'EOF'
<the block's rendered elements>
EOF
```

The tool parses and validates the fragment — no wrapper or `<question>` line, no text outside
the elements, no `<alternative>` element, exactly one `<recommendation>` whose `option` names
one of the block's own `<alternative>` ids, every `<depends-on>` resolving to another block
of the document that carries `<alternative>` elements and to one of that block's ids, a target
block carrying alternatives and no `<recommendation>` yet — and writes those elements into the
existing block re-rendered in canonical form, adding, dropping, and editing no `<alternative>`.

- **Silent, exit 0** — the block is annotated. It gets no console mention. Move on to the next
  block.
- **One `Error: <reason>` line on stderr, exit 1** — the fragment was refused and the document
  is unchanged. The fragment is yours, so a refusal is a rendering slip to correct, never a
  skip: fix the elements against what that line names and run the same call again.

Write the blocks **in any order** — the order step 1c printed is as good as any. The tool
resolves a `<depends-on>` against its target's alternatives, which every block already
carries, so a block may be written before or after the sibling it depends on, and nothing here
orders the calls. When every picked block has been written, step 4 is over: go to step 5.

### 5. Commit the run once, before the sort

After the last `embed` call, and before step 6's sort, run one `lift` per block you
annotated in step 4:

```
python3 .agents/plugins/cairn/tools/open_questions.py lift <MILESTONE_DIR> "<Short Title>"
```

Each call prints one line, "`<option>` — `<rationale>`", read from the `<recommendation>`
element the `embed` call wrote. Gather those lines, one per annotated block in the order you
wrote them: together they are this run's commit body. Then read and follow the shared commit
procedure at `.agents/plugins/cairn/shared/commit-procedure.md`, carrying out its steps yourself.
Supply it these three inputs:

- **PATHS** — this run's own change: `<MILESTONE_DIR>/open_questions.xml` (the one document
  the `embed` calls wrote).
- **SUBJECT** — `Recommendation-annotation: <milestone_id>`.
- **BODY** — the gathered `lift` lines, one per line, verbatim.

That procedure owns the path-scoped staging (never `git add -A`), the dirty-own-path no-op
guard, and the commit. Commit **once per run** — the whole-set granularity is the point: the
run's picks were one judgment, and its one commit records them together with their reasoning
in the body. A run whose every step-1c block was skipped in step 3 wrote nothing, so there is
nothing to lift and the guard stages nothing: it commits nothing here and falls through to
the sort exactly as a run that annotated every block does. This pass requires **no** clean
working tree: the commit is path-scoped to the one document, so a dirty tree elsewhere stays
out of it. Hold whether this commit landed: step 7 reads it.

### 6. Sort the document once, after the run's commit

This is a **fixed end-of-run step, reached on every run that found questions**: a run whose
step 1c printed nothing and picked for no one, a run whose every block was skipped, and a run
that annotated every block all arrive here, and none of them exits to step 7's no-op line
without running it. Only a document with no questions at all (step 1a) and the step-1b stop
come before it. Run it **once**, after step 5's commit has landed (or at once when there was
nothing to pick), never between the `embed` calls:

```
python3 .agents/plugins/cairn/tools/open_questions.py sort <MILESTONE_DIR>
```

It rewrites the document with the `<recommendation>`-bearing blocks first, in exactly the
order the answer sweep's `walk` will dispatch them, and every block still carrying none last in
its prior order — so a reader of the document meets the questions whose answers no dependency
can nullify before the questions that build on them — and it leaves a document already in
that order as it is. A mutator, it prints nothing on success; a failure is one
`Error: <reason>` line on stderr with the document unchanged — print that line and carry on to
step 7 as a run whose sort committed nothing.

Then commit the reorder as its own commit. Read and follow the shared commit procedure at
`.agents/plugins/cairn/shared/commit-procedure.md`, carrying out its steps yourself. Supply it
these two inputs, and **no BODY**:

- **PATHS** — `<MILESTONE_DIR>/open_questions.xml` (the one document the `sort` call rewrote).
- **SUBJECT** — `Question-ordering: <milestone_id>`.

That procedure owns the path-scoped staging (never `git add -A`), the dirty-own-path no-op
guard, and the commit. Its guard is the sort's **only** no-op test: a document the sort left as
it stood — already in sorted order, the identity — leaves the path unchanged, so the guard
fires and nothing is committed, while a document in which the sort moved a block leaves the
path dirty, so the reorder is committed. Never test the outcome yourself — no `list` before and
after, no diff read — and never fold the reorder into the run's annotation commit: step 5's
`Recommendation-annotation:` commit has already landed by the time the sort runs, so no
annotation rides in the `Question-ordering:` commit and no reorder rides in the annotation
commit — each subject stays true to what its commit holds. Hold whether this commit landed or
the guard fired: step 7 reads it.

### 7. Report

Print exactly one fixed terse status line for the whole run, chosen by **what this run
committed**: test these three in strict order and print the first that holds.

1. **An `embed` wrote** — step 5's `Recommendation-annotation: <milestone_id>` commit landed
   because at least one block was annotated — print `Recommendations embedded.`, whether or
   not step 6's sort also committed.
2. **Else the sort committed** — no `embed` wrote, but step 6's `Question-ordering:
   <milestone_id>` commit landed because the sort moved a block — print `Questions reordered.`
3. **Else nothing was committed** — no `embed` wrote and step 6's dirty-own-path guard fired —
   print no success line; print instead a distinct one-line message stating that nothing
   changed and why: every block already carried a `<recommendation>` element, or every block
   step 1c printed was skipped in step 3 because no option of its set survived, and the
   document was already in sorted order.

Each line is the whole of its output and names no identifier: no annotated-vs-skipped
breakdown, no moved-block count, no per-question listing, and no consumer pointer to the
`/answer-open-question-with-recommendation` / `/answer-all-open-questions-with-recommendation`
skills. Those three lines are the whole vocabulary, and the strict order is what keeps each
true to the git log: the success line means there are new recommendations to answer, the
reorder line that the document was reordered and nothing else was committed, and the no-op
line that this run left git history untouched.

Alongside whichever line is chosen, print only the blocks step 3 **skipped** — the ones no
option of which survived a recorded decision. List each as an advisory: its Short Title, the
decision that closed its set, and the remedy — run the tool's bare `strip` on that block, then
`/provide-alternatives-to-all-open-questions` to enumerate a fresh set, then this skill again
— one per line. This survives the terse-reporting rule because nothing else records it: the
run's commit and the annotated `open_questions.xml` show only the blocks that *were*
annotated, and the `Question-ordering:` commit shows only where blocks moved, so a block left
un-annotated is git-absent and the console must carry it, and a bare re-run of this skill
alone would only skip it again.

A block that **was** annotated gets **no console mention at all**, however its fragment
reached the document — first call or after a corrected one. The embedded block in the diff
is the whole record.

If there were no questions at all, say so and stop (step 1a) — nothing to report. If step 1b
stopped the run, its stop message is the whole output — nothing was committed, and nothing
is reported here.
