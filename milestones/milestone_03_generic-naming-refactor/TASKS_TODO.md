# TASKS TODO

## Sweep Scattered Generic "Implementation" Prose From The Authoring/Clarification Skills

Four skills still use the word "implementation"/"implementable" incidentally in prose, leftover coding flavor the milestone's goal retires: `discuss-new-task` ("ambiguous implementation issue", "mid-implementation", "full implementation detail", "independently implementable", "concrete implementation issue" — including in its `description:` frontmatter), `submit-task` ("single implementation issue", "implementation-ready task" — including its `description:` frontmatter), `derive-tasks` ("independently-implementable task briefs", "satisfied by the current implementation" ×2), and `specify-milestone-starting-state` ("internal implementation detail"). Reword each to neutral English that keeps the meaning (e.g. "issue", "mid-flight", "detail", "independently completable", "the existing/current code").

**Notes:**
- Per the *Prefer domain-neutral terms* answering principle, choose phrasing case-by-case; some hits sit in the skills' `description:` frontmatter (their discoverability text) — reword those too, keeping the description's trigger meaning intact.
- Leave the renamed handles/headings and the `complete`/`derive`/`submit` vocabulary already shipped untouched — this task only retires the residual generic "implementation" wording in these four files.

**Success:**
- `git grep -ni implement -- skills/discuss-new-task skills/submit-task skills/derive-tasks skills/specify-milestone-starting-state` returns zero hits.
- Each skill's `description:` frontmatter still reads coherently and conveys the same when-to-use trigger.

---
