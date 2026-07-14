# Milestone 11: Terse Skill Reporting

## Goal

Reduce token spend on runtime console reporting across the file-mutating skills and orchestrators. Every skill that changes files and commits its work should, on the success path, print only a single terse status line (e.g. "Milestone defined.", "All tasks completed.", "Recommendations embedded.") instead of a prose summary of what it did — the committed diff and git log are the durable record, so re-narrating that work to the console is redundant.

Apply by editing each affected skill's SKILL.md directly (no shared reporting-convention file). Cut everything on the success path to the bare status line, also removing the next-step/follow-up pointers these skills print, including finish-current-milestone's runtime recommendation of /capture-milestone-principle-updates (retiring that runtime behavior; the handoff stays documented).

Out of scope / unchanged: the inherently conversational skills (discuss-milestone-goal, discuss-open-question, discuss-new-task, ask-in-milestone-context) are untouched; failure and clean-stop paths keep their full explanatory messages (only success reporting goes terse); and no skill's file-writing behavior changes — for review-milestone-requirements in particular, only its console messages are trimmed, its requirements.md edits are untouched.

Additionally, all project documentation (CLAUDE.md, README.md, and any affected invariants — e.g. the invariant stating finish-current-milestone "recommends at runtime" capture-milestone-principle-updates) must be updated to reflect this terse-reporting change.

## Relevant starting state

## Decisions

## Out of Scope

