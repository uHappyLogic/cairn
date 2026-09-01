# TASKS TODO

## Consolidate CLAUDE.md Invariants Section

Rewrite the `## Invariants to preserve when editing skills` section of `CLAUDE.md` as a whole, once and only after every runtime-file deduplication task above has finished, merging overlapping bullets and absorbing the rationale those tasks appended or extended, so that every cut the sweep justified against an invariant still has its survival home in the consolidated text. This single pass replaces the append-or-extend-only freeze the sweep worked under and must precede the fresh-context re-audit. Verified by its own constraint-preservation ledger over `CLAUDE.md` in this task's `TASKS_DONE.md` entry — one `**Verified:**` bullet per invariant merged or reshaped, naming the consolidated bullet where its content now lives — rather than by the runtime layer's ledgers.

---

## Verify README Claims Against Swept Layer

Run a verification pass over `README.md`'s skill reference and workflow prose against the deduplicated runtime layer and consolidated `CLAUDE.md`, editing only where a sweep edit made an existing claim false and adding no new prose — in particular, no sentence describing the runtime-files-never-restate-invariants authoring convention, whose single home is the CLAUDE.md invariant. Verified by a `**Verified:**` list in this task's `TASKS_DONE.md` entry naming each README claim checked and, for any edit made, the runtime change that falsified it.

---

## Run Fresh-Context Runtime Layer Re-Audit

In a fresh context, audit every `skills/*/SKILL.md`, `agents/*.md`, and `shared/*.md` file plus the sweep tasks' `**Verified:**` ledgers (checking each ledger claim against the live file, with git history supplying the original text) and report findings without fixing anything, classifying each as a blocking lost constraint (an imperative removed with no surviving home, or a ledger claim that does not hold) or a residual restatement (a remaining `## Rules` heading, editor-facing rationale still in a runtime file, or cross-file narration beyond the one contract sentence). Exclude residuals already registered with a reason in `temp/milestone_15_findings.md`, and return a clean verdict only when there are zero loss findings and no unregistered residuals; findings that are not clean become follow-up fix tasks queued ahead of the two tasks below, followed by a further whole-layer re-audit, repeating until a run is clean. Verified by the classified findings list and verdict recorded in this task's `TASKS_DONE.md` entry.

---

## Measure And Report Word-Count Removal

Measure the actual word removal of the sweep with `wc -w` over `skills/`, `agents/`, and `shared/` against the 32,758-word baseline, and report it in total and per cut class (summing the per-class figures the deduplication tasks' ledgers recorded) as the honest outcome against the non-binding roughly 11,000-word target, treating any shortfall as information only and never as a trigger for further cuts. Verified by the total and per-class figures recorded in this task's `TASKS_DONE.md` entry alongside the baseline they are measured against.

---

## Extend Transpile Script And Regenerate Tree

Extend `scripts/migrate_skills_to_agy.py` with a wholesale copy of `shared/` into `.agents/plugins/cairn/`, in the shape of the existing `agents/` copytree, so every `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference in the generated skills and agents resolves to a present file, then run `uv run scripts/migrate_skills_to_agy.py` once the re-audit loop has closed so the checked-in tree reflects the final deduplicated layer; rewriting the `${CLAUDE_PLUGIN_ROOT}` reference text to an Antigravity-resolvable path stays out of scope and is recorded as a follow-up in this task's `TASKS_DONE.md` entry. Verified by inspecting the regenerated file list for the 7 `shared/` files and by confirming every generated `SKILL.md` and agent file is byte-identical to its source.

---
