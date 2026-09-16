# TASKS DONE

## Configure Root Repository Settings

Flip the four repository settings on `uHappyLogic/cairn` that the milestone's decisions state as fact: enable Discussions (`has_discussions=true`, leaving GitHub's six default categories exactly as created — no `.github/DISCUSSION_TEMPLATE/`), enable private vulnerability reporting with one `gh api --method PUT` toggle, and run `gh repo edit uHappyLogic/cairn --enable-squash-merge=false --enable-wiki=false`. Git never records a repository setting, so the task's `TASKS_DONE.md` entry is the only record: verify by reading `has_discussions` back as `true`, private vulnerability reporting as enabled, `allow_squash_merge` as `false`, and `has_wiki` as `false`, and record each read-back among the Verified bullets.

**Verified:**

- `has_discussions` reads back `true`: `gh api repos/uHappyLogic/cairn --jq .has_discussions` returns `true` — before this task it returned `false`. Enabled by the one API toggle `gh api --method PATCH repos/uHappyLogic/cairn -F has_discussions=true`, whose response already carried `"has_discussions":true`.
- The Discussions category set is GitHub's six defaults exactly as created: a GraphQL `discussionCategories` query on `uHappyLogic/cairn` returns `totalCount` 6 with the nodes Announcements (`announcements`), General (`general`), Ideas (`ideas`), Polls (`polls`), Q&A (`q-a`, the only `isAnswerable: true` category), and Show and tell (`show-and-tell`) — none pruned, renamed, or added, so the chooser's `discussions/new?category=q-a` contact link points at a category that exists by construction — and no `.github/DISCUSSION_TEMPLATE/` was written: `.github/` still holds only `assets/readme/cairn-banner.png`.
- Private vulnerability reporting reads back enabled: `gh api repos/uHappyLogic/cairn/private-vulnerability-reporting` returns `{"enabled":true}` — before this task it returned `{"enabled":false}`. Enabled by the one toggle `gh api --method PUT repos/uHappyLogic/cairn/private-vulnerability-reporting` (exit 0, empty body).
- `allow_squash_merge` reads back `false`: `gh api repos/uHappyLogic/cairn --jq .allow_squash_merge` returns `false` — before this task it returned `true`. Set by the one call `gh repo edit uHappyLogic/cairn --enable-squash-merge=false --enable-wiki=false` (exit 0); `allow_merge_commit` and `allow_rebase_merge` both still read `true`, so the merge-commit pull-request contract holds.
- `has_wiki` reads back `false`: `gh api repos/uHappyLogic/cairn --jq .has_wiki` returns `false` — before this task it returned `true`. Set by that same `gh repo edit` call, so the root repository now matches the wiki-disabled `cairn-claude` and `cairn-antigravity`; `has_issues` and `has_projects` remain `true`, untouched.
- The act is remote-only and this entry is its only record: `git status --porcelain` shows no working-tree change beyond this TODO→DONE move, and the three commands above — run with `gh` 2.96.0 as `uHappyLogic` — are the whole change; nothing under the tree was created or edited.

---

## Add Drift-Gate CI Workflow And Badge

Add a GitHub Actions workflow under `.github/workflows/` that triggers on `push` and `pull_request` with no branch filter and no `paths` filter, installs `uv` and runs `uv run scripts/build_hosts.py --check`, pinning both actions (checkout and uv setup) to full 40-character commit SHAs each followed by a `# vX.Y.Z` comment, with no Dependabot configuration. Add a third shields.io badge to the README's centred badge row beside the release badge, `https://img.shields.io/github/actions/workflow/status/uHappyLogic/cairn/<workflow-file>?branch=main&event=push&style=flat&label=ci`, wrapped in a link to `actions/workflows/<workflow-file>?query=branch%3Amain`, where `<workflow-file>` is the workflow's file name fixed here. Verify the workflow YAML parses, both SHAs resolve to the commented releases, and the badge and link URLs name the same workflow file.

**Verified:**

- `.github/workflows/drift-gate.yml` exists (the workflow file name this task fixes) and loads under `yaml.safe_load` (`uv run python`, pyyaml from `uv.lock`) into a mapping whose `jobs` key holds the one job `check`.
- Its trigger is the list `on: [push, pull_request]` — exactly those two events, and the list form carries no `branches`, `branches-ignore`, `tags`, `paths`, or `paths-ignore` filter on either.
- The `check` job's steps are, in order, `actions/checkout`, `astral-sh/setup-uv`, and one `run` step whose command is exactly `uv run scripts/build_hosts.py --check`; the job also sets `permissions: contents: read`, the least the read-only gate needs.
- Both `uses:` lines match `^\s*- uses: <owner>/<repo>@[0-9a-f]{40} # v\d+\.\d+\.\d+$`: `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1` and `astral-sh/setup-uv@bec219d24cd3e171d82865faccec33120bb574f4 # v10.1.0`. Each commented tag resolves to its pinned SHA on the action's repository — `gh api repos/actions/checkout/git/ref/tags/v7.0.1` and `gh api repos/astral-sh/setup-uv/git/ref/tags/v10.1.0` return `object.sha` equal to the pin, both tags lightweight (`object.type` `commit`, nothing to peel), `git ls-remote --tags` agrees, and each is that repository's latest non-prerelease release (`gh release view --repo …`, published 2026-07-20 and 2026-09-10); the setup-uv line is byte-identical to the pinned form in setup-uv's own README.
- No Dependabot configuration exists: neither `.github/dependabot.yml` nor `.github/dependabot.yaml` is present, and `.github/workflows/drift-gate.yml` is the only file added under `.github/`.
- The root `README.md`'s centred `<p align="center">` row now holds three `<img>` badges, the new one directly after the release badge's `</a>` and before the license badge, with `src` exactly `https://img.shields.io/github/actions/workflow/status/uHappyLogic/cairn/drift-gate.yml?branch=main&event=push&style=flat&label=ci` wrapped in `<a href="https://github.com/uHappyLogic/cairn/actions/workflows/drift-gate.yml?query=branch%3Amain">`; the host README templates under `scripts/hosts/` carry no badge row and were left untouched.
- The badge `src`, the link `href`, and the file on disk name the same workflow file: a grep of README's `actions/workflow/status/…` and `actions/workflows/…` paths collapses to the single basename `drift-gate.yml`, and `ls .github/workflows/` lists exactly `drift-gate.yml`.
- `uv run scripts/build_hosts.py --check` — the workflow's step command run locally, and the repository's done-verification — exits 0 with "Check passed: hosts/antigravity/ and hosts/claude/ match a fresh build of core/ at version 1.4.0."; `git status --porcelain` shows only `README.md` modified and `.github/workflows/` added beyond this TODO→DONE move.

---

## Add Contributor Covenant Code Of Conduct

Add a root `CODE_OF_CONDUCT.md` that is Contributor Covenant 2.1 verbatim, with its single `[INSERT CONTACT METHOD]` slot filled with the git author address `kosiak.lukasz@gmail.com` and nothing else changed, so GitHub's content detection labels it Contributor Covenant. Verify by diffing the file against the canonical 2.1 text: the only difference is the filled slot.

**Verified:**

- `CODE_OF_CONDUCT.md` exists at the repository root (5480 bytes, 85 lines), beside `LICENSE` and `README.md`.
- Its text is Contributor Covenant 2.1 verbatim: `diff` against the canonical 2.1 Markdown fetched from `https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md` (sha256 `977d7813…37ba`) yields exactly one hunk, `40c40`, and a word-level diff of that line shows only `[INSERT CONTACT METHOD]` → `kosiak.lukasz@gmail.com`; with line 40 dropped from both, the remaining 84 lines are byte-identical — the canonical file's leading blank line, its five reference-link lines, and its trailing blank line all kept as they come, so nothing else changed.
- No `[INSERT CONTACT METHOD]` placeholder remains (`grep -c` returns 0) and `kosiak.lukasz@gmail.com` appears exactly once — the git author address every existing commit carries: `git log --format=%ae | sort -u` lists that one address across all 601 commits.
- The text is the version GitHub's detector labels Contributor Covenant: line 74 reads "adapted from the Contributor Covenant, version 2.1", the 2.1 the `### Code of conduct` decision names; the canonical contributor-covenant.org file is the reference (GitHub's `/codes_of_conduct/contributor_covenant` API body is the hard-wrapped 2.0 text, a different version, so it is not what "verbatim 2.1" is diffed against), and the remote `community/profile` read-back can only follow a push, which this task never performs.
- It stays root-only, as the `### Distribution tree hygiene files` decision fixes: `find` names `./CODE_OF_CONDUCT.md` as the only such file in the tree, none exists under `core/`, `scripts/hosts/`, or either `hosts/<host>/` tree, `scripts/build_hosts.py` copies only `LICENSE` into a host tree, and `uv run scripts/build_hosts.py --check` — the repository's one automated check — exits 0 with "Check passed: hosts/antigravity/ and hosts/claude/ match a fresh build of core/ at version 1.4.0."
- The change set is exactly the new file: `git status --porcelain` shows only `?? CODE_OF_CONDUCT.md` beyond this TODO→DONE move (the fetched reference copies live under the gitignored `temp/`).

---
