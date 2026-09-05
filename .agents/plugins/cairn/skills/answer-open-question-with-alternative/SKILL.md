---
name: answer-open-question-with-alternative
description: Record a chosen alternative from an open question's embedded analysis as that question's answer in the current milestone's requirements.md.
---

# answer-open-question-with-alternative

Records a **named `<alternative>`** from one open question's embedded analysis as its answer
**inline, in the current conversation** — never in a subagent — so the recording reasoning
(which block was resolved, which alternative was chosen, what decision was folded in, what
cascaded) stays in context for follow-up.

This is the sibling of `answer-open-question-with-recommendation`: same recommend-sweep
annotations, same recording core, but the answer is the `<alternative>` **you** name by its
`id` rather than the one `<recommendation>` the sweep picked — which lets you record a
decision that *overrides* the recommendation, or resolve a question the sweep left genuinely
tied. There is deliberately **no** batch or agent form of this skill; to record every
recommendation-bearing question at its *recommended* option unattended, use
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
recommendation path uses for "`<option>` — `<rationale>`". Never invent answer text.

### 4. Record the answer via the shared recording core

Hand the resolved **`<Short Title>`** and the derived **ANSWER** to
`${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` and follow it unchanged **yourself, in this
conversation** (its own step 1 re-resolves the milestone you already found — harmless). That
procedure owns the recording work — locate, analyse, remove the whole
`<open-question …>`…`</open-question>` block, fold the decision into `## Decisions` as clean
prose, and cascade to any mooted siblings.

Do **not** spawn any subagent — there is no `answer-open-question-with-alternative` agent.

### 5. Commit the alternative answer

Read and follow the shared commit procedure at
`${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you
need to resolve the path), carrying out its steps yourself. Supply it these inputs, using the
`<MILESTONE_DIR>` from step 1:

- **PATHS** — this skill's own edit: `<MILESTONE_DIR>/requirements.md`.
- **SUBJECT** — exactly `Alternative-answer: <Short Title>` (the answered question's handle).
  This distinct subject does **not** match `/capture-milestone-principle-updates`'s
  `^Manual-answer:` grep, so capture never harvests it.
- **Body** — the lifted alternative content (the `<id>` — `<what-it-is>` answer text derived in
  step 3, with XML entities un-escaped) — the answer that was recorded.

That procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit.
Its no-op guard also covers this skill's clean-stop cases: if the guard in step 2 fired or the
recording core in step 4 stopped on a mismatch, `requirements.md` is unchanged, so nothing is
staged and nothing is committed.

### 6. Report findings

On the success path — the alternative was recorded and committed — print exactly one fixed
terse status line, carrying no identifier (no Short Title, no alternative id, no commit
subject):

```
Answer recorded.
```

Do **not** re-narrate which question resolved, which alternative you recorded (its id or how it
read), or how the document changed (the resolved block, the decision folded into
`## Decisions`, any cascading resolutions). Alongside the terse line keep only the one piece of
genuinely git-absent advisory output: any new open questions the recorded decision may have
introduced — surface these but do **not** add them to the document without user confirmation.

**No-op case:** if step 5's dirty-own-path guard fired — nothing was committed because
`requirements.md` was unchanged (the step 2 guard fired, or the recording core in step 4
stopped on a mismatch) — do **not** print the terse success line. Instead print a single line
stating that nothing was recorded and briefly why.

Then stay available: the user may now ask follow-up questions or request adjustments, with the
full recording context still in hand.
