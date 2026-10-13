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
