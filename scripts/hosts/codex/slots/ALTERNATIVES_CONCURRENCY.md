Dispatch one read-only subagent per question step 1b printed, in **rounds of at most the
session's configured subagent thread cap**: the value of the `agents.max_threads` setting in the
session's configuration (also read under its newer name,
`agents.max_concurrent_threads_per_session`), or 6, its default, when the setting is unset; a
spawn beyond the cap is refused. Dispatch a round of up to that many pending questions at once,
each under its own task name, then wait with the `wait_agent` tool until every agent in the
round has delivered its final message. One `wait_agent` call names no agent: it returns at the
first update from any of them, or at its timeout, and each agent's final message reaches you on
its own, so call it again, with a long `timeout_ms`, until the round's last final message has
arrived, and only then run the batch call (sub-step **d**) once over the round's files. A
finished agent holds no slot and needs no closing, so when that batch call refuses no file,
dispatch the next round at the full cap. When it refuses some, send every repair together
(sub-step **e**), wait the same way until every agent of the repair set has delivered its final
message — with no other agent running, every update is the repair set's — and run one more
batch call over the repaired files; only then dispatch the next round at the full cap. Repairs
never share a wait with a first dispatch and never take a slot from the next round. Repeat until
every question step 1b printed has been dispatched and its round batched. No ranking or ordering
precedes the dispatches: an alternative set is enumerated against the sibling questions as scope
only, never against how a sibling will settle, so no dispatch reads what another wrote and their
order changes nothing. However many run at once, the run writes the same blocks and lands the
same commits; the cap changes only wall-clock time.
