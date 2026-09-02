# TASKS TODO

## Clear Capture Opening-Paragraph Reasoning Restatement

Cut the residual restatement the fourth whole-layer re-audit found — `skills/capture-milestone-principle-updates/SKILL.md:10-11`'s "Those commit bodies are where the reusable reasoning lives — the alternatives weighed, the trade-off accepted." — whose two halves are both carried with strictly more runner-facing detail by step 2's body-reading bullet at `:58-60` ("**Read the commit bodies, not just the subjects.** … the reusable reasoning is in the **body**") and step 3.1's extraction instruction at `:70-72` ("the realistic alternatives that were weighed, why one was chosen, the trade-off accepted"), so the *Step-less rule placement* decision does not sanction the opening-paragraph copy; cut it only after confirming its content survives at those points of use, or else register it in `temp/milestone_15_findings.md` with the reason it was not fixed. In the same pass, repoint the `**Verified:**` ledger bullet at `TASKS_DONE.md:420` that names the cut sentence as a live home ("the runner-facing 'Those commit bodies are where the reusable reasoning lives' stays"), since an unrepointed citation becomes a blocking loss finding in the next re-audit. Verified by a per-file constraint-preservation ledger carrying one bullet per passage cut or registered and one per ledger bullet repointed, naming where that content now survives, together with confirmation that no runner-facing instruction was removed and no frontmatter `description` was edited.

---

## Repoint Seventeen Stale Ledger Citations

Rewrite the seventeen `**Verified:**` ledger citations in `TASKS_DONE.md` that no longer hold against the live tree, since a ledger claim that does not hold is a blocking loss finding the milestone cannot register away: the fourteen bullets whose `CLAUDE.md` line numbers the *Consolidate CLAUDE.md Invariants Section* task renumbered so they now land on wholly unrelated invariants — `:78` (its "lines 78, 80, 81, 86, and 90" belong at 77, 78, 79 and 83), `:399`/`:400`/`:404`/`:428` ("line 97" belongs at 90), `:421`/`:422`/`:423`/`:430` ("line 98" belongs at 90), `:451`/`:452`/`:453` ("line 100" belongs at 91), and `:459`/`:464` ("line 95" belongs at 88) — plus three wrong glosses: `:280`'s "whose three bullets each carry their own list-the-available-ids instruction" (the middle guard bullet instead points the user at `/recommend-all-open-questions`), `:518`'s "the boundary-line CLI with the explicit no-`xmllint` clause survives in" seven named locations (only `skills/recommend-all-open-questions/SKILL.md`, `skills/answer-all-open-questions-with-recommendation/SKILL.md`, and `skills/discuss-open-question/SKILL.md` carry the `xmllint` negation), and `:516`'s citation of `define-milestone-goal` step 5 for the directory-creation claim that lives in step 4. Each rewrite must name the content's live location confirmed by opening it rather than by trusting the old pointer, and no runtime file under `skills/`, `agents/`, or `shared/` is edited. Verified by a ledger carrying one bullet per citation repointed, naming the live location it now cites and confirming that location resolves.

---

## Fifth Whole-Layer Runtime Re-Audit Pass

In a fresh context, repeat the whole-layer audit over every `skills/*/SKILL.md`, `agents/*.md`, and `shared/*.md` file plus the sweep tasks' `**Verified:**` ledgers (checking each ledger claim against the live file, with git history supplying the original text) once the two fix tasks above have landed, reporting findings without fixing anything and classifying each as a blocking lost constraint or a residual restatement, exactly as the four prior re-audits did. Exclude residuals already registered with a reason in `temp/milestone_15_findings.md`, and return a clean verdict only when there are zero loss findings and no unregistered residuals; findings that are not clean become further fix tasks queued ahead of the two remaining tasks, followed by another whole-layer re-audit, repeating until a run is clean. Verified by the classified findings list and verdict recorded in this task's `TASKS_DONE.md` entry.

---

## Measure And Report Word-Count Removal

Measure the actual word removal of the sweep with `wc -w` over `skills/`, `agents/`, and `shared/` against the 32,758-word baseline, and report it in total and per cut class (summing the per-class figures the deduplication tasks' ledgers recorded) as the honest outcome against the non-binding roughly 11,000-word target, treating any shortfall as information only and never as a trigger for further cuts. Verified by the total and per-class figures recorded in this task's `TASKS_DONE.md` entry alongside the baseline they are measured against.

---

## Extend Transpile Script And Regenerate Tree

Extend `scripts/migrate_skills_to_agy.py` with a wholesale copy of `shared/` into `.agents/plugins/cairn/`, in the shape of the existing `agents/` copytree, so every `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference in the generated skills and agents resolves to a present file, then run `uv run scripts/migrate_skills_to_agy.py` once the re-audit loop has closed so the checked-in tree reflects the final deduplicated layer; rewriting the `${CLAUDE_PLUGIN_ROOT}` reference text to an Antigravity-resolvable path stays out of scope and is recorded as a follow-up in this task's `TASKS_DONE.md` entry. Verified by inspecting the regenerated file list for the 7 `shared/` files and by confirming every generated `SKILL.md` and agent file is byte-identical to its source.

---
