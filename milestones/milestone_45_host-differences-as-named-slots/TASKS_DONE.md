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
