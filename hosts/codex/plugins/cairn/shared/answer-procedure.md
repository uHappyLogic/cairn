# Answer-recording procedure (shared core)

This is the single source of truth for recording an answer to one open question of a
milestone: the decision lands under `## Decisions` of `<MILESTONE_DIR>/requirements.md` and
the answered block leaves `<MILESTONE_DIR>/open_questions.xml`. It is followed inline by the
single-question answer skills. The inline answer sweep draws only on its analyse step's
first two questions and its fold step's rules for what a decision says and the shape it
takes — never on the rewrites and notes that answer the analyse step's fourth question, nor
on its tool steps, which the sweep's own batched call replaces. The caller supplies the
inputs below and wraps the result; this file describes only the recording work itself —
locate, analyse, fold, note, remove, cascade.

Every read and write of `open_questions.xml` here is a call to the plugin's open-question
tool, `python3 ${PLUGIN_ROOT}/tools/open_questions.py <subcommand> <MILESTONE_DIR> …`,
written out in full on every call, never through a variable, alias, or function of your own
defined to stand for the command or any part of it; the tool is that file's sole writer: a
read prints the bare value asked for, a write prints nothing on
success, and any failure is one `Error: <reason>` line on stderr with a non-zero exit and the
document left byte-for-byte unchanged. Never edit `open_questions.xml` yourself.

## Inputs

This procedure records one decision given five inputs the caller supplies, the last two
optional:

- **MILESTONE_DIR** — the already-resolved directory of the milestone the question belongs
  to, the `<MILESTONE_DIR>` every path and tool call below uses. The caller resolves it; this
  procedure never looks the milestone up.
- **SHORT TITLE** — the resolved handle of an existing `<open-question>` block to answer
  (its `id`, compared case-insensitively). The caller has already obtained it; locating the
  matching block is this procedure's job.
- **ANSWER** — the answer text for that question.
- **RECORDED OPTION** *(optional)* — the option or alternative id the caller lifted as the
  decision, when it lifted one: the block's `<recommendation option="…">` value or the chosen
  `<alternative id="…">` value, as plain text. Supplied, it is what step 5 passes to the
  tool's `remove` as `--option`, so the blocks that depended on the answered one are
  reconciled against it as an exact id; absent, step 5 forms the one judgment described
  there. The caller either passes it or passes nothing — this procedure never derives it by
  parsing ANSWER, whose form is the caller's own convention.
- **UNDERMINED PICKS** *(optional)* — the Short Titles of other open questions whose
  standing pick the caller judged the answer undermines. Supplied, step 5 passes them to
  the tool's `remove` as `--undermined`, exactly as given; absent, step 5 passes no
  `--undermined`. Which picks an answer undermines is the caller's judgment alone — this
  procedure never names one itself and never adds to, trims, or re-judges the list.

## Procedure

### 1. Locate the question

Run

```
python3 ${PLUGIN_ROOT}/tools/open_questions.py locate <MILESTONE_DIR> "<SHORT TITLE>"
```

On success it prints the matched block verbatim — its `<question>` and, when the recommend
sweep annotated it, its `<alternative id="…">`, `<applied-principle>`, `<depends-on>`, and
`<recommendation>` children. Hold that print: step 2 reasons over it and step 5 judges
against its alternative ids.

If it fails — no block's `id` matches SHORT TITLE — **stop without changing anything** and
report the mismatch, quoting the tool's `Error:` line, which lists every id the document
holds so the caller can retry.

### 2. Analyse the answer

Before editing, reason about the answer's implications:

- Does it resolve the question completely, or leave a sub-question open?
- Does it introduce a concrete constraint that belongs under `## Decisions`?
- Does it make any other entry moot, or force a specific answer to one?
- Does it contradict or supersede anything already written in the document?

Judge each contradiction the fourth question finds with a standing `## Decisions` entry —
one that cannot hold as written beside the decision:

- **Plainly superseded** — the answer is clearly meant to replace that entry: step 3
  rewrites the entry's conflicting text in place, and no note is written for it.
- **Not plainly settled** — the answer does not plainly settle which of the two should
  hold: the entry stays as written and step 4 notes the pair. Doubt notes: an entry the
  answer only arguably replaces is noted, never rewritten.

This analysis is how you reach the right edits in steps 3–6; it is not itself written into
the document. Do not invent implications the answer text does not directly support, and if
the answer is ambiguous or incomplete, remove what is clearly resolved and surface the rest
rather than guessing — never add a brand-new question block to the document.

### 3. Fold the decision into `## Decisions`

Add a concise statement under `## Decisions` of `<MILESTONE_DIR>/requirements.md` — in the
relevant existing subsection, or a new subsection if none fits — capturing what was decided
and any constraint it imposes. Write it as **clean prose with no citation marker**: the
document records the decision itself, not where it came from. Match the live document's
section names, and match each entry's shape to the subsection it lands in: a prose paragraph
where the milestone's `## Decisions` holds one subsection per decision, a
`- **Lead.** text` bullet where it holds topical subsections of bullets.

Two cases edit an existing entry in place, under its own heading and in its own shape:

- **A conflict question.** When the answered question asks which of two `## Decisions`
  entries stands, naming the `###` heading each sits under, edit the losing entry in place:
  rewrite its conflicting text so it agrees with the entry that stands, keeping whatever of
  it still holds, and leave the entry that stands as written. That rewrite is the whole
  record of the answer — add nothing, folding no separate statement anywhere under
  `## Decisions`.
- **A plainly superseded entry.** For each entry step 2 judged plainly superseded, rewrite
  its conflicting text in place, in the same pass of targeted edits as the fold, so it agrees
  with the decision, and keep the rest of the entry as written.

Write these edits **before** removing the answered block in step 5; the recorded decision
always lands first.

### 4. Note the contradictions left standing

For each pair step 2 judged not plainly settled, write one note under
`## Noted contradictions` of `<MILESTONE_DIR>/requirements.md`, the section standing
directly after `## Decisions` and before `## Out of Scope`. When the file holds no such
section, insert its heading together with the first note, after the last line of
`## Decisions` and before the `## Out of Scope` heading; otherwise add the note at the end of
the section. When step 2 noted nothing, this step changes nothing.

Each note is one `- ` bullet naming the two conflicting entries — the entry step 3 wrote or
rewrote and the standing one — each by the `###` heading it sits under, with enough of its
lead or opening words to tell it apart wherever it shares that heading with another entry or
sits among several bullets, then one sentence in your own words stating what each entry says
and why both cannot hold. Write no question text: the next
`/review-milestone-requirements` pass authors the open question from the note.

Write the notes, like the fold, **before** removing the answered block in step 5.

### 5. Remove the answered block

Run

```
python3 ${PLUGIN_ROOT}/tools/open_questions.py remove <MILESTONE_DIR> "<SHORT TITLE>" [--option "<OPTION>"] [--undermined "<UNDERMINED SHORT TITLE>" …]
```

whether or not the block carries embedded children, with `--undermined` followed by every
Short Title of UNDERMINED PICKS as given, each its own quoted argument, when the caller
supplied that input and left off when it did not. In that one write the tool deletes the
block and reconciles every block that depended on it — a dependent that assumed the
`--option` given loses only that tag and keeps its analysis; every other dependent, and every
dependent when no `--option` is given, loses its `<recommendation>`, `<depends-on>`, and
`<applied-principle>` children while keeping its `<alternative>` children, and is the
recommendation pass's (`/recommend-all-open-questions`) to re-pick over that kept set —
leaving no `<depends-on>` tag naming the removed block; a block named under `--undermined`
is reconciled in that same write as a dependent no tag declares. What this step owns is
deciding `--option`:

- **RECORDED OPTION supplied** — pass it as `--option`, verbatim.
- **RECORDED OPTION absent** (a literal answer) — form **one** verdict: does ANSWER plainly
  settle on one of the answered block's own `<alternative id>` values, as step 1's print
  shows them? Judge it in prose against that closed set — never by parsing ANSWER, and never
  dependent by dependent. When it plainly does, pass that alternative's id as `--option`;
  when it settles on none of them, or only arguably on one, or the block carries no
  alternatives, pass nothing. Strip on doubt: a dependent whose assumed option the answer
  only arguably preserves is exactly what a bare `remove` strips of its pick, and the next
  run of the recommendation pass re-picks it against the alternatives it kept.

The tool refuses an `--option` naming none of the block's alternatives and leaves the
document unchanged; its `Error:` line lists the ids, so correct the value against them (or
pass nothing) and run the call again. It likewise refuses an `--undermined` title that
matches no block, or that names the answered block itself, with the document unchanged; its
`Error:` line names that title, so correct the list and run the same call again.

### 6. Cascade to mooted entries

If the decision moots another entry or forces its answer, fold any implied constraint into
`## Decisions` the same way and then remove that entry with a bare `remove` — no `--option`,
since nothing was recorded for it:

```
python3 ${PLUGIN_ROOT}/tools/open_questions.py remove <MILESTONE_DIR> "<MOOTED SHORT TITLE>"
```

one call per mooted entry. Each call reconciles that entry's dependents itself, so nothing
is left for this procedure to tidy, and this procedure reports nothing about what the calls
of steps 5 and 6 reconciled — the two edited files are the record.

Then both files are left in the now-updated state for any further work.

Make the `## Decisions` folds of steps 3 and 6 separate, targeted edits — one per decision —
rather than one large rewrite of a long file, and write each note of step 4 the same way. Do
not otherwise rewrite or restructure `requirements.md`, with one exception: step 3's in-place
rewrite of an existing entry — the losing entry of a conflict question, or an entry the
answer plainly supersedes — each its own targeted edit. Every change to `open_questions.xml`
is a tool call above.
