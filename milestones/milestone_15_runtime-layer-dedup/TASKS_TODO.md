# TASKS TODO

## Relocate Migrate-Workspace Maintainer Prose

Move the two maintainer-facing sentences left in `skills/migrate-workspace/SKILL.md`'s
`## Migration catalog (the extension point)` section — "**Each future milestone that changes a
workspace artifact appends one entry here**; the workflow below applies whatever the catalog
contains, so the procedure never changes — only this list grows" and "If a template later changes,
update the matching catalog entry's `Rewrite to` so the destination tracks it" — into a matching
`CLAUDE.md` invariant first and then cut them from the runtime file, since both address someone
registering a future migration rather than the runner executing one and neither changes what a
`/migrate-workspace` run does. Because that same prose is the survival home the completed sweep's
ledger cited when cutting the file's `## Adding a future migration` section, the corresponding
`TASKS_DONE.md` bullet must be repointed at the new `CLAUDE.md` home in the same pass so no ledger
claim is falsified by the cut. Verified by confirming the two sentences are absent from the
`SKILL.md`, present in the `CLAUDE.md` invariant, and cited there by the repointed ledger bullet,
with the runner-facing "Treat those templates as the authority for the target state" instruction
and every catalog entry left intact.

---

## Re-Audit Runtime Layer After Fixes

In a fresh context, repeat the whole-layer audit over every `skills/*/SKILL.md`, `agents/*.md`, and
`shared/*.md` file plus the sweep tasks' `**Verified:**` ledgers (checking each ledger claim against
the live file, with git history supplying the original text) once the two fix tasks above have
landed, reporting findings without fixing anything and classifying each as a blocking lost
constraint or a residual restatement, exactly as the first re-audit did. Exclude residuals already
registered with a reason in `temp/milestone_15_findings.md`, and return a clean verdict only when
there are zero loss findings and no unregistered residuals; findings that are not clean become
further fix tasks queued ahead of the two remaining tasks, followed by another whole-layer
re-audit, repeating until a run is clean. Verified by the classified findings list and verdict
recorded in this task's `TASKS_DONE.md` entry.

---


## Measure And Report Word-Count Removal

Measure the actual word removal of the sweep with `wc -w` over `skills/`, `agents/`, and `shared/` against the 32,758-word baseline, and report it in total and per cut class (summing the per-class figures the deduplication tasks' ledgers recorded) as the honest outcome against the non-binding roughly 11,000-word target, treating any shortfall as information only and never as a trigger for further cuts. Verified by the total and per-class figures recorded in this task's `TASKS_DONE.md` entry alongside the baseline they are measured against.

---

## Extend Transpile Script And Regenerate Tree

Extend `scripts/migrate_skills_to_agy.py` with a wholesale copy of `shared/` into `.agents/plugins/cairn/`, in the shape of the existing `agents/` copytree, so every `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference in the generated skills and agents resolves to a present file, then run `uv run scripts/migrate_skills_to_agy.py` once the re-audit loop has closed so the checked-in tree reflects the final deduplicated layer; rewriting the `${CLAUDE_PLUGIN_ROOT}` reference text to an Antigravity-resolvable path stays out of scope and is recorded as a follow-up in this task's `TASKS_DONE.md` entry. Verified by inspecting the regenerated file list for the 7 `shared/` files and by confirming every generated `SKILL.md` and agent file is byte-identical to its source.

---
