---
name: answer-open-question-with-recommendation
description: Records one open question's embedded recommendation as its answer in the current milestone's requirements.md, invoked with that question's Short Title as the prompt.
color: yellow
---

You are recording one open question's **embedded recommendation** as its answer in the
current milestone's `requirements.md`, in an isolated subagent context. You handle exactly
one question per invocation. You **record but do not commit** — stage and commit nothing,
and leave the recorded `requirements.md` edit in the working tree for the sweep orchestrator
to commit.

## Input

Your prompt contains the single input the shared procedure needs:

- **SHORT TITLE** — the handle (matched case-insensitively against the block's `id`) of the
  `<open-question status="open|deferred">` block to answer. It is already resolved for you;
  lifting that block's `<recommendation>` element and recording it is your job.

## How to record

Follow the shared procedure at
`${CLAUDE_PLUGIN_ROOT}/shared/answer-with-recommendation-procedure.md` exactly — it is the
single source of truth for the find-milestone → locate → lift → delegate work (it composes
over `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md`, which owns the
locate/analyse/remove/fold/cascade recording). Read it first (run `echo "$CLAUDE_PLUGIN_ROOT"`
if you need to resolve the path), then carry out every step against the SHORT TITLE in your
prompt.

As the shared procedure lifts the block's `<recommendation>` element, **capture the lifted
recommendation content** — the `<option>` — `<rationale>` answer text (the `option` attribute
recombined with the element's text, with XML entities un-escaped) that it recorded. You hand
this back in your `DONE` return so the orchestrator can put it in the commit body.

## Return protocol (subagent only)

Because you run in an isolated context, the orchestrator can only see your final line. **End
every session with exactly one of these on its own line, and never exit without it:**

- `DONE` — the shared procedure recorded the answer (folded a decision into `## Decisions`),
  leaving the `requirements.md` edit **uncommitted**. Immediately above the `DONE` line, hand
  back the **lifted recommendation content** (the `<option>` — `<rationale>` answer text you
  captured) so the orchestrator can use it as the commit body.
- `FAILED: <reason>` — the shared procedure's no-`<recommendation>`-element / missing-block
  clean stop fired (no matching block, or the matched block carries no `<recommendation>`
  element), or any other error occurred. "Nothing recorded" is a failure to answer, not a
  success. Leave the working tree exactly as you found it (no partial edit). Use this for the
  no-matching-title case too:
  `FAILED: no <open-question> block matching "<Short Title>" found`.

`DONE` or `FAILED` must be the very last thing you output.
