# TASKS TODO

## Tool List Alternatives Filters

Retire `list --unannotated` and give `list` two symmetric filters, `--without-alternatives` (blocks carrying no `<alternative>` children) and `--without-recommendation` (today's `--unannotated` meaning), re-pointing the five test files that spell the old flag (`test_list.py`, `test_sort.py`, `test_walk.py`, `test_embed.py`, `test_strip.py`). The alternatives pass dispatches on the first filter, the recommendation pass stops on it and skips on the second. Verified by both pytest runs passing with no `--unannotated` left under `core/tools/` or `tests/`.

---

## Tool Two-Shape Embed Subcommand

Give `embed` a required, mutually exclusive `--alternatives` / `--recommendation` flag pair over one shared validation core: `--alternatives` slices between its own first and last `<alternative>` anchor lines, is accepted only when the block carries no `<alternative>` yet, and writes only the alternatives; `--recommendation` is accepted only when the block carries at least one `<alternative>` and no `<recommendation>` yet, validates the recommendation's `option` against the block's own alternative ids, resolves each `<depends-on>` against a sibling that carries `<alternative>` children and one of that sibling's ids (the target-carries-a-`<recommendation>` half of the check dropped), and writes only its own child kinds so the alternative set stays frozen between the passes. Verified by `tests/test_embed.py` pinning every refusal reason of both shapes under both pytest runs.

---

## Split Shared Recommend Procedure

Split `core/shared/recommend-procedure.md` into an enumeration half at a new `core/shared/alternatives-procedure.md` — its own grounding step plus the 2–4 honest alternatives with what-it-is / key advantage / key drawback, loading neither the principle store nor the disclosure duty — and a pick half that keeps the `recommend-procedure.md` path, self-contained with its own grounding step, the principle store as a weighted advisory factor, the sibling-dependency disclosure duty, and one hedge-free recommendation over an alternative set it takes as input. Two runners at different times are two units of work, so the halves are two texts. Verified by both files reading as execution-neutral procedures and `uv run scripts/build_hosts.py --check` passing after a rebuild.

---

## Rename Agent To Alternatives-Only

Move `core/agents/recommend-open-question.md` to `core/agents/provide-alternatives-to-open-question.md`, update its frontmatter `name`, and make it an alternatives-only read-only subagent that follows the enumeration procedure and returns only the `<alternative>` elements with their `<advantage>` and `<drawback>` children, its step-4 self-check bounded by first non-whitespace text starting `<alternative` and last non-whitespace text ending `</alternative>`, a `FAILED: <reason>` last line on failure. Re-point every reference to the old name under `core/` and `docs/`. Verified by the build passing and grep finding the old name in neither tree.

---

## Provide Alternatives Sweep Skill

Create `core/skills/provide-alternatives-to-all-open-questions/SKILL.md`, an orchestrator that gathers with `list`, `list --without-alternatives`, and `locate`, dispatches `cairn:provide-alternatives-to-open-question` once per question lacking alternatives — all together where the host can run several agent dispatches at once and one after another where it cannot, in one capability-keyed sentence with no cap — and runs the three-stage per-return pipeline on each return as it lands (last-line `FAILED:` verdict, `embed --alternatives` through a quoted heredoc, one repair with the corrective template rewritten for the alternatives-only fragment). It commits each embedded return under `Alternatives-annotation: <Short Title>` with no body and reports `Alternatives embedded.`, the no-op line, or the still-skipped advisory. Verified by a frontmatter description within 25 words, the build passing, and a run over a milestone with bare blocks landing one commit per block.

---

## Inline Recommendation Pass Skill

Rewrite `core/skills/recommend-all-open-questions/SKILL.md` as an inline skill that dispatches no agents: it stops when `list --without-alternatives` prints anything, gathers `list --without-recommendation`, reads the document whole, follows the pick procedure over the whole set at once, and embeds each block's `<recommendation>`, `<depends-on>`, and `<applied-principle>` with `embed --recommendation` in any order, leaving standing recommendations untouched, picking the best surviving alternative of a stale set with the killed option named in the rationale, and skipping only a set with nothing left (naming the full strip plus an alternatives re-run). It commits once per run under `Recommendation-annotation: <milestone_id>` with one `lift` line per annotated question as the body, gathered after the embeds and before the end-of-run sort and its `Question-ordering:` commit, keeping the three report lines with `strip --recommendation` plus a re-run as the revision hatch. Verified by the build passing and a run over a milestone whose blocks carry alternatives landing that one commit.

---

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
