# TASKS TODO

## Resolve Four Remaining Layer Residuals

Cut or register the four residual restatements the third whole-layer re-audit found: `shared/recommend-procedure.md:67-68`'s closing "How that unit is laid out, marked up, and either shown to the user or handed back for embedding is the wrapper's concern, not this file's." (editor-addressed boundary narration restating the head paragraph's own "The caller supplies the one input below and renders the result" clause at `:6-8`, while the runner-facing contiguous-unit constraint at `:65-67` must stay), `shared/complete-procedure.md:162-163`'s "The `**Verified:**` label is the completion record and is deliberately distinct from any label a task list uses to author work." (design justification carried in the CLAUDE.md task-altitude invariant, sitting in the layer's hottest per-task file), `skills/submit-task/SKILL.md:14`'s "Never queue a duplicate of an existing pending or completed task." (folded into the opening paragraph although the rule is not step-less, since step 2's duplicate check at `:43` already carries it with strictly more runner-facing value), and `skills/answer-all-open-questions-with-recommendation/SKILL.md:87-89`'s "The agent owns **all** document mutation but does **not** commit — it records the answer and hands the recorded-but-uncommitted edit back. You commit it (step 2c) before dispatching the next question, so one commit = one answer." (repeating the opening contract paragraph at `:17-20`, the sentence immediately above it at `:85`, and step 2c at `:95` and `:105`). Each is cut only after confirming its content survives at its point of use in the same file or in a CLAUDE.md invariant, or else registered in `temp/milestone_15_findings.md` with the reason it was not fixed, since the milestone cannot converge while an unregistered residual stands. Verified by a per-file constraint-preservation ledger carrying one bullet per passage cut or registered, naming where that content now survives, together with confirmation that no runner-facing instruction was removed and no frontmatter `description` was edited.

---

## Repoint Three Stale Ledger Citations

Rewrite the three `**Verified:**` ledger claims in `TASKS_DONE.md` that the residual cleanups falsified, since a ledger claim that does not hold against the live file is a blocking loss finding the milestone cannot register away: `:71`'s citation of `shared/recommend-procedure.md`'s now-cut Inputs-scope home "Rendering the result and any side-effects are the caller's job.", `:306`'s claim that "Add no `refresh`/selectable mode" survives at its point of use in `skills/recommend-all-open-questions/SKILL.md` step 2's escape-hatch paragraph, and `:462`'s quotation of the live heading as `## Migration catalog (the extension point)`; fix in the same pass the two off-by-one citations at `:670` (`:70-72`) and `:687` (`:68-69`), both of which now name a line past the end of the 68-line `shared/recommend-procedure.md`. Each bullet is rewritten to name a home actually in force against the live tree — the surviving same-file sentence, the matching `CLAUDE.md` invariant, or both — without weakening the claim or touching any other ledger text, and the same repointing is applied to any further ledger citation the preceding residual-cleanup task newly invalidates. Verified by re-reading each rewritten bullet against the live files it cites and confirming every quoted fragment resolves and every named survival home is in force.

---

## Third Whole-Layer Runtime Re-Audit Pass

In a fresh context, repeat the whole-layer audit over every `skills/*/SKILL.md`, `agents/*.md`, and `shared/*.md` file plus the sweep tasks' `**Verified:**` ledgers (checking each ledger claim against the live file, with git history supplying the original text) once the two fix tasks above have landed, reporting findings without fixing anything and classifying each as a blocking lost constraint or a residual restatement, exactly as the three prior re-audits did. Exclude residuals already registered with a reason in `temp/milestone_15_findings.md`, and return a clean verdict only when there are zero loss findings and no unregistered residuals; findings that are not clean become further fix tasks queued ahead of the two remaining tasks, followed by another whole-layer re-audit, repeating until a run is clean. Verified by the classified findings list and verdict recorded in this task's `TASKS_DONE.md` entry.

---

## Measure And Report Word-Count Removal

Measure the actual word removal of the sweep with `wc -w` over `skills/`, `agents/`, and `shared/` against the 32,758-word baseline, and report it in total and per cut class (summing the per-class figures the deduplication tasks' ledgers recorded) as the honest outcome against the non-binding roughly 11,000-word target, treating any shortfall as information only and never as a trigger for further cuts. Verified by the total and per-class figures recorded in this task's `TASKS_DONE.md` entry alongside the baseline they are measured against.

---

## Extend Transpile Script And Regenerate Tree

Extend `scripts/migrate_skills_to_agy.py` with a wholesale copy of `shared/` into `.agents/plugins/cairn/`, in the shape of the existing `agents/` copytree, so every `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference in the generated skills and agents resolves to a present file, then run `uv run scripts/migrate_skills_to_agy.py` once the re-audit loop has closed so the checked-in tree reflects the final deduplicated layer; rewriting the `${CLAUDE_PLUGIN_ROOT}` reference text to an Antigravity-resolvable path stays out of scope and is recorded as a follow-up in this task's `TASKS_DONE.md` entry. Verified by inspecting the regenerated file list for the 7 `shared/` files and by confirming every generated `SKILL.md` and agent file is byte-identical to its source.

---
