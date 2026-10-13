Dispatch one read-only subagent per question step 1b printed, **all of them together in one
message** — with no cap beyond one dispatch per surviving question — and run every dispatch in
the background, never in the foreground: each `Agent` call returns at once, and each agent's
ending wakes you with its final message. Run the batch call (sub-step **d**) every time you wake
with landed returns, over whatever has landed by then. No foreground shell loop, background
shell loop, or event monitor serves as the wait: the wake-ups the agents' endings bring are the
whole wait. No ranking or ordering precedes the dispatches: an alternative set is enumerated
against the sibling questions as scope only, never against how a sibling will settle, so no
dispatch reads what another wrote and their order changes nothing.
