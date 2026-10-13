Dispatch one read-only subagent per question step 1b printed, **all of them together in one
`invoke_subagent` call** — one entry in its `Subagents` array per surviving question, with no
cap beyond one dispatch per surviving question. The call returns at once, before any agent has
ended, and each agent's final message reaches you as a message from it, which wakes you once it
ends. Run the batch call (sub-step **d**) every time you wake with landed returns, over whatever
has landed by then. No foreground shell loop, background shell loop, scheduled timer, event
monitor, or polling of the running subagents serves as the wait: the wake-ups the agents'
messages bring are the whole wait. No ranking or ordering precedes the dispatches: an
alternative set is enumerated against the sibling questions as scope only, never against how a
sibling will settle, so no dispatch reads what another wrote and their order changes nothing.
