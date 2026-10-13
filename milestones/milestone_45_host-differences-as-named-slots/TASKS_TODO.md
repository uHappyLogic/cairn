# TASKS TODO

## Antigravity Hands-On Check And Definition

Run a hands-on check against the locally installed `agy` covering dispatch, waiting, continuing an agent, and the context file, and rewrite every Antigravity slot value from what it shows, naming no host: `CONTEXT_FILE` becomes `AGENTS.md` at the workspace root (the README template's `/init` sentence rewritten to name it, with no migration, fallback, or notice beyond the release's ordinary changelog), `ALTERNATIVES_CONCURRENCY` and the two new slots describe this host's own single mechanisms, and native agent loading is added only if a file the build can already emit suffices (a manifest template beside `plugin.json` or a relocation through the existing layout and renames), otherwise the values describe the generic-subagent fallback that reads the plugin's agent file by its plugin-root path, with the build's key schema and code gaining nothing. Correct every non-slot Antigravity fact the check contradicts when the correction is an edit to an existing settings value or template (`plugin_root` with the README install path that must match it, the `/init` sentence, the `plugin.json` fields, a new root-level manifest rendered as a template included), record any contradiction needing a new settings key, an unrendered template kind, or build code under this milestone's Out of Scope naming the fact and what `agy` showed, and record the check once as a single dated block in the header comment of `scripts/hosts/antigravity/settings.toml` naming the `agy` version and what was observed of the four points, with per-slot comments kept mechanism-only. Verified by rebuilding with `--check` passing and a search of `hosts/antigravity` finding no other host's tool, file, or command named.

---

## Antigravity Command-Line Facts In Docs

Check every Antigravity command-line fact on `docs/ways-of-using-cairn.md` against the locally installed `agy` (the invocation form, `--dangerously-skip-permissions`, `--model` with `agy models`, `--add-dir` and its need on every `agy` line, and the move-a-line rule) and correct each one that differs, and replace the `--effort` value lists with a pointer to each host's own `--help` so the page lists no effort values for any host. Verified by reading the corrected legend and chains back against `agy --help` and `agy models` output.

---

## Rewrite Docs For Slot-Only Host Differences

Rewrite `docs/design-claims.md` (claim 18's "names the capability, and the runtime selects the branch" sentence and example, and claim 13's once-per-run-or-once-per-wake-up wording), the `docs/skill-reference.md` alternatives-pass entry ("the one host-dependent paragraph", the inline `SendMessage` and rounds mentions, every "where the host" branch), and the two "where the host can wait" sentences of `docs/workflow.md` so they state that host differences reach `core/` only as named slots whose values sit inline or in files, that each rendered tree describes only its own wait and repair mechanism and never names another host's, and describe the alternatives pass's collection and repair as each host's definition now has them. Verified by a search of `docs/` finding none of the retired capability-conditional phrasing and the descriptions matching the three definitions' slot values.

---

## Restructure CONTRIBUTING Development Section

Restructure `CONTRIBUTING.md ## Development`: replace its `settings.toml` sentence and its inline check list with a short description of what a host definition is (settings plus templates, with wording differences as named slots whose values sit inline or in `slots/` files) and a pointer to the build script's docstring as the one complete reference for settings keys and checks; extend the test paragraph to cover the build rendering test, which runs under the pinned interpreter only and is skipped by the floor run; and state the development rule for contributors that host differences reach `core/` as named slots rather than capability-conditional prose and that a rendered tree never names another host's mechanism. Verified by reading the section against the build docstring and the committed definitions.

---

## Rewrite CLAUDE.md Invariants For Slots

Rewrite the `CLAUDE.md` invariants and Development notes to match the finished milestone: the "Host wording differences are named slots" invariant retires the Claude/Antigravity byte-identity as a test and the sentence making the Antigravity value the Claude Code paragraph, states that slots are preferred over capability-conditional prose, names the two new slots and the retired `AGENT_TOOL` and `ALTERNATIVES_AGENT`, describes `ALTERNATIVES_CONCURRENCY` as one single-mechanism paragraph per host, and records file-backed values under `slots/` as the convention with the inline form still accepted; the "name no host" invariant states that it covers every rendered runtime file, slot values included, with the new development rule that a rendered tree never names another host's mechanism (a rule, not a check, since `host-name-in-core` keeps scanning `core/` only) and the dated per-host check record as the only place a check is recorded; and the repository layout, `tests/` entry, and `## Development` bullets name `slots/`, the pinned-only rendering test, and the declare-every-slot requirement, with no tool version or observed-behaviour fact entering the file. Verified by a search of `CLAUDE.md` finding no retired statement and every rewritten sentence matching the committed definitions, build, and tests.

---
