# TASKS TODO

## Correct Three Remaining False Ledger Claims

Correct the three `**Verified:**` ledger claims in `TASKS_DONE.md` that the sixth re-audit found do not hold against the live tree, since a false ledger claim is a blocking loss finding the milestone cannot register away: at `:893` the two commit hashes are swapped against their task titles (`4e6ec51` is *Clear Capture Opening-Paragraph Reasoning Restatement*, which edited the capture skill, and `31c8257` is *Repoint Seventeen Stale Ledger Citations*, which touched only the two task-list files — the same entry contradicts itself at `:903`); at `:895` the claim that "the only nine bullets naming a now-cut passage" are the nine it lists is falsified by `:420`, a tenth such bullet that names the cut "Those commit bodies are where the reusable reasoning lives" passage and is itself already repointed; and at `:134` the gloss "each naming the full `<open-question …>`-through-`</open-question>` deletion" is false because only the first two of `skills/review-milestone-requirements/SKILL.md`'s three step-2 reconcile bullets (`:67`, `:68`) name that span, the flag-don't-delete bullet at `:69` carrying no deletion-span text. Rewrite each so it states what actually holds, without weakening any bullet's substantive claim (both fix tasks did land; no bullet still names a cut passage as a live home; the whole-block-removal rule does survive in bullets 1 and 2 and in the `CLAUDE.md` invariant) and without touching any other ledger text or any file under `skills/`, `agents/`, or `shared/`. Verified by re-resolving each corrected claim against the live tree and git history.

---

## Seventh Whole-Layer Runtime Re-Audit Pass

In a fresh context, repeat the whole-layer audit over every `skills/*/SKILL.md`, `agents/*.md`, and `shared/*.md` file plus the sweep tasks' `**Verified:**` ledgers (checking each ledger claim against the live file, with git history supplying the original text) once the fix task above has landed, reporting findings without fixing anything and classifying each as a blocking lost constraint or a residual restatement, exactly as the six prior re-audits did. Exclude residuals already registered with a reason in `temp/milestone_15_findings.md`, and return a clean verdict only when there are zero loss findings and no unregistered residuals; findings that are not clean become further fix tasks queued ahead of the two remaining tasks, followed by another whole-layer re-audit, repeating until a run is clean. Verified by the classified findings list and verdict recorded in this task's `TASKS_DONE.md` entry.

---

## Measure And Report Word-Count Removal

Measure the actual word removal of the sweep with `wc -w` over `skills/`, `agents/`, and `shared/` against the 32,758-word baseline, and report it in total and per cut class (summing the per-class figures the deduplication tasks' ledgers recorded) as the honest outcome against the non-binding roughly 11,000-word target, treating any shortfall as information only and never as a trigger for further cuts. Verified by the total and per-class figures recorded in this task's `TASKS_DONE.md` entry alongside the baseline they are measured against.

---

## Extend Transpile Script And Regenerate Tree

Extend `scripts/migrate_skills_to_agy.py` with a wholesale copy of `shared/` into `.agents/plugins/cairn/`, in the shape of the existing `agents/` copytree, so every `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference in the generated skills and agents resolves to a present file, then run `uv run scripts/migrate_skills_to_agy.py` once the re-audit loop has closed so the checked-in tree reflects the final deduplicated layer; rewriting the `${CLAUDE_PLUGIN_ROOT}` reference text to an Antigravity-resolvable path stays out of scope and is recorded as a follow-up in this task's `TASKS_DONE.md` entry. Verified by inspecting the regenerated file list for the 7 `shared/` files and by confirming every generated `SKILL.md` and agent file is byte-identical to its source.

---
