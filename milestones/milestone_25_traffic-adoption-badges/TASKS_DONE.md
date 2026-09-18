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

## Store Traffic Token Secret And Delete PAT

Store the value of `temp/PAT` as the `TRAFFIC_TOKEN` repository secret on `uHappyLogic/cairn`, `uHappyLogic/cairn-claude`, and `uHappyLogic/cairn-antigravity` with `gh secret set`, then delete `temp/PAT` so the token exists only in GitHub's write-only secret store, recording the deletion in this task's `TASKS_DONE.md` entry because `temp/` is gitignored and nothing in git would otherwise record it. Verified when `gh secret list` on each of the three repositories shows `TRAFFIC_TOKEN` and `test ! -e temp/PAT` succeeds.

**Verified:**

- Pre-store identity: `temp/PAT` was the token the prior task verified and no replacement was minted — 93 bytes, `github_pat_` prefix, last byte `0x34`, no trailing newline — and it still authenticated as `uHappyLogic` (`GET /user` returned HTTP 200 with `login: uHappyLogic`) immediately before it was stored.
- The secret name is the one the workflows read: the three `traffic-badges.yml` copies (`.github/workflows/`, `hosts/claude/.github/workflows/`, `hosts/antigravity/.github/workflows/`) and their two `scripts/hosts/<host>/` templates each carry two `token: ${{ secrets.TRAFFIC_TOKEN }}` lines, so `TRAFFIC_TOKEN` is the name stored.
- `gh secret set TRAFFIC_TOKEN --app actions -R uHappyLogic/<repo> < temp/PAT` ran once per repository with the file's own bytes on stdin (never retyped or copied), exiting 0 on `cairn`, `cairn-claude`, and `cairn-antigravity`, so the stored value is exactly the verified 93-byte token.
- `gh secret list --app actions -R uHappyLogic/<repo>` shows `TRAFFIC_TOKEN` on all three repositories, and `gh api repos/uHappyLogic/<repo>/actions/secrets/TRAFFIC_TOKEN` returns it as an Actions repository secret created 2026-09-18T14:45:06Z (`cairn`), 14:45:07Z (`cairn-claude`), and 14:45:08Z (`cairn-antigravity`).
- `temp/PAT` was removed (`rm temp/PAT`) only after that listing held on all three, and `test ! -e temp/PAT` succeeds.
- No second store: immediately before the deletion, a fixed-string search over the whole working tree (gitignored files included, `.git/` searched separately) found the token value in `temp/PAT` and nowhere else, and the task wrote it to no other file, so from the deletion on the token exists only in GitHub's write-only secret store, recoverable only by regenerating it on its settings page and re-setting all three repositories.
- The deletion of `temp/PAT` is recorded here, in this entry, because `temp/` is gitignored and nothing in git would otherwise record it.
- The task changed no tracked file (`git status --porcelain` was empty before the task-list move; `uv run scripts/build_hosts.py --check` passes at 1.5.1), so its change set is the two task-list files only.

---

## Seed Traffic Data Branches Via Dispatch

Trigger one `workflow_dispatch` run of `traffic-badges.yml` on each of the three repositories with `gh workflow run`, wait for each run to succeed, and confirm each repository now has a `traffic-data` branch carrying `totals.json`, `views-unique.svg`, and `clones-unique.svg`, so every badge URL resolves before the README references it. Read the earliest date recorded in each branch's `totals.json` and note it in the `TASKS_DONE.md` entry, since the adoption caption's start date is read off the seeded branches. Verified when `gh run list` shows a successful run per repository and `curl` on each of the six `https://raw.githubusercontent.com/uHappyLogic/<repo>/traffic-data/<output>` badge URLs returns HTTP 200.

**Verified:**

- Pre-flight held on the live deliverables of the prior tasks before anything was dispatched: `gh secret list --app actions -R uHappyLogic/<repo>` listed `TRAFFIC_TOKEN` (stored 2026-09-18T14:45:06–08Z) on `cairn`, `cairn-claude`, and `cairn-antigravity`; `gh workflow list` showed `traffic-badges` as `active` on all three; and `gh api repos/uHappyLogic/<repo>/branches` listed only `main` on each — the earlier `workflow_dispatch` runs of 14:26–14:38Z (two on `cairn`, one on each distribution repository) had all failed with an empty `INPUT_TOKEN` (`GitHub API 401 Unauthorized` on `/traffic/views`, the secret not yet existing) and their commit-and-push step was skipped, so no `traffic-data` branch existed.
- One `workflow_dispatch` run of `traffic-badges.yml` was triggered per repository with `gh workflow run traffic-badges.yml -R uHappyLogic/<repo> --ref main` at 14:47:54Z: run 35358466324 on `cairn` (at `main` = `99b848d`, the pushed `Release: 1.5.1` tip, whose workflow copy is byte-identical to HEAD's), 35358469558 on `cairn-claude` (`69497f3`), and 35358472204 on `cairn-antigravity` (`a69fd8e`).
- Each run was waited on (`gh run watch --exit-status`) and concluded `success`: `gh run list -R uHappyLogic/<repo> --workflow traffic-badges.yml` shows for each repository exactly one run created at or after 14:47:54Z, `event: workflow_dispatch`, `status: completed`, `conclusion: success`, on `headBranch: main`.
- Each repository now has a `traffic-data` branch: `gh api repos/uHappyLogic/<repo>/branches` lists `main` and `traffic-data` on all three, and `gh api "repos/uHappyLogic/<repo>/contents?ref=traffic-data"` returns exactly the three files `totals.json`, `views-unique.svg`, and `clones-unique.svg` on each, written by two `github-actions[bot]` commits `chore: update traffic badge` (one per step, 14:48:02–09Z).
- `curl` on each of the six badge URLs `https://raw.githubusercontent.com/uHappyLogic/<repo>/traffic-data/<output>` (`views-unique.svg` and `clones-unique.svg` on `cairn`, `cairn-claude`, `cairn-antigravity`) returns HTTP 200 with `content-type: image/svg+xml`; each SVG renders its step's label (`unique views` / `unique clones`) and a total equal to the sum of per-day `uniques` in its branch's `totals.json` — `cairn` 18 views / 115 clones, `cairn-claude` 3 / 9, `cairn-antigravity` 3 / 4.
- The earliest date recorded in each branch's `totals.json` is **2026-09-04** on all three repositories (`cairn`, `cairn-claude`, and `cairn-antigravity` alike): every seed holds the same 14 days, `2026-09-04` through `2026-09-17`, in both its `views` and `clones` maps (`schema: 1`, `updatedAt` 2026-09-18T14:48:04–09Z), so the three seeds share one start date and the adoption caption needs no second parenthesised date.
- The task changed no tracked file (`git status --porcelain` was empty after the runs and `uv run scripts/build_hosts.py --check` passes at 1.5.1); every change it made lives on GitHub, and its change set is the two task-list files only.

---

## Add README Adoption Table Section

Insert a `## Adoption` section into `README.md` after `## Skill reference` and before `## Contributing`, holding a GitHub-flavoured pipe table with header row repository | unique views | unique clones and one row per repository labelled with its full `uHappyLogic/<repo>` name as a link to the repository, each badge cell a Markdown image at the badge's raw `traffic-data` URL with its column name as alt text wrapped in a link to that repository's `traffic-data` branch page, followed by a caption paragraph stating that counts are cumulative since the earliest day in each `traffic-data` branch's `totals.json` written as a date (a second date in parentheses for the distribution rows when theirs differs), that a unique count is the sum of each day's unique visitors or cloners so a visitor returning on another day counts again, that clone counts include the badge workflow's own daily fetch of the traffic-data branch (one unique clone and two clones per repository per day), and that the monorepo's additionally include CI checkouts; the page's opening banner, badge block, title, pitch, and install sections stay exactly as they are. Verified when the section sits between those two headings, every badge image URL and every link in the table returns HTTP 200, and the caption carries the date and all three caveats.

**Verified:**

- `README.md` carries exactly one `## Adoption` heading, and in the file's `##` heading sequence it sits immediately after `## Skill reference` (following its last entry, `goto-next-milestone`) and immediately before `## Contributing`.
- Under `## Adoption` is a GitHub-flavoured Markdown pipe table whose header row is `| repository | unique views | unique clones |` over a `| --- | --- | --- |` delimiter row, with exactly three body rows in the order `uHappyLogic/cairn`, `uHappyLogic/cairn-claude`, `uHappyLogic/cairn-antigravity`.
- Each row's first cell is the full `uHappyLogic/<repo>` name as a Markdown link to `https://github.com/uHappyLogic/<repo>`; no short name is used.
- Each badge cell is the Markdown image `![unique views](…)` / `![unique clones](…)` — alt text equal to its column name — at `https://raw.githubusercontent.com/uHappyLogic/<repo>/traffic-data/views-unique.svg` / `clones-unique.svg` (the output names the seeded branches carry), wrapped in a link to `https://github.com/uHappyLogic/<repo>/tree/traffic-data`; all six badges are linked, and none links to a workflow-runs page.
- The paragraph immediately following the table is the caption, and it states (a) counts are cumulative since 2026-09-04, the earliest day in each `traffic-data` branch's `totals.json` — one date and no parenthesised second, because the live `totals.json` on all three branches was re-read and each begins on 2026-09-04 (14 days through 2026-09-17); (b) a unique count is the sum of each day's unique visitors or cloners, so a visitor returning on another day counts again; (c) clone counts include the badge workflow's own daily fetch of the `traffic-data` branch (one unique clone and two clones per repository per day); (d) the monorepo's additionally include CI checkouts.
- `git diff --numstat README.md` is 10 insertions and 0 deletions, and everything from the file's first byte through the `## Skill reference` heading is byte-identical to `HEAD:README.md`, so the opening banner, badge block, `---` rule, `# Cairn` title, pitch, and `## Installation` sections stay exactly as they were.
- Every URL in the table returns HTTP 200 to `curl -L`: the three repository links, the three `tree/traffic-data` branch links (`text/html`), and the six badge image URLs (`image/svg+xml`).
- `uv run scripts/build_hosts.py --check` passes at 1.5.1 (the root README is hand-authored, not a build input, and the committed host trees still match a fresh build).

---
