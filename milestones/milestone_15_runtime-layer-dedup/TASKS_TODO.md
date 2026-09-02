# TASKS TODO

## Clear Three Opening-Paragraph Restatements From Layer

Cut or register the three residual restatements the third whole-layer re-audit found: `skills/answer-open-question-with-recommendation/SKILL.md:39-40`'s justification tail "— that would discard the recording context this skill exists to keep" (the last surviving instance of a clause the sweep already cut from both sibling skills, `skills/complete-task/SKILL.md` and `skills/answer-open-question-with-alternative/SKILL.md`, with its content standing at `:8-9` and in the CLAUDE.md inline-vs-isolated invariant), `skills/capture-milestone-principle-updates/SKILL.md:19`'s "It captures only genuinely reusable rules, and never writes the store without the user's explicit say-so." (a two-clause rule whose halves are carried with strictly more runner-facing value by step 3.2 at `:79-83` and step 4.2 at `:117`, so the Step-less rule placement decision does not sanction the opening-paragraph copy), and the same file's `:17` "Presence of an entry means it is confirmed — there is no status field." (duplicating the step-4a schema bullet "**No status field.** Presence in the file means confirmed." at `:153`, the point where the runner actually authors an entry). Each is cut only after confirming its content survives at its point of use or in a CLAUDE.md invariant, or else registered in `temp/milestone_15_findings.md` with the reason it was not fixed; in the same pass, repoint the three `**Verified:**` ledger bullets that name the cut text as a live home — `TASKS_DONE.md:271` ("stay inline"), `:421` ("stays in the opening paragraph"), and `:416` ("and in the opening paragraph") — since an unrepointed citation becomes a blocking loss finding in the next re-audit. Verified by a per-file constraint-preservation ledger carrying one bullet per passage cut or registered and one per ledger bullet repointed, naming where that content now survives, together with confirmation that no runner-facing instruction was removed and no frontmatter `description` was edited.

---

## Fourth Whole-Layer Runtime Re-Audit Pass

In a fresh context, repeat the whole-layer audit over every `skills/*/SKILL.md`, `agents/*.md`, and `shared/*.md` file plus the sweep tasks' `**Verified:**` ledgers (checking each ledger claim against the live file, with git history supplying the original text) once the residual task above has landed, reporting findings without fixing anything and classifying each as a blocking lost constraint or a residual restatement, exactly as the three prior re-audits did. Exclude residuals already registered with a reason in `temp/milestone_15_findings.md`, and return a clean verdict only when there are zero loss findings and no unregistered residuals; findings that are not clean become further fix tasks queued ahead of the two remaining tasks, followed by another whole-layer re-audit, repeating until a run is clean. Verified by the classified findings list and verdict recorded in this task's `TASKS_DONE.md` entry.

---

## Measure And Report Word-Count Removal

Measure the actual word removal of the sweep with `wc -w` over `skills/`, `agents/`, and `shared/` against the 32,758-word baseline, and report it in total and per cut class (summing the per-class figures the deduplication tasks' ledgers recorded) as the honest outcome against the non-binding roughly 11,000-word target, treating any shortfall as information only and never as a trigger for further cuts. Verified by the total and per-class figures recorded in this task's `TASKS_DONE.md` entry alongside the baseline they are measured against.

---

## Extend Transpile Script And Regenerate Tree

Extend `scripts/migrate_skills_to_agy.py` with a wholesale copy of `shared/` into `.agents/plugins/cairn/`, in the shape of the existing `agents/` copytree, so every `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference in the generated skills and agents resolves to a present file, then run `uv run scripts/migrate_skills_to_agy.py` once the re-audit loop has closed so the checked-in tree reflects the final deduplicated layer; rewriting the `${CLAUDE_PLUGIN_ROOT}` reference text to an Antigravity-resolvable path stays out of scope and is recorded as a follow-up in this task's `TASKS_DONE.md` entry. Verified by inspecting the regenerated file list for the 7 `shared/` files and by confirming every generated `SKILL.md` and agent file is byte-identical to its source.

---
