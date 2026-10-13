The moment a batch call prints refused
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

Where the single wait is the dispatch call's own blocking form, send every repair **without
blocking**, so each later wake-up that brings repaired returns runs a batch call over whatever
has landed by then; otherwise wait on the repair set as the paragraph opening this step
describes. Either way a repaired file lands at its Short Title's path — the refused one already
moved aside — and gets no special handling: the next batch call embeds and commits it like any
other, and the repaired agent's final message gets the same last-line verdict (sub-step **c**).
