# Milestone 22: Drop Open-Question Status

## Goal

Remove the `status` attribute from `<open-question>` blocks so the opening boundary tag is exactly `<open-question id="Short Title">`, and delete every rule that existed only to carry the open/deferred distinction: the review skill's Blocking/Deferred triage and deferred authoring template (findings it would have deferred are authored as ordinary questions), the deferred pass-through in the derive-tasks precondition and the review skill's convergence verdict (both become "no `<open-question>` block remains"), and every "open or deferred", "whatever its status", and "reads no status" qualifier across skills/, agents/, shared/, README.md, and the CLAUDE.md invariants, including milestone 21's accepted residual about deferred targets carrying forward. Regenerate the Antigravity tree so it carries no trace of the attribute. No migration is needed: no live requirements.md holds a block today.

## Relevant starting state

## Decisions

## Out of Scope

