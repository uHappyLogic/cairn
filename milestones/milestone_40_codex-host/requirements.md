# Milestone 40: Codex host

## Goal

Add Codex as a third supported host: a `scripts/hosts/codex/` definition that renders `core/` into a committed `hosts/codex/` tree installable as a Codex plugin, with the whole pipeline working there, including both dispatched agents running as Codex subagents. `core/` and the build may change where Codex requires it, provided the Claude Code and Antigravity trees keep their behaviour. The milestone ends release-ready across the full surface (the `uHappyLogic/cairn-codex` distribution repository, its README, CONTRIBUTING and traffic-workflow templates, the root README install section, the issue-form host dropdown, the release skill, and Codex coverage in `docs/`) and is verified by a small live Codex run sized for a free-tier account: plugin install, one inline skill, and one dispatch of each agent.

## Relevant starting state

### Host definitions and the build

Two host definitions exist, `scripts/hosts/claude/` and `scripts/hosts/antigravity/`, each a `settings.toml` beside template files (`README.md`, `CONTRIBUTING.md`, `.github/workflows/traffic-badges.yml`, and the host's manifest: `.claude-plugin/plugin.json` plus `.claude-plugin/marketplace.json` for Claude Code, a root `plugin.json` for Antigravity). `scripts/build_hosts.py` discovers hosts by scanning that directory and holds no host-specific code. Its settings key set is fixed (`plugin_name`, `plugin_root`, `prose_drop_patterns`, `strip_frontmatter_keys`, `renames`, `exclude`, `[layout]`), and a missing or unknown key is a build error. Rendering copies every `core/` file to its layout path with three text operations only (replace `{{PLUGIN_ROOT}}` with the host's literal, delete regex matches, strip frontmatter keys), then renders templates filling only `{{VERSION}}` and `{{NAME}}`; it cannot convert a file's format or generate a file from another. The `host-name-in-core` check forbids every definition directory name as its own word anywhere in `core/`; the word `codex` occurs nowhere in `core/` today. No test under `tests/` covers the build script.

### Committed host trees

`hosts/claude/` and `hosts/antigravity/` are build output with the same four directories (`skills/` with 22 skills, `agents/` with 2 agents, `shared/` with 8 procedures, `tools/` with 2 Python tools) plus the rendered templates and `LICENSE`. They differ in the plugin-root literal (`${CLAUDE_PLUGIN_ROOT}` against the workspace-relative `.agents/plugins/cairn`), the manifest files, and the agents' `color` key, which the Antigravity definition strips. The root `.claude-plugin/marketplace.json` points at `./hosts/claude` and is the only marketplace file the build validates outside a host tree.

### Dispatched agents and their dispatch sites

`core/agents/complete-task.md` and `core/agents/provide-alternatives-to-open-question.md` are Markdown files with YAML frontmatter (`name`, `description`, `color`) whose body is the agent's instructions. Two skills dispatch them: `complete-all-tasks` (one agent per task, sequential, judged by a last-line `DONE`/`FAILED` token) and `provide-alternatives-to-all-open-questions` (one read-only agent per question, in parallel where the host can and sequentially where it cannot, with one repair that continues the same agent session where the host can and re-dispatches a fresh agent where it cannot). Both sites instruct the runner to "Use the `Agent` tool with `subagent_type` set to" the namespaced registry name `cairn:<agent>`, and the repair branch refers to "the agent id the `Agent` tool returned". Both agents call the tools through `{{PLUGIN_ROOT}}` paths, and `complete-task` reads `{{PLUGIN_ROOT}}/shared/complete-procedure.md`.

### Host-facing wording in `core/`

Ten `core/` files name `CLAUDE.md` (35 mentions) as the project's environment-context file: skills and `complete-procedure.md` read it for the environment, `finish-current-milestone` updates it for lasting changes, and `init-milestone-base-workflow` creates it or appends the `## Milestone Workflow` section to it and tells the user to run `/init` to fill it. Skills refer to each other and to themselves in the `/skill-name` slash form throughout. `complete-procedure.md` and `specify-milestone-starting-state` name the tools `Read`, `Edit`, and `Bash`. Every tool call is written as `python3 {{PLUGIN_ROOT}}/tools/<tool>.py …`, and shared procedures are referenced as `{{PLUGIN_ROOT}}/shared/<name>.md`.

### Distribution repositories, traffic workflow, and the release skill

`uHappyLogic/cairn-claude` and `uHappyLogic/cairn-antigravity` exist; `uHappyLogic/cairn-codex` does not (`gh repo view` fails to resolve it). `.claude/skills/release-plugin/SKILL.md` enumerates hosts with `ls -1 scripts/hosts/` and derives each distribution repository as `uHappyLogic/cairn-<host>`, so its pre-flight (step 2f) and publish (step 8d) loops name no host; for a missing repository it stops and prints the `gh repo create` and `gh repo edit` commands. The traffic-badge workflow is three hand-kept copies (the root one and one template per host) that differ only in the leading comment naming their repository, and each pushes with a `TRAFFIC_TOKEN` secret that is a fine-grained token scoped to exactly the three existing repositories. Each host README template opens with that repository's two traffic badges and carries a host-specific installation section that the root README's subsection repeats word for word.

### Root surfaces that enumerate hosts

`README.md` lists three repositories in its adoption table and has `### Claude Code` and `### Antigravity` subsections under `## Installation`, followed by a shared bootstrap step that names `/init` and `CLAUDE.md`. `.github/ISSUE_TEMPLATE/bug.yml` has a required host dropdown with the options `claude` and `antigravity` and a description naming both. `CONTRIBUTING.md` (`## Development`) and `SECURITY.md` each say "both" hosts or repositories and name the two. `docs/ways-of-using-cairn.md` documents headless runs as `claude -p "/cairn:<skill>"` or `agy -p "/cairn:<skill>"`, explains each flag per host, and describes a one-line host swap between those two binaries; `docs/skill-reference.md` mentions hosts only by capability.

### Codex on this machine

`codex-cli 0.159.3` is installed at `~/.local/bin/codex`, which is on the login-shell PATH but not on a non-login shell's. The account is free tier, so live model runs are a scarce resource; everything below was read from `--help` output and local files with no model call. `codex features list` reports `plugins`, `multi_agent`, `skill_search`, and `hooks` as stable and enabled, and `multi_agent_v2` as stable and disabled. The CLI has `codex plugin marketplace add <SOURCE>` (a local path, `owner/repo[@ref]`, or a Git URL), `codex plugin add <PLUGIN>@<MARKETPLACE>`, and `codex exec [PROMPT]` for non-interactive runs with `-m/--model`, `-s/--sandbox`, `-C/--cd`, `--add-dir`, `--skip-git-repo-check`, and `--dangerously-bypass-approvals-and-sandbox`; it has no `-p` prompt flag (`-p` selects a config profile) and no `--effort` flag. No plugin is installed, the only configured marketplace is `openai-curated`, and neither `~/.codex/agents/` nor `~/.agents/` exists.

### How shipped Codex plugins are laid out

The locally cached `openai-curated` marketplace (62 plugins under `~/.codex/.tmp/plugins/`) declares itself in `.agents/plugins/marketplace.json`, with each entry's `source` an object (`{"source": "local", "path": "./plugins/<name>"}`) and a `policy` block. Every one of its plugins keeps its manifest at `.codex-plugin/plugin.json`, none at the plugin root; the manifests carry `name`, `version`, and `description`, 45 of them point `skills` at `./skills/`, and none declares a non-null `agents` key. Twelve plugins have an `agents/` directory, typically holding an `openai.yaml` interface file; three of them also hold Markdown agent files (9 in total, of which one plugin's 3 carry `name`/`description` frontmatter), and no plugin ships a TOML agent file. Their skills reference bundled files as `$PLUGIN_ROOT/skills/…` in shell commands (16 occurrences) or with prose placeholders such as `<plugin-root>` (about 40).

### What Codex's documentation states

Fetched on 2026-10-01 and not confirmed by a live run. The plugin build page describes a root `plugin.json` as the portable manifest with `.codex-plugin/plugin.json` as a compatibility fallback, a `skills/` directory discovered without per-skill manifest entries, and the environment variables `PLUGIN_ROOT` (with `CLAUDE_PLUGIN_ROOT` as a legacy alias) pointing at the installed plugin root. The skills page requires `name` and `description` in `SKILL.md` frontmatter, lists `.agents/skills` directories as the repository and user discovery locations, and gives `$skillname` or `/skills` as the explicit invocation in the CLI. The subagents page defines custom agents as TOML files in `~/.codex/agents/` or the project's `.codex/agents/` with `name`, `description`, and `developer_instructions`, says subagents run in parallel under a configurable thread cap, and does not say whether a plugin can ship custom agents or whether a finished subagent thread accepts a follow-up message. Codex reads `AGENTS.md` as its project instruction file; this repository's `AGENTS.md` is a symlink to `CLAUDE.md`.

### Known gaps

There is no `scripts/hosts/codex/` definition, no `hosts/codex/` tree, and no `uHappyLogic/cairn-codex` repository. The build has no way to emit an agent in a format other than the Markdown file `core/` holds. Whether Codex resolves a plugin-shipped agent by a `cairn:<agent>` name, exposes `PLUGIN_ROOT` to the commands a skill runs, or accepts `/cairn:<skill>` as an invocation is not established by anything on this machine.

## Decisions

### Codex manifest location

The Codex tree keeps its manifest only at `.codex-plugin/plugin.json`, a template at `scripts/hosts/codex/.codex-plugin/plugin.json` rendered to the same relative path the way the Claude Code host renders `.claude-plugin/plugin.json`. The tree has no `plugin.json` at its root. This is the only location shipped Codex plugins are seen to use and the one the installed binary names in every manifest lookup, it needs no build change, and if Codex ever retires the path the move is one template file.

## Out of Scope

