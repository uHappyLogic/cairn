# TASKS TODO

## Reconcile Residual Heading/State Echoes With Completed Renames

Two skills still carry "implementation"-flavored prose that names sections this milestone already renamed, leaving them inconsistent with the shipped vocabulary. `answer-open-question` reports document changes as "implementation-decision updates", which must reflect the renamed `## Decisions` section. `goto-next-milestone` suggests the user "fill in the implementation context", referring to the section now named `## Relevant starting state` (written by `specify-milestone-starting-state`). Reword both so they read as plain, domain-neutral English consistent with the completed renames, without changing what either skill does.

**Notes:**
- The two sites: `skills/answer-open-question/SKILL.md` (the "what changed" reporting line — "implementation-decision updates") and `skills/goto-next-milestone/SKILL.md` (the next-step suggestion — "fill in the implementation context").
- Match the already-shipped vocabulary: decisions live under `## Decisions`; the baseline section is `## Relevant starting state`. Do not reintroduce a retired term.

**Success:**
- `git grep -ni implementation -- skills/answer-open-question skills/goto-next-milestone` returns zero hits.
- Both skills still describe the same behavior (answer-open-question still reports which parts of the document changed; goto-next-milestone still points at filling the starting-state section as the next step).

---

## Retire Coding-Flavored "Implementation Phase" Framing In Highlight-Open-Questions

`highlight-milestone-requirements-open-questions/SKILL.md` repeatedly frames the post-requirements work as "implementation" — the phase, its choices, and when it "begins" (e.g. "ready enough for implementation", "the implementation phase", "leave implementation choices ambiguous", "force a wrong implementation", "before implementation begins", "decided during implementation", "begin implementation"). This is the coding-specific vocabulary the milestone's goal retires so the plugin reads as a generic idea-to-done workflow. Reword these to domain-neutral terms that preserve the skill's logic, keeping the Blocking/Deferred question distinction intact (Blocking = must be resolved before the work starts; Deferred = settle while doing the work).

**Notes:**
- Per the project's *Prefer domain-neutral terms* answering principle, word choice is case-by-case — pick the natural neutral phrasing per sentence (e.g. "the work", "before work begins", "while doing the work", "at completion time"); do not mechanically substitute one fixed token.
- Scope is this one file. Do not touch the protected/renamed handles or headings — only the generic "implementation" prose.

**Success:**
- `git grep -ni implement -- skills/highlight-milestone-requirements-open-questions` returns zero hits.
- The skill still distinguishes Blocking from Deferred questions and still emits the `> **Deferred — <Short Title>:**` annotation format unchanged.

---

## Sweep Scattered Generic "Implementation" Prose From The Authoring/Clarification Skills

Four skills still use the word "implementation"/"implementable" incidentally in prose, leftover coding flavor the milestone's goal retires: `discuss-new-task` ("ambiguous implementation issue", "mid-implementation", "full implementation detail", "independently implementable", "concrete implementation issue" — including in its `description:` frontmatter), `submit-task` ("single implementation issue", "implementation-ready task" — including its `description:` frontmatter), `derive-tasks` ("independently-implementable task briefs", "satisfied by the current implementation" ×2), and `specify-milestone-starting-state` ("internal implementation detail"). Reword each to neutral English that keeps the meaning (e.g. "issue", "mid-flight", "detail", "independently completable", "the existing/current code").

**Notes:**
- Per the *Prefer domain-neutral terms* answering principle, choose phrasing case-by-case; some hits sit in the skills' `description:` frontmatter (their discoverability text) — reword those too, keeping the description's trigger meaning intact.
- Leave the renamed handles/headings and the `complete`/`derive`/`submit` vocabulary already shipped untouched — this task only retires the residual generic "implementation" wording in these four files.

**Success:**
- `git grep -ni implement -- skills/discuss-new-task skills/submit-task skills/derive-tasks skills/specify-milestone-starting-state` returns zero hits.
- Each skill's `description:` frontmatter still reads coherently and conveys the same when-to-use trigger.

---
