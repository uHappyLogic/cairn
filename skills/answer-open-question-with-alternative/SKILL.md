---
name: answer-open-question-with-alternative
description: Record a chosen `<alternative>` from an open question's embedded analysis as its answer in the current milestone's requirements.md inline in this conversation, then commit that answer on its own. Use when the recommend sweep has annotated a question with alternatives and you want to accept a specific alternative — named by its id, not necessarily the recommended one — as the decision for a single named question you want to stay available to discuss afterwards.
model: opus
---

# answer-open-question-with-alternative

Records a **named `<alternative>`** from one open question's embedded analysis as its answer
**inline, in the current conversation** — not in a subagent. Running inline is the whole
point: the recording reasoning (which block was resolved, which alternative was chosen, what
decision was folded in, what cascaded) stays in context, so you can follow up right after —
ask why that alternative read the way it did, tweak the recorded decision, or answer the next
question — without the context being thrown away.

This is the sibling of `answer-open-question-with-recommendation`. That skill lifts the one
`<recommendation>` the recommend sweep picked; **this** skill lifts an `<alternative>` **you**
name by its `id` — which lets you record a decision that *overrides* the recommendation, or
resolve a question the sweep left genuinely tied. Both read the same recommend-sweep
annotations and both compose over the same recording core
(`${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md`); they differ only in **which** embedded
element becomes the answer.

There is deliberately **no** batch/agent form of this skill (no
`answer-all-open-questions-with-alternative`, no per-question agent). Choosing *which*
alternative wins is per-question human judgment — there is no rule an orchestrator could apply
to pick one, so unlike the recommendation path there is nothing to sweep. If you want every
recommendation-bearing question recorded at its *recommended* option unattended, that is
`/answer-all-open-questions-with-recommendation`.

## Invocation

```
/answer-open-question-with-alternative <Short Title>. <Alternative Id>
```

Split the argument on the **first `.`** — exactly as `answer-open-question` does. Everything
before it is `<Short Title>` (the question handle); everything after it is `<Alternative Id>`
(the `id` of the `<alternative>` to record). Trim surrounding whitespace from both halves.

- `<Short Title>` must match (case-insensitive, against the block's `id`) an existing
  `<open-question status="open|deferred">` block that the `/recommend-all-open-questions` sweep
  has already annotated with `<alternative>` elements.
- `<Alternative Id>` must match (case-insensitive, against the `id` attribute) one of that
  block's embedded `<alternative id="...">` elements.

The procedure resolves the current milestone itself, so nothing needs to be looked up first.

## Workflow

### 1. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`
(run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path). Never use a hardcoded
task-list path. Hold `<MILESTONE_DIR>` — you need it for the delegated recording and the
commit.

### 2. Locate the question and the chosen alternative

Locating blocks by handle is a deterministic lookup, so query it with the line-oriented CLI
(`awk`/`sed`/`grep`) keyed on the `<open-question …>` / `</open-question>` boundary lines
rather than reading the whole file to eyeball a header. Every `<open-question>` block lives
under the single `## Open questions` section of `<MILESTONE_DIR>/requirements.md`.

- **Find the question block.** For each `<open-question …>` opening boundary line, pull its
  `id` attribute with an attribute-name-anchored regex — `id="([^"]*)"` — so the match is
  independent of attribute order. The captured value is stored **entity-escaped**, so reverse
  the five-predefined-entity substitution on it before comparing — replace `&lt;`→`<`,
  `&gt;`→`>`, `&quot;`→`"`, `&apos;`→`'`, and `&amp;`→`&` **last**. Case-fold both that
  un-escaped `id` and `<Short Title>` and compare; the block whose `id` case-folds equal is the
  match. It spans from its `<open-question …>` opening boundary line through the next
  `</open-question>` closing boundary line — one boundary-token pair per block, shared by open
  and deferred blocks (they differ only in the `status` value), so the locate is uniform.

- **Find the chosen alternative within it.** Inside the matched block, scan its
  `<alternative id="...">` opening lines, pull each `id` the same way (attribute-name-anchored
  regex, reverse entity-escaping), and case-fold-compare against `<Alternative Id>`. The
  `<alternative>` whose `id` case-folds equal is the one to lift; it spans from its
  `<alternative id="...">` opening line through its `</alternative>` closing line.

**Guard — clean stop, change nothing.** Stop without editing anything and report why if
either lookup fails:
- No block's `id` case-folds equal to `<Short Title>` (list the available question ids so the
  user can retry).
- The matched block carries **no** `<alternative>` elements at all — the
  `/recommend-all-open-questions` sweep never annotated it. Point the user at
  `/recommend-all-open-questions` first.
- The block has alternatives but **none** whose `id` case-folds equal to `<Alternative Id>`
  (list that block's available alternative ids so the user can retry).

This mirrors `shared/answer-procedure.md`'s clean stop on a Short-Title mismatch: nothing is
recorded. This locating is a **read** to derive the answer — it is not the recording core's
own locate/remove step, which runs later inside the delegated procedure.

### 3. Lift the alternative into the answer

Within the chosen `<alternative id="...">` element, read two things as a single-element CLI
read:

- its `id` attribute (attribute-name-anchored regex, `id="([^"]*)"`), and
- its **what-it-is text** — the element's own text node, i.e. everything between the
  `<alternative …>` opening tag and its first child element (`<advantage>`). Ignore the child
  `<advantage>` and `<drawback>` elements: they are the trade-off analysis, not the decision.

Both are stored **entity-escaped**, so reverse the five-predefined-entity substitution on each
— replace `&lt;`→`<`, `&gt;`→`>`, `&quot;`→`"`, `&apos;`→`'`, and `&amp;`→`&` **last** — to
recover clean unescaped text. Derive **ANSWER** by recombining the un-escaped `id` with the
un-escaped what-it-is text as "`<id>` — `<what-it-is>`" (the id, then a spaced em dash, then
the what-it-is sentence). That string is the answer text — the same anchor form the
recommendation path uses for "`<option>` — `<rationale>`".

### 4. Record the answer via the shared recording core

Hand the resolved **`<Short Title>`** and the derived **ANSWER** to
`${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` and follow it unchanged **yourself, in this
conversation** (its own step 1 re-resolves the milestone you already found — harmless). It is
the single source of truth for the recording work — locate the block, analyse, remove the
whole `<open-question …>`…`</open-question>` block, fold the decision into `## Decisions` as
clean prose, and cascade to any mooted siblings. Do **not** restate its steps here.

Do **not** spawn any subagent — there is no `answer-open-question-with-alternative` agent, and
running inline is what keeps the recording context for follow-up.

### 5. Commit the alternative answer

**Only if step 4 actually recorded the answer** — i.e. the shared procedure folded a decision
into `## Decisions` rather than stopping on a mismatch. If the guard in step 2 fired or the
recording core stopped without changes, there is nothing to commit; do not run these commands.

Stage **only** this skill's own `requirements.md` edit — path-scoped, never `git add -A` — and
commit it on its own, using the `<MILESTONE_DIR>` from step 1:

```
git add <MILESTONE_DIR>/requirements.md
git commit -m "Alternative-answer: <Short Title>" -m "<lifted alternative content>"
```

- **Subject:** exactly `Alternative-answer: <Short Title>` (the answered question's handle).
  This distinct subject keeps the commit out of finish-time
  `/capture-milestone-principle-updates`: it does **not** match capture's `^Manual-answer:`
  grep, so capture never harvests it. The rationale matches recommendation-answers — the
  recorded body is the analyst's alternative text, not user-deliberated reasoning — so it stays
  outside the capture grep with **no** change to capture's logic. The distinct subject is the
  honest git-log provenance discriminator.
- **Body:** the lifted alternative content (the `<id>` — `<what-it-is>` answer text derived in
  step 3, with XML entities un-escaped) — the answer that was recorded.

Committing here is a deliberate, documented exception to the project's "individual skills never
commit" rule — this skill records a decision, so it commits its decision atomically with a
greppable subject, exactly as `answer-open-question` and `answer-open-question-with-recommendation`
do. Path-scoped staging keeps the commit touching only `requirements.md` and never sweeps in
unrelated working-tree changes.

### 6. Report findings

After committing, briefly state:
- Which question was resolved, which alternative you recorded (id + how it read), and how the
  document changed (resolved block, decision folded into `## Decisions`, any cascading
  resolutions).
- Any new open questions the recorded decision may have introduced — surface these but do
  **not** add them to the document without user confirmation.

Then stay available: the user may now ask follow-up questions or request adjustments, with the
full recording context still in hand.

## Rules

- Split the argument on the **first `.`** — `<Short Title>` before it, `<Alternative Id>`
  after — and trim both; this mirrors `answer-open-question`.
- Derive ANSWER **only** from the chosen `<alternative>` — its `id` recombined with its
  what-it-is text as "`<id>` — `<what-it-is>`" — never from its `<advantage>`/`<drawback>`
  children (trade-off analysis, not the decision) and never invent answer text.
- The lift lives here; the recording (locate / analyse / remove whole block / fold into
  `## Decisions` / cascade) lives **only** in `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md`.
  Never duplicate or restate folding into `## Decisions` or cascading here.
- Run everything **inline** — there is no agent form of this skill, and no batch
  `answer-all-open-questions-with-alternative` (picking which alternative wins is per-question
  human judgment, not a rule an orchestrator could sweep).
- Both guards are clean stops that change and commit nothing: no matching question id, a block
  with no `<alternative>` elements, or no alternative matching `<Alternative Id>`. On a stop,
  list the available ids (question ids, or that block's alternative ids) so the user can retry.
- Commit **only** when step 4 actually recorded the answer. Stage path-scoped —
  `git add <MILESTONE_DIR>/requirements.md`, never `git add -A`. The commit carries the lifted
  alternative content in its **body** and the subject `Alternative-answer: <Short Title>`,
  which stays outside `/capture-milestone-principle-updates`'s `^Manual-answer:` grep.
  Committing here is a deliberate, documented exception to the "individual skills never commit"
  rule.
