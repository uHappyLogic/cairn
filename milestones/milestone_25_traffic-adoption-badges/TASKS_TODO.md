# TASKS TODO

## Verify Inactivity Disable Precedent Evidence

Establish, with read-only `gh api` calls against the public REST API, that the action's daily push keeps a scheduled workflow clear of GitHub's 60-day inactivity disable: read the live state of `albertoarena/github-traffic-badge` — its scheduled traffic workflow still `active` past day 60 since the last human commit of 2026-07-05, with only `github-actions[bot]` pushes to `traffic-data` and every run schedule-triggered — and then, after each distribution repository's first scheduled run at 03:17 UTC, confirm the same signal there: `pushed_at` advanced and a public PushEvent on `refs/heads/traffic-data`. Record the dated observations both in the Inactivity evidence decision of `requirements.md` and in this task's `**Verified:**` entry. Verified when both readings are recorded with their dates and the distribution repositories' workflow state reads `active`.

---
