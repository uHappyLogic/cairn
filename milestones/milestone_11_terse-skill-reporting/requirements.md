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

## Out of Scope

## Open questions

<open-question id="No-op pass reporting" status="open">
  <question>When a committing skill's pass changes no files and its dirty-own-path no-op guard fires (for example a review-milestone-requirements pass that reconciled nothing, a recommend sweep that found no open questions, or a capture pass that distilled no principle), there is no commit or diff to serve as the durable record the terse-reporting rationale relies on. Should such a no-op pass still collapse to a single terse status line, and if so what should it convey, or should it keep an explanatory message precisely because nothing was recorded to git?</question>
  <alternative id="Concise explanatory no-op line">
    The no-op path prints a short one-line message stating that nothing changed and briefly why (e.g. &quot;No open questions found; nothing to recommend.&quot;), distinct from the terse success line, on the grounds that with no commit or diff the console is the only record — aligning the no-op with the failure and clean-stop paths the milestone already exempts from the terse cut.
    <advantage>Honors the terse-reporting rationale exactly: terseness is justified only because git holds the durable record, and a no-op leaves git untouched, so the console must carry the explanation — mirroring the goal&apos;s own decision to keep full messages on failure/clean-stop paths and the commit procedure&apos;s existing &quot;report the no-op&quot; step.</advantage>
    <drawback>Adds a distinct no-op branch to author and keep worded in each committing skill, marginally more than one uniform status line.</drawback>
  </alternative>
  <alternative id="Bare terse no-op line">
    Collapse the no-op to a single fixed bare status line of its own (e.g. &quot;Nothing to recommend.&quot;) — terse like the success line, just a different sentence, carrying no &quot;why&quot;.
    <advantage>Keeps one uniform terse rule with minimal wording while still letting the user distinguish a no-op from a real change.</advantage>
    <drawback>A bare line with no git backing can under-explain why nothing happened when the user expected a change, and the console is the sole record so the missing &quot;why&quot; cannot be recovered from a diff.</drawback>
  </alternative>
  <alternative id="Reuse the success terse line">
    Print the same terse success line regardless of whether the pass changed anything, making the no-op indistinguishable from a real committed change.
    <advantage>Absolute simplicity — one line and one branch, no special no-op handling at all.</advantage>
    <drawback>Actively misleading: the user cannot tell a real change from a no-op, and unlike a genuine success there is no diff or commit to inspect, so it hides a possibly surprising &quot;nothing happened&quot; outcome behind a confirmation of success.</drawback>
  </alternative>
  <recommendation option="Concise explanatory no-op line">Terse reporting is earned only where the committed diff and git log are the durable record; a no-op commits nothing, so — exactly as the milestone already keeps failure and clean-stop paths explanatory and as commit-procedure already instructs to &quot;report the no-op&quot; — the no-op path should keep a concise one-line message saying nothing changed and why.</recommendation>
</open-question>

<open-question id="Non-redundant advisories" status="open">
  <question>Some skills emit success-path output that is not a re-narration of the committed diff but genuinely new information absent from the git log: review-milestone-requirements' convergence verdict and still-open list, derive-tasks' flag for any requirement it could not trace to a task, and the answer skills' note about new open questions an answer may have exposed. Does the terse cut apply to this non-redundant advisory output too, collapsing it to the bare status line, or is git-log-absent advisory information exempt and preserved on the success path?</question>
  <alternative id="Preserve advisories">
    Exempt genuinely git-absent advisory output and keep it on the success path: the terse cut removes only diff re-narration, while decision-critical information the commit never captured &mdash; review-milestone-requirements&apos; convergence verdict and still-open list, derive-tasks&apos; untraceable-requirement flag, the answer skills&apos; newly-exposed-question note &mdash; is preserved alongside the status line.
    <advantage>Faithful to the milestone&apos;s own stated rationale (re-narration is redundant because git is the durable record), which by construction does not reach information absent from git, and it keeps each loop-engine skill&apos;s decision-critical reason to exist &mdash; a bare &quot;Requirements reviewed.&quot; would force a re-read or re-run to learn whether the doc is ready for derive-tasks, plausibly costing more tokens than the cut saves.</advantage>
    <drawback>Introduces a per-skill judgment about what counts as &quot;non-redundant advisory&quot; versus &quot;narration,&quot; softening the clean bright-line rule and leaving room for a skill to justify keeping prose.</drawback>
  </alternative>
  <alternative id="Collapse everything">
    Apply the terse cut uniformly with no exemption, collapsing the advisory output to the bare status line too; the user re-derives convergence, coverage gaps, or newly-exposed questions by re-reading requirements.md or re-running the skill.
    <advantage>An unambiguous bright-line rule with zero per-skill judgment, maximally faithful to the goal text&apos;s literal &quot;cut everything on the success path to the bare status line&quot; and to token minimization.</advantage>
    <drawback>Guts the function of the very skills whose purpose is the advisory: review-milestone-requirements exists to report convergence, and derive-tasks explicitly mandates &quot;flag as a gap &mdash; never silently omit&quot; &mdash; collapsing these silently drops the one output the user ran the skill to get, likely inverting the token goal via re-runs.</drawback>
  </alternative>
  <alternative id="Fold into status line">
    Keep a single line but let it carry the git-absent scalar &mdash; e.g. &quot;Requirements reviewed &mdash; 2 open, not ready for derive-tasks.&quot; &mdash; so the discipline of one line holds while the decision-critical bit survives.
    <advantage>Reconciles the literal single-line instruction with substance, preserving the readiness/coverage signal at near-zero token cost.</advantage>
    <drawback>Multi-item advisories (a long still-open list, several coverage gaps) do not fit one scalar line, stretching &quot;bare status line&quot; past its intent, and it prejudges the separate &quot;Terse line shape&quot; open question by deciding what the line may contain.</drawback>
  </alternative>
  <recommendation option="Preserve advisories">Preserve genuinely git-absent advisory output; the milestone&apos;s redundancy rationale does not reach information the diff and git log never captured, and the convergence verdict, coverage-gap flag, and newly-exposed-question note are each skill&apos;s decision-critical reason to run &mdash; while every output that is a diff re-narration still collapses. Recommended over folding-into-the-line because that answers the separate &quot;Terse line shape&quot; question and cannot hold multi-item advisories.</recommendation>
</open-question>

<open-question id="Terse-reporting invariant" status="deferred">
  <question>Beyond revising the existing CLAUDE.md text this change affects, should a dedicated CLAUDE.md invariant be added that codifies the terse-success-reporting rule itself so future skill edits inherit the convention, or is updating the existing affected wording sufficient?</question>
  <alternative id="Add dedicated invariant">
    Add a new standalone paragraph to CLAUDE.md's "Invariants to preserve when editing skills" section that codifies the terse-success-reporting rule (success path prints one terse status line; failure/clean-stop paths keep full messages; conversational and exempt skills untouched), alongside revising the specific affected wording.
    <advantage>Gives the cross-cutting convention a single durable home so every future committing skill inherits it — matching exactly how the commit convention is pinned as its own big invariant, and doing so is more necessary here because this milestone adds no shared reporting-convention file to otherwise carry the rule.</advantage>
    <drawback>Adds another long paragraph to an already very long invariants list, and unlike the commit invariant it can point to no shared procedure as the mechanism's source of truth.</drawback>
  </alternative>
  <alternative id="Fold into commit invariant">
    Extend the existing "Committing is a property of the skill layer" invariant with a terse-reporting clause rather than adding a separate one, since both scope to the same set of file-mutating committing skills.
    <advantage>Keeps the invariants list from growing and co-locates the rule with the closely related "committing skill" scope it shares.</advantage>
    <drawback>That invariant is already the section's most overloaded paragraph; appending an unrelated-mechanism clause buries the reporting rule where a future editor scanning for reporting guidance would not find it, weakening the very inheritance the codification is meant to provide.</drawback>
  </alternative>
  <alternative id="Update affected wording only">
    Revise just the specific existing text this change touches (the finish-current-milestone "recommends at runtime" invariant lines and layout line) and add no invariant codifying the general rule.
    <advantage>Smallest, most conservative edit — exactly the documentation scope the milestone goal already names, with no net-new invariant prose to maintain.</advantage>
    <drawback>Leaves the cross-cutting convention uncaptured anywhere authoritative, so a future skill author has no single rule stating "success path = one terse line" and can silently drift back to prose reporting — the precise regression a codified convention prevents.</drawback>
  </alternative>
  <recommendation option="Add dedicated invariant">A terse-reporting rule that binds every future committing skill needs a durable authoritative home, and with no shared reporting-convention file to carry it the standalone invariant is the only such home — directly mirroring how the equally cross-cutting commit convention earns its own invariant, while folding it into that already-overloaded commit paragraph would bury it.</recommendation>
</open-question>

