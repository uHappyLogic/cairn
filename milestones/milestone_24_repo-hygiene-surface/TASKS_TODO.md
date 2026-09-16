# TASKS TODO

## Configure Root Repository Settings

Flip the four repository settings on `uHappyLogic/cairn` that the milestone's decisions state as fact: enable Discussions (`has_discussions=true`, leaving GitHub's six default categories exactly as created — no `.github/DISCUSSION_TEMPLATE/`), enable private vulnerability reporting with one `gh api --method PUT` toggle, and run `gh repo edit uHappyLogic/cairn --enable-squash-merge=false --enable-wiki=false`. Git never records a repository setting, so the task's `TASKS_DONE.md` entry is the only record: verify by reading `has_discussions` back as `true`, private vulnerability reporting as enabled, `allow_squash_merge` as `false`, and `has_wiki` as `false`, and record each read-back among the Verified bullets.

---

## Add Drift-Gate CI Workflow And Badge

Add a GitHub Actions workflow under `.github/workflows/` that triggers on `push` and `pull_request` with no branch filter and no `paths` filter, installs `uv` and runs `uv run scripts/build_hosts.py --check`, pinning both actions (checkout and uv setup) to full 40-character commit SHAs each followed by a `# vX.Y.Z` comment, with no Dependabot configuration. Add a third shields.io badge to the README's centred badge row beside the release badge, `https://img.shields.io/github/actions/workflow/status/uHappyLogic/cairn/<workflow-file>?branch=main&event=push&style=flat&label=ci`, wrapped in a link to `actions/workflows/<workflow-file>?query=branch%3Amain`, where `<workflow-file>` is the workflow's file name fixed here. Verify the workflow YAML parses, both SHAs resolve to the commented releases, and the badge and link URLs name the same workflow file.

---

## Add Contributor Covenant Code Of Conduct

Add a root `CODE_OF_CONDUCT.md` that is Contributor Covenant 2.1 verbatim, with its single `[INSERT CONTACT METHOD]` slot filled with the git author address `kosiak.lukasz@gmail.com` and nothing else changed, so GitHub's content detection labels it Contributor Covenant. Verify by diffing the file against the canonical 2.1 text: the only difference is the filled slot.

---

## Write Security Policy File

Add a root `SECURITY.md` that directs vulnerability reports to GitHub private vulnerability reporting only — the root repository's Report a vulnerability form — with no email address, and a supported-versions table naming the latest release only, stating that every fix ships as a new release to both distribution repositories. Verify the file names no email, links the private reporting form, and its table names exactly the current latest release tag.

---

## Add Issue Forms And Chooser Config

Add three YAML issue forms under `.github/ISSUE_TEMPLATE/`: a bug form with a required host dropdown of the two values mirroring `scripts/hosts/`, a required cairn-version text input, and a required skill-invoked text input; a feature form; and a proposal form whose required fields are a goal statement in the shape a milestone `## Goal` takes, the motivation, what is in and out of scope, and a checkbox committing the proposer to run the milestone in a fork through `/finish-current-milestone`. Beside them add `config.yml` with `blank_issues_enabled: false` and one contact link — name Ask a question, url `https://github.com/uHappyLogic/cairn/discussions/new?category=q-a`, about usage and how-to questions — and no security link. Verify every form loads as YAML with the required fields marked required and the chooser config carries exactly that one link.

---

## Add Pull-Request Template

Add a single `.github/PULL_REQUEST_TEMPLATE.md` that opens with two fill-in lines — the reserved milestone id (the `milestone_<N>_<slug>` directory name the maintainer's `Milestone-definition:` commit created on `main`) and `Closes #<proposal issue>` — followed by a reviewer checklist of what a finished contributor milestone leaves in the tree: `milestones/<id>/requirements.md` with no `<open-question>` block, `TASKS_TODO.md` with no task section, `TASKS_DONE.md` carrying every task with its Verified bullets, `milestones/README.md` with the milestone's history entry and the pointer at `none`, one `Milestone-finish: <id>` commit on the branch, `CLAUDE.md` touched only for lasting changes, and `hosts/` rebuilt (confirmed by the drift-gate status check). Verify the file carries exactly those two fill-ins and those checklist items and no generic checklist.

---

## Write Root Contributing Guide

Add a root `CONTRIBUTING.md` whose first section spells out the proposal-then-reserved-milestone handoff as an ordered list, one step per act: file the proposal issue; the maintainer accepts by running `/define-milestone-goal` on `main` while their pointer reads `none`, whose `Milestone-definition:` commit reserves `milestone_<N>_<slug>` without activating it; fork and branch from that commit; run `/goto-next-milestone` first; run the requirements-and-task pipeline through `/finish-current-milestone` as one step linking the README's Workflow pipeline; sync from `main` by merge only (never rebase) and only while its `Current milestone:` line reads `none` (checkable with `git show origin/main:milestones/README.md`), aborting a pointer conflict rather than resolving it; rebuild `hosts/` and pass `--check`; open the pull request, merged as a merge commit (squash merges are disabled), after which the maintainer runs `/capture-milestone-principle-updates` — noting there is no plain-pull-request tier and small fixes are filed as issues, and that the design invariants live in `CLAUDE.md`. The section after it is the README's `## Development` body moved whole, with its one in-section link re-pointed to `README.md#installation`; this task leaves `README.md` untouched. Verify the ordered steps match the decisions and the Development text equals the README section apart from that one link.

---

## Render Host Contributing Pointer Templates

Add a `CONTRIBUTING.md` template to each host definition directory (`scripts/hosts/claude/`, `scripts/hosts/antigravity/`) that renders into the host tree and points contributors at the root repository `uHappyLogic/cairn` for issues and pull requests, naming the root's private vulnerability reporting form for security reports beside the issue route; `SECURITY.md` and `CODE_OF_CONDUCT.md` stay root-only and are not rendered or copied. Rebuild both host trees with `uv run scripts/build_hosts.py` and commit them, so each host tree carries exactly `README.md`, `LICENSE`, and `CONTRIBUTING.md` as its non-plugin files. Verify `uv run scripts/build_hosts.py --check` passes and `hosts/<host>/CONTRIBUTING.md` exists for both hosts.

---

## Backfill Changelog From GitHub Releases

First demote the nine `##` milestone-section lines on the eight sectioned monorepo release pages (`0.9.8` through `1.4.0`) to `###` with one `gh release edit --notes-file` loop that changes no other line, then write a root `CHANGELOG.md` from one uniform loop over all sixteen tags (`gh release view --json body` with `publishedAt` as the date): a title, a one-line note that each entry is that release's notes verbatim, newest first, and per release a `## <VERSION> — <YYYY-MM-DD>` heading directly over the body exactly as returned — link-only and empty bodies included, nothing reconstructed — with no Unreleased section and no reference-link list. Verify, and record among the Verified bullets, that every entry read back from the file equals its release-page body byte for byte.

---

## Release Skill Maintains Changelog Entry

Edit `.claude/skills/release-plugin/SKILL.md` so a release keeps `CHANGELOG.md` identical to the release notes: step 5 composes the milestone sections at `###` (only on a fresh run — a resumption skips it whole); step 6 prepends the `## <VERSION> — <YYYY-MM-DD>` entry below the changelog title and stages `CHANGELOG.md` beside the existing version paths in the one `Release: <VERSION>` commit, with step 6b and `CLAUDE.md`'s Development sentence about that commit updated to name the changelog entry; a pre-flight gate beside the tag-existence check requires no entry for `<VERSION>` on a fresh run and exactly one at `HEAD` on a resumption; and steps 7 and 8 show and publish the entry extracted from `HEAD:CHANGELOG.md` (the lines under its heading up to the next `##` heading, blank lines trimmed) on a fresh run and a resumption alike, with the extraction rule stated exactly. Verify by reading the skill through both paths — fresh and resumption — and confirming every step names the committed entry as its source and the staged path list includes `CHANGELOG.md`.

---

## Release Skill Revises Notes At Pause

Extend step 7 of `.claude/skills/release-plugin/SKILL.md` with a third answer beside publish and stop: while the `Release: <VERSION>` commit is still unpushed (after a fetch, `git merge-base --is-ancestor HEAD origin/main` fails), a revision applies the maintainer's stated change to the `<VERSION>` entry in the working `CHANGELOG.md` (a hand edit already made there counts the same), stages it with `git add -- CHANGELOG.md`, amends with `git commit --amend --no-edit` so the subject is untouched, re-extracts the entry from `HEAD:CHANGELOG.md`, shows it in full, and asks again; once `origin/main` carries the commit a revision request is a stop naming that reason, and step 6d's one-commit sentence names this as the run's only amend. Verify by reading step 7 and 6d together: the amend is path-scoped, subject-preserving, and gated on the unpushed check.

---

## Replace README Development With Contributing Section

Remove the README's `## Development` section (its body now lives in `CONTRIBUTING.md`) and put a `## Contributing` section in its place, between the skill reference and `## Self-dogfooding`, in the one-line shape of `## License`: one sentence naming the `core/`-once-rebuild model with a link to `CONTRIBUTING.md` for the full contributor path, then one line each routing bug reports and proposals to the issue forms, questions to the Discussions tab, vulnerability reports to `SECURITY.md`, and release notes to `CHANGELOG.md` — five or six lines, with `CODE_OF_CONDUCT.md` left to GitHub's About sidebar and the badge row untouched. Verify no `## Development` heading remains, every linked file exists in the tree, and nothing in the repository links to the README's `#development` anchor.

---
