# Answer-with-recommendation procedure (shared core)

This is the single source of truth for recording one open question's **embedded
recommendation** as its answer in a milestone. It composes over
`shared/answer-procedure.md` (the recording core): it lifts the `<recommendation>` element
the recommend sweep embedded in the question block, then delegates the actual recording to
that core unchanged. It is followed inline by the `answer-open-question-with-recommendation`
skill and, once per question, by the inline answer sweep. The caller supplies the inputs
below and wraps the result; this file describes only the work itself — lift, delegate.

## Inputs

This procedure records one recommendation-derived answer given two inputs the caller
supplies:

- **MILESTONE_DIR** — the already-resolved directory of the milestone the question belongs
  to, the `<MILESTONE_DIR>` every tool call below uses. The caller resolves it; this
  procedure never looks the milestone up, and hands it on to the recording core as that
  core's own `MILESTONE_DIR` input.
- **SHORT TITLE** — the resolved handle of an existing `<open-question>` block to answer
  (its `id`, compared case-insensitively). The caller has already obtained it; lifting the
  block's `<recommendation>` element and delegating the recording are this procedure's job.

The ANSWER is **not** an input here — this procedure *derives* it by lifting the block's
embedded `<recommendation>` element. That derived ANSWER, together with MILESTONE_DIR,
SHORT TITLE, and the lifted `option` value as RECORDED OPTION, is what it hands to
`shared/answer-procedure.md`.

## Procedure

### 1. Lift the recommendation

Run the plugin's open-question tool:

```
python3 .agents/plugins/cairn/tools/open_questions.py lift <MILESTONE_DIR> "<SHORT TITLE>"
```

On success it prints one line, "`<option>` — `<rationale>`": the block's
`<recommendation option="…">` value, a spaced em dash, then the element's text, both as
plain text. That whole line is **ANSWER**, and its text before the first spaced em dash (the
whole line when there is none) is **RECORDED OPTION**. Derive both from this print alone —
never from a sibling `<applied-principle>` or `<alternative>`, which keeps the answer
provenance-free by construction — and never invent answer text.

**No-`<recommendation>`-element guard.** If the call fails — no block's `id` matches
SHORT TITLE, or the matched block carries no `<recommendation>` element (the recommend sweep
never annotated it, or the question was added afterward) — **stop without changing
anything** and report why, quoting the tool's `Error:` line: nothing is recorded.

### 2. Delegate to the recording core

Hand the given **MILESTONE_DIR** and **SHORT TITLE**, the derived **ANSWER**, and the
**RECORDED OPTION** lifted in step 1 (passed separately, so the core hands it to the tool
as an exact id rather than parsing it out of ANSWER) to
`.agents/plugins/cairn/shared/answer-procedure.md` and follow it unchanged. That procedure owns the recording work (locate, analyse, fold, remove, cascade);
this procedure only lifts and delegates.
