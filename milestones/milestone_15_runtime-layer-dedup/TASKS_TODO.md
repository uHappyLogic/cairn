# TASKS TODO

## Seventh Whole-Layer Runtime Re-Audit Pass

In a fresh context, repeat the whole-layer audit over every `skills/*/SKILL.md`, `agents/*.md`, and `shared/*.md` file plus the sweep tasks' `**Verified:**` ledgers (checking each ledger claim against the live file, with git history supplying the original text) once the fix task above has landed, reporting findings without fixing anything and classifying each as a blocking lost constraint or a residual restatement, exactly as the six prior re-audits did. Exclude residuals already registered with a reason in `temp/milestone_15_findings.md`, and return a clean verdict only when there are zero loss findings and no unregistered residuals; findings that are not clean become further fix tasks queued ahead of the two remaining tasks, followed by another whole-layer re-audit, repeating until a run is clean. Verified by the classified findings list and verdict recorded in this task's `TASKS_DONE.md` entry.

---

## Extend Transpile Script And Regenerate Tree

Extend `scripts/migrate_skills_to_agy.py` with a wholesale copy of `shared/` into `.agents/plugins/cairn/`, in the shape of the existing `agents/` copytree, so every `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference in the generated skills and agents resolves to a present file, then run `uv run scripts/migrate_skills_to_agy.py` once the re-audit loop has closed so the checked-in tree reflects the final deduplicated layer; rewriting the `${CLAUDE_PLUGIN_ROOT}` reference text to an Antigravity-resolvable path stays out of scope and is recorded as a follow-up in this task's `TASKS_DONE.md` entry. Verified by inspecting the regenerated file list for the 7 `shared/` files and by confirming every generated `SKILL.md` and agent file is byte-identical to its source.

---
