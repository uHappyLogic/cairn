# Milestone 11: Terse Skill Reporting

## Goal

Reduce token spend on runtime console reporting across the file-mutating skills and orchestrators. Every skill that changes files and commits its work should, on the success path, print only a single terse status line (e.g. "Milestone defined.", "All tasks completed.", "Recommendations embedded.") instead of a prose summary of what it did — the committed diff and git log are the durable record, so re-narrating that work to the console is redundant.

Apply by editing each affected skill's SKILL.md directly (no shared reporting-convention file). Cut everything on the success path to the bare status line, also removing the next-step/follow-up pointers these skills print, including finish-current-milestone's runtime recommendation of /capture-milestone-principle-updates (retiring that runtime behavior; the handoff stays documented).

Out of scope / unchanged: the inherently conversational skills (discuss-milestone-goal, discuss-open-question, discuss-new-task, ask-in-milestone-context) are untouched; failure and clean-stop paths keep their full explanatory messages (only success reporting goes terse); and no skill's file-writing behavior changes — for review-milestone-requirements in particular, only its console messages are trimmed, its requirements.md edits are untouched.

Additionally, all project documentation (CLAUDE.md, README.md, and any affected invariants — e.g. the invariant stating finish-current-milestone "recommends at runtime" capture-milestone-principle-updates) must be updated to reflect this terse-reporting change.

## Relevant starting state

### Per-skill success-path reporting (the "Confirm"/"Report" step)

Every file-mutating, committing skill ends its `## Workflow` with a dedicated final step that narrates the success path to the console — variously titled "Confirm" (`define-milestone-goal` step 6, `specify-milestone-starting-state` step 7, `finish-current-milestone` step 9, `goto-next-milestone` step 5, `submit-task` step 6), "Report findings" (`answer-open-question` step 5, `answer-open-question-with-recommendation` step 3, `answer-open-question-with-alternative` step 6), "Report" (`recommend-all-open-questions` step 6, `answer-all-open-questions-with-recommendation` step 3, `capture-milestone-principle-updates` step 6), "Report and hand off" (`modify-milestone-goal` step 6), "Report convergence" (`review-milestone-requirements` step 5), "Verify coverage and report" (`derive-tasks` step 8), "Report completion" (`complete-all-tasks` step 3), or "Hand back" (`complete-task` step 3). These steps currently instruct a prose summary — e.g. `define-milestone-goal` reports the directory created and goal written; `answer-open-question` restates which question resolved, how the document changed, and any cascades; `derive-tasks` lists the ordered task titles; `finish-current-milestone` reports the milestone name, task count, the bullet list written to README, and the pointer clear. This re-narrates work the committed diff and `git log` already record.

### Embedded next-step / handoff pointers

Most of these report steps also print a "Suggest the next step" pointer to the following skill: `define-milestone-goal` → `/specify-milestone-starting-state`, `specify-milestone-starting-state` and `goto-next-milestone` → `/review-milestone-requirements` / `/specify-milestone-starting-state`, `review-milestone-requirements` → `/discuss-open-question` or `/answer-open-question` plus a `/derive-tasks`-readiness verdict, `recommend-all-open-questions` → the two `answer-…-with-recommendation` consumers, `modify-milestone-goal` → `/review-milestone-requirements`. These handoff pointers are part of the success-path output the goal targets for removal (the handoffs remain documented in README/CLAUDE.md).

### finish-current-milestone's runtime recommendation of capture

`finish-current-milestone` step 9 does more than report: after clearing the pointer it prints an ordered "Suggest the next steps" block whose first item **recommends running `/capture-milestone-principle-updates`** ("Recommended now that the milestone has just closed … but never auto-run"), second item `/define-milestone-goal`. This runtime recommendation is called out in the goal for retirement (the handoff stays documented, not printed). It is pinned as an invariant in `CLAUDE.md` (the layout line and the ordering invariant both say `finish-current-milestone` "**recommends (never auto-runs)**" capture) and described in `README.md` (the *Ending a milestone* prose and the answer-principle-learning-loop section).

### Orchestrator reporting

The four orchestrators report over their whole run, not one item: `complete-all-tasks` step 3 reports "all tasks completed" and lists every task done; `recommend-all-open-questions` step 6 reports which questions were annotated vs. skipped plus the consumer pointer; `answer-all-open-questions-with-recommendation` step 3 reports per-answer outcomes; `derive-tasks` step 8 summarizes the ordered titles and flags coverage gaps. Their failure/partial paths (e.g. `complete-all-tasks` "stop the loop and report which task failed") are separate from the success reporting.

### Dispatched agents (not console reporters)

The per-item agents (`agents/complete-task.md`, `agents/submit-task.md`, `agents/recommend-open-question.md`, `agents/answer-open-question-with-recommendation.md`) return a structured `DONE`/`FAILED` (or the ready-to-embed XML) to their orchestrator rather than printing user-facing console output, so they are not sources of the redundant success narration this milestone targets — the reporting lives in the user-facing SKILL.md files.

### Out-of-scope neighbors (for boundary clarity)

The purely conversational skills — `discuss-milestone-goal`, `discuss-open-question`, `discuss-new-task`, `ask-in-milestone-context` — change no files and produce no commit; the goal leaves them untouched. The two non-committing exempt skills (`init-milestone-base-workflow`, `migrate-workspace`) leave changes staged for the user. Failure and clean-stop paths (parse errors, Short-Title mismatches, the `answer-open-question` redirect guard, no-matching-id stops) keep their full explanatory messages — only success reporting is in scope. No skill's file-writing or commit behavior changes; `review-milestone-requirements` in particular keeps its `requirements.md` edits and only trims console messages.

### There is no shared reporting-convention file

Reporting is authored inline in each SKILL.md's final step — there is no shared `report-procedure.md` analogous to `shared/commit-procedure.md`. The goal mandates editing each affected SKILL.md directly rather than introducing one. (For contrast, `shared/commit-procedure.md` centralizes commit mechanics and emits no console narration of its own.)

### Documentation to update

Two docs describe this behavior and must track the change: `CLAUDE.md` (the `finish-current-milestone` layout line at ~line 60 and the ordering invariant at ~line 98, both asserting the runtime "recommends (never auto-runs)" of capture) and `README.md` (the *Ending a milestone* prose at ~line 188 and the learning-loop/skill-reference sections that mention the runtime recommendation and the per-skill "suggest next step" behavior).

## Decisions

### Terse status line shape

The single terse success line is a fixed sentence with no identifier (exactly the goal's examples — "Milestone defined.", "All tasks completed."); it does not carry the milestone id, task heading, or commit subject. Each orchestrator prints one such line for the whole run, with no per-item output during the loop.

### Non-redundant advisory output

Genuinely git-absent advisory output is preserved on the success path rather than collapsed into the terse status line: the terse cut removes only re-narration of the committed diff, while decision-critical information the commit never captured — review-milestone-requirements' convergence verdict and still-open list, derive-tasks' flag for any requirement it could not trace to a task, and the answer skills' note about newly-exposed open questions — is kept alongside the terse status line. Every success-path output that is a diff re-narration still collapses.

### No-op pass reporting

When a committing skill's pass changes no files and its dirty-own-path no-op guard fires, it does not collapse to the terse success line: because a no-op commits nothing, git holds no durable record, so the console must carry the explanation. Such a pass prints a concise one-line message stating that nothing changed and briefly why (distinct from the terse success line) — mirroring how failure and clean-stop paths keep their full explanatory messages and how commit-procedure already instructs to "report the no-op". Terse success reporting is earned only where the committed diff and git log are the durable record.

### Codifying the terse-reporting convention

Beyond revising the specific existing CLAUDE.md text this change touches, a dedicated standalone invariant is added to CLAUDE.md's "Invariants to preserve when editing skills" section codifying the terse-success-reporting rule (success path prints one terse status line; failure/clean-stop paths keep full messages; conversational and exempt skills untouched). The cross-cutting convention needs a durable authoritative home, and with no shared reporting-convention file to carry it the standalone invariant is the only such home — mirroring how the equally cross-cutting commit convention earns its own invariant rather than being folded into another already-overloaded paragraph.

## Out of Scope

## Open questions

