The moment a batch call prints refused
files, send every one of that call's repairs together in the same turn — immediately, never
held back as a second phase once the first returns have all landed. Repair each question by
the first of these two branches that applies:

- **Continue the same agent session.** While you still hold that dispatch's handle — a
  follow-up message with the `SendMessage` tool addressed to the agent id the `Agent` tool
  returned — send the corrective message below to **that same agent**. Its context is intact,
  so it rewrites its file from the analysis it already did.
- **Re-dispatch one fresh agent.** Where the handle is gone, dispatch **one** fresh
  `cairn:provide-alternatives-to-open-question` agent for that question with the `Agent` tool,
  in the background like the first dispatches, passing the **same prompt** as the original
  dispatch with the corrective message below appended to it as a shape reminder. This second
  dispatch redoes the analysis, so it is the fallback branch, never the preferred one.

Send every repair **without blocking** — a follow-up returns at once, as a background dispatch
does — so each later wake-up that brings repaired returns runs a batch call over whatever has
landed by then. A repaired file lands at its Short Title's path — the refused one already moved
aside — and gets no special handling: the next batch call embeds and commits it like any other,
and the repaired agent's final message gets the same last-line verdict (sub-step **c**).
