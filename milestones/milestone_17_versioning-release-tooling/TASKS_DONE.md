# TASKS DONE

## Version Script Writes Every Version Surface

Add a version script under `scripts/` that takes one bare `MAJOR.MINOR.PATCH` literal as its argument, refuses anything else, and writes it into `.claude-plugin/plugin.json`, a new `version` field on the single `plugins[]` entry in `.claude-plugin/marketplace.json`, and `pyproject.toml` (moving `cairn-tooling` off its independent `0.1.0`), keeping the matching `cairn-tooling` version line in `uv.lock` in step; it never touches the generated `.agents/plugins/cairn/plugin.json`, git, or `gh`. The milestone needs one command that bumps every source version literal so a release leaves no per-file judgement call. Verified by running it with a test version, confirming exactly those files changed with the literal in each, and reverting.

**Verified:**

- `scripts/set_version.py` exists under `scripts/` and runs as `uv run scripts/set_version.py <version>`.
- It accepts exactly one bare `MAJOR.MINOR.PATCH` literal and refuses anything else with a non-zero exit and no file change: zero arguments, two arguments, `v1.2.3`, `1.2`, `1.2.3.4`, `1.2.3-rc1`, `abc`, and `01.2.3` all stopped with an error and left the tree clean.
- A run with test version `9.9.9` wrote `"version": "9.9.9"` into `.claude-plugin/plugin.json`.
- The same run added `"version": "9.9.9"` to the single `plugins[]` entry in `.claude-plugin/marketplace.json`, which carried no version field before.
- The same run moved `pyproject.toml`'s `[project]` version off `0.1.0` to `version = "9.9.9"`.
- The same run kept `uv.lock`'s `cairn-tooling` `[[package]]` version in step at `version = "9.9.9"`.
- `git status --porcelain` after that run listed exactly those four files as modified (plus the new untracked script), each `git diff` hunk touching only its version line, and `git status --porcelain .agents/` was empty, so the generated `.agents/plugins/cairn/plugin.json` was not touched.
- The script invokes no git and no `gh`: it imports only `json`, `os`, `re`, and `sys`, with no `subprocess` or `os.system` use, and the only `.agents`/git/gh mentions in the file are in its docstring.
- A second identical run left the same four modified files and nothing further, and a run from a directory without the surfaces failed before writing anything, leaving all files unchanged.
- Reverting the four files with `git checkout --` restored `0.9.9`/`0.1.0` and left the working tree carrying only the new script.

---

## Transpiler Copies Plugin Version Into Manifest

Change `scripts/migrate_skills_to_agy.py` so the manifest dict it writes to `.agents/plugins/cairn/plugin.json` carries a `version` key read from `.claude-plugin/plugin.json` at generation time, so the generated tree is correct on every regeneration path including a bare standalone `uv run scripts/migrate_skills_to_agy.py`. The milestone needs the generated manifest to carry a version while keeping the source manifest the single source of truth. Verified by regenerating the tree and confirming the generated manifest's `version` equals the source manifest's `0.9.9`, with no other generated file changing.

**Verified:**

- `scripts/migrate_skills_to_agy.py` reads `.claude-plugin/plugin.json` at generation time and copies its `version` value into the dict it writes to `.agents/plugins/cairn/plugin.json`.
- No version literal is hard-coded in the transpiler: a repo-root grep for `[0-9]+\.[0-9]+\.[0-9]+` over the script returns nothing, so the source manifest is the sole source.
- A bare `uv run scripts/migrate_skills_to_agy.py` from the repository root produced a generated manifest whose `version` is `"0.9.9"`, equal to the source manifest's value.
- The generated manifest keeps its existing `$schema`, `name`, and `description` keys unchanged: `git diff` on it shows only the added `version` line.
- After that regeneration `git status --porcelain` listed `.agents/plugins/cairn/plugin.json` as the only changed generated file (alongside the edited script), and a second run added no further changes.
- A source manifest that is missing, unreadable, or carries no `version` value stops the run with a clear error and a non-zero exit before any generated manifest is written, rather than emitting a version-less manifest.
- Pointing the script at a source manifest carrying `3.4.5` produced a generated manifest with `"version": "3.4.5"`, confirming the value is read per run rather than fixed.

---
