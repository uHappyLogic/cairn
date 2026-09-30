# TASKS TODO

## State New Rules In Skill Reference And Claims

Update `docs/skill-reference.md` to state the enumeration rules briefly in the `discuss-open-question`, `provide-alternatives-to-all-open-questions`, and alternatives-subagent entries and the one-axis rule in the `review-milestone-requirements` entry, and rewrite claim 4's Design in `docs/design-claims.md` to say the alternatives are distinct and cover the decision, with no count and its Metric line left as it is. Both pages otherwise still describe the retired count guideline. It is verified by reading those entries against the final runtime wording, finding no count guideline for alternatives left in either page, and confirming `docs/workflow.md` is unedited.

---

## Lower Alternatives Pass Effort In Usage Chains

In `docs/ways-of-using-cairn.md`, move every `provide-alternatives-to-all-open-questions` line from `--effort xhigh` to `--effort high` on `opus` and change each prose sentence naming that line's effort with it, so the page shows the setting the alternatives pass actually runs at. It is verified by no alternatives-pass line or sentence on the page naming `xhigh`, with every other chain line's settings unchanged.

---

## Add Distinct And Covering Invariant Bullet

Add one dedicated bullet to the invariants section of `CLAUDE.md` explaining why an alternative set must be distinct and covering (every two options differ in substance on an axis, and the set covers the underlying decision, including dropping the thing where viable), why the "two to four" count guideline was removed and must not be restored, why each option states its axis positions, and how the one-axis authoring rule in `review-milestone-requirements` stops the set from growing. It records the rationale the runtime files leave out, stating the rule and its generic failure patterns without measurement figures. It is verified by reading the bullet against the final runtime wording and confirming it carries no figure and nothing from the benchmark data.

---

## Write Benchmark Harness Idea Document

Write the uncommitted idea document under `temp/` for a committed benchmark harness, drawing on how the one-off re-run check was prepared, run, and judged. The goal names it as one of the milestone's two idea documents, since the repository holds no harness, eval directory, or judge. It is verified by the file existing under `temp/`, describing the harness concretely enough to seed a future milestone, and `git status` showing nothing new to commit from it.

---

## Write Question Framing Idea Document

Write the uncommitted idea document under `temp/` on further improvements to how `review-milestone-requirements` frames questions: shared premises, splitting existing compound questions, and the four candidate tests for detecting a second axis (an independent-settlement test, surface-wording cues, an option-grid preview, and an independence test prompted by wording cues). The goal names it as the second idea document, and the one-axis decision carries those detection tests into it for a separate future milestone. It is verified by the file existing under `temp/` with every one of those topics covered and `git status` showing nothing new to commit from it.

---
