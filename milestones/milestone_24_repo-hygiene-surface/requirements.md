# Milestone 24: Repo Hygiene Surface

## Goal

Give the cairn repository the hygiene surface a first-time visitor scans for. Add a GitHub Actions workflow that runs `uv run scripts/build_hosts.py --check` on every push and pull request, with a CI badge beside the release badge; a root `CONTRIBUTING.md` (edit `core/`, rebuild, invariants live in `CLAUDE.md`), `SECURITY.md`, `CODE_OF_CONDUCT.md`, bug and feature issue templates, and a pull-request template; a `CONTRIBUTING.md` template in each host definition that renders into the host tree and points contributors at the root repository; an in-repo `CHANGELOG.md` backfilled from every existing GitHub Release and thereafter maintained by `/release-plugin`, which prepends each release's composed notes and stages the file in the `Release: <VERSION>` commit so the changelog, the monorepo release, and the distribution releases carry identical notes; and Discussions enabled on the root repository. `FUNDING.yml` and release cadence are out of scope.

## Relevant starting state

## Decisions

## Out of Scope

