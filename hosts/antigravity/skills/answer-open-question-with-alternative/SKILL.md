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
  `<open-question>` block in `<MILESTONE_DIR>/open_questions.xml` that the
  `/recommend-all-open-questions` sweep has already annotated with `<alternative>` elements.
- `<Alternative Id>` must match (case-insensitive, against the `id` attribute) one of that
  block's embedded `<alternative id="...">` elements.

The skill resolves the current milestone itself, so nothing needs to be looked up first.

## Workflow

### 1. Find the current milestone

Follow `.agents/plugins/cairn/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded
task-list path. Hold `<MILESTONE_DIR>` — you need it for the lift, the delegated recording,
and the commit.

### 2. Lift the chosen alternative into the answer

Every read and write of `<MILESTONE_DIR>/open_questions.xml` is a call to the plugin's
open-question tool, that file's sole writer — never read or edit it yourself. Run

```
python3 .agents/plugins/cairn/tools/open_questions.py lift <MILESTONE_DIR> "<Short Title>" --alternative "<Alternative Id>"
```

On success it prints one line, "`<id>` — `<what-it-is>`": the chosen alternative's `id` as the
document holds it, a spaced em dash, then the element's own what-it-is text, both as plain
text, with its `<advantage>` and `<drawback>` children excluded (they are the trade-off
analysis, not the decision). That whole line is **ANSWER** — the same anchor form the
recommendation path uses for "`<option>` — `<rationale>`" — and its text before the first
spaced em dash is **RECORDED OPTION**. Derive both from this print alone; never invent
answer text.

**Guard — clean stop, change nothing.** If the call fails, stop without editing anything and
report why, quoting the tool's `Error:` line, which names the failed lookup:
- no block's `id` matches `<Short Title>` — the line lists the ids the document holds, so the
  user can retry;
- the matched block carries **no** `<alternative>` elements at all — the
  `/recommend-all-open-questions` sweep never annotated it; point the user at that sweep first;
- the block has alternatives but none whose `id` matches `<Alternative Id>` — the line lists
  that block's alternative ids, so the user can retry.

### 3. Record the answer via the shared recording core

Hand the resolved **`<Short Title>`**, the derived **ANSWER**, and the **RECORDED OPTION**
from step 2 (the same value ANSWER opens with, passed separately so the core hands it to the
tool as an exact id rather than parsing it out of ANSWER) to
`.agents/plugins/cairn/shared/answer-procedure.md` and follow it unchanged **yourself, in this
conversation** (its own step 1 re-resolves the milestone you already found — harmless). That
procedure owns the recording work — locate, analyse, fold the decision into `## Decisions` of
`requirements.md` as clean prose, remove the block from `open_questions.xml`, and cascade to
any mooted siblings.

Do **not** spawn any subagent — there is no `answer-open-question-with-alternative` agent.

### 4. Commit the alternative answer

Read and follow the shared commit procedure at
`.agents/plugins/cairn/shared/commit-procedure.md`, carrying out its steps yourself. Supply it these three inputs, using the
`<MILESTONE_DIR>` from step 1:

- **PATHS** — this skill's own edits: `<MILESTONE_DIR>/open_questions.xml` and
  `<MILESTONE_DIR>/requirements.md`.
- **SUBJECT** — exactly `Alternative-answer: <Short Title>` (the answered question's handle).
  This distinct subject marks an override of the embedded recommendation: when
  `/capture-milestone-principle-updates` walks a milestone's answer commits across all three
  subjects, it reads this one as an override signal, like `Manual-answer:`, and — because the
  body below carries no user rationale — asks the user then why the alternative was preferred;
  `Recommendation-answer:` commits are evidence about existing principles only.
- **BODY** — the lifted alternative: the "`<id>` — `<what-it-is>`" line the `lift` call printed
  in step 2, verbatim — the answer that was recorded.

That procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit.
Its no-op guard also covers this skill's clean-stop cases: if step 2 stopped on the tool's
`Error:` line or the recording core in step 3 stopped on one, neither file changed, so
nothing is staged and nothing is committed.

### 5. Report findings

On the success path — the alternative was recorded and committed — print exactly one fixed
terse status line, carrying no identifier (no Short Title, no alternative id, no commit
subject):

```
Answer recorded.
```

Do **not** re-narrate which question resolved, which alternative you recorded (its id or how it
read), or how the documents changed (the removed block, the decision folded into
`## Decisions`, any cascading resolutions). Alongside the terse line keep only the one piece of
genuinely git-absent advisory output: any new open questions the recorded decision may have
introduced — surface these but do **not** add them to the document without user confirmation.

**No-op case:** if step 4's dirty-own-path guard fired — nothing was committed because
neither file changed (step 2 or the recording core in step 3 stopped on the tool's `Error:`
line) — do **not** print the terse success line. Instead print a single line stating that
nothing was recorded and briefly why.

Then stay available: the user may now ask follow-up questions or request adjustments, with the
full recording context still in hand.
