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
