# TASKS DONE

## File-Backed Slot Values In Build

Extend `scripts/build_hosts.py` so each `[slots]` entry may be either a plain string or a one-key inline table `NAME = { file = "slots/NAME.md" }` whose path is relative to the definition directory and must stay under its `slots/` subdirectory, which template discovery skips; the file is read as UTF-8 with exactly one trailing `\n` or `\r\n` removed when present and every other byte substituted as written, and the loader refuses a missing file, a path outside `slots/`, and an entry that is neither form with a `BuildError` naming the slot and the refusal. No duplicate-source rule, precedence, or message is added (a second source is a repeated TOML key the parser already refuses), the inline form stays accepted, and the module docstring documents the file-backed form and `slots/` so it remains the one complete reference for settings keys and checks. Verified by `uv run scripts/build_hosts.py --check` passing against the unchanged definitions and by the committed `hosts/` trees not changing.

**Verified:**

- `load_definition` in `scripts/build_hosts.py` accepts each `[slots]` entry as a plain string or a one-key inline table `{ file = "slots/NAME.md" }` resolved relative to the definition directory, and file-backed values load identically to the inline ones (a scratch copy of the Claude Code definition with all eight slots moved to files yields the same slot map and the same template list).
- Template discovery skips the definition's `slots/` subdirectory, so no value file is rendered as a template.
- A value file is read as UTF-8 bytes with exactly one trailing `\n` or `\r\n` removed when present (`X.md\r\n` gives `X.md`, `X.md\n\n` gives `X.md\n`, `X.md` with no newline stays `X.md`).
- The loader raises a `BuildError` naming `slots.<NAME>` and the refusal for a missing value file, a path outside `slots/` (`slots/../settings.toml` and `../claude/slots/...`), and an entry that is neither form (an integer, and a table with an extra key).
- No duplicate-source rule is added: a second entry for one slot is a repeated TOML key, which `tomllib` refuses ("Cannot overwrite a value"); the inline string form stays accepted.
- The module docstring documents the file-backed form, the `slots/` subdirectory, the line-ending rule, and the refusals, so it remains the one complete reference for settings keys and checks.
- `uv run scripts/build_hosts.py --check` passes against the unchanged definitions, and `git status` shows no change under `hosts/` (only `scripts/build_hosts.py` modified); `uv run pytest` still passes (544 tests).

---

## Build Rendering Test Under Pinned Interpreter

Add one test module under `tests/` that opens with a module-level `pytest.skip(allow_module_level=True)` when `sys.version_info` is below `(3, 11)`, placed before any import of the build, then renders a small synthetic `core/` and one synthetic host definition (a `settings.toml` with inline and file-backed slots plus whatever templates it needs) into `tmp_path` by importing the build in-process, monkeypatching its module-level `CORE_DIR`, `LICENSE_FILE`, and `DEFINITIONS_DIR` onto the fixture, and calling `load_definition` and `render_host`, asserting the rendered files including a file-backed value landing in the right substitution order. The same module carries one case each for the three new loader refusals (a missing value file, a `..` escape outside `slots/`, and an integer entry), each writing a minimal definition into `tmp_path`, calling `load_definition` directly, and asserting a `BuildError` whose message names the slot and the refusal; the build code, `conftest.py`, `pyproject.toml`, and both pytest commands stay unchanged, and `main` and the check set are not exercised. Verified by `uv run pytest` passing with the module collected and `uv run --no-project --python 3.9 --with pytest pytest` reporting it skipped.

**Verified:**

- `tests/test_build_rendering.py` exists under `tests/` and opens with a module-level `pytest.skip(..., allow_module_level=True)` when `sys.version_info < (3, 11)`, placed before any import of the build.
- The module imports `scripts/build_hosts.py` in-process, monkeypatches its `CORE_DIR`, `LICENSE_FILE`, and `DEFINITIONS_DIR` onto a synthetic `core/`, `LICENSE`, and one synthetic host definition in `tmp_path` (a `settings.toml` with one inline and one file-backed slot, a `slots/` value file, and a `README.md` template), and calls `load_definition` and `render_host`.
- The rendering case asserts the loaded slot map, the template list (the `slots/` file is not a template), the exact rendered file set, and every rendered file's exact contents, including the file-backed value with one trailing newline removed, its `{{PLUGIN_ROOT}}` replaced after the slot fill, its drop-pattern text removed after both, and the stripped frontmatter key.
- The module carries one case each for a missing value file, a `..` escape outside `slots/`, and an integer entry, each writing a minimal definition into `tmp_path`, calling `load_definition` directly, and asserting a `BuildError` whose message names `slots.BAD_SLOT` and the refusal.
- The build code, `conftest.py`, `pyproject.toml`, and both pytest commands are unchanged, `main` and the check set are not exercised, and `uv run scripts/build_hosts.py --check` still passes.
- `uv run pytest` passes with the module collected (548 passed, its 4 cases included).
- `uv run --no-project --python 3.9 --with pytest pytest` reports the module skipped (544 passed, 1 skipped).

---

## Move Every Slot Value Into Files

Rewrite the `[slots]` table of all three `scripts/hosts/<host>/settings.toml` files so every slot, the one-word and empty values included (`CONTEXT_FILE`, and the empty `COMPLETE_TASK_PROMPT_INSTRUCTIONS` and `ALTERNATIVES_PROMPT_INSTRUCTIONS` of Claude Code and Antigravity among them), is bound as `NAME = { file = "slots/NAME.md" }` to a file under that definition's `slots/` subdirectory, keeping each slot declared once with its explanatory comment above its entry, and holding a value that must end in a newline (the Codex prompt-opener values that end in two) in a file ending in one more newline than the value carries. This is a storage move only: no value's text changes. Verified by rebuilding and confirming `git status` shows no change under `hosts/` and `uv run scripts/build_hosts.py --check` passes.

**Verified:**

- All three `scripts/hosts/<host>/settings.toml` files bind every one of their eight slots as `NAME = { file = "slots/NAME.md" }` (8 such entries per file, no inline `[slots]` value left), the one-word `CONTEXT_FILE` and the empty `COMPLETE_TASK_PROMPT_INSTRUCTIONS` and `ALTERNATIVES_PROMPT_INSTRUCTIONS` included.
- Each definition's `slots/` subdirectory holds exactly the eight value files its entries name, each containing the former inline value plus one trailing newline (the empty values as a lone newline, the Codex prompt-opener values ending in three newlines for a value carrying two).
- Each slot stays declared once in its `[slots]` table with its explanatory comment above its entry, in the original order; only the table's lead comment changed, to say the values sit in `slots/` files with one extra trailing newline.
- No value's text changed: `uv run scripts/build_hosts.py` rebuilt all three trees and `git status` shows no change under `hosts/`.
- `uv run scripts/build_hosts.py --check` passes, and `uv run pytest` still passes (548 tests).

---

## Slot The Alternatives Pass Host Passages

In `core/skills/provide-alternatives-to-all-open-questions/SKILL.md` replace the four capability-conditional passages the starting state names with two new slots: one for the opening paragraph's concurrency phrase ("they run together where the host allows it"), and one repair slot holding the sub-step e lead-in, the two repair branches, and the repair-wait sentence, reordering sub-step e so that slotted text is contiguous ahead of the fixed corrective message, its fill rule, and the one-repair cap, which stay in `core/`, while `ALTERNATIVES_CONCURRENCY` and sub-steps d and f stay as they are. Retire the `AGENT_TOOL` and `ALTERNATIVES_AGENT` slots from `core/` and every definition, writing their wording literally inside each host's repair value, and seed each host's two new values as `slots/` files with exactly the text its tree renders today, so no slot value carries a placeholder other than `{{PLUGIN_ROOT}}`. Verified by rebuilding and confirming every `hosts/` tree is byte-identical to before and `--check` passes.

**Verified:**

- `core/skills/provide-alternatives-to-all-open-questions/SKILL.md` replaces the opening paragraph's "they run together where the host allows it" with `{{ALTERNATIVES_PARALLELISM}}` and opens sub-step e with `{{ALTERNATIVES_REPAIR}}` (the lead-in, both repair branches, and the repair-wait paragraph, contiguous), followed in `core/` by the fixed corrective message (its introducing sentence reworded from "Both branches send" to "Every repair sends", so `core/` presumes no branch count), its fill rule, and the one-repair cap; `{{ALTERNATIVES_CONCURRENCY}}` and sub-steps d and f are unchanged.
- `AGENT_TOOL` and `ALTERNATIVES_AGENT` appear nowhere under `core/` or `scripts/`: their entries and `slots/` files are removed from all three definitions, and their wording (`` `Agent` tool `` with the `cairn:` registry name for Claude Code and Antigravity, `` `spawn_agent` tool `` with the default (generic) subagent for Codex) is written literally inside each host's `slots/ALTERNATIVES_REPAIR.md`.
- Each definition binds `ALTERNATIVES_PARALLELISM` and `ALTERNATIVES_REPAIR` as `{ file = "slots/NAME.md" }` with a comment above each entry, and each value file holds exactly the text its tree rendered before plus one trailing newline; no slot value file carries a `{{` placeholder other than `{{PLUGIN_ROOT}}`.
- `uv run scripts/build_hosts.py` rebuilt all three trees: the only changed files are the three rendered alternatives-pass SKILL.md files, and in each the change is exactly the mandated sub-step e reorder (the repair-wait paragraph moved ahead of the corrective message) plus the "Every repair sends" rewording; undoing those two reproduces the previous file byte for byte, and every other `hosts/` file is byte-identical to before (the reorder the decision requires makes full byte identity of that one file impossible).
- `uv run scripts/build_hosts.py --check` passes, and `uv run pytest` still passes (548 tests).

---
