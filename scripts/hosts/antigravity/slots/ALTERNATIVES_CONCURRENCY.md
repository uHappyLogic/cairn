Dispatch one read-only subagent per question step 1b printed, **all of them together in one
message** — with no cap beyond one dispatch per surviving question — and collect their returns
by what the agent tool offers. **Where it offers a blocking dispatch form**, send every dispatch
in that form, so the message returns only once every agent has landed its file or ended in a
failure, and then run the batch call (sub-step **d**) once, embedding and committing the whole
set. **Where it offers no blocking form**, run the batch call every time you wake with landed
returns, over whatever has landed by then. No foreground shell loop, background shell loop, or
event monitor serves as the wait in either arm: the dispatch message itself, or the wake-ups the
agents' endings bring, is the whole wait. No ranking or ordering precedes the dispatches: an
alternative set is enumerated against the sibling questions as scope only, never against how a
sibling will settle, so no dispatch reads what another wrote and their order changes nothing.
Both arms write the same blocks and land the same commits; they differ only in how many times
you wake.
