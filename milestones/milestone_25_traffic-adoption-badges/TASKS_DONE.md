# TASKS DONE

## Relax Build Placeholder Gate For Expressions

Change the build's `unfilled-placeholder` check in `scripts/build_hosts.py` from any `{{` to a `{{` not immediately preceded by `$` (the lookbehind `(?<!\$)\{\{`), so a GitHub Actions `${{ … }}` expression passes in any rendered file of any host while a bare `{{VERSION}}`, `{{NAME}}`, or `{{PLUGIN_ROOT}}` still fails, and reword the script's docstring and the CLAUDE.md clauses that say no `{{` anywhere to no `{{` outside a `${{` expression. The two distribution workflow templates cannot pass the build without this. Verified when `uv run scripts/build_hosts.py --check` still passes on the unchanged trees, a scratch render containing `${{ secrets.X }}` passes the check, and one containing a bare `{{X}}` fails it.

**Verified:**

- `scripts/build_hosts.py`'s `unfilled-placeholder` check matches with the compiled regex `(?<!\$)\{\{` (`UNFILLED_PLACEHOLDER_RE.search(line)`, a `{{` not immediately preceded by `$`) instead of the substring test `"{{" in line`.
- The check stays one uniform test over every rendered text file of every host — no path-scoped exemption, template escape, or new `settings.toml` key — and no `settings.toml` or template file changed; the change set is `scripts/build_hosts.py` and `CLAUDE.md` only.
- The script docstring's `unfilled-placeholder` line reads no `"{{"` outside a `"${{"` expression anywhere in the tree (with the lookbehind and the pass/fail cases in its parenthetical) rather than no `"{{"` anywhere in the tree.
- Both CLAUDE.md clauses — the `scripts/build_hosts.py` layout entry's "no {{ left anywhere" and the Development section's "no `{{` is left anywhere in the tree" — now read no `{{` left anywhere outside a `${{` expression, each with the lookbehind, the uniform-check statement, and the pass/fail cases in a parenthetical; a grep finds no other CLAUDE.md statement of the old rule.
- `uv run scripts/build_hosts.py --check` exits 0 on the unchanged committed trees ("Check passed: hosts/antigravity/ and hosts/claude/ match a fresh build of core/ at version 1.5.0.").
- A scratch render (a temporary copy of the build inputs with a `.github/workflows/scratch.yml` template under both `scripts/hosts/claude/` and `scripts/hosts/antigravity/` containing `${{ secrets.X }}` and `${{ github.token }}`) built with exit 0 and both rendered files carried the expressions byte-for-byte intact.
- A scratch render whose template carried a bare `{{X}}` aborted with exit 1 and an `unfilled-placeholder` failure naming that line for both hosts; a template `{{PLUGIN_ROOT}}` line and a `core/` file's bare `{{VERSION}}` and `{{NAME}}` each tripped the same failure, and a line mixing `${{ ok }}` with a bare `{{X}}` still failed (the lookbehind is per-occurrence, not per-line).

---

## Author Monorepo Traffic Badges Workflow

Add `.github/workflows/traffic-badges.yml` (`name: traffic-badges`) to the monorepo beside `drift-gate.yml`: a `workflow_dispatch` plus one cron `17 3 * * *` commented as daily at 03:17 UTC, `permissions: {}` with a one-line comment that the job token is unused because the action reads the Traffic API and pushes with `TRAFFIC_TOKEN`, and two steps of `albertoarena/github-traffic-badge` pinned to `56f6f3e0ed586f14440561758b197ca57a38f480` with a `# v1.1.4` comment, one for metric `views-unique` and one for `clones-unique`, each passing `token: ${{ secrets.TRAFFIC_TOKEN }}`, `label` `unique views` / `unique clones`, `color` `3b82f6`, `style` `flat`, and `output` `views-unique.svg` / `clones-unique.svg` written out explicitly, with no leading inert-copy comment. This is the monorepo's one of the three hand-kept copies, and CLAUDE.md's description of `drift-gate.yml` as the only workflow is updated to name it. Verified when the file loads as valid YAML, `actionlint` or an equivalent reports no error, and a grep for `github-traffic-badge@` finds the pinned SHA.

**Verified:**

- `.github/workflows/traffic-badges.yml` exists beside `drift-gate.yml`, its first line is `name: traffic-badges`, and the file carries no leading comment (zero `#`-prefixed lines, no inert-copy header).
- Its triggers are `workflow_dispatch` plus exactly one `schedule` entry, `cron: '17 3 * * *'`, followed on the same line by the comment `# daily at 03:17 UTC`.
- Its permissions block is `permissions: {}` followed on the same line by the one-line comment `# job token unused: the action reads the Traffic API and pushes with TRAFFIC_TOKEN`, and no `contents:` grant appears anywhere in the file.
- The one job `badges` has exactly two steps, each `uses: albertoarena/github-traffic-badge@56f6f3e0ed586f14440561758b197ca57a38f480 # v1.1.4`; the input names `token`, `metric`, `label`, `color`, `style`, and `output` match the action's `action.yml` at that SHA, read via `gh api`.
- Step one passes `token: ${{ secrets.TRAFFIC_TOKEN }}`, `metric: views-unique`, `label: unique views`, `color: 3b82f6`, `style: flat`, `output: views-unique.svg`; step two passes the same `token`, `color`, and `style` with `metric: clones-unique`, `label: unique clones`, `output: clones-unique.svg` — every rendering input written explicitly, none inherited from the action's defaults.
- `CLAUDE.md`'s layout entry for `drift-gate.yml` no longer calls it "the one CI workflow" but "the CI workflow, one of the two workflows under .github/workflows/ (the other is traffic-badges.yml below)", and a new layout entry for `.github/workflows/traffic-badges.yml` describes the monorepo's hand-kept copy (triggers, `permissions: {}`, the pinned SHA, both steps' inputs, the traffic-data branch, the by-hand cross-copy grep); a grep finds no remaining only-workflow claim in `CLAUDE.md`, `README.md`, or `CONTRIBUTING.md`, and the "only automated check" sentence stays true because the traffic workflow is not a check.
- `yaml.safe_load` loads the file: `name` is `traffic-badges`, `on` holds `workflow_dispatch` and the one cron, `permissions` is an empty mapping, and every `with:` value of both steps — `color: 3b82f6` included — is a string.
- `actionlint` 1.7.12 (the prebuilt release binary, since Homebrew is blocked by the Xcode licence) reports no error on `.github/workflows/traffic-badges.yml` (exit 0), as it does on `drift-gate.yml`.
- `grep -n 'github-traffic-badge@' .github/workflows/traffic-badges.yml` finds the pinned SHA `56f6f3e0ed586f14440561758b197ca57a38f480` on both step lines (14 and 22).
- `uv run scripts/build_hosts.py --check` still passes ("Check passed: hosts/antigravity/ and hosts/claude/ match a fresh build of core/ at version 1.5.0."); the change set is `.github/workflows/traffic-badges.yml` and `CLAUDE.md` only, touching neither `core/`, `scripts/hosts/`, nor `hosts/`.

---

## Add Distribution Traffic Workflow Templates

Add `scripts/hosts/claude/.github/workflows/traffic-badges.yml` and `scripts/hosts/antigravity/.github/workflows/traffic-badges.yml`, each identical to the monorepo workflow except for a leading comment stating that it runs only in `uHappyLogic/cairn-<host>` and does nothing in an installed copy, so the existing recursive template rule renders each to the same relative path in `hosts/<host>/` and the next release publishes it; no shared template source is added and neither `settings.toml` changes. Rebuild both host trees and widen CLAUDE.md's host-tree contract that names README.md, CONTRIBUTING.md, and LICENSE as the tree's only non-plugin files to name the workflow beside them. Verified when `uv run scripts/build_hosts.py --check` passes, `hosts/claude/.github/workflows/traffic-badges.yml` and `hosts/antigravity/.github/workflows/traffic-badges.yml` exist with the `${{ secrets.TRAFFIC_TOKEN }}` expression intact, and a grep for `github-traffic-badge@` across all three copies returns the same SHA.

**Verified:**

- `scripts/hosts/claude/.github/workflows/traffic-badges.yml` exists and `diff` against `.github/workflows/traffic-badges.yml` reports only three added leading lines (`0a1,3`): the two-line comment `# This workflow runs only in the uHappyLogic/cairn-claude repository and does nothing in an` / `# installed copy of this plugin.` and one blank line; every other byte is the monorepo workflow's.
- `scripts/hosts/antigravity/.github/workflows/traffic-badges.yml` exists with the same `0a1,3` diff, its comment naming `uHappyLogic/cairn-antigravity`.
- No shared template source was added (no new directory beside `scripts/hosts/`, no new `core/` directory, `scripts/build_hosts.py` untouched) and `git diff --quiet` confirms neither `scripts/hosts/claude/settings.toml` nor `scripts/hosts/antigravity/settings.toml` changed; the working-tree change set is the two templates, the two rendered workflows, and `CLAUDE.md`.
- After `uv run scripts/build_hosts.py` (exit 0, 36 + 37 files), `hosts/claude/.github/workflows/traffic-badges.yml` and `hosts/antigravity/.github/workflows/traffic-badges.yml` exist, each `cmp`-identical to its template (the template carries no `{{VERSION}}`/`{{NAME}}` slot), and a fixed-string grep counts two `token: ${{ secrets.TRAFFIC_TOKEN }}` lines in each — the expression intact, as in the monorepo copy.
- `uv run scripts/build_hosts.py --check` exits 0 ("Check passed: hosts/antigravity/ and hosts/claude/ match a fresh build of core/ at version 1.5.0.").
- `grep -h 'github-traffic-badge@'` over the monorepo workflow and both templates yields six lines carrying one SHA, `56f6f3e0ed586f14440561758b197ca57a38f480`.
- `CLAUDE.md`'s `hosts/<host>/` layout entry now names `.github/workflows/traffic-badges.yml` beside README.md, CONTRIBUTING.md, and the copy of LICENSE as "exactly those four non-plugin files", describing the workflow as that host's hand-kept copy rendered from its `scripts/hosts/<host>/` template, identical to the monorepo's except for the leading inert-in-an-installed-copy comment; the `scripts/hosts/<host>/` layout entry and the Development section's enumeration of each definition's templates name the slot-free workflow template beside the README and CONTRIBUTING pointer, so no CLAUDE.md enumeration of the tree or its templates omits it.

---

## Scope Distribution README Build Claims

Amend five files by hand so every claim about the distribution repositories stays true once a `traffic-data` branch exists: in both distribution README templates scope the generated-do-not-edit note to Every file on `main`, this README included, is rendered …, and append one sentence naming the exception — the repository's only other branch, `traffic-data`, is not built from anything; the traffic workflow this tree carries, which runs only in this repository and never in an installed copy, writes its per-day data file and badge SVGs there daily for the adoption table in the root repository's README, and no release touches it — kept generic about file and workflow names; change the Antigravity template's and the root README's Installation line to since `main` advances only by release snapshots; and scope the two CONTRIBUTING.md pointers' every-file claim the same way, taking nothing more. Rebuild the host trees so the rendered READMEs and CONTRIBUTING files carry the wording. Verified when `uv run scripts/build_hosts.py --check` passes and a grep for `release snapshots` shows only the scoped phrase in both README copies.

**Verified:**

- In both `scripts/hosts/claude/README.md` and `scripts/hosts/antigravity/README.md` the generated-do-not-edit note opens "Every file on `main`, this README included, is rendered from the sources of …" — the claim scoped to the default branch with the rest of that sentence unchanged (`git diff` shows the one-word substitution `in this repository` → `on \`main\`` and nothing else in it).
- Both README templates carry one added sentence, placed directly after the scoped claim and before the Issues sentence, naming the exception: "The repository's only other branch, `traffic-data`, is not built from anything — the traffic workflow this tree carries, which runs only in this repository and never in an installed copy, writes its per-day data file and badge SVGs there daily for the adoption table in the root repository's README, and no release touches it." A grep for `totals.json`, `views-unique`, `clones-unique`, and `traffic-badges` across the five hand-edited files finds nothing, so the sentence names no file and no workflow.
- `scripts/hosts/antigravity/README.md`'s Installation line now reads "since `main` advances only by release snapshots" in place of "since `cairn-antigravity` advances only by release snapshots".
- The root `README.md`'s `### Antigravity` Installation line (line 59) carries the same corrected phrase "since `main` advances only by release snapshots".
- Both `scripts/hosts/claude/CONTRIBUTING.md` and `scripts/hosts/antigravity/CONTRIBUTING.md` read "Every file on `main` is rendered from the sources of …" (one occurrence each), carry no `traffic-data` mention (zero occurrences each), and show no other change in `git diff`.
- The hand-edited change set is exactly the five files named — the two README templates, the two CONTRIBUTING pointers, and the root `README.md` — with `git diff --stat` empty for `core/`, `scripts/build_hosts.py`, both `settings.toml` files, and `.github/`.
- `uv run scripts/build_hosts.py` exits 0 (36 + 37 files) and the four rendered copies — `hosts/claude/README.md`, `hosts/antigravity/README.md`, `hosts/claude/CONTRIBUTING.md`, `hosts/antigravity/CONTRIBUTING.md` — are `cmp`-identical to their templates (the READMEs after filling `{{VERSION}}` with `1.5.0`), so they carry the wording.
- `uv run scripts/build_hosts.py --check` exits 0 ("Check passed: hosts/antigravity/ and hosts/claude/ match a fresh build of core/ at version 1.5.0.").
- `grep -rn 'release snapshots'` over `README.md`, `scripts/hosts/antigravity/README.md`, and `hosts/antigravity/README.md` returns one line per file, each the scoped phrase "since `main` advances only by release snapshots", and a repository-wide grep for the old "`cairn-antigravity` advances" phrase finds nothing.

---

## Extend Token With Contents Write Access

Have the maintainer add Contents: Read and write for `uHappyLogic/cairn`, `cairn-claude`, and `cairn-antigravity` to the existing fine-grained token on its GitHub settings page, keeping the 93-byte value at `temp/PAT` unchanged rather than minting a replacement, because the action's push step needs contents-write access the token lacks as stored (an HTTPS push dry-run is refused with 403 on all three today). Verified when a second HTTPS push dry-run authenticated with `temp/PAT` is accepted on all three repositories and the token still reads `/traffic/views` and `/traffic/clones` on each with HTTP 200.

**Verified:**

- `temp/PAT` is unchanged: 93 bytes, `github_pat_` prefix, last byte `0x34` (no trailing newline) — no replacement token was minted.
- The token still authenticates as `uHappyLogic` (`GET /user` returns HTTP 200 with `login: uHappyLogic`) and the response carries no `github-authentication-token-expiration` header, so its ownership and no-expiration setting stand as recorded.
- The token reads `/repos/uHappyLogic/<repo>/traffic/views` and `/traffic/clones` with HTTP 200 on `cairn`, `cairn-claude`, and `cairn-antigravity` (all six reads 200).
- A second HTTPS push dry-run authenticated with `temp/PAT` — `git push --dry-run https://github.com/uHappyLogic/<repo>.git HEAD:refs/heads/zz-token-dry-run`, the credential supplied as `x-access-token` by an inline helper — is accepted on all three repositories, each reporting `* [new branch] HEAD -> zz-token-dry-run`, where the same dry-run was refused with `403` (`Permission to uHappyLogic/<repo>.git denied to uHappyLogic`) before the grant.
- The dry-run wrote nothing: `gh api repos/uHappyLogic/<repo>/branches` lists only `main` on all three repositories.
- The task changed no file in the repository; its change set is the two task-list files.

---

## Cut Patch Release For Workflow Templates

With every task that changes `hosts/` landed — the build-gate change, the two workflow templates, and the README wording — run `/release-plugin 1.5.1` so the release's empty-range path (no milestone finish since 1.5.0) publishes each rebuilt `hosts/<host>/` tree as a `Release: 1.5.1` commit on `uHappyLogic/cairn-claude` and `uHappyLogic/cairn-antigravity`, the one documented route by which distribution `main` advances; the patch number is right because nothing in the plugin runtime changes for a consumer. Every later task depends on the distribution repositories carrying the workflow. Verified when the `1.5.1` tag exists on all three repositories and `gh api repos/uHappyLogic/cairn-<host>/contents/.github/workflows/traffic-badges.yml` returns the file on both distribution repositories.

**Verified:**

- Every task that changes `hosts/` landed before the release: the four `Tasklist-completion:` commits — `e945bd2` (relax build placeholder gate), `9d15504` (author monorepo workflow), `1f38546` (add distribution workflow templates), `523a5d8` (scope distribution README build claims) — are each ancestors of the `Release: 1.5.1` commit `99b848d`.
- Exactly one `Release: 1.5.1` commit (`99b848d`) sits on `main`, changing only the four version surfaces (`VERSION`, `pyproject.toml`, `uv.lock`, `.claude-plugin/marketplace.json`), `CHANGELOG.md` (12 added lines, no deletions), and the version slots of the four rendered manifests and READMEs under `hosts/` — 10 files; `VERSION` and every rendered manifest at that commit carry `1.5.1`.
- The release took the empty-range path: `git log --grep='^Milestone-finish: ' 1.5.0..99b848d -- milestones/README.md` returns nothing, the nearest tag below `1.5.1` is `1.5.0`, and `CHANGELOG.md` carries exactly one `## 1.5.1 — 2026-09-18` heading, first in the file above `## 1.5.0 — 2026-09-17`, whose body is a `### Changes since 1.5.0` section closing with the `1.5.0...1.5.1` Full Changelog link.
- The `1.5.1` tag exists on all three repositories: on `uHappyLogic/cairn` it resolves to `99b848d` both locally and on `origin` (`origin/main` is at that commit); on `uHappyLogic/cairn-claude` it resolves to `69497f3` and on `uHappyLogic/cairn-antigravity` to `a69fd8e`, in each case the same commit that repository's `main` names.
- Each distribution commit is a `Release: 1.5.1` commit whose tree is byte-identical to the monorepo's `99b848d:hosts/<host>` (`ca6f02d…` for claude, `ba191ba…` for antigravity), with the provenance body `Source: uHappyLogic/cairn@99b848dc457c7c91d8b4a39b7409cd5593fdd900`, `Path: hosts/<host>/`, `Notes: https://github.com/uHappyLogic/cairn/releases/tag/1.5.1`.
- A non-draft GitHub release `1.5.1` exists on `uHappyLogic/cairn`, `uHappyLogic/cairn-claude`, and `uHappyLogic/cairn-antigravity`, each body identical to the committed `CHANGELOG.md` entry.
- `gh api repos/uHappyLogic/cairn-<host>/contents/.github/workflows/traffic-badges.yml` returns HTTP 200 with the file (989 bytes on claude, 994 on antigravity) on both distribution repositories; the decoded content is byte-identical to `hosts/<host>/.github/workflows/traffic-badges.yml` and to its `scripts/hosts/<host>/` template, opens with the inert-copy comment naming `uHappyLogic/cairn-<host>`, carries the pinned SHA `56f6f3e0ed586f14440561758b197ca57a38f480` on both step lines, and holds two intact `token: ${{ secrets.TRAFFIC_TOKEN }}` lines.
- Nothing in the plugin runtime changed for a consumer, so the patch number is right: `git diff --stat 1.5.0 1.5.1 -- hosts/<host>/` touches only the manifests' version slots, `README.md`, `CONTRIBUTING.md`, and the new workflow on each host — zero paths under `skills/`, `agents/`, or `shared/`.
- `uv run scripts/build_hosts.py --check` exits 0 on HEAD ("match a fresh build of core/ at version 1.5.1") and the tracked tree is clean; the release itself was committed and published by the earlier `/release-plugin 1.5.1` run (a re-run would stop at the skill's tag-exists gate, correctly, since a published release is never re-cut), so this completion re-cuts nothing and its change set is the two task-list files only.

---
