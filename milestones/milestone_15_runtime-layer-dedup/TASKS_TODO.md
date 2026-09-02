# TASKS TODO

## Correct One False Ledger Grep Claim

Rewrite the false evidence parenthetical in the `**Verified:**` ledger bullet at `TASKS_DONE.md:863`, since a ledger claim that does not hold against the live tree is a blocking loss finding the milestone cannot register away: its assertion that grepping for `line 97`, `line 98`, `line 100`, `line 95`, `line-98`, and `lines 78, 80` over the ledgers "returns no hit outside the *Consolidate CLAUDE.md Invariants Section* entry's own old-line remap table" does not reproduce — the grep returns 21 lines, of which only `:497` is that remap table, while `:492`/`:495`/`:496` are separate old-line bullets in the same entry and `:827`, `:859`, and `:864`-`:877` sit outside it entirely. Rewrite the parenthetical to name the hit classes that actually remain (the Consolidate entry's own old-line bullets and remap table, the fourth re-audit's historical LOSS-1 finding list, and this task's own description and per-citation ledger bullets, all of which necessarily quote the old numbers as history), without weakening the bullet's substantive claim that all seventeen citations were rewritten and without touching any other ledger text or any file under `skills/`, `agents/`, or `shared/`. Verified by re-running the stated grep and confirming every line it returns falls into a class the rewritten parenthetical names.

---

## Sixth Whole-Layer Runtime Re-Audit Pass

In a fresh context, repeat the whole-layer audit over every `skills/*/SKILL.md`, `agents/*.md`, and `shared/*.md` file plus the sweep tasks' `**Verified:**` ledgers (checking each ledger claim against the live file, with git history supplying the original text) once the fix task above has landed, reporting findings without fixing anything and classifying each as a blocking lost constraint or a residual restatement, exactly as the five prior re-audits did. Exclude residuals already registered with a reason in `temp/milestone_15_findings.md`, and return a clean verdict only when there are zero loss findings and no unregistered residuals; findings that are not clean become further fix tasks queued ahead of the two remaining tasks, followed by another whole-layer re-audit, repeating until a run is clean. Verified by the classified findings list and verdict recorded in this task's `TASKS_DONE.md` entry.

---

## Measure And Report Word-Count Removal

Measure the actual word removal of the sweep with `wc -w` over `skills/`, `agents/`, and `shared/` against the 32,758-word baseline, and report it in total and per cut class (summing the per-class figures the deduplication tasks' ledgers recorded) as the honest outcome against the non-binding roughly 11,000-word target, treating any shortfall as information only and never as a trigger for further cuts. Verified by the total and per-class figures recorded in this task's `TASKS_DONE.md` entry alongside the baseline they are measured against.

---

## Extend Transpile Script And Regenerate Tree

Extend `scripts/migrate_skills_to_agy.py` with a wholesale copy of `shared/` into `.agents/plugins/cairn/`, in the shape of the existing `agents/` copytree, so every `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference in the generated skills and agents resolves to a present file, then run `uv run scripts/migrate_skills_to_agy.py` once the re-audit loop has closed so the checked-in tree reflects the final deduplicated layer; rewriting the `${CLAUDE_PLUGIN_ROOT}` reference text to an Antigravity-resolvable path stays out of scope and is recorded as a follow-up in this task's `TASKS_DONE.md` entry. Verified by inspecting the regenerated file list for the 7 `shared/` files and by confirming every generated `SKILL.md` and agent file is byte-identical to its source.

---
