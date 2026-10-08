---
name: provide-alternatives-to-all-open-questions
description: Annotate every open question in the current milestone lacking alternatives with a set of alternatives, dispatching one subagent per question.
---

# provide-alternatives-to-all-open-questions

This is the first of the two annotating passes over a milestone's open questions: it gives
every `<open-question>` block that carries no `<alternative>` children yet an honest set of
alternatives, and the recommendation pass, `/recommend-all-open-questions`, later picks one of
them per block against that frozen set. Per question it dispatches a subagent, read-only
toward the project, that writes the `<alternative>` elements — the block's XML sub-elements —
to one file in the run's scratch directory outside the repository and ends with the bare token
`DONE`, so a return never travels through the orchestrator's context. The orchestrator is the
only party in this pass that changes the question document, `<MILESTONE_DIR>/open_questions.xml`
— every read and write it makes of that document is a call to the plugin's open-question tool,
`list` to gather and check and `embed` to write, never a direct read or edit, and each call is
written out in full as its fenced block shows it, never through a variable, alias, or function
of your own defined to stand for the command or any part of it. Alternatives are enumerated per
question against the siblings as scope only, so the dispatches are independent: they run
together where the host allows it, and the files they land are embedded and committed in
batches, one fixed shell call per batch — one `Alternatives-annotation: <Short Title>` commit
per annotated question, none for a skipped one. It is **argument-free**, records **no
decisions**, triggers **no cascades**, and writes no `<recommendation>` — it only supplies the
alternatives the recommendation pass reads.

## Usage

```
/provide-alternatives-to-all-open-questions
```

Takes no arguments — it sweeps every `<open-question>` block in the current milestone's
`open_questions.xml`.

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`.
Never use a hardcoded path.

### 1. Gather the questions once, in two tool calls

**a. Every question.** Run

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py list <MILESTONE_DIR>
```

It prints the `id` (Short Title) of every `<open-question>` block, one per line in document
order. If it prints nothing, the document holds no questions: say so and stop. If it fails, its
one `Error: <reason>` line on stderr is the report: print it and stop.

**b. The ones without alternatives.** Run

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py list --without-alternatives <MILESTONE_DIR>
```

It prints, in document order, the ids of the blocks carrying no `<alternative>` element — the
ones this run annotates. Every other block already carries its alternatives and is **skipped**
(step 2). If this call prints nothing, every block already carries alternatives: there is
nothing to dispatch, so skip step 3 and go straight to step 4's no-op line.

Hold the ids **b** printed: each is the Short Title its question's dispatch prompt carries, and
nothing else is gathered for a dispatch — the subagent fetches its own block. They are also the
gathered ids step 3's closing check is read against.

Gather this set **once**: there is **no** per-question live-re-check against the document and
**no** outer re-gather loop. This run only adds children to blocks — it records no decisions
and triggers no cascades — so the question set never shrinks under it and the gathered ids
stay valid for the whole run.

### 2. Blocks already carrying alternatives are skipped (re-run idempotency)

Step 1's `--without-alternatives` filter is the whole skip test: a block that already carries
an `<alternative>` element is never dispatched and never re-annotated, so re-runs are cheap and
an existing alternative set is left as it stands — that set is frozen for the recommendation
pass, which picks against it. The primary re-run motive is exactly the bare set a later
`/review-milestone-requirements` pass surfaces.

**Escape hatch for a stale alternative set:** to force a fresh set on a block, run

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py strip <MILESTONE_DIR> "<Short Title>" …
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

### 3. Dispatch the subagents and embed their files in batches

Dispatch one read-only subagent per question step 1b printed, **all of them together in one
message** — with no cap beyond one dispatch per surviving question — and collect their returns
by what the agent tool offers. **Where it offers a blocking dispatch form**, send every dispatch
in that form, so the message returns only once every agent has landed its file or ended in a
failure, and then run the batch call (sub-step **d**) once, embedding and committing the whole
set. **Where it offers no blocking form**, run the batch call every time you wake with landed
returns, over whatever has landed by then. No foreground shell loop, background shell loop, or
event monitor serves as the wait in either arm: the dispatch message itself, or the wake-ups the
agents' endings bring, is the whole wait. No ranking or ordering precedes the dispatches: an
alternative set is enumerated against the sibling questions as scope only, never against how a
sibling will settle, so no dispatch reads what another wrote and their order changes nothing.
Both arms write the same blocks and land the same commits; they differ only in how many times
you wake.

**a. Create the run's scratch directory.** Before the first dispatch, run

```
mktemp -d
```

once and hold the path it prints as `<scratch dir>`: a fresh, uniquely named directory under
the system temp location that belongs to this run alone, so no other run's returns can reach
it. Every agent writes its return into it, and every later command in this step names it by
that path, written out in full.

**b. Dispatch one subagent per question step 1b printed.**

Use the `Agent` tool with `subagent_type` set to the namespaced registry name of the
`provide-alternatives-to-open-question` agent (singular — the per-question subagent) under this
plugin's namespace, `cairn:provide-alternatives-to-open-question` — one dispatch per surviving
question. Pass it that question's **Short Title**, the `<MILESTONE_DIR>` resolved in step 0, and
the `<scratch dir>` created in sub-step **a**, and nothing else — the three values the
orchestrator already holds:

```
Enumerate the alternatives for this single open question.

Short Title: <Short Title>

Milestone directory: <MILESTONE_DIR>

Scratch directory: <scratch dir>
```

The prompt carries no question text and no block: the subagent fetches its own block and its
sibling scope through the plugin's open-question tool and reads the milestone's documents
itself, read-only, for whatever surrounding grounding it needs, so the orchestrator never reads
them to assemble context.

The subagent is **read-only toward the project** — it mutates nothing there. Its one write is
its return, outside the repository: the ready-to-embed XML sub-elements — one
`<alternative id="...">` element per option, each with its what-it-is text and child
`<advantage>` and `<drawback>` elements, and **only** those child elements, never the
`<open-question>` wrapper, the `<question>` element, a `<recommendation>`, an
`<applied-principle>`, or a `<depends-on>` element — written to
`<scratch dir>/<Short Title>.xml` under a temporary name and renamed into place, so no scan
ever selects a half-written file. Its final message is then the bare token `DONE`, or
`FAILED: <reason>` when it could not land that file. The return never comes back in the
message, and the orchestrator does **all** the writing of the document, through the tool.

**c. Last-line verdict on each final message.** As each agent ends, read the **last
non-whitespace line** of its final message. If that line begins with `FAILED:`, the agent
failed explicitly: skip that question alone — note its Short Title with the reason (the text
after `FAILED:`) for the step-4 advisory — and make no further attempt on it, **never a
repair**. This verdict is the only judging you do yourself, and nothing else is judged or
cross-checked: a `DONE` is never checked against the scratch directory, and a final message
that is neither token is not judged at all. Whatever file an agent landed is the batch call's
to embed, and a question whose file never landed is caught by the closing check (sub-step
**g**).

**d. Embed and commit every landed file in one batch call.** Each time the paragraph opening
this step has you batch — once its wait returns, or each time you wake with landed returns —
run this one fixed shell call, written out in full exactly as shown, with only `<scratch dir>`
and `<MILESTONE_DIR>` replaced by their paths:

```
mkdir -p "<scratch dir>/processed"
find "<scratch dir>" -maxdepth 1 -type f -name '*.xml' | while IFS= read -r f; do
  t="${f##*/}"; t="${t%.xml}"
  if err="$(python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py embed --alternatives <MILESTONE_DIR> "$t" < "$f" 2>&1)"; then
    if [ -n "$(git status --porcelain -- <MILESTONE_DIR>/open_questions.xml)" ]; then
      out="$(git add <MILESTONE_DIR>/open_questions.xml 2>&1 && git commit -q -m "Alternatives-annotation: $t" 2>&1)" ||
        printf '%s\t%s\n' "$t" "$(printf '%s\n' "$out" | head -n 1)"
    fi
  else
    printf '%s\t%s\n' "$t" "$err"
  fi
  mv "$f" "<scratch dir>/processed/"
done
```

It scans exactly the `*.xml` files directly inside the scratch directory — never a file still
under its temporary name, never the `processed` subdirectory — and for each one takes the
Short Title from the file name and redirects the file into `embed --alternatives`, which writes
the file's `<alternative>` elements into the existing block in canonical form or refuses it
with one `Error:` line and the document unchanged. Each question the tool accepted is then
committed by the steps of the shared commit procedure at
`${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` — its dirty-own-path guard, the path-scoped
`git add` of `<MILESTONE_DIR>/open_questions.xml` alone (never `git add -A`), and a subject-only
commit under `Alternatives-annotation: <Short Title>` with **no body** — with git's success
output silenced. Every file the call piped, accepted or refused, is then moved into the
`processed` subdirectory, so the next scan sees only files that landed after this one and no
file is ever piped twice; the record of what was piped lives on disk, never in your context.
This pass requires **no** clean working tree: each commit is path-scoped to the one document,
so a dirty tree elsewhere stays out of it.

What the call prints is the whole outcome. It prints nothing when every file embedded and
committed; otherwise one line per refused file or failed commit — the Short Title, a tab, then
the tool's `Error:` line or git's first line. An annotated question gets no line.

- A line whose text after the tab begins `Error:` is a **refused file**: that question's block
  is unchanged. Hold the line verbatim — it fills that question's repair (sub-step **e**), or,
  when the question has already had its repair, its advisory entry.
- Any other line is a **failed commit**: the embed wrote, but git refused the commit. That
  question gets no repair, since its block already carries alternatives and a second embed
  would be refused; note its Short Title with git's line for the step-4 advisory.

**e. Repair every refused file once, all together.** The moment a batch call prints refused
files, send every one of that call's repairs together in the same turn — immediately, never
held back as a second phase once the first returns have all landed. Repair each question by
whichever of these two branches the host supports, in this order:

- **Continue the same agent session.** Where the host can continue a finished agent session and
  you still hold that dispatch's handle — a follow-up message addressed to the agent id the
  `Agent` tool returned — send the corrective message below to **that same agent**. Its context
  is intact, so it rewrites its file from the analysis it already did.
- **Re-dispatch one fresh agent.** Where the host cannot continue a finished agent session, or
  the handle is gone, dispatch **one** fresh `cairn:provide-alternatives-to-open-question` agent
  for that question with the `Agent` tool, passing the **same prompt** as the original dispatch
  with the corrective message below appended to it as a shape reminder. This second dispatch
  redoes the analysis, so it is the fallback branch, never the preferred one.

Both branches send this fixed one-paragraph corrective message, whose single slot is
`<Error line>`:

```
A previous return for this question could not be embedded — <Error line>. Write the
`<alternative>` elements — each with its what-it-is text and its child `<advantage>` and
`<drawback>` elements — afresh as the whole content of your scratch file, under its temporary
name and then renamed into place, as your instructions describe, and check that content against
both shape tests before writing it: its first non-whitespace text starts with `<alternative`,
and its last non-whitespace text ends with `</alternative>`. Write those `<alternative>`
elements and nothing else — no grounding summary above them, no closing remark below them, and
no `<recommendation>`, `<applied-principle>`, or `<depends-on>` element among them — then end
with the bare token `DONE`, or with `FAILED: <reason>` if you cannot.
```

Fill `<Error line>` with the refused file's `Error:` line from the batch call's print,
verbatim — the same line the skip advisory would carry — so the one attempt is aimed rather
than blind. Never quote the offending file back to the agent; the tool's line names what
failed.

Where the single wait is the dispatch call's own blocking form, send every repair **without
blocking**, so each later wake-up that brings repaired returns runs a batch call over whatever
has landed by then; otherwise wait on the repair set as the paragraph opening this step
describes. Either way a repaired file lands at its Short Title's path — the refused one already
moved aside — and gets no special handling: the next batch call embeds and commits it like any
other, and the repaired agent's final message gets the same last-line verdict (sub-step **c**).

Spend at most **one** repair per question: the only thing you track per question is whether it
has had its repair. A repaired question whose agent ends `FAILED:`, or whose file is refused
again, is a **skip of that question alone, never a run stop**: repair nothing more, note its
Short Title with that second reason (the `FAILED:` text or the second `Error:` line) for the
step-4 advisory, and carry on with the others.

**f. Wait until every agent has ended, and delete nothing.** A blocking wait that ends with
dispatched agents still unfinished skips nothing: run the batch call over whatever has landed,
then wait again for the agents still outstanding, and repeat — with no limit on how many times
— until every dispatched agent, first dispatch or repair, has ended and the files it landed
have been batched.

You delete nothing at any point in the run — no scratch file, no `processed` subdirectory, no
scratch directory. The run's directory and every return in it, embedded or refused, are left to
the system's own temp handling, so a refused return the advisory reports stays available for
inspection.

**g. Closing check.** After the last batch call, run once

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py list --without-alternatives <MILESTONE_DIR>
```

Every id it prints that is among the ids step 1b gathered and is not already noted for the
advisory goes into the step-4 advisory with the fixed reason `no annotation landed` — an agent
ended without its file landing, whatever its final message said. Its block stays bare for the
next run of this pass to re-dispatch. Hold the print: it also chooses step 4's status line.
Then go to step 4.

### 4. Report

Print exactly one fixed terse status line for the whole run, chosen by the closing check's
print (step 3 sub-step **g**):

1. **A gathered id is missing from it** — at least one question this run dispatched now carries
   alternatives, its `Alternatives-annotation: <Short Title>` commit landed by a batch call —
   print `Alternatives embedded.`
2. **Else nothing was annotated** — every id step 1b gathered is still printed, or step 1b
   printed nothing and no dispatch ran — print no success line; print instead a distinct
   one-line message stating that nothing changed and why: every block already carried
   `<alternative>` elements (step 1b printed nothing), or every dispatched question was still
   skipped.

Each line is the whole of its output and names no identifier: no annotated-vs-skipped
breakdown, no per-question listing, and no next-step pointer to `/recommend-all-open-questions`.
The success line means there are new alternative sets for the recommendation pass to pick
against, and the no-op line that this run left git history untouched.

Alongside whichever line is chosen, print only the questions step 3 noted for the advisory — an
agent that ended `FAILED:` (sub-step **c**), a file refused **again** after its one repair or a
repaired agent that ended `FAILED:` (sub-step **e**), a failed commit (sub-step **d**), and a
gathered question with no annotation landed (sub-step **g**). List each as an advisory: its
Short Title with the reason it was skipped on (the second reason where a repair was spent), one
per line. This survives the terse-reporting rule because nothing else records it: the
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
