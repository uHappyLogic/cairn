The moment a batch call prints refused
files, send every one of that call's repairs together in the same turn — immediately, never
held back as a second phase once the first returns have all landed. Repair each question by
the first of these two branches that applies:

- **Continue the same agent session.** While you still hold the conversation id the
  `invoke_subagent` tool returned for that dispatch, send the corrective message below to
  **that same agent** with the `send_message` tool, its `Recipient` set to that conversation id.
  A finished agent waits idle with its context intact, so it rewrites its file from the analysis
  it already did.
- **Re-dispatch one fresh agent.** Where that conversation id is gone, dispatch **one** fresh
  `provide-alternatives-to-open-question` agent for that question with the `invoke_subagent`
  tool, passing the **same prompt** as the original dispatch with the corrective message below
  appended to it as a shape reminder. This second dispatch redoes the analysis, so it is the
  fallback branch, never the preferred one.

Send every repair **without blocking** — `send_message` returns at once, as an
`invoke_subagent` dispatch does — so each later wake-up that brings repaired returns runs a
batch call over whatever has landed by then. A repaired file lands at its Short Title's path —
the refused one already moved aside — and gets no special handling: the next batch call embeds
and commits it like any other, and the repaired agent's final message gets the same last-line
verdict (sub-step **c**).
