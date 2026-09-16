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

### Contributor workflow

An outside contribution is proposal-first, then a contributor-run milestone on a maintainer-reserved slot. A substantive change is proposed as an issue or Discussion; acceptance is the maintainer running `/define-milestone-goal` on `main` with the accepted proposal and activating it with `/goto-next-milestone` once the current-milestone pointer is free. The contributor branches from that commit and runs the full requirements-and-task pipeline through `/finish-current-milestone` in a fork, and the pull request is merged with a merge commit — squash merges are disabled on the repository — so the milestone commits survive for release notes and for `/capture-milestone-principle-updates`, which the maintainer runs after the merge. There is no plain-pull-request tier: small fixes are filed as issues for the maintainer to make.

### Continuous integration

The drift-gate workflow triggers on `push` and `pull_request` with no branch filter and no `paths` filter, so the gate runs on every commit reaching any branch of the root repository, on every pull request, and on each release tag push. Filtering is deliberately not done: the gate finishes in 0.2 seconds inside a half-minute free job, so filtering buys nothing measurable, while a `paths` list would be a hand-maintained second copy of the build's input set — the very drift the gate exists to catch — and a path-skipped run would leave a pull request with no status. Every push and pull request is the goal's literal wording, and the two-event trigger has nothing to curate.

### Code of conduct

`CODE_OF_CONDUCT.md` is Contributor Covenant 2.1 verbatim, with its single `[INSERT CONTACT METHOD]` slot filled with the git author address every existing commit already carries, `kosiak.lukasz@gmail.com`. 2.1 is the current 2.x text and the one GitHub's content detection labels Contributor Covenant on the Community Standards page (a 3.0 file resolves to Other), and it has one slot to fill instead of 3.0's two authored notes. The contact is an email because GitHub offers no private conduct channel — issues and Discussions are public, and private vulnerability reporting is for security — and the author address is the only one that verifiably exists and is read, so naming it exposes a rendered file to crawler indexing but publishes no new information. A dedicated conduct address would be chosen only if a monitored mailbox on a maintainer-controlled domain already existed; none does, and creating one for a repository with no community yet would be an inbox nobody checks.

### Security policy

`SECURITY.md` directs vulnerability reports to GitHub private vulnerability reporting only — the root repository's Report a vulnerability form — and the milestone enables private vulnerability reporting on `uHappyLogic/cairn` with one `gh api --method PUT` toggle of the same kind as the Discussions enable. Private reporting puts each report where the fix happens, as a draft advisory with a private thread and a publish step, instead of in a gmail inbox. No email address appears in the file: the maintainer publishes none today, and a fallback address is a one-line addition should one ever be wanted, so nothing is lost by leaving it out. The supported-versions table names the latest release only and states that every fix ships as a new release to both distribution repositories — the one honest value, because the sixteen releases are strictly linear, the release skill publishes only `main`'s HEAD, and both patch releases (1.0.1, 1.1.1) landed on the newest minor.

### Issue templates

The bug and feature issue templates are YAML issue forms, not Markdown templates. Host, cairn version, and skill invoked are the three facts a cairn bug cannot be reproduced without and exactly what free text loses, and required form fields are the only mechanism that guarantees them on a repository with no issues yet and no triage history to fall back on. The host is a two-value dropdown mirroring `scripts/hosts/`, and the version and skill are free-text inputs, so no field enumerates the 21 skills a list would have to track. The one cost is the `gh` CLI gap — it does not detect YAML forms — which a reporter crosses with `gh issue create --web`; a Markdown template would only paper over that gap, since `gh` pre-fills sections it does not enforce, so Markdown would be chosen only if terminal-filed issues were expected to be the main channel.

### Changelog

`CHANGELOG.md` puts a plain version-date heading over each release's body verbatim: a title, a one-line note that each entry is that release's notes verbatim, newest first, and per release a heading of the form `## <VERSION> — <YYYY-MM-DD>` (the em-dash style of the `milestones/README.md` history headings) directly over the release body, whose milestone sections sit at `###` so they nest under it. There is no Unreleased section and no reference-link list; the body's `**Full Changelog**` line is the compare link. The goal fixes the entry body as the release's composed notes, identical across the changelog and the three release pages, which rules out the categorised body that is Keep a Changelog's substance and leaves only its skeleton to borrow — and that skeleton costs more than it reads: an Unreleased section nothing fills between releases, a reference-link list duplicating the body's own Full Changelog line, and three edits per release in place of one prepend. The plain heading keeps the release write to one prepend below the title with no other slot in the file, and the backfill to a loop over `gh release view --json body` with the `publishedAt` date as each heading's date. The one shape change is that `/release-plugin` step 5 composes the milestone sections at `###` from this release on, and the eight existing sectioned bodies (0.9.8 through 1.4.0) are demoted once in the backfill, so the entry stays byte-identical to the body — which is also what a later reread from the file needs should the release body ever be read back from `CHANGELOG.md`.

The backfill carries the eight link-only releases, 0.9.0 through 0.9.7, verbatim: each entry is the plain version-date heading over the body exactly as `gh release view` returns it, however thin — a lone `**Full Changelog**` compare link, or nothing at all where the published body is empty — with no notes reconstructed from the milestone history or commit ranges and no release page edited. The goal names the existing releases as the backfill's source and requires the changelog and the release pages to carry identical notes, and under the plain heading over the verbatim body that is a single `gh release view` loop that holds for all sixteen entries with no exception. Reconstructing would turn eight entries into a September rewrite a reader cannot distinguish from notes that shipped, and the only way to reconstruct without breaking identity would be to rewrite eight published release pages — the one thing that would change the choice, taken only if the maintainer wants those pages rewritten. The compare link still gives each early entry its commit range, and `milestones/README.md` already holds the condensed per-milestone story.

Once the `Release: <VERSION>` commit exists, the release body is the committed changelog entry: the entry for `<VERSION>` extracted from `HEAD:CHANGELOG.md` — the lines under its `## <VERSION> — <YYYY-MM-DD>` heading up to the next `##` heading, blank lines trimmed — so `/release-plugin` step 7 shows and step 8 publishes that text on a fresh run and a resumption alike, and the changelog, the monorepo release, and the two distribution releases stay identical even when a run fails between creating them. Step 5 composes the body only on a fresh run; a resumption skips it whole and reads the entry back rather than recomposing a condensed rewrite that could hand a distribution release notes differing from a monorepo release already created. Under the plain heading form the extraction is a fixed line range and the body is byte-identical to the entry. A pre-mutation gate beside the tag-existence check requires that no entry for `<VERSION>` exists on a fresh run and that exactly one exists at `HEAD` on a resumption — one grep that flips on resumption — so a stale unpublished Release commit buried below `HEAD`, which would otherwise gain a duplicate entry in a later commit that succeeds, stops in pre-flight instead. The accepted cost is that the skill must state the extraction rule exactly, and that a resumption's skipped step 5 leaves its cross-check and empty-range confirmation un-rerun, resting on the committed entry as the evidence they passed.

## Out of Scope

## Open questions

<open-question id="Contributing vs Development overlap">
  <question>Does the root CONTRIBUTING.md absorb the README Development section (with the README linking out to it), or summarize the contributor path and link to the README section that stays authoritative?</question>
</open-question>
<open-question id="README links to hygiene files">
  <question>Beyond the CI badge, should README.md gain a Contributing section or links to CONTRIBUTING.md, SECURITY.md, CHANGELOG.md, and Discussions, or stay untouched?</question>
</open-question>
<open-question id="Blank issues and contact links">
  <question>Should an ISSUE_TEMPLATE config.yml disable blank issues and route questions to a Discussions category once Discussions is enabled?</question>
</open-question>
<open-question id="Unused wiki tab">
  <question>Should the unused wiki be disabled on the root repository so a visitor sees no empty Wiki tab, or be left enabled?</question>
</open-question>
<open-question id="Squash merge setting">
  <question>Is disabling squash merges on the root repository, which the contributor-workflow decision requires so a contributor milestone&apos;s Milestone-finish: and answer commit subjects survive the merge, a task of this milestone alongside enabling Discussions, or a repository setting the maintainer flips by hand outside any task?</question>
</open-question>
<open-question id="Proposal intake route">
  <question>Is the proposal that precedes a contributor-run milestone filed through a dedicated proposal issue form beside the bug and feature templates, through a Discussions category once Discussions is enabled, or through the feature template as it stands?</question>
</open-question>
<open-question id="CONTRIBUTING.md handoff wording">
  <question>Does the root CONTRIBUTING.md spell out the proposal-then-reserved-milestone handoff step by step (propose, maintainer defines and activates the milestone on main, branch from that commit, run the pipeline through /finish-current-milestone, merge commit), or state the contract in a sentence and point at the README workflow documentation for the steps?</question>
</open-question>
<open-question id="Pull-request template milestone field">
  <question>Does the pull-request template ask for the reserved milestone id and the proposal it was accepted in, so a reviewer can check the branch carries that milestone&apos;s artifacts, or stay a generic checklist (rebuilt hosts/ trees, --check green, CLAUDE.md invariants preserved)?</question>
</open-question>
<open-question id="CI action pinning">
  <question>Should the drift-gate workflow pin its checkout and uv setup actions to full commit SHAs or to major-version tags?</question>
</open-question>
<open-question id="CI badge source">
  <question>Is the CI badge a shields.io workflow-status badge matching the two existing badges or GitHub&apos;s native badge.svg, and does it report the main branch only or the latest run on any branch?</question>
</open-question>
<open-question id="Distribution tree hygiene files">
  <question>Beyond the CONTRIBUTING.md template, should SECURITY.md and CODE_OF_CONDUCT.md also be rendered into each host tree so a visitor to a distribution repository finds them, or stay root-only?</question>
</open-question>
<open-question id="Backfilled release page headings">
  <question>Since the backfill demotes the milestone sections of the eight sectioned releases (0.9.8 through 1.4.0) to ###, are those eight release pages edited to match so the changelog and release bodies stay identical, or is the heading-level divergence for backfilled entries accepted?</question>
</open-question>
<open-question id="Notes edit at release pause">
  <question>Now that the release body is the committed changelog entry, can the maintainer revise the notes at the step-7 pause, and if so does the skill amend the unpushed Release commit or must the run be aborted and restarted?</question>
</open-question>
<open-question id="Pointer held during contribution">
  <question>While a contributor-run milestone holds the current-milestone pointer on main, is the maintainer blocked from starting their own milestones until the merge, and how is the pointer freed if the contribution is abandoned?</question>
</open-question>
<open-question id="Discussions categories">
  <question>Does enabling Discussions keep GitHub&apos;s default category set, or does the milestone curate categories (for example a proposals category) for the intake routes the templates point at?</question>
</open-question>
