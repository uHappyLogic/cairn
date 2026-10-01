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

### Codex install route

The `uHappyLogic/cairn-codex` distribution repository is a marketplace whose plugin sits in a subdirectory, the layout Codex's curated marketplace uses. The repository root holds `.agents/plugins/marketplace.json` (marketplace name `cairn`) with one `cairn` entry whose `source` is `{"source": "local", "path": "./plugins/cairn"}`. The Codex host definition's `[layout]` maps all four `core/` directories, and the manifest, under `plugins/cairn/`, so the plugin root is `plugins/cairn/` and the manifest lands at `plugins/cairn/.codex-plugin/plugin.json`; README, CONTRIBUTING, LICENSE and the traffic workflow stay at the repository root. Users install at user level with `codex plugin marketplace add uHappyLogic/cairn-codex`, then `codex plugin add cairn@cairn`, and no other install route is documented. This copies the only marketplace layout Codex has been seen to load, so the install rests on no unproven self-referencing source path, at the cost of one extra directory level.

### Supported Codex surfaces

The README and the distribution repository name the Codex command-line tool as the supported surface and say nothing about the desktop app or the IDE extension, neither claiming nor ruling them out. Every word of the support claim is then backed by the milestone's live verification and matches the CLI-shaped install commands.

### Codex sandbox requirements

Interactive sessions run under Codex's workspace-write sandbox with the on-request approval policy, and nothing in `config.toml` changes. The Codex instructions name that configuration, say that every git staging or commit step a skill takes will ask for approval because this sandbox keeps the project's `.git` directory read-only, and say that the plugin's `python3` tools need only read access to the installed plugin directory. Headless `codex exec` runs carry `--dangerously-bypass-approvals-and-sandbox`, the Codex counterpart of the `--dangerously-skip-permissions` flag the other hosts' headless lines already use. This keeps Codex's protections in interactive use, explains the one prompt a sandboxed user will always meet, and rests on no unverified reviewer or permissions profile.

### Existing-host preservation bar

The bar is strict identity. Measured against the trees as released at `Release: 1.7.6` (5305f43), the milestone leaves every file under `hosts/claude/` and `hosts/antigravity/` byte-identical: `git diff 5305f43 -- hosts/claude hosts/antigravity` is empty at the end of the milestone, apart from the version slots a later release commit writes. No other evidence is needed, because identical text cannot change behaviour. Any change to `core/` or the build must render to the same bytes for those two hosts, so every Codex difference reaches only the Codex tree.

### Unverified behaviour probes

The unverified Codex behaviours are settled as far as possible without a model call, before the decisions that depend on them: from the openai/codex source at the installed 0.159.3 version, and from Codex CLI subcommands that call no model (`codex plugin marketplace add` and `codex plugin add` on a fixture, `codex plugin list`, and `codex debug prompt-input`, which renders the model-visible prompt input and so shows how installed plugin skills and agents are presented). The findings go into the starting state. The goal's end-of-milestone verification run is the only live session; the runtime-only behaviours that non-model evidence cannot settle (whether a finished subagent accepts a follow-up message, how a model resolves a spawn by name) stay unconfirmed until that run, and the design avoids leaning on them.

### Quota exhaustion fallback

If the free-tier limit stops the live verification partway, the milestone stays open and nothing is finished or released while any of the four checks (the plugin install, the inline skill, and one dispatch of each agent) is still unrun. Evidence from the checks that already passed is kept as valid. When the limit resets, verification picks up at the first unrun check, and this repeats until all four have passed.

### Traffic token extension

The release skill gets a check in its step 2f host loop that names no host: for every distribution repository it checks that a `TRAFFIC_TOKEN` secret exists, using `gh secret list --repo uHappyLogic/cairn-<host>`. If the secret is missing, the skill stops and prints the maintainer's instructions without running anything, the same way it already handles a missing repository; those instructions say to extend the one token to the new repository, regenerate it, and re-set the secret in every repository. The step itself happens at the first Codex release, not inside the milestone, and the milestone's task list holds no task for it. The `CLAUDE.md` Development note changes from three repositories to four.

## Out of Scope

