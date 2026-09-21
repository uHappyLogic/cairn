# Answer-recording procedure (shared core)

This is the single source of truth for recording an answer to one open question of the
current milestone: the decision lands under `## Decisions` of `<MILESTONE_DIR>/requirements.md`
and the answered block leaves `<MILESTONE_DIR>/open_questions.xml`. It is followed inline by
the `answer-open-question` skill and once per resolved question by an orchestrator sweeping
several. The caller supplies the inputs below and wraps the result; this file describes only
the recording work itself — locate, analyse, fold, remove, cascade.

Every read and write of `open_questions.xml` here is a call to the plugin's open-question
tool, `python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py <subcommand> <MILESTONE_DIR> …`, that
file's sole writer: a read prints the bare value asked for, a write prints nothing on
success, and any failure is one `Error: <reason>` line on stderr with a non-zero exit and the
document left byte-for-byte unchanged. Never edit `open_questions.xml` yourself.

## Inputs

This procedure records one decision given three inputs the caller supplies, the third
optional:

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

## Procedure

### 1. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 2. Locate the question

Run

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py locate <MILESTONE_DIR> "<SHORT TITLE>"
```

On success it prints the matched block verbatim — its `<question>` and, when the recommend
sweep annotated it, its `<alternative id="…">`, `<applied-principle>`, `<depends-on>`, and
`<recommendation>` children. Hold that print: step 3 reasons over it and step 5 judges
against its alternative ids.

If it fails — no block's `id` matches SHORT TITLE — **stop without changing anything** and
report the mismatch, quoting the tool's `Error:` line, which lists every id the document
holds so the caller can retry.

### 3. Analyse the answer

Before editing, reason about the answer's implications:

- Does it resolve the question completely, or leave a sub-question open?
- Does it introduce a concrete constraint that belongs under `## Decisions`?
- Does it make any other entry moot, or force a specific answer to one?
- Does it contradict or supersede anything already written in the document?

This analysis is how you reach the right edits in steps 4–6; it is not itself written into
the document. Do not invent implications the answer text does not directly support, and if
the answer is ambiguous or incomplete, remove what is clearly resolved and surface the rest
rather than guessing — never add a brand-new question block to the document.

### 4. Fold the decision into `## Decisions`

Add a concise statement under `## Decisions` of `<MILESTONE_DIR>/requirements.md` — in the
relevant existing subsection, or a new subsection if none fits — capturing what was decided
and any constraint it imposes. Write it as **clean prose with no citation marker**: the
document records the decision itself, not where it came from. Match the live document's
section names.

Write this edit **before** removing the answered block in step 5; the recorded decision
always lands first.

### 5. Remove the answered block

Run

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py remove <MILESTONE_DIR> "<SHORT TITLE>" [--option "<OPTION>"]
```

whether or not the block carries embedded children. In that one write the tool deletes the
block and reconciles every block that depended on it — a dependent that assumed the
`--option` given keeps its analysis, every other dependent is stripped to its `<question>` —
leaving no `<depends-on>` tag naming the removed block. What this step owns is deciding
`--option`:

- **RECORDED OPTION supplied** — pass it as `--option`, verbatim.
- **RECORDED OPTION absent** (a literal answer) — form **one** verdict: does ANSWER plainly
  settle on one of the answered block's own `<alternative id>` values, as step 2's print
  shows them? Judge it in prose against that closed set — never by parsing ANSWER, and never
  dependent by dependent. When it plainly does, pass that alternative's id as `--option`;
  when it settles on none of them, or only arguably on one, or the block carries no
  alternatives, pass nothing. Strip on doubt: a dependent whose assumed option the answer
  only arguably preserves is exactly what a bare `remove` strips, and the next recommend
  sweep regenerates it.

The tool refuses an `--option` naming none of the block's alternatives and leaves the
document unchanged; its `Error:` line lists the ids, so correct the value against them (or
pass nothing) and run the call again.

### 6. Cascade to mooted entries

If the decision moots another entry or forces its answer, fold any implied constraint into
`## Decisions` the same way and then remove that entry with a bare `remove` — no `--option`,
since nothing was recorded for it:

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py remove <MILESTONE_DIR> "<MOOTED SHORT TITLE>"
```

one call per mooted entry. Each call reconciles that entry's dependents itself, so nothing
is left for this procedure to tidy, and this procedure reports nothing about what the calls
of steps 5 and 6 reconciled — the two edited files are the record.

Then both files are left in the now-updated state for any further work.

Make the `## Decisions` folds of steps 4 and 6 separate, targeted edits — one per decision —
rather than one large rewrite of a long file, and do not otherwise rewrite or restructure
`requirements.md`; every change to `open_questions.xml` is a tool call above.
