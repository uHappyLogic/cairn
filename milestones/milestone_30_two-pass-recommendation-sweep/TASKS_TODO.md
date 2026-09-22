# TASKS TODO

## Discuss Reuses Frozen Alternatives

Update `core/skills/discuss-open-question/SKILL.md` to work on a question in any state: when the block carries embedded `<alternative>` elements it reuses them as the option set (an option the set lacks may be put on the table marked as a departure), and when bare it follows the enumeration procedure first; it then follows the pick procedure to state one recommendation of its own, showing any embedded `<recommendation>` beside it as the sweep's standing pick and saying plainly whether the two agree and why. Verified by the skill referencing both procedures in order, the build passing, and a dry run on an annotated block and on a bare one.

---

## Narrow Cascade Prose In Answer Path

Rewrite the sentences in `core/shared/answer-procedure.md`, `core/skills/review-milestone-requirements/SKILL.md`, and `core/skills/answer-all-open-questions-with-recommendation/SKILL.md` that describe the cascade's strip outcome so they state the narrowed contract: a stripped dependent loses its `<recommendation>`, `<depends-on>`, and `<applied-principle>` children, keeps its `<alternative>` children, and is the recommendation pass's to re-pick. Verified by grep finding no runtime sentence still claiming a dependent is stripped to its `<question>` and the build passing.

---

## Sync CLAUDE.md To Two-Pass Shape

Update `CLAUDE.md`: the layout entries for the new skill, the renamed agent, the new shared procedure, the tool's subcommand list, and the test files; the pipeline listing; the four invariants (the sweep, the agent's rendering, the answer-recording cascade, the dispatched-agent return contract); the commit conventions with `Alternatives-annotation: <Short Title>` and `Recommendation-annotation: <milestone_id>`; the reporting carve-out with `Alternatives embedded.`; and every `--unannotated` mention. Verified by grep finding no `--unannotated`, no `recommend-open-question`, and no strip-to-bare claim left, and every invariant describing the behaviour the runtime files now carry.

---

## Sync Docs Pages To Two-Pass Shape

Update `docs/workflow.md`'s "Iterating milestone requirements" diagram and prose to add a `/provide-alternatives-to-all-open-questions` node between the review and recommend nodes, the README's simplified loop diagram to match, and `docs/skill-reference.md` with an entry for the new skill, the renamed agent's entry, and rewritten `recommend-all-open-questions` and `discuss-open-question` entries. Verified by the mermaid blocks rendering, `--check` passing, and no stale flag or agent name left in `docs/` or `README.md`.

---

## Headless Chains Add Alternatives Line

Update `docs/ways-of-using-cairn.md`: insert `claude -p "/cairn:provide-alternatives-to-all-open-questions" --dangerously-skip-permissions --model "opus" --effort xhigh` between the review and recommend lines of every chain carrying a recommend line, change every `/cairn:recommend-all-open-questions` line to `--model "fable" --effort high`, and rewrite each affected way's settings sentence to name the two settings (the stuck-milestone way no longer states that every line runs at max). Ordered last because the two skills must exist before the page records them. Verified by every fenced line being runnable as written and the page's three sibling links intact.

---
