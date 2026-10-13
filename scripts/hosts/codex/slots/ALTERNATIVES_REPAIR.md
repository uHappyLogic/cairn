The moment a batch call prints refused
files, send every one of that call's repairs together in the same turn — immediately, before
the next round is dispatched. Repair each question by the first of these two branches that
applies:

- **Continue the same agent session.** While you still hold the canonical task name the
  `spawn_agent` tool returned for that dispatch, send the corrective message below to **that
  same agent** with the `followup_task` tool addressed to that task name, which starts a new
  turn on the finished agent (never `send_message`, which starts none). Its context is intact,
  so it rewrites its file from the analysis it already did.
- **Re-dispatch one fresh agent.** Where that task name is gone, spawn **one** fresh default
  (generic) subagent for that question with the `spawn_agent` tool, under a task name no earlier
  dispatch of this session used (a name already used is refused), passing the **same prompt** as
  the original dispatch with the corrective message below appended to it as a shape reminder.
  This second dispatch redoes the analysis, so it is the fallback branch, never the preferred
  one.

Then wait on the repair set as the paragraph opening this step describes. A repaired file lands
at its Short Title's path — the refused one already moved aside — and gets no special handling:
the next batch call embeds and commits it like any other, and the repaired agent's final message
gets the same last-line verdict (sub-step **c**).
