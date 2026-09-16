# Milestone 24: Repo Hygiene Surface

## Goal

Give the cairn repository the hygiene surface a first-time visitor scans for. Add a GitHub Actions workflow that runs `uv run scripts/build_hosts.py --check` on every push and pull request, with a CI badge beside the release badge; a root `CONTRIBUTING.md` (edit `core/`, rebuild, invariants live in `CLAUDE.md`), `SECURITY.md`, `CODE_OF_CONDUCT.md`, bug and feature issue templates, and a pull-request template; a `CONTRIBUTING.md` template in each host definition that renders into the host tree and points contributors at the root repository; an in-repo `CHANGELOG.md` backfilled from every existing GitHub Release and thereafter maintained by `/release-plugin`, which prepends each release's composed notes and stages the file in the `Release: <VERSION>` commit so the changelog, the monorepo release, and the distribution releases carry identical notes; and Discussions enabled on the root repository. `FUNDING.yml` and release cadence are out of scope.

## Relevant starting state

### GitHub repository surface

`.github/` exists but holds only `assets/readme/cairn-banner.png` — no `workflows/`, no `ISSUE_TEMPLATE/`, no `PULL_REQUEST_TEMPLATE.md`. GitHub's community-profile API for `uHappyLogic/cairn` scores the repository 42%: `license` and `readme` present; `code_of_conduct`, `contributing`, `issue_template`, and `pull_request_template` missing. Repository settings: issues enabled, wiki enabled (unused), Discussions disabled; both distribution repositories (`uHappyLogic/cairn-claude`, `uHappyLogic/cairn-antigravity`) have issues disabled by design. `README.md` opens with the banner and a centered `<p>` holding exactly two shields.io badges — the release badge (`github/v/release/uHappyLogic/cairn`, tag display) and a static MIT license badge — and has no Contributing, Security, or Changelog section.

### Continuous integration

No CI exists. The repository's only automated check is `uv run scripts/build_hosts.py --check` — the drift gate that renders every host from `core/`, runs the full validation set, compares byte-for-byte against the committed `hosts/<host>/` trees, writes nothing, and exits non-zero listing differing paths — and today it runs only by hand or as pre-flight gate 2e of `/release-plugin`. Tooling is `uv` with Python `>=3.11` (`.python-version` pins `3.13`), one dependency (`pyyaml`) pinned in `uv.lock`, and `pyproject.toml` marked `package = false`; the drift gate also asserts the root `.claude-plugin/marketplace.json` entry equals `VERSION`.

### Host definitions and template rendering

Each host is a definition directory `scripts/hosts/<host>/` whose every file other than `settings.toml` is a template rendered to the same relative path in `hosts/<host>/`, with `{{VERSION}}` filled from the root `VERSION` and `{{NAME}}` from `plugin_name` (`scripts/build_hosts.py`, `render_host`). Claude's templates are `README.md`, `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json`; Antigravity's are `README.md` and `plugin.json`. `LICENSE` is not a template — the build copies the root file by a dedicated code path — so a new text template with no slots would render unchanged and pass the gate's `unfilled-placeholder` check. Both distribution `README.md` templates already carry a "Generated — do not edit" paragraph directing issues and pull requests to `uHappyLogic/cairn`, and a `## Source` section linking the release tag and noting that the release page carries the notes.

### Release skill and release notes

`.claude/skills/release-plugin/SKILL.md` is the maintainer-only release procedure. Step 5 composes `<RELEASE_BODY>` in context and mutates nothing: one `## <Title> (milestone <N>)` section per `Milestone-finish:` commit in `<LAST_TAG>..HEAD` (highest number first, bullets condensed from that milestone's `milestones/README.md` history entry), closed by a `**Full Changelog**: …/compare/<LAST_TAG>...<VERSION>` line; an empty range instead builds a `## Changes since <LAST_TAG>` section behind a maintainer confirmation. Step 6 runs `set_version.py`, rebuilds, stages exactly `VERSION`, `pyproject.toml`, `uv.lock`, `.claude-plugin/marketplace.json`, and `hosts/` path-scoped, records the one `Release: <VERSION>` commit, and verifies `git status --porcelain --untracked-files=no` is empty; step 6 is skipped whole on a resumption (HEAD subject already `Release: <VERSION>`). The skill (step 6b) and `CLAUDE.md`'s Development section both state that the release commit "changes version slots and nothing else, by construction", resting on pre-flight 2a (clean tracked tree) and 2e (drift gate). The notes exist only in context until step 8c writes them to a temp file for `gh release create --notes-file`; each distribution repository's release carries the identical body, and its `Release:` commit body links to the monorepo release page for notes. Step 7 shows `<VERSION>` and the full `<RELEASE_BODY>` as the run's single pause, after the commit.

### Existing release history

Sixteen GitHub releases exist, tagged bare `0.9.0` through `1.4.0`, published 2026-06-12 through 2026-09-15, each titled by its tag. The eight bodies `0.9.0`–`0.9.7` carry only the `**Full Changelog**` compare link (`0.9.0`'s points at `/commits/0.9.0`); the eight from `0.9.8` on carry milestone sections in the step-5 shape (`0.9.9` has two). Publish dates are available via `gh release list --json tagName,publishedAt`. No `CHANGELOG.md` exists anywhere in the repository.

### Contribution-relevant documentation

`README.md`'s `## Development` section already documents the core-once-rebuild model, the three `build_hosts.py` invocations, the `VERSION`/`set_version.py` rule, the distribution repositories, and the directory-marketplace developer install; `## Self-dogfooding` notes that `milestones/` holds the project's own live workflow artifacts. The design invariants a contributor must preserve live in `CLAUDE.md` (~100 KB, also reachable as the `AGENTS.md` symlink) under "Invariants to preserve when editing skills". Commits follow function-derived `<Marker>: <descriptor>` subjects. `LICENSE` is MIT; no security-contact or conduct text exists in any file.

## Decisions

## Out of Scope

## Open questions

<open-question id="CI trigger scope">
  <question>Should the drift-gate workflow run on pushes to every branch or only to main (plus every pull request), and should it be path-filtered to the build inputs (core/, scripts/, hosts/, VERSION, the root marketplace) or run on every change?</question>
</open-question>
<open-question id="Contributor workflow expectation">
  <question>Must an outside contribution go through the milestone workflow this repository runs on itself (milestone artifacts, Marker-colon commit subjects), or is a plain pull request editing core/ with rebuilt hosts/ trees and a passing drift gate sufficient?</question>
</open-question>
<open-question id="Contributing vs Development overlap">
  <question>Does the root CONTRIBUTING.md absorb the README Development section (with the README linking out to it), or summarize the contributor path and link to the README section that stays authoritative?</question>
</open-question>
<open-question id="README links to hygiene files">
  <question>Beyond the CI badge, should README.md gain a Contributing section or links to CONTRIBUTING.md, SECURITY.md, CHANGELOG.md, and Discussions, or stay untouched?</question>
</open-question>
<open-question id="Conduct text and contact">
  <question>Which code-of-conduct text is adopted (Contributor Covenant 2.1, the GitHub-recognized default, or 3.0), and which contact address does its enforcement clause name?</question>
</open-question>
<open-question id="Security reporting channel">
  <question>Does SECURITY.md direct reports to GitHub private vulnerability reporting (which must be enabled on the repository), to an email address, or both, and which versions does it declare supported?</question>
</open-question>
<open-question id="Issue template format">
  <question>Are the bug and feature templates YAML issue forms with structured fields (host, cairn version, skill invoked) or Markdown templates with free-text sections?</question>
</open-question>
<open-question id="Blank issues and contact links">
  <question>Should an ISSUE_TEMPLATE config.yml disable blank issues and route questions to a Discussions category once Discussions is enabled?</question>
</open-question>
<open-question id="Changelog entry heading form">
  <question>Does each CHANGELOG.md entry follow Keep a Changelog conventions (a bracketed version heading with date, reference-style compare links, an Unreleased section) or a plain version-and-date heading over the release body verbatim?</question>
</open-question>
<open-question id="Link-only release backfill">
  <question>For the eight releases 0.9.0 through 0.9.7 whose bodies are only the compare link, does the backfill carry those bodies verbatim or reconstruct condensed notes from the milestone history and commit ranges?</question>
</open-question>
<open-question id="Release body source of truth">
  <question>Once /release-plugin writes the changelog entry, does the publish step read the release body from the committed CHANGELOG.md entry (so a resumption rereads it instead of recomposing) or keep the in-context body, and does pre-flight guard against an entry for the release version already being present?</question>
</open-question>
<open-question id="Unused wiki tab">
  <question>Should the unused wiki be disabled on the root repository so a visitor sees no empty Wiki tab, or be left enabled?</question>
</open-question>
