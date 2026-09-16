# TASKS TODO

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
