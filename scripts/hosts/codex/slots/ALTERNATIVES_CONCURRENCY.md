Dispatch one read-only subagent per question step 1b printed, in **rounds of at most the
session's configured subagent thread cap**: the value of the `agents.max_threads` setting in the
session's configuration (also read under its newer name,
`agents.max_concurrent_threads_per_session`), or 6, its default, when the setting is unset.
Dispatch a round of up to that many pending questions at once, then wait in **one** `wait_agent`
call on every agent in the round until each has landed its file or ended in a failure, and run
the batch call (sub-step **d**) once over the round's files. When that batch call refuses no
file, close the round's agents with the `close_agent` tool and dispatch the next round at the full
cap. When it refuses some, first close the round's accepted and skipped agents with
`close_agent`, keeping the refused ones open so repair by continuation still reaches them; then
send every repair together (sub-step **e**), wait in one `wait_agent` call on the repair set
alone, and run one more batch call over the repaired files; only then close the repaired agents
and dispatch the next round at the full cap. Repairs never share a wait with a first dispatch and
never take a slot from the next round. Repeat until every question step 1b printed has been
dispatched and its round batched. No ranking or ordering precedes the dispatches: an alternative
set is enumerated against the sibling questions as scope only, never against how a sibling will
settle, so no dispatch reads what another wrote and their order changes nothing. However many run
at once, the run writes the same blocks and lands the same commits; the cap changes only
wall-clock time.
