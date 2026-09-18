# TASKS TODO

## Store Traffic Token Secret And Delete PAT

Store the value of `temp/PAT` as the `TRAFFIC_TOKEN` repository secret on `uHappyLogic/cairn`, `uHappyLogic/cairn-claude`, and `uHappyLogic/cairn-antigravity` with `gh secret set`, then delete `temp/PAT` so the token exists only in GitHub's write-only secret store, recording the deletion in this task's `TASKS_DONE.md` entry because `temp/` is gitignored and nothing in git would otherwise record it. Verified when `gh secret list` on each of the three repositories shows `TRAFFIC_TOKEN` and `test ! -e temp/PAT` succeeds.

---

## Seed Traffic Data Branches Via Dispatch

Trigger one `workflow_dispatch` run of `traffic-badges.yml` on each of the three repositories with `gh workflow run`, wait for each run to succeed, and confirm each repository now has a `traffic-data` branch carrying `totals.json`, `views-unique.svg`, and `clones-unique.svg`, so every badge URL resolves before the README references it. Read the earliest date recorded in each branch's `totals.json` and note it in the `TASKS_DONE.md` entry, since the adoption caption's start date is read off the seeded branches. Verified when `gh run list` shows a successful run per repository and `curl` on each of the six `https://raw.githubusercontent.com/uHappyLogic/<repo>/traffic-data/<output>` badge URLs returns HTTP 200.

---

## Add README Adoption Table Section

Insert a `## Adoption` section into `README.md` after `## Skill reference` and before `## Contributing`, holding a GitHub-flavoured pipe table with header row repository | unique views | unique clones and one row per repository labelled with its full `uHappyLogic/<repo>` name as a link to the repository, each badge cell a Markdown image at the badge's raw `traffic-data` URL with its column name as alt text wrapped in a link to that repository's `traffic-data` branch page, followed by a caption paragraph stating that counts are cumulative since the earliest day in each `traffic-data` branch's `totals.json` written as a date (a second date in parentheses for the distribution rows when theirs differs), that a unique count is the sum of each day's unique visitors or cloners so a visitor returning on another day counts again, that clone counts include the badge workflow's own daily fetch of the traffic-data branch (one unique clone and two clones per repository per day), and that the monorepo's additionally include CI checkouts; the page's opening banner, badge block, title, pitch, and install sections stay exactly as they are. Verified when the section sits between those two headings, every badge image URL and every link in the table returns HTTP 200, and the caption carries the date and all three caveats.

---

## Verify Inactivity Disable Precedent Evidence

Establish, with read-only `gh api` calls against the public REST API, that the action's daily push keeps a scheduled workflow clear of GitHub's 60-day inactivity disable: read the live state of `albertoarena/github-traffic-badge` — its scheduled traffic workflow still `active` past day 60 since the last human commit of 2026-07-05, with only `github-actions[bot]` pushes to `traffic-data` and every run schedule-triggered — and then, after each distribution repository's first scheduled run at 03:17 UTC, confirm the same signal there: `pushed_at` advanced and a public PushEvent on `refs/heads/traffic-data`. Record the dated observations both in the Inactivity evidence decision of `requirements.md` and in this task's `**Verified:**` entry. Verified when both readings are recorded with their dates and the distribution repositories' workflow state reads `active`.

---
