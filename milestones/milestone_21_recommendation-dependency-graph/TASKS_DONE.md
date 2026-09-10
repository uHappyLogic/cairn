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
