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
