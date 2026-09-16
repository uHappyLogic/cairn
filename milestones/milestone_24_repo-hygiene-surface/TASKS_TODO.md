# TASKS TODO

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
