# TASKS DONE

## Replace Independence Clause With Disclosure Duty

Rewrite `shared/recommend-procedure.md` step 1 so the "never treat another question's recommendation as an input" clause is replaced by a caller-neutral disclosure duty: when a recommendation leans on a still-open sibling's recommendation, name that sibling and the option assumed. Add the one sentence `skills/discuss-open-question/SKILL.md` needs so its inline run renders that duty as prose. Verified by reading both files: no independence wording remains and the duty is stated once, in the core, with no XML markup.

**Verified:**

- `shared/recommend-procedure.md` step 1 contains no independence wording — no "formed in isolation", no "never treat another question's recommendation as an input".
- Step 1 states a caller-neutral disclosure duty once: when a recommendation leans on a still-open sibling's recommendation, name that sibling and the option assumed.
- The core carries no XML markup for the duty (no `<depends-on>` or other element name).
- `skills/discuss-open-question/SKILL.md` gains exactly one sentence directing its inline run to render that duty as prose (naming sibling and option), without restating the duty's substance or adding markup.
- No other step in either file changes.

---

## Render Depends-On Elements In Recommend Agent

Update `agents/recommend-open-question.md` so step 1 drops the independence rule (sibling recommendations already embedded are legitimate inputs) and step 3's rendering spec gains the self-closing `<depends-on question="Short Title" option="Option"/>` element, emitted only for a sibling that already carries embedded children in the block the agent read, naming that sibling's `id` and one of its `<alternative>` ids, placed after the alternatives and any `<applied-principle>` elements and immediately before `<recommendation>`. A coupling on a sibling not yet annotated is expressed as prose inside the affected `<drawback>` or the rationale, with no option-less tag form; step 4's two-test self-check stays unchanged. Verified by reading: the shape example shows the child order alternatives, applied-principles, depends-on, recommendation, and the emit-only-when-target-annotated rule is explicit.

**Verified:**

- Step 1 of `agents/recommend-open-question.md` no longer says "never treat another question's recommendation as an input"; it states that a sibling already carrying embedded children in the block the agent read is a legitimate input.
- Step 3's shape example contains a self-closing `<depends-on question="…" option="…"/>` line placed after the `<applied-principle>` line and immediately before `<recommendation>`, so the child order shown is alternatives, applied-principles, depends-on, recommendation.
- Step 3 states the emit-only-when-target-annotated rule explicitly: a `<depends-on>` element is emitted only for a sibling that already carries embedded children in the block the agent read, naming that sibling's `id` and one of its `<alternative>` ids.
- Step 3 states that a coupling on a not-yet-annotated sibling is expressed as prose inside the affected `<drawback>` or the rationale, with no option-less tag form.
- Step 4's two-test self-check (first text `<alternative`, last text `</recommendation>`) is byte-identical to its pre-task form.
- Frontmatter unchanged (parses under `yaml.safe_load`, 19-word description) and `uv run scripts/migrate_skills_to_agy.py` succeeds, regenerating the agent's copy under `.agents/plugins/cairn/agents/`.

---

## Sequential Ordered Dispatch In Recommend Sweep

Rework `skills/recommend-all-open-questions/SKILL.md` steps 1–4 so the sweep ranks its surviving questions most-significant-first by judgment over only what the gather yields (each block's `id`, `status`, and `<question>` text, reading no more of `requirements.md`), dispatches strictly sequentially, and embeds each accepted region by whole-block-replacement `Edit` before the next dispatch so later agents read the embedded siblings; the repair attempt then runs immediately for that question rather than "while the other dispatches are still in flight". Extend the embedded-block example with a `<depends-on>` line, and extend the escape-hatch note so a regenerated block whose new option differs from what surviving dependents assumed leaves those dependents exactly as they are, with no mismatch advisory. Verified by reading: no parallel or independence language remains, and the commit still happens once at the end.

**Verified:**

- Step 3 opens by ranking the surviving questions most-significant-first by judgment over exactly what step 1's gather yielded — each block's `id`, `status`, and `<question>` text — and states that no more of `requirements.md` is read to rank them.
- Dispatch is stated as strictly sequential in that order, with each question judged and embedded or skipped before the next is dispatched; `grep -i` finds no "independent"/"in parallel"/"never feed"/"in flight"/"interleave" dispatch language left (the only "independent" hit is the pre-existing attribute-order remark on regex extraction; "never in parallel" is the prohibition itself).
- Step 4 embeds each accepted region by whole-block-replacement `Edit` immediately, before the next dispatch, and states that later agents read the embedded siblings in `requirements.md`.
- Sub-step d runs the single repair immediately for that question, before the next dispatch; the "while the other dispatches are still in flight" wording and the interleaving repair-spent-marker rationale are gone, with the one-repair-per-question limit kept.
- The embedded-block example carries a `<depends-on question="…" option="…"/>` line between `<applied-principle>` and `<recommendation>`, the parenthetical covers its once-per-embedded-sibling-or-none cardinality, and step 3's return description names the element.
- The step-2 escape hatch lists `<depends-on>` among the children to delete and states that a regenerated block whose new option differs from what surviving dependents assumed leaves those dependents exactly as they are — no strip, no `option` rewrite, no mismatch advisory — with reconciliation left to the answer-time cascade.
- Step 5 still commits once at the end of the run, never inside the dispatch loop; the gate (six tests) and corrective message are untouched for the next task.
- Frontmatter unchanged (parses under `yaml.safe_load`, 18-word description); `uv run scripts/migrate_skills_to_agy.py` succeeds and the regenerated `.agents/plugins/cairn/skills/recommend-all-open-questions/SKILL.md` differs from the source only by the path rewrite.

---

## Add Dependency Resolution Gate Test

Add a seventh test to the acceptance gate in `skills/recommend-all-open-questions/SKILL.md` step 3c that resolves every returned `<depends-on>` line against the `<open-question>` blocks still present under `## Open questions` that carry embedded children (without reading `status`) and the target's `<alternative id` lines, with entity-unescaped case-folded comparison, and a miss producing a reason string that takes the single repair attempt and skips only on a second failure, exactly like the other structural misses; no cycle test is added. Update the fixed corrective message so its element ordering names the `<depends-on>` elements between the applied-principles and the recommendation. Verified by reading: the gate lists seven line-grep tests, the orchestrator never edits or drops a returned element, and the reason strings name the new test.

**Verified:**

- Step 3c's acceptance gate lists exactly seven numbered line-grep tests; test 7 resolves every `<depends-on` line in the region — its `question` value against the `id` of an `<open-question>` block still present under `## Open questions` that carries embedded children, and its `option` value against that target block's `<alternative id` values — with entity escapes reversed and case-folding on both sides, attributes read by attribute-name-anchored regex.
- Test 7 states it reads no `status` (a `status="deferred"` target is as valid as an open one), reaches into the live document only by re-slicing the `## Open questions` section with step 1's boundary-line CLI, resolves one hop only, and adds no cycle check (`grep cycle` hits only that no-cycle-check sentence).
- The reason-string list names the new test's two misses (`a depends-on question value names no still-present annotated <open-question> id`, `a depends-on option value matches none of the target block's <alternative> ids`); the miss paragraph routes a test-7 miss through the single repair attempt and second-failure skip like every other structural miss, and states it is never resolved by dropping or rewriting the offending line — step 4's "never edits, reorders, or drops a returned element" sentence is intact.
- The fixed corrective message orders the elements as `<alternative>`, then `<applied-principle>`, then `<depends-on>`, then the single `<recommendation>`.
- `git diff -U0` shows hunks only in sub-steps 3c and 3d; frontmatter parses under `yaml.safe_load` with an 18-word description.
- `uv run scripts/migrate_skills_to_agy.py` succeeds and the regenerated `.agents/plugins/cairn/skills/recommend-all-open-questions/SKILL.md` differs from the source only by the shared-path rewrite.

---

## Extend Answer Cascade With Dependency Reconciliation

Widen `shared/answer-procedure.md` to three inputs by adding an optional RECORDED OPTION (the un-escaped option or alternative id the caller lifted), whose presence selects exact id comparison and whose absence selects a judgment of whether ANSWER invalidates the assumed option, and extend step 6's cascade so that after the answered block and any mooted entries are removed, every surviving block whose `<depends-on question="…">` names a removed block is reconciled: an agreeing option deletes only that `<depends-on>` line, while a disagreeing option, an inconclusive judgment, or a target removed as a mooted entry with no option strips that dependent's embedded children transitively, leaving the bare `<open-question>` wrapper and `<question>` for the next recommend sweep. The core prints nothing and stays execution-neutral, and the fold-before-remove order is preserved. Verified by reading: both branches are stated once, "strip on doubt" is explicit, and no anchor-string parsing enters the core.

**Verified:**

- `## Inputs` in `shared/answer-procedure.md` declares three inputs — SHORT TITLE, ANSWER, and an optional RECORDED OPTION described as the un-escaped `<recommendation option>` / `<alternative id>` value the caller lifted; its presence selects exact id comparison and its absence selects a judgment of whether ANSWER invalidates the assumed option, and the core states it never derives it by parsing ANSWER (no `<option> — <rationale>` anchor parsing; `grep rationale` finds no hit in the core).
- Step 6 reconciles, only after the answered block and every mooted entry are removed, every surviving block whose `<depends-on question="…">` (attribute-name-anchored regex, entity-unescaped, case-folded as step 2 matches `id`) names a removed block.
- The agreeing branch is stated once: matching option (equal ids with RECORDED OPTION, or ANSWER plainly leaving the assumed option standing without it) deletes only that one `<depends-on …/>` line, leaving the block's other children intact.
- The disagreeing branch is stated once and covers differing ids, an inconclusive judgment, and a target removed as a mooted entry with no recorded option; it strips every child between `<question>` and `</open-question>`, leaving the bare wrapper and `<question>` for the next recommend sweep, and stripping is stated as transitive over dependents of stripped blocks.
- "Strip on doubt" is explicit ("whenever the agreeing case cannot be affirmed, this branch applies").
- The core stays execution-neutral and silent: `grep -Ei 'commit|DONE|FAILED|git add|print|console'` finds no hit, and the reconciliation states it produces no report of its own.
- Fold-before-remove is preserved: step 4 (fold) still precedes step 5 (remove), the cascade stays step 6 and last, and step 5's child list now also names `<depends-on>`.
- `uv run scripts/migrate_skills_to_agy.py` succeeds and `.agents/plugins/cairn/shared/answer-procedure.md` differs from the source only by the `${CLAUDE_PLUGIN_ROOT}` path rewrite.

---

## Pass Recorded Option From Lifting Callers

Update the three callers of the recording core so `shared/answer-with-recommendation-procedure.md` step 4 passes the un-escaped `option` value it lifted as RECORDED OPTION, `skills/answer-open-question-with-alternative/SKILL.md` step 4 passes the un-escaped chosen `id`, and `skills/answer-open-question/SKILL.md` step 3 explicitly passes no RECORDED OPTION so the cascade takes the judgment mode. Verified by reading the three delegation sentences, with no other step in those files changed.

**Verified:**

- `shared/answer-with-recommendation-procedure.md` step 4's delegation sentence hands `shared/answer-procedure.md` the resolved SHORT TITLE, the derived ANSWER, and — as RECORDED OPTION — the un-escaped `option` value lifted in step 3, passed separately so the core compares it as an exact id rather than parsing ANSWER.
- `skills/answer-open-question-with-alternative/SKILL.md` step 4's delegation sentence hands the core `<Short Title>`, the derived ANSWER, and — as RECORDED OPTION — the un-escaped chosen alternative `id` from step 3, on the same separate-not-parsed terms.
- `skills/answer-open-question/SKILL.md` step 3 passes SHORT TITLE and ANSWER and explicitly passes **no** RECORDED OPTION, stating that a literal answer lifts no option id so the core's cascade takes its judgment mode (deciding from the ANSWER prose whether each dependent's assumed option still stands).
- No other step in those three files changed: `git diff -U0` shows one hunk at each delegation sentence and, in the with-recommendation procedure only, a matching one-clause amendment to the non-step `## Inputs` hand-off sentence so it no longer contradicts step 4.
- Both skills' frontmatter still loads under `yaml.safe_load` with their descriptions unchanged (18 and 19 words).
- `uv run scripts/migrate_skills_to_agy.py` succeeds and the three regenerated copies under `.agents/plugins/cairn/` differ from their sources only by the `${CLAUDE_PLUGIN_ROOT}` path rewrite and echo-hint drop.

---
