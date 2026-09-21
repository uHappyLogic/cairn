# Answer-with-recommendation procedure (shared core)

This is the single source of truth for recording one open question's **embedded
recommendation** as its answer in the current milestone. It composes over
`shared/answer-procedure.md` (the recording core): it lifts the `<recommendation>` element
the recommend sweep embedded in the question block, then delegates the actual recording to
that core unchanged. It is followed inline by the `answer-open-question-with-recommendation`
skill and in isolation by the `answer-open-question-with-recommendation` agent. The caller
supplies the one input below and wraps the result; this file describes only the work itself
— resolve, lift, delegate.

## Inputs

This procedure records one recommendation-derived answer given one input the caller
supplies:

- **SHORT TITLE** — the resolved handle of an existing `<open-question>` block to answer
  (its `id`, compared case-insensitively). The caller has already obtained it; lifting the
  block's `<recommendation>` element and delegating the recording are this procedure's job.

The ANSWER is **not** an input here — this procedure *derives* it by lifting the block's
embedded `<recommendation>` element. That derived ANSWER, together with SHORT TITLE and the
lifted `option` value as RECORDED OPTION, is what it hands to `shared/answer-procedure.md`.

## Procedure

### 1. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 2. Lift the recommendation

Run the plugin's open-question tool:

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py lift <MILESTONE_DIR> "<SHORT TITLE>"
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

### 3. Delegate to the recording core

Hand the resolved **SHORT TITLE**, the derived **ANSWER**, and the **RECORDED OPTION** lifted
in step 2 (passed separately, so the core hands it to the tool as an exact id rather than
parsing it out of ANSWER) to `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` and follow it
unchanged. That procedure owns the recording work (locate, analyse, fold, remove, cascade);
this procedure only lifts and delegates.
