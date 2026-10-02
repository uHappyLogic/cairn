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

## Slot Agent Dispatch Wording in Core

Put the host-dependent dispatch wording of `complete-all-tasks` and `provide-alternatives-to-all-open-questions` (the "Use the `Agent` tool with `subagent_type` set to" sentences and the repair branch's reference to the agent id that tool returned) behind named slots whose Claude Code and Antigravity values are today's exact text. The Codex values spawn Codex's default (generic) subagent with a prompt that tells it to read and follow the plugin's agent file by its plugin-root path, followed by the task heading or the Short Title and milestone directory as today; that instructions path is the one value the Codex dispatch prompt adds. Verified by the rebuilt Codex tree's dispatch sites pointing at agent files that pass `dangling-plugin-root`, with `git diff 5305f43 -- hosts/claude hosts/antigravity` empty.

**Verified:**

- `core/skills/complete-all-tasks/SKILL.md` carries the dispatch sentence as `{{COMPLETE_TASK_DISPATCH}}` and opens its dispatch prompt with `{{COMPLETE_TASK_PROMPT_INSTRUCTIONS}}`; `core/skills/provide-alternatives-to-all-open-questions/SKILL.md` carries its dispatch paragraph as `{{ALTERNATIVES_DISPATCH}}`, opens its dispatch prompt with `{{ALTERNATIVES_PROMPT_INSTRUCTIONS}}`, and names the repair branches' tool as `{{AGENT_TOOL}}` (the agent id it returned, and the tool a fresh agent is dispatched with) and the re-dispatched agent as `{{ALTERNATIVES_AGENT}}`; `core/` names no `Agent` tool, `subagent_type`, or `cairn:` registry name any more.
- `scripts/hosts/claude/settings.toml` and `scripts/hosts/antigravity/settings.toml` declare all six slots with today's exact text (the two prompt-instruction slots empty), and `scripts/hosts/codex/settings.toml` declares the Codex values, each slot under a comment explaining it.
- The rebuilt Codex tree's `complete-all-tasks` spawns one default (generic) subagent with the `spawn_agent` tool and no custom agent type, with a prompt that opens `Read and follow the agent instructions in ${PLUGIN_ROOT}/agents/complete-task.md.` followed by the unchanged task-name line; its `provide-alternatives-to-all-open-questions` does the same with `${PLUGIN_ROOT}/agents/provide-alternatives-to-open-question.md` followed by the unchanged Short Title and milestone-directory prompt, states that the instructions path is the one value added to the two the orchestrator already holds, and its repair branches address the agent id the `spawn_agent` tool returned and re-dispatch a fresh default subagent with the same prompt; the Codex tree names no `Agent` tool, `subagent_type`, or `cairn:` registry name.
- Every Codex dispatch-site path resolves to `plugins/cairn/agents/complete-task.md` or `plugins/cairn/agents/provide-alternatives-to-open-question.md`, both present, and `dangling-plugin-root` passes.
- `uv run scripts/build_hosts.py` builds all three hosts and `uv run scripts/build_hosts.py --check` passes (including `slot-declaration` and `unfilled-placeholder`), and `git diff 5305f43 -- hosts/claude hosts/antigravity` is empty.
- `uv run pytest` passes (527 tests).

---

## Slot Alternatives Pass Thread Cap Wording

Put the uncapped all-at-once wording of the dispatch step in `provide-alternatives-to-all-open-questions` behind a named slot that Claude Code and Antigravity fill with today's exact text. The Codex value names an explicit limit: keep at most the session's configured subagent thread cap in flight at once (Codex's `agents.max_threads` setting, or the default value the prose states, taken from Codex's documentation), and as each question's pipeline finishes (embedded and committed, or skipped after its one repair) close its agent and dispatch the next pending question, leaving repair by continuation unaffected. Verified by reading the rebuilt Codex skill's dispatch step and by `git diff 5305f43 -- hosts/claude hosts/antigravity` staying empty.

**Verified:**

- `core/skills/provide-alternatives-to-all-open-questions/SKILL.md` carries step 3's opening paragraph (the uncapped all-at-once dispatch wording) as the single named slot `{{ALTERNATIVES_CONCURRENCY}}`.
- `scripts/hosts/claude/settings.toml` and `scripts/hosts/antigravity/settings.toml` declare `ALTERNATIVES_CONCURRENCY` with today's exact paragraph, and `scripts/hosts/codex/settings.toml` declares the Codex value, each under a comment explaining the slot.
- The rebuilt Codex skill's dispatch step (`hosts/codex/plugins/cairn/skills/provide-alternatives-to-all-open-questions/SKILL.md`, step 3) keeps at most the session's configured subagent thread cap in flight at once, naming the `agents.max_threads` setting (and its newer name `agents.max_concurrent_threads_per_session`) or 6, its default, when unset; as each question's pipeline finishes (embedded and committed, or skipped on an explicit failure or after its one repair) it closes that question's agent with the `close_agent` tool and dispatches the next pending question; it states that an agent is closed only once its pipeline has finished, so repair by continuation still reaches the same agent; it no longer says "no cap".
- `uv run scripts/build_hosts.py` builds all three hosts and `uv run scripts/build_hosts.py --check` passes (including `slot-declaration` and `unfilled-placeholder`), and `git diff 5305f43 -- hosts/claude hosts/antigravity` is empty.
- `uv run pytest` passes (527 tests).

---

## Write Codex Distribution Repository Templates

Add the root-level templates of `scripts/hosts/codex/`: the `CONTRIBUTING.md` pointer, the `.github/workflows/traffic-badges.yml` copy, and a `README.md` that opens with the badge strip the other two host templates share and names the Codex command-line tool as the supported surface, saying nothing about the desktop app or the IDE extension. The README gives the install commands `codex plugin marketplace add uHappyLogic/cairn-codex` then `codex plugin add cairn@cairn` as the only route, the `$cairn:init-milestone-base-workflow` invocation form with a note that the slash names inside the skills refer to the same skills, `AGENTS.md` as the context file, and the sandbox instructions: workspace-write with on-request approval and no `config.toml` change, every git staging or commit step asking for approval because that sandbox keeps `.git` read-only, and the `python3` tools needing only read access to the installed plugin directory. Verified by a rebuild that lands all three files at the root of `hosts/codex/` beside `LICENSE` and passes `--check`.

**Verified:**

- `scripts/hosts/codex/` holds the three root-level templates `README.md`, `CONTRIBUTING.md`, and `.github/workflows/traffic-badges.yml`; the workflow is the other hosts' copy with only its leading comment naming `uHappyLogic/cairn-codex`, and the CONTRIBUTING pointer is the other hosts' pointer naming the Codex distribution.
- The README opens with the two-badge strip in the exact shape the Claude Code and Antigravity templates share, pointing at `uHappyLogic/cairn-codex`'s `traffic-data` branch.
- The README names the Codex command-line tool as the supported surface and mentions neither the desktop app nor the IDE extension.
- The README gives `codex plugin marketplace add uHappyLogic/cairn-codex` then `codex plugin add cairn@cairn` as the only install route.
- The README uses the `$cairn:init-milestone-base-workflow` invocation form and notes that the slash names inside the skills refer to the same skills.
- The README names `AGENTS.md` as the context file (the skills read it, the bootstrap writes there, Codex's `/init` documents the project in it).
- The README's sandbox instructions name workspace-write with the on-request approval policy and no `config.toml` change, say every git staging or commit step asks for approval because that sandbox keeps `.git` read-only, and say the `python3` tools need only read access to the installed plugin directory.
- `uv run scripts/build_hosts.py` lands `README.md`, `CONTRIBUTING.md`, and `.github/workflows/traffic-badges.yml` at the root of `hosts/codex/` beside `LICENSE` (version slot filled), `uv run scripts/build_hosts.py --check` passes, and `git diff 5305f43 -- hosts/claude hosts/antigravity` is empty.

---

## Add Codex Installation to Root README

Add a `### Codex` subsection under `## Installation` in the root `README.md` that repeats the Codex README template's installation section word for word, including its `$cairn:init-milestone-base-workflow` form, so the landing page covers the third host. The adoption table gains no `uHappyLogic/cairn-codex` row in this milestone. Verified by comparing the subsection against `scripts/hosts/codex/README.md` and confirming the adoption table is unchanged.

**Verified:**

- `README.md` has a `### Codex` subsection under `## Installation`, placed after `### Antigravity` and before `### Bootstrap your project`.
- The subsection is byte-identical to the `### Codex` subsection of `scripts/hosts/codex/README.md` (heading through the sandbox paragraph), checked by a Python string comparison of the two slices.
- The subsection carries the `$cairn:init-milestone-base-workflow` form.
- `git diff README.md` removes no line and touches only the `## Installation` section, so the adoption table is unchanged and gains no `uHappyLogic/cairn-codex` row.
- `uv run scripts/build_hosts.py --check` passes.

---

## Add Codex to Issue Form Dropdown

Add `codex` as a third option of the required host dropdown in `.github/ISSUE_TEMPLATE/bug.yml` and name Codex, installed from `cairn-codex` with its manifest at `.codex-plugin/plugin.json`, in the field descriptions that enumerate hosts, so a Codex bug can be reported against the right host. Verified by the file loading as YAML with three host options.

**Verified:**

- `.github/ISSUE_TEMPLATE/bug.yml` loads with `yaml.safe_load`, and its required `host` dropdown has exactly three options in order: `claude`, `antigravity`, `codex`.
- The host dropdown's description names `codex` as Codex, installed from `cairn-codex`, beside the two existing hosts.
- The Cairn version field's description names `.codex-plugin/plugin.json` as the manifest on Codex, beside the Claude Code and Antigravity paths.

---

## Name Codex in Contributing and Security

Change only the sentences that list hosts or repositories: in `CONTRIBUTING.md` (`## Development`) the supported-hosts sentence becomes a three-host sentence, the definition-directory list adds `scripts/hosts/codex/`, the committed-tree list adds `hosts/codex/`, and the distribution-repository sentence adds a `cairn-codex` link; in `SECURITY.md` "both distribution repositories" becomes all three, with a `cairn-codex` link beside the other two. Verified by reading both files and finding no sentence that still enumerates only two hosts or repositories.

**Verified:**

- In `CONTRIBUTING.md` `## Development`, the supported-hosts sentence reads "This project supports Claude Code, Google Antigravity, and Codex from one source."
- The definition-directory list reads `scripts/hosts/claude/`, `scripts/hosts/antigravity/`, and `scripts/hosts/codex/`.
- The committed-tree list in the build validation paragraph reads `hosts/claude/`, `hosts/antigravity/`, and `hosts/codex/`.
- The distribution-repository sentence links [`cairn-codex`](https://github.com/uHappyLogic/cairn-codex) beside `cairn-claude` and `cairn-antigravity`, with `cairn-claude` still named the recommended install source.
- `SECURITY.md` says "all three distribution repositories" and links `cairn-codex` beside `cairn-claude` and `cairn-antigravity`.
- Reading both files, no sentence still enumerates only two hosts or repositories (the remaining "both" and "two" refer to the two pytest runs), and no other sentence changed.
- `uv run scripts/build_hosts.py --check` still passes.

---

## Document Codex Headless Runs in Docs

Extend the "Notation and flags" section of `docs/ways-of-using-cairn.md` so Codex is a third binary: `codex exec '$cairn:<skill>'` is the Codex form of a line, the permission bypass maps to `--dangerously-bypass-approvals-and-sandbox`, `--model` has a counterpart in `-m`, `--effort` has no flag, `--add-dir` exists under the same name, and the `<goal>` rule becomes "no single quote" on Codex lines. The one-line swap rule is extended so a line moves to Codex by changing the binary, dropping `--model` and `--effort`, replacing the permission flag, and rewriting `"/cairn:<skill>"` to `'$cairn:<skill>'`. Verified by reading the section against those points and confirming no chain gained a Codex line and the page names no Codex model id or effort level.

**Verified:**

- The "Notation and flags" section of `docs/ways-of-using-cairn.md` names `codex exec '$cairn:<skill>'` as the Codex form of a line, beside the `claude -p` and `agy -p` forms.
- The permission-flag bullet maps `--dangerously-skip-permissions` to the Codex counterpart `--dangerously-bypass-approvals-and-sandbox`.
- The `--model` bullet gives `-m` as its Codex counterpart.
- The `--effort` bullet states Codex has no effort flag.
- The `--add-dir` bullet states the flag exists on all three hosts under the same name.
- The `<goal>` placeholder rule says no single quote on a Codex line (no double quote stays the rule elsewhere).
- The swap rule moves a line to Codex by changing the binary to `codex exec`, dropping `--model` and `--effort`, replacing the permission flag with `--dangerously-bypass-approvals-and-sandbox`, and rewriting `"/cairn:<skill>"` to `'$cairn:<skill>'`.
- No chain gained a Codex line (`grep -n '^codex' docs/ways-of-using-cairn.md` prints nothing).
- The page names no Codex model id or effort level.

---

## Add Traffic Token Check to Release Skill

Add a check that names no host to the step 2f host loop of `.claude/skills/release-plugin/SKILL.md`: for every distribution repository it runs `gh secret list --repo uHappyLogic/cairn-<host>` and, when the `TRAFFIC_TOKEN` secret is missing, stops and prints the maintainer's instructions without running anything, the same way a missing repository is handled. Those instructions say to extend the one token to the new repository, regenerate it, and re-set the secret in every repository, then after publishing to run the repository's `traffic-badges` workflow once by `workflow_dispatch` and add the repository's row to the root README's adoption table in its own commit, apart from the `Release:` commit; the `CLAUDE.md` Development note changes from three repositories to four. Verified by reading the step for the check, the printed instructions, and the absence of any host name.

**Verified:**

- Step 2f of `.claude/skills/release-plugin/SKILL.md` runs `gh secret list --repo uHappyLogic/cairn-<host>` for every host in the `ls -1 scripts/hosts/` loop whose repository exists, treats the secret as present only when an output line begins with `TRAFFIC_TOKEN`, and counts a missing repository as missing the token too.
- A missing token stops the run after every host is checked, and the skill prints the instructions without running anything they name, the same way and in the same step as the missing-repository commands, which are printed first.
- The printed instructions say to extend the one fine-grained token to the new repository, regenerate it, and re-set the `TRAFFIC_TOKEN` secret in every repository (the monorepo and one `gh secret set` line per host definition).
- The printed instructions say that after publishing the maintainer runs the repository's `traffic-badges` workflow once by `workflow_dispatch` (`gh workflow run traffic-badges.yml --repo uHappyLogic/cairn-<host>`) and then adds its row to the root README's adoption table in its own commit, apart from the `Release:` commit.
- No line added to the release skill names a host (`git diff` added lines contain none of `codex`, `claude`, `antigravity`, `agy`).
- The `CLAUDE.md` Development note reads "a fine-grained PAT on exactly the four repositories".
- `uv run scripts/build_hosts.py --check` passes.

---
