# Milestone 25: Traffic Adoption Badges

## Goal

Publish adoption evidence in README.md as a table of albertoarena/github-traffic-badge badges — one row per repository (uHappyLogic/cairn, cairn-claude, cairn-antigravity), two columns (unique views, unique clones), and a caption stating the counts are cumulative from the workflows' first run and that the monorepo's clones include CI checkouts. Each repository runs a daily scheduled workflow (the action pinned to a full commit SHA, one step per metric writing a distinct SVG to the traffic-data branch): the monorepo's under .github/workflows/, each distribution repository's rendered from a scripts/hosts/<host>/ template into its hosts/<host>/ tree so releases publish it. The milestone stores the fine-grained PAT at temp/PAT as the TRAFFIC_TOKEN secret on all three repositories with gh secret set, seeds every traffic-data branch once via workflow_dispatch before the README references its badges, and verifies that the action's daily push keeps the distribution repositories' cron workflows from GitHub's 60-day inactivity disable.

## Relevant starting state

### README badge block

`README.md` opens with the banner image and one centred `<p>` of three shields.io badges — release (`github/v/release`), `ci` (reading `drift-gate.yml`'s status on `main`), and license — all `style=flat`, each wrapped in a link. The rest of the file is plain Markdown under `# Cairn` (`## Why Cairn?`, `## Installation`, `## How it works`, `## Workflow pipeline`, `## How skills commit`, `## Skill reference`, `## Contributing`, `## Self-dogfooding`, `## License`); it contains no Markdown table and no mention of traffic, adoption, or usage figures anywhere. The monorepo README is hand-authored; only the distribution READMEs are built from templates.

### Monorepo GitHub Actions

`.github/workflows/drift-gate.yml` is the only workflow: `on: [push, pull_request]` with no branch or path filter, `permissions: contents: read`, and its two actions pinned to full commit SHAs each followed by a `# vX.Y.Z` comment bumped by hand (no Dependabot); every run performs an `actions/checkout`. Repository settings: Actions enabled, all actions allowed, `sha_pinning_required` off, default `GITHUB_TOKEN` permissions read-only. The repository has a single branch, `main`, and no repository secrets.

### Distribution repositories

`uHappyLogic/cairn-claude` and `uHappyLogic/cairn-antigravity` each hold exactly one commit — the root commit `Release: 1.5.0` of 2026-09-17, tagged `1.5.0` — on their only branch `main`, with no workflows, no secrets, and issues, Discussions, wiki, and projects disabled; Actions is enabled on both with all actions allowed and read-only default token permissions. They change only when `/release-plugin` publishes: `git commit-tree` over the monorepo's `HEAD:hosts/<host>` tree object, pushed over SSH (`git@github.com:uHappyLogic/cairn-<host>.git`) atomically to `main` and the version tag, so between releases they receive no pushes at all. Nothing in the project records whether a workflow's own pushes count as repository activity for GitHub's 60-day scheduled-workflow disable.

### Host build and templates

Every file under `scripts/hosts/<host>/` other than `settings.toml` is a template rendered to the same relative path in `hosts/<host>/` (the walk is recursive and hidden directories render — `scripts/hosts/claude/.claude-plugin/` already does), substituting only the `{{VERSION}}` and `{{NAME}}` slots; `prose_drop_patterns`, `strip_frontmatter_keys`, and `exclude` apply to `core/` files only, and there is no per-template escape or opt-out. The validation gate's `unfilled-placeholder` check fails the whole build on any line containing `{{` in any rendered text file, templates included, so a workflow file using GitHub's `${{ … }}` expression syntax cannot pass the build as it stands. `--check` compares the render byte-for-byte with the committed trees and runs in CI on every push and pull request. Whatever the tree carries reaches consumers whole: the release publishes it verbatim, Claude Code marketplace installs clone the distribution repository, and the Antigravity install extracts the full `main` tarball into `.agents/plugins/cairn/`.

### The github-traffic-badge action

`albertoarena/github-traffic-badge` is a composite action (MIT, zero runtime dependencies, Node 20+, run with `node` on the runner) whose latest release is `v1.1.4` (2026-06-17) at commit `56f6f3e0ed586f14440561758b197ca57a38f480`, which the `v1` tag also points at; the default branch carries later unreleased commits (HEAD `63470f9`, 2026-07-05). Inputs: `token` (required — a PAT; the default `GITHUB_TOKEN` gets 403 on the Traffic API), `metric` (`views` | `clones` | `views-unique` | `clones-unique`), `label`, `color`, `style`, `output` (default `badge.svg`), `branch` (default `traffic-data`), `commit-message`, `base`, `abbreviated`, `lowercase`, `font-size`; outputs `total` and `badge-path`. Each run re-clones the data branch (orphan on first run) into a fresh temp directory over HTTPS using the same `token`, fetches both `/traffic/views` and `/traffic/clones` (the API's 14-day window), upserts both into one shared date-keyed `totals.json`, renders the one requested metric to `<output>`, then commits as `github-actions[bot]` and pushes with that token — so multiple steps with distinct `output` names share one `totals.json` and each step sees the previous step's push. A unique-metric total is the sum of per-day `uniques` over every day the branch has recorded, beginning with the 14 days the first run captured. The badge URL form is `https://raw.githubusercontent.com/<owner>/<repo>/traffic-data/<output>`.

### Token, secrets, and current traffic

`temp/` is gitignored; `temp/PAT` holds a 93-byte fine-grained token (`github_pat_` prefix, no trailing newline) that authenticates as `uHappyLogic`, for which the API returns no `github-authentication-token-expiration` header. It reads `/traffic/views` and `/traffic/clones` on all three repositories (HTTP 200), but a dry-run HTTPS push with it is refused on all three (`403`, permission denied), so as stored it lacks the contents-write access the action's push step uses. `gh` is logged in as `uHappyLogic` (scopes `gist`, `read:org`, `repo`; git protocol ssh), and no `TRAFFIC_TOKEN` — or any other — secret exists on any of the three repositories. The Traffic API's current 14-day figures: `cairn` 56 views / 9 unique, 398 clones / 112 unique; `cairn-claude` 4 / 2 views, 11 / 9 clones; `cairn-antigravity` 8 / 2 views, 6 / 4 clones — no data older than 14 days is retrievable.

## Decisions

## Out of Scope

## Open questions

<open-question id="Placeholder gate for workflows">
  <question>How does a workflow template under scripts/hosts/&lt;host&gt;/ carry the ${{ secrets.TRAFFIC_TOKEN }} expression syntax past the build gate that fails on any {{ in a rendered file — a path-scoped exemption of the check, a template escape sequence the render expands, or a new definition key listing exempt templates?</question>
</open-question>
<open-question id="PAT push access">
  <question>The stored fine-grained PAT reads traffic on all three repositories but cannot push, while the action pushes the traffic-data branch with that same token: is the token extended in place with Contents read and write on the three repositories before it is stored as TRAFFIC_TOKEN, or is a new token minted and temp/PAT replaced?</question>
</open-question>
<open-question id="PAT file retention">
  <question>Once TRAFFIC_TOKEN is set on all three repositories, is the gitignored temp/PAT file deleted, or kept so the secret can be set again later?</question>
</open-question>
<open-question id="Distribution seeding sequence">
  <question>Each distribution repository receives its workflow only when a release publishes hosts/&lt;host&gt;/, yet every traffic-data branch must be seeded before README.md references its badge: does the milestone cut a release to publish the workflows (and at which version), push the workflows to the distribution repositories once by hand, or hold the README table until after the next regular release?</question>
</open-question>
<open-question id="Workflow copy duplication">
  <question>With the monorepo workflow hand-authored under .github/workflows/ and each distribution workflow rendered from its own scripts/hosts/&lt;host&gt;/ template, the same workflow exists in three copies: is that duplication accepted, or does the build gain a shared template rendered into every host tree?</question>
</open-question>
<open-question id="Workflow name and cron time">
  <question>What file name, workflow name, and daily cron time (UTC) does the traffic workflow use, and do the three repositories run at the same time or staggered?</question>
</open-question>
<open-question id="Workflow permissions block">
  <question>The action pushes with the PAT rather than GITHUB_TOKEN, yet its README prescribes permissions contents: write: does the traffic workflow declare contents: read as drift-gate does, or contents: write as the action documents?</question>
</open-question>
<open-question id="Badge rendering parameters">
  <question>What label text, color, style, and output SVG file names do the two badges per repository use, given that the table columns already name the metrics and the existing README badges use style=flat?</question>
</open-question>
<open-question id="Adoption table placement">
  <question>Where does the adoption table go in README.md — inside the header badge block, in a new section (and where in the section order), or beside Self-dogfooding?</question>
</open-question>
<open-question id="Table markup and links">
  <question>Is the adoption table a Markdown table or HTML like the header badge block, are the row labels full owner/repo names or short names, and do the row labels or badges link anywhere (the repository, its traffic-data branch, the workflow runs)?</question>
</open-question>
<open-question id="Caption precision">
  <question>Beyond the two facts the goal fixes, does the caption also state that counts include the 14 days the first run captured, that unique counts sum per-day uniques, and that each row starts from the first run of its own workflow (the distribution rows later than the monorepo row)?</question>
</open-question>
<open-question id="Self-clone inflation">
  <question>Every step of the action fetches the repository over git by the same mechanism as actions/checkout, which the caption already treats as a counted clone, so the workflow inflates the clone counts of every repository daily — including the distribution repositories the caption presents as CI-free: is that accepted, mitigated, or disclosed in the caption?</question>
</open-question>
<open-question id="Inactivity disable evidence">
  <question>GitHub disables a scheduled workflow only after 60 idle days, so what evidence verifies within the milestone that the daily traffic-data push keeps the distribution workflows active — GitHub documentation, an API read-back of the workflow state after some days, or a follow-up check scheduled beyond the milestone?</question>
</open-question>
<open-question id="Workflow in installed trees">
  <question>A workflow file in hosts/&lt;host&gt;/ reaches every consumer install — the Antigravity tarball extracts it under .agents/plugins/cairn/.github/workflows/ and Claude Code clones it: is that inert file accepted in installed plugin trees, or kept out of what consumers receive?</question>
</open-question>
<open-question id="Distribution README wording">
  <question>The distribution README templates state that every file in the repository is rendered by the host build and that main advances only by release snapshots: are they amended to account for the action-written traffic-data branch and the workflow that writes it?</question>
</open-question>
