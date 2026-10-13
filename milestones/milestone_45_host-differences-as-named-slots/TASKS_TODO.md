# TASKS TODO

## File-Backed Slot Values In Build

Extend `scripts/build_hosts.py` so each `[slots]` entry may be either a plain string or a one-key inline table `NAME = { file = "slots/NAME.md" }` whose path is relative to the definition directory and must stay under its `slots/` subdirectory, which template discovery skips; the file is read as UTF-8 with exactly one trailing `\n` or `\r\n` removed when present and every other byte substituted as written, and the loader refuses a missing file, a path outside `slots/`, and an entry that is neither form with a `BuildError` naming the slot and the refusal. No duplicate-source rule, precedence, or message is added (a second source is a repeated TOML key the parser already refuses), the inline form stays accepted, and the module docstring documents the file-backed form and `slots/` so it remains the one complete reference for settings keys and checks. Verified by `uv run scripts/build_hosts.py --check` passing against the unchanged definitions and by the committed `hosts/` trees not changing.

---

## Build Rendering Test Under Pinned Interpreter

Add one test module under `tests/` that opens with a module-level `pytest.skip(allow_module_level=True)` when `sys.version_info` is below `(3, 11)`, placed before any import of the build, then renders a small synthetic `core/` and one synthetic host definition (a `settings.toml` with inline and file-backed slots plus whatever templates it needs) into `tmp_path` by importing the build in-process, monkeypatching its module-level `CORE_DIR`, `LICENSE_FILE`, and `DEFINITIONS_DIR` onto the fixture, and calling `load_definition` and `render_host`, asserting the rendered files including a file-backed value landing in the right substitution order. The same module carries one case each for the three new loader refusals (a missing value file, a `..` escape outside `slots/`, and an integer entry), each writing a minimal definition into `tmp_path`, calling `load_definition` directly, and asserting a `BuildError` whose message names the slot and the refusal; the build code, `conftest.py`, `pyproject.toml`, and both pytest commands stay unchanged, and `main` and the check set are not exercised. Verified by `uv run pytest` passing with the module collected and `uv run --no-project --python 3.9 --with pytest pytest` reporting it skipped.

---

## Move Every Slot Value Into Files

Rewrite the `[slots]` table of all three `scripts/hosts/<host>/settings.toml` files so every slot, the one-word and empty values included (`CONTEXT_FILE`, and the empty `COMPLETE_TASK_PROMPT_INSTRUCTIONS` and `ALTERNATIVES_PROMPT_INSTRUCTIONS` of Claude Code and Antigravity among them), is bound as `NAME = { file = "slots/NAME.md" }` to a file under that definition's `slots/` subdirectory, keeping each slot declared once with its explanatory comment above its entry, and holding a value that must end in a newline (the Codex prompt-opener values that end in two) in a file ending in one more newline than the value carries. This is a storage move only: no value's text changes. Verified by rebuilding and confirming `git status` shows no change under `hosts/` and `uv run scripts/build_hosts.py --check` passes.

---

## Slot The Alternatives Pass Host Passages

In `core/skills/provide-alternatives-to-all-open-questions/SKILL.md` replace the four capability-conditional passages the starting state names with two new slots: one for the opening paragraph's concurrency phrase ("they run together where the host allows it"), and one repair slot holding the sub-step e lead-in, the two repair branches, and the repair-wait sentence, reordering sub-step e so that slotted text is contiguous ahead of the fixed corrective message, its fill rule, and the one-repair cap, which stay in `core/`, while `ALTERNATIVES_CONCURRENCY` and sub-steps d and f stay as they are. Retire the `AGENT_TOOL` and `ALTERNATIVES_AGENT` slots from `core/` and every definition, writing their wording literally inside each host's repair value, and seed each host's two new values as `slots/` files with exactly the text its tree renders today, so no slot value carries a placeholder other than `{{PLUGIN_ROOT}}`. Verified by rebuilding and confirming every `hosts/` tree is byte-identical to before and `--check` passes.

---

## Claude Code Hands-On Check And Values

Run a hands-on check against the locally installed `claude`, with its documentation alongside, covering dispatch, waiting, continuing a finished agent, and the context file, and from it write the Claude Code values of the two new slots by lifting the arm of the former capability-conditional wording that applies to Claude Code, kept as written except where the check contradicts it; rewrite `ALTERNATIVES_CONCURRENCY` to the single wait mechanism the check observes with no capability condition, dropping the other arm, the "Both arms" closing sentence, and the capability wording of its comment; and keep the other seven existing values unless the check contradicts one. Record the check once as a single dated block in the header comment of `scripts/hosts/claude/settings.toml` naming the installed version and exactly the slots and points the check sourced or confirmed, keep every per-slot comment describing only what the value stands for and why in mechanism terms with no version, and keep every value free of any host name including its own. Verified by rebuilding with `--check` passing and reading the rendered `hosts/claude` alternatives pass as describing one wait mechanism and only the repair branches this host has.

---

## Codex Repair Values From Hands-On Run

Rewrite the Codex values of the two new slots from Codex's documentation plus a hands-on run of the locally installed `codex` that exercises exactly what they describe (sending a follow-up to a finished subagent, re-spawning a fresh generic subagent, and waiting with `wait_agent` on a repair set alone), leaving the eight existing Codex values as they stand unless the run contradicts one the new values depend on, and record the run as a single dated block in the header comment of `scripts/hosts/codex/settings.toml` naming the installed version and exactly the new repair values and any contradicted existing value, claiming nothing about an untouched value. Under the other-host rule, reword the Codex README template's "never to `CLAUDE.md`" clause so no file in the Codex tree names another host's mechanism, contrastive mentions included. Verified by rebuilding with `--check` passing and a search of `hosts/codex` finding no other host's tool, file, or command named.

---

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
