# TASKS TODO

## Rewrite Docs For Slot-Only Host Differences

Rewrite `docs/design-claims.md` (claim 18's "names the capability, and the runtime selects the branch" sentence and example, and claim 13's once-per-run-or-once-per-wake-up wording), the `docs/skill-reference.md` alternatives-pass entry ("the one host-dependent paragraph", the inline `SendMessage` and rounds mentions, every "where the host" branch), and the two "where the host can wait" sentences of `docs/workflow.md` so they state that host differences reach `core/` only as named slots whose values sit inline or in files, that each rendered tree describes only its own wait and repair mechanism and never names another host's, and describe the alternatives pass's collection and repair as each host's definition now has them. Verified by a search of `docs/` finding none of the retired capability-conditional phrasing and the descriptions matching the three definitions' slot values.

---

## Restructure CONTRIBUTING Development Section

Restructure `CONTRIBUTING.md ## Development`: replace its `settings.toml` sentence and its inline check list with a short description of what a host definition is (settings plus templates, with wording differences as named slots whose values sit inline or in `slots/` files) and a pointer to the build script's docstring as the one complete reference for settings keys and checks; extend the test paragraph to cover the build rendering test, which runs under the pinned interpreter only and is skipped by the floor run; and state the development rule for contributors that host differences reach `core/` as named slots rather than capability-conditional prose and that a rendered tree never names another host's mechanism. Verified by reading the section against the build docstring and the committed definitions.

---

## Rewrite CLAUDE.md Invariants For Slots

Rewrite the `CLAUDE.md` invariants and Development notes to match the finished milestone: the "Host wording differences are named slots" invariant retires the Claude/Antigravity byte-identity as a test and the sentence making the Antigravity value the Claude Code paragraph, states that slots are preferred over capability-conditional prose, names the two new slots and the retired `AGENT_TOOL` and `ALTERNATIVES_AGENT`, describes `ALTERNATIVES_CONCURRENCY` as one single-mechanism paragraph per host, and records file-backed values under `slots/` as the convention with the inline form still accepted; the "name no host" invariant states that it covers every rendered runtime file, slot values included, with the new development rule that a rendered tree never names another host's mechanism (a rule, not a check, since `host-name-in-core` keeps scanning `core/` only) and the dated per-host check record as the only place a check is recorded; and the repository layout, `tests/` entry, and `## Development` bullets name `slots/`, the pinned-only rendering test, and the declare-every-slot requirement, with no tool version or observed-behaviour fact entering the file. Verified by a search of `CLAUDE.md` finding no retired statement and every rewritten sentence matching the committed definitions, build, and tests.

---
