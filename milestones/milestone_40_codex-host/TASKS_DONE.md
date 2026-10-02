# TASKS DONE

## Add Wording Slot Operation to Build

`scripts/build_hosts.py` gains a slot operation: `core/` may carry named placeholder slots in the style of `{{PLUGIN_ROOT}}`, a new settings key holds each host's value for every slot, and one more named check (listed in the docstring's checks, with no pytest tests added) fails when any host declares a slot name that appears nowhere in `core/` or when the set of declared slot names differs between hosts, while a slot a host fails to fill is left to the existing `unfilled-placeholder` check. Both existing definitions declare the new key with no slots yet, so every Codex wording difference in this milestone has one mechanism to ride on. Verified by a passing build with `git diff 5305f43 -- hosts/claude hosts/antigravity` empty, and by a scratch slot that renders per host and trips each of the new check's two failure modes before being removed.

**Verified:**

- `scripts/build_hosts.py` fills named `{{SLOT_NAME}}` placeholders (upper-case letters, digits, underscores) in every rendered `core/` text file from the host's values, in one pass before `{{PLUGIN_ROOT}}` is replaced, so a slot value may carry `{{PLUGIN_ROOT}}` and no other placeholder.
- The settings schema has the new required key `slots` (a TOML table of slot name to string); a definition missing it, or declaring a malformed or reserved (`PLUGIN_ROOT`, `VERSION`, `NAME`) slot name or a non-string value, is refused before any build runs.
- `scripts/hosts/claude/settings.toml` and `scripts/hosts/antigravity/settings.toml` each declare an empty `[slots]` table with a comment explaining the key.
- A new named check, `slot-declaration`, runs on every build and `--check` over all definitions, is listed in the docstring's checks, and fails when a host declares a slot name absent from `core/` or when the declared slot-name sets differ between hosts; a `core/` slot a host does not declare is left in place and is caught by `unfilled-placeholder` (its docstring line says so). No pytest tests were added.
- `uv run scripts/build_hosts.py` passes, `uv run scripts/build_hosts.py --check` passes, and `git diff 5305f43 -- hosts/claude hosts/antigravity` is empty.
- In a scratch copy of the repository, a scratch slot `{{SCRATCH_SLOT}}` in `core/shared/commit-procedure.md` rendered per host (Claude Code's value carrying `{{PLUGIN_ROOT}}` rendered as `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`, Antigravity's as its own wording); a slot declared by both hosts but used nowhere in `core/` failed `slot-declaration` for each host; a slot declared only by Claude Code failed `slot-declaration` for Antigravity (with `unfilled-placeholder` on the unfilled site); after removing the scratch the rendered trees were identical to the committed ones.
- `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest` both pass (527 tests).

---
