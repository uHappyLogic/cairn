# Starting-state procedure (shared core)

This is the single source of truth for writing a milestone's `## Relevant starting state`
section, a first run and a refresh alike: the `specify-milestone-starting-state` skill follows
it whenever it runs, and the `derive-tasks` and `submit-task` skills follow it in place when
their own check finds the ground moved. The runner supplies the input below and wraps the
result; this file describes only the work itself — check, explore, edit, clear the picks the
change undermines. It records nothing: what the runner does with the edited files is stated in
the runner's own file.

The section is reference material, not decisions: the facts every later decider forms its
picks and decisions against, and the as-of a recorded decision is read back with. One shape
serves both runs. A first run edits the empty section into existence; a refresh edits the
filled section in place, changing what no longer holds, adding what is new, and leaving every
subsection whose facts still hold byte-identical, so the change to the section is the change in
the ground and nothing else.

## Input

- **MILESTONE_DIR** — the already-resolved directory of the milestone whose starting state is
  written, its path exactly as resolved, trailing slash included. The runner resolves it; this
  procedure never looks the milestone up.

The milestone's **scope** is the directory holding its `milestones/` container: `<scope>` for
`<scope>/milestones/<slug>/`, the workspace root for `milestones/<slug>/`.

Every milestones-tool call below runs from the workspace root as the full fixed command
`python3 ~/.gemini/config/plugins/cairn/tools/milestones.py <query> …`, written out in full on every call and
never through a variable, alias, or function of your own defined to stand for the command or any
part of it. Make every one of them before step 5's edit.

**Any milestones-tool call that fails** — any non-zero exit, whatever its `Error:` line says —
is one condition: **stop without changing anything**, before any edit of the section, any pick
clearing, and anything your runner would do next. Report the fixed line
`Starting state stopped — a milestones-tool read failed.` first, then below it the call's
`Error:` line from stderr, verbatim. That is the whole report, and the run ends there.

## Procedure

### 1. Check whether the ground moved

Run:

```
python3 ~/.gemini/config/plugins/cairn/tools/milestones.py since <MILESTONE_DIR>
```

Its first line, when it prints one, is the anchor: the commit that last recorded this
milestone's starting state. Every line beneath it is a later commit that changed the scope
outside the milestone's own directory, or a revision of the milestone's own goal. Read its print
as exactly one of three outcomes:

- **No line at all** — there is no starting state yet: this is a **first run**. Go on to
  step 2.
- **The anchor alone** — the ground has not moved since the section was written: explore
  nothing, edit nothing, and clear nothing. The procedure ends here; your runner reports as its
  own file states.
- **Anything beyond the anchor** — the ground moved: this is a **refresh**. Hold the lines
  beneath the anchor — they say where to look first — and go on to step 2.

### 2. Read the goal and the project's environment

Read `<MILESTONE_DIR>/requirements.md` in full. Its `## Goal` is the lens for everything that
follows: surface only starting state directly relevant to achieving or building on that goal.
On a refresh, hold the `## Relevant starting state` section as it stands, subsection by
subsection: it is what step 5 edits.

Read `AGENTS.md` at the workspace root for the project's environment. If it carries no
description of the project's domain context or working conventions, suggest the user run
`/init` to enrich it first — richer project context yields a sharper starting state — then
proceed with whatever the project reveals. Hold from it the project's domain context (what the
project is and how its material is organized, which anchors all exploration), its working
conventions, the tools available for deeper inspection (MCP tools included), and how work is
verified as done.

### 3. Explore the scope, then the adjacent material

Explore the scope first, then the material outside it that the goal reaches. On a refresh,
re-check each standing subsection's facts against the project as it now is, starting where the
lines step 1 held point. Focus on:

- **Existing artifacts relevant to the goal** — the artifacts, sections, and components whose
  names or responsibilities overlap with the goal. Read what they expose — their outward-facing
  surface. Skip internal detail.
- **Existing capabilities** — if the goal builds on something that already exists, its current
  state and how other work connects to it.
- **Supporting materials** — settings, reference data, or structures the milestone will likely
  touch.
- **Known gaps** — if the goal requires something that clearly does not exist yet, state it as
  a gap in one sentence and move on; do not design its replacement here.

Do not exhaustively catalog everything — stay goal-relevant. Depth over breadth: a precise
description of one related area is more useful than a surface mention of ten. Use `find`,
`grep`, and `Read` for file-based exploration, and the MCP tools `AGENTS.md` documents
where they are relevant.

### 4. Read the record and what is in flight

Read the record of finished and live work in two tiers. First the overview of the scope:

```
python3 ~/.gemini/config/plugins/cairn/tools/milestones.py milestones --milestone <MILESTONE_DIR>
```

Then, for each finished milestone whose overview line bears on the goal, a deeper read: its
finish summary through `python3 ~/.gemini/config/plugins/cairn/tools/milestones.py summary <path>`, or its
recorded decisions through `python3 ~/.gemini/config/plugins/cairn/tools/milestones.py show <path>`, `<path>`
the milestone path exactly as the overview printed it. Read no verified bar: make no
`tasks --with-body` call. Past tasks reach the starting state only as the titles the overview and
the summaries already carry.

Then what is in flight, the other live milestones whose scope overlaps this one's:

```
python3 ~/.gemini/config/plugins/cairn/tools/milestones.py live <MILESTONE_DIR>
```

For each line it prints, note the milestone by path, whether it is `started`, and its goal in a
sentence, read from its `requirements.md`. For each `started` one, also read, as prose, the
decisions in its `requirements.md` and the remaining tasks in its `TASKS_TODO.md` that touch what
this goal reaches: a started milestone holds the scope and will finish before this one takes a
task, so what it has decided is the best description of the ground this milestone will execute
against, and is left to it rather than re-decided here. A milestone that is only `defined` is
listed by its goal alone, since nothing of it is settled.

### 5. Edit the section

Edit `## Relevant starting state` in `<MILESTONE_DIR>/requirements.md` in place, structured as
named subsections, one per relevant system or area:

```markdown
## Relevant starting state

### <System Name>

<2–5 sentences: what exists, where it lives, what it exposes, and any known limitations relevant to the goal.>

### <Another System>

...
```

Write only what currently exists, in the tree, in the record, and in flight: no intended
behaviour and no speculation about future state. Keep each subsection tight; the audience will
use it to make decisions and needs facts, not commentary.

On a first run, write the empty section into existence. On a refresh, change only what no
longer holds and add only what is new: every subsection whose facts still hold stays
byte-identical, not reworded, because the same facts written in fresh prose are noise in the
change. Touch no other section of `requirements.md`: no decision is rewritten here, since the
review pass is where a decision is weighed against a changed fact. An exploration may find
nothing changed and leave the section exactly as it stood; nothing records that, so the next run
in the same stale window explores again, a repeat accepted as the cost of keeping no state.

### 6. Clear the picks the changed facts undermine

A changed starting state is a premise change: a standing pick — the `<recommendation>` element
an open question carries — formed against the old facts would otherwise be recorded as given.
Read `<MILESTONE_DIR>/open_questions.xml` whole with the file-reading tool; that whole read is for
reasoning only, and every change to the document is a call to the plugin's open-question tool,
`python3 ~/.gemini/config/plugins/cairn/tools/open_questions.py <subcommand> <MILESTONE_DIR> …`, written out in
full on every call and never through a variable, alias, or function of your own. Never edit the
file yourself.

The changed facts are what step 5's edit altered, added, or removed. For each block carrying a
pick, hold two texts: the what-it-is text of the `<alternative>` its `<recommendation option="…">`
names, and the one-line rationale that is the `<recommendation>` element's own text. Read them
against the changed facts. The pick is **undermined** when either holds:

- **The option can no longer be carried out.** The recommended alternative, as its what-it-is
  text reads, cannot be carried out on the ground the edited section describes.
- **The stated reason no longer holds.** The rationale states or plainly presupposes a fact the
  edit changed, so the reason no longer holds as written, even though the option itself could
  still be carried out.

Judge it in prose, from those two texts as written. Do not re-form the recommender's judgment:
do not weigh the block's other alternatives, ask which option is now best, or decide whether the
same option would be picked again for a different reason. **Doubt strips**: a pick only arguably
untouched is named, because a cleared block keeps its alternatives and the next recommendation
pass re-picks over them, while a stale pick left standing is recorded as a decision. A pick that
merely shares a topic with a changed fact is not named. Judge each block on its own two texts
only: a block whose `<depends-on>` names an undermined block is not named on that account.

When at least one pick is undermined, clear them all with one call, every named block's Short
Title (its `id` as the document holds it) its own quoted argument:

```bash
python3 ~/.gemini/config/plugins/cairn/tools/open_questions.py strip --recommendation <MILESTONE_DIR> "<Short Title>" …
```

It clears each named block's pick and keeps its `<alternative>` children, touching no other
block; the clearing is not transitive, so add no block the tags lead to. When no pick is
undermined, the document holds no pick, or step 5 left the section as it stood, make no call.

If the call exits non-zero, correct the named Short Titles against its `Error:` line — the tool
refuses an unknown title with the document unchanged — and run the call once more. If that
second call also exits non-zero, stop: report the fixed line
`Starting state stopped — clearing the undermined picks failed.` first, then below it the second
call's `Error:` line verbatim and that the section edit stands uncommitted in
`requirements.md`. The run ends there.

### 7. Hand back the change

The procedure ends with `<MILESTONE_DIR>/requirements.md` edited, or left as it stood, and with
`<MILESTONE_DIR>/open_questions.xml` changed exactly when step 6 cleared a pick. Your runner's own
file states what it does with them.
