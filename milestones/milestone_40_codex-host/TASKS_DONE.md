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

## Add Plugin Directory Key to Build

`scripts/build_hosts.py` gains one more required settings key, `plugin_dir`: the path from the host tree's root to the directory that `plugin_root` stands for at runtime, declared as the empty string by the Claude Code and Antigravity definitions. The `dangling-plugin-root` check resolves each plugin-root reference against the tree's `plugin_dir` instead of the tree root, definition validation fails when any `[layout]` value falls outside `plugin_dir`, and the check's docstring line and the settings comment explain the key, so a Codex tree whose plugin sits under `plugins/cairn` is checked exactly as strictly as the other two. Verified by a passing build with `git diff 5305f43 -- hosts/claude hosts/antigravity` empty, and by a scratch definition showing a reference resolved under a non-empty `plugin_dir` and a layout value outside it refused.

**Verified:**

- `SETTINGS_SCHEMA` in `scripts/build_hosts.py` carries the new required string key `plugin_dir`; a definition missing it is refused (`is missing the key(s) plugin_dir`, exit 2), unknown keys are still refused, and a `plugin_dir` that is absolute or escapes the tree is refused.
- `scripts/hosts/claude/settings.toml` and `scripts/hosts/antigravity/settings.toml` each declare `plugin_dir = ""` under a comment explaining the key (the path from the tree root to the directory `plugin_root` stands for, the check resolving against it, layout values having to lie inside it, other paths staying tree-root relative).
- The `dangling-plugin-root` check resolves each plugin-root reference against the tree's `plugin_dir` instead of the tree root, otherwise unchanged; rendering code is untouched.
- Definition validation refuses any `[layout]` value outside `plugin_dir` (`layout.<key> is ..., outside plugin_dir ...`, exit 2).
- The module docstring names `plugin_dir` among the settings and explains it, and the `dangling-plugin-root` docstring line states that references resolve against `plugin_dir`.
- `uv run scripts/build_hosts.py` and `uv run scripts/build_hosts.py --check` pass, and `git diff 5305f43 -- hosts/claude hosts/antigravity` is empty.
- In a scratch copy of the repository, a scratch definition with `plugin_dir = "plugins/cairn"` and its layout under `plugins/cairn/` built cleanly with its plugin-root references resolved under `plugins/cairn/`; with `plugin_dir = "plugins"` the same references failed `dangling-plugin-root`; a layout value `tools = "tools"` outside `plugins/cairn` was refused; the scratch copy was then deleted.
- `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest` both pass (527 tests).

---

## Create Codex Host Definition and Tree

Add `scripts/hosts/codex/`: a `settings.toml` with `plugin_root` set to `${PLUGIN_ROOT}`, `plugin_dir` set to `plugins/cairn`, and a `[layout]` mapping all four `core/` directories under `plugins/cairn/`; the manifest template at `scripts/hosts/codex/plugins/cairn/.codex-plugin/plugin.json`; and a `.agents/plugins/marketplace.json` template with marketplace name `cairn` and one `cairn` entry whose `source` is `{"source": "local", "path": "./plugins/cairn"}`. Commit the rebuilt `hosts/codex/` tree, which is the installable Codex plugin every later task builds on: its agents stay the Markdown files `core/` holds, with no TOML file and no format conversion, and there is no `plugin.json` at the tree root or the plugin root. Verified by a build and `--check` passing over all three hosts with `git diff 5305f43 -- hosts/claude hosts/antigravity` empty.

**Verified:**

- `scripts/hosts/codex/settings.toml` carries the full key set of the other two definitions, with `plugin_name = "cairn"`, `plugin_root = "${PLUGIN_ROOT}"`, `plugin_dir = "plugins/cairn"`, an empty `[slots]` table, and a `[layout]` mapping `skills`, `agents`, `shared`, and `tools` to `plugins/cairn/<dir>`; the build accepts it as a valid definition.
- The manifest template sits at `scripts/hosts/codex/plugins/cairn/.codex-plugin/plugin.json` (name `{{NAME}}`, version `{{VERSION}}`, the shared description, author, and `skills` pointing at `./skills/`) and renders to `hosts/codex/plugins/cairn/.codex-plugin/plugin.json`, which parses as JSON with version `1.7.6`.
- The marketplace template sits at `scripts/hosts/codex/.agents/plugins/marketplace.json` with marketplace name `cairn` and exactly one plugin entry named `cairn` (from `{{NAME}}`) whose `source` is `{"source": "local", "path": "./plugins/cairn"}`, with the `policy` and `category` fields the curated marketplace's entries carry; it renders to `hosts/codex/.agents/plugins/marketplace.json` and parses as JSON.
- `hosts/codex/` holds the rendered tree: `LICENSE` and `.agents/plugins/marketplace.json` at its root, and the 22 skills, 2 agents, 8 shared procedures, 2 tools, and `.codex-plugin/plugin.json` under `plugins/cairn/` (37 files).
- The two agents under `hosts/codex/plugins/cairn/agents/` are the Markdown files `core/agents/` holds, differing only by `{{PLUGIN_ROOT}}` rendered as `${PLUGIN_ROOT}` and the stripped Claude-only `color` key; the tree holds no `.toml` file.
- There is no `plugin.json` at `hosts/codex/plugin.json` or `hosts/codex/plugins/cairn/plugin.json`.
- The Codex tree carries neither other host's plugin-root literal, and every `${PLUGIN_ROOT}/…` reference resolves under `plugins/cairn/` (`foreign-plugin-root` and `dangling-plugin-root` pass).
- `uv run scripts/build_hosts.py` builds all three hosts, `uv run scripts/build_hosts.py --check` passes over `hosts/antigravity/`, `hosts/claude/`, and `hosts/codex/`, and `git diff 5305f43 -- hosts/claude hosts/antigravity` is empty.

---

## Slot Context File Name in Core

Replace every mention of `CLAUDE.md` in `core/` with a named slot whose value is `CLAUDE.md` for Claude Code and Antigravity and `AGENTS.md` for Codex, so the Codex tree's skills and `complete-procedure.md` read `AGENTS.md` for environment context, its bootstrap creates `AGENTS.md` or appends the Milestone Workflow section to it and points at `/init`, and its `finish-current-milestone` updates `AGENTS.md`. Verified by the rebuilt `hosts/codex/` tree naming `CLAUDE.md` nowhere and `git diff 5305f43 -- hosts/claude hosts/antigravity` staying empty.

**Verified:**

- Every one of the 35 `CLAUDE.md` mentions across the ten `core/` files (`shared/complete-procedure.md` and the skills `ask-in-milestone-context`, `define-milestone-goal`, `derive-tasks`, `discuss-milestone-goal`, `discuss-new-task`, `finish-current-milestone`, `goto-next-milestone`, `init-milestone-base-workflow`, `specify-milestone-starting-state`) is replaced by the named slot `{{CONTEXT_FILE}}`; `core/` names `CLAUDE.md` nowhere, and the two frontmatter descriptions carrying the slot still load with `yaml.safe_load`.
- `scripts/hosts/claude/settings.toml` and `scripts/hosts/antigravity/settings.toml` declare `CONTEXT_FILE = "CLAUDE.md"` and `scripts/hosts/codex/settings.toml` declares `CONTEXT_FILE = "AGENTS.md"` in their `[slots]` tables, each under a comment explaining the slot.
- The rebuilt `hosts/codex/` tree names `CLAUDE.md` nowhere (`grep -rn CLAUDE hosts/codex` finds nothing) and carries the 35 `AGENTS.md` mentions: its `complete-procedure.md`, `derive-tasks`, `specify-milestone-starting-state`, `discuss-milestone-goal`, `discuss-new-task`, and `ask-in-milestone-context` read `AGENTS.md` for environment context; its `init-milestone-base-workflow` creates `AGENTS.md` (headed `# AGENTS.md`) or appends the `## Milestone Workflow` section to it and names an `AGENTS.md` written by `/init`; its `finish-current-milestone` updates `AGENTS.md`.
- `uv run scripts/build_hosts.py` builds all three hosts and `uv run scripts/build_hosts.py --check` passes (including `slot-declaration` and `unfilled-placeholder`), and `git diff 5305f43 -- hosts/claude hosts/antigravity` is empty.
- `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest` both pass (527 tests).

---
