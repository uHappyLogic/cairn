# TASKS TODO

## Add Root VERSION File And Version Script

Create a root `VERSION` file holding the bare `1.4.0` literal and nothing else as the single source of truth for the plugin version, and rewrite `scripts/set_version.py <MAJOR.MINOR.PATCH>` to write `VERSION`, `pyproject.toml`, `uv.lock`, and the root `.claude-plugin/marketplace.json` entry in lockstep (all-or-nothing, as today), never writing any manifest under `hosts/` and no longer treating the root `.claude-plugin/plugin.json` as a surface. Verified by running the script with a throwaway version, confirming exactly those four files change and carry the literal, then restoring `1.4.0`.

---

## Author Claude And Antigravity Host Definitions

Create the declarative host definition directories `scripts/hosts/claude/` and `scripts/hosts/antigravity/`, each holding a settings file — the plugin-root placeholder replacement value (`${CLAUDE_PLUGIN_ROOT}` for Claude Code, `.agents/plugins/cairn` for Antigravity), prose patterns to drop (none), frontmatter keys to strip (`color` for Antigravity, none for Claude Code), output layout and file renames, and excluded paths (no entry for the retired `migrate-workspace` skill) — beside that host's manifest templates with version and name slots: a `.claude-plugin/plugin.json` plus a `.claude-plugin/marketplace.json` with source `"."` and marketplace name `cairn` for Claude Code, and a `plugin.json` with `$schema` `https://antigravity.google/schemas/v1/plugin.json` for Antigravity. Verified when every difference the current `scripts/migrate_skills_to_agy.py` performs is expressed as a settings entry or a template slot under one shared settings shape, with no host-specific Python anywhere.

---

## Author Distribution README Templates

Add a `README.md` template with a version slot to each host definition directory, containing a one-paragraph statement of what the repository is, a generated-do-not-edit notice routing issues and pull requests to `uHappyLogic/cairn`, that host's own install subsection in the exact wording the install-documentation decision fixes (Claude Code: `/plugin marketplace add uHappyLogic/cairn-claude` then `/plugin install cairn@cairn`, with the migration note in `cairn-claude`'s template only; Antigravity: `mkdir -p .agents/plugins/cairn`, `curl -sL` of the `cairn-antigravity` `archive/refs/heads/main.tar.gz` archive piped through `tar -xz --strip-components=1 -C .agents/plugins/cairn`, and one sentence on pinning by swapping `main` for a release tag) followed by `/init-milestone-base-workflow` and `/init`, a pointer to the source repository with the release tag and release URL derived from the version, and a license line naming MIT and pointing at the `LICENSE` file in the same tree. Verified when each template renders to a README whose only per-release change is the version literal and whose install subsection is word-for-word the one the root `README.md` will carry for that host.

---

## Implement Build Script With Validation Gate

Write `scripts/build_hosts.py`, invoked as `uv run scripts/build_hosts.py [<host> ...] [--check]`, which discovers definitions by scanning `scripts/hosts/`, renders each selected host from `core/` into a temporary directory (placeholder substitution, frontmatter-key strips, renames, exclusions, manifest and README templates filled from `VERSION`, and a copy of the root `LICENSE`), runs the full check set — the pre-render guard that `core/` names no host, frontmatter present and `yaml.safe_load`-able with `name` and `description`, every description at or under 25 words, no `{{` anywhere in the tree, no other host's plugin-root literal, every occurrence of the host's own plugin-root literal followed by a path that resolves to a file in that tree, no stripped frontmatter key still present, and every rendered manifest version slot plus the root `marketplace.json` entry carrying exactly the `VERSION` literal — and swaps the results into `hosts/<host>/` only when every selected host passes, otherwise exiting non-zero listing every failing file and check with no tree touched, while `--check` compares the render byte-for-byte against the committed `hosts/<host>/` trees, writes nothing, and exits non-zero listing the differing paths. Verified by building both hosts into committed `hosts/claude/` and `hosts/antigravity/` trees, confirming `--check` then passes, and confirming that a deliberately injected `{{` or host name in a `core/` file aborts the whole build without writing.

---

## Rewrite Release Pre-Flight And Version Steps

Update `.claude/skills/release-plugin/SKILL.md` so its untracked-files pre-flight covers `core/` and `scripts/hosts/` instead of the root trees, a fifth pre-flight gate runs `uv run scripts/build_hosts.py --check` before anything is written and stops on drift listing the differing paths (remedy: rebuild, commit the sync as a standalone commit, re-run), and a per-host pre-flight stop checks that `uHappyLogic/cairn-<host>` exists with `gh repo view` for every `scripts/hosts/<host>/` and, when missing, prints the exact `gh repo create` (public, with a description, no `--license`, `--add-readme`, or `--gitignore`) and `gh repo edit` (topics added; issues, wiki, and projects disabled) commands rather than creating the repository; then rewrite its version step to run `set_version.py`, rebuild with `uv run scripts/build_hosts.py`, stage `VERSION`, `pyproject.toml`, `uv.lock`, `.claude-plugin/marketplace.json`, and `hosts/` path-scoped, and drop the absorbed-drift advisory so the Release commit changes only version slots by construction. Verified by walking the rewritten procedure against the live repository: every command it names exists, and no reference to `.agents/`, `migrate_skills_to_agy.py`, or the root `plugin.json` remains.

---

## Add Distribution Publish Step To Release

Add step 8d to the release skill: after the monorepo `main` push, tag push, and GitHub release are each skipped or done, for each host in `scripts/hosts/` definition order derive the distribution repository `uHappyLogic/cairn-<host>` and remote `git@github.com:uHappyLogic/cairn-<host>.git`, query `git ls-remote --tags` for `refs/tags/<VERSION>`, and when absent fetch distribution `main` into `FETCH_HEAD` (absent on the first publish, making it a parentless root commit), `git commit-tree` the tree `git rev-parse HEAD:hosts/<host>` with `FETCH_HEAD` as sole parent under subject `Release: <VERSION>` and a fixed provenance body (`uHappyLogic/cairn@<SHA>`, path `hosts/<host>/`, the monorepo release URL, never the notes), and push atomically to `refs/heads/main` and `refs/tags/<VERSION>`; when present, compare that tag's tree id against `HEAD:hosts/<host>` and skip on equality or stop reporting both tree ids and the tag's commit SHA without ever moving the tag; then check-then-do a distribution GitHub release with `gh release view <VERSION>` and `gh release create <VERSION> --title <VERSION> --verify-tag --notes-file <BODY_FILE>` reusing step 8c's body file, where an existing non-draft release skips and anything else stops. Verified by rehearsing the plumbing sequence against a throwaway local bare remote (first publish as root commit, second as its child, already-published skip, mismatch stop) and by reading that no clone, temporary directory, or file copy appears in the step.

---

## Create Distribution Repositories

As the once-only maintainer act this milestone records, create `uHappyLogic/cairn-claude` and `uHappyLogic/cairn-antigravity` with the `gh repo create` command the release skill's pre-flight prints — public, with a description, deliberately empty (no `--license`, `--add-readme`, or `--gitignore`) — then run `gh repo edit` on each to add topics and disable issues, wiki, and projects so feedback routes to `uHappyLogic/cairn`. Verified when `gh repo view` succeeds for both, each shows zero commits with issues, wiki, and projects disabled, and the commands run match the ones the pre-flight prints.

---

## Rewrite Install Documentation

Rewrite the Installation section of `README.md` into one subsection per host followed by the shared bootstrap steps — Claude Code: `/plugin marketplace add uHappyLogic/cairn-claude` then `/plugin install cairn@cairn`; Antigravity: `mkdir -p .agents/plugins/cairn`, `curl -sL` of the `cairn-antigravity` `archive/refs/heads/main.tar.gz` archive piped through `tar -xz --strip-components=1 -C .agents/plugins/cairn`, and one sentence on pinning by swapping `main` for a release tag; then `/init-milestone-base-workflow` and `/init` — plus a Claude Code migration note stating that installs pinned to `uHappyLogic/cairn` keep working and updating because that marketplace now serves `./hosts/claude`, and that switching to the recommended source is `/plugin marketplace remove cairn`, `/plugin marketplace add uHappyLogic/cairn-claude`, `/plugin install cairn@cairn`; the monorepo is named as an install source only under Development, as the maintainer's directory-marketplace source. Verified when `cairn-claude` reads as the recommended install source and each per-host subsection matches the corresponding dist README template word for word.

---

## Rewrite Layout Documentation And Stale References

Rewrite the `## Repository layout` block, the `## Development` section, and every invariant in `CLAUDE.md` that references runtime files by root `skills/`, `agents/`, or `shared/` paths, `${CLAUDE_PLUGIN_ROOT}`, the transpiler, or `.agents/plugins/cairn/` so they describe `core/` with `{{PLUGIN_ROOT}}`, the `scripts/hosts/<host>/` definitions, `scripts/build_hosts.py` with its `--check` mode, the committed `hosts/<host>/` trees, the root `VERSION` file, and the two distribution repositories, and rewrite the Development section of `README.md` likewise; in the same edit delete the four stale `migrate-workspace` references (the `README.md` commit-exemption sentence, the two `CLAUDE.md` exemption mentions, and the whole Migration-catalog invariant bullet). Verified when a grep of both files finds no `migrate-workspace`, `migrate_skills_to_agy`, or `.agents/plugins` mention outside historical milestone records and every path the two documents name exists in the repository.

---

## Cut Over To Generated Claude Tree

Repoint the root `.claude-plugin/marketplace.json` entry's `source` from `"."` to `"./hosts/claude"` (the monorepo keeps this hand-held marketplace, still named `cairn`), and in the same change delete the root `skills/`, `agents/`, `shared/`, and `.agents/` trees, the root `.claude-plugin/plugin.json` whose content now lives in the Claude host template, and `scripts/migrate_skills_to_agy.py` outright with no deprecation shim or alias, updating the `pyproject.toml` description that still names the transpiler. This is deliberately the last task, because the running plugin resolves its shared procedures from the root trees until it lands. Verified when `uv run scripts/build_hosts.py --check` still passes, `git ls-files` lists none of the removed paths, and the marketplace entry resolves to `hosts/claude/.claude-plugin/plugin.json`.

---
