# Milestone 21: Recommendation Dependency Graph

## Goal

Make `recommend-all-open-questions` dispatch sequentially in most-significant-first order, embedding each result before the next dispatch, so every recommendation may build on sibling recommendations already embedded and must declare each such use as a `<depends-on question="Short Title" option="Option"/>` child of its block, pointing only at still-open siblings. Extend the shared answer procedure's cascade so that recording an answer either removes the dependents' matching tags when the recorded option agrees with what they assumed, or strips the dependents' embedded children transitively when it disagrees (an exact id comparison for alternative and recommendation answers, a judgment of whether the recorded answer invalidates the assumed option for manual answers), leaving those blocks for the next recommend sweep to regenerate; the answer sweep walks the dependency graph from its origins. Retires the recommendation-independence invariant.

## Relevant starting state

### Recommend sweep (`skills/recommend-all-open-questions/SKILL.md`)

The sweep gathers every `status="open"`/`status="deferred"` block once via the boundary-line CLI, skips any block already containing a `<recommendation>` element, and dispatches one `cairn:recommend-open-question` agent per surviving question. Step 3 declares the dispatches independent and explicitly parallelizable ("never feed one question's recommendation into another"), and step 4 embeds every accepted return after all dispatches by whole-block-replacement `Edit`, inserting the children between `<question>` and `</open-question>` at a 2-space indent. Each return passes a four-stage pipeline: last-line `FAILED:` verdict, extraction from the first `<alternative` line to the last `</recommendation>` line, a six-test acceptance gate, then one repair (same-session `SendMessage`, else one fresh re-dispatch). Gate test 3 forbids only `<open-question>`/`</open-question>`/`<question>`/`</question>` lines, so an additional child element line passes the gate today unexamined; tests 4–6 check exactly one `<recommendation` line, at least one `<alternative id` line, and an `option` value matching an alternative id. The documented refresh path for a stale recommendation is manual: delete the block's embedded children, keep the wrapper and `<question>`, re-run. It commits once at the end under `Recommendation-annotation: <milestone_id>`.

### Recommend agent and shared core (`agents/recommend-open-question.md`, `shared/recommend-procedure.md`)

The agent's prompt carries the Short Title, `<MILESTONE_DIR>`, and the question's full block; it reads `requirements.md` and the live project read-only, so it already sees sibling blocks and whatever children they carry. Its rendering spec (step 3) names exactly three child element kinds — `<alternative id>` with `<advantage>`/`<drawback>`, `<applied-principle>`, `<recommendation option>` — with entity escaping and one-element-per-citation for `<applied-principle>`. Its step 4 self-check runs only the two boundary tests (first text `<alternative`, last text `</recommendation>`). The "never treat another question's recommendation as an input" rule is stated in three runtime places — `recommend-procedure.md` step 1, the agent's step 1, and the sweep's step 3 — and once as the "Recommendation independence" clause of the `recommend-all-open-questions` invariant in `CLAUDE.md`. `discuss-open-question` runs the same shared core inline for one question and renders no XML.

### Shared answer procedure (`shared/answer-procedure.md`)

Execution-neutral core with three callers: `answer-open-question` (literal ANSWER, `Manual-answer:`), `shared/answer-with-recommendation-procedure.md` (ANSWER lifted as `<option> — <rationale>`, `Recommendation-answer:`, run by the skill inline and by the agent in the sweep), and `answer-open-question-with-alternative` (ANSWER lifted as `<id> — <what-it-is>`, `Alternative-answer:`). Steps: locate the block by case-folded, entity-unescaped `id` via the CLI; analyse; fold into `## Decisions`; delete the whole block as a re-queried line range; cascade. Step 6's cascade has exactly two outcomes per sibling — mooted (fold its implied constraint, remove it) or untouched — and nothing in the procedure edits a surviving sibling's embedded children. The two lifting callers read the block's `<recommendation option>` / `<alternative id>` before delegating, so the recorded option is known to them; the literal caller passes prose and knows no option.

### Answer sweep (`skills/answer-all-open-questions-with-recommendation/SKILL.md`)

Gathers only recommendation-bearing blocks, orders them "loosely most-significant → least" by judgment (no structural signal exists for the order), and walks that list exactly once, strictly sequentially. Its per-question re-check skips a question whose block is gone **or whose `<recommendation>` element is gone**, so a block whose children vanish mid-sweep is already tolerated as a benign skip. The orchestrator lifts the recommendation text during that re-check for the commit body and commits each answer itself after the agent returns `DONE`.

### Principle capture's diff read (`skills/capture-milestone-principle-updates/SKILL.md`)

Capture reconstructs what the user saw from each answer commit's removed lines, locating the answered block by its `-<open-question id="…"` opening boundary and reading through `-</open-question>`; "any other removed block in the same diff is a cascaded sibling" and contributes nothing. Removed lines that belong to no removed block are not addressed by that read. Its agreement test compares the recorded option against the removed `<recommendation option>` (exact for alternatives, judgment for manual prose) — the same comparison the goal needs at answer time. The store `milestones/answer_decision_principles.md` currently holds four entries and is read in place by the recommend core.

### Evidence of undeclared coupling (milestone 19 history)

In milestone 19 the sweep annotated ten blocks. The manual override `Manual-answer: Store rewrite confirmation granularity` (`caf5370`) recorded a different option than recommended; the following `Requirements-review:` pass (`eaf00b8`) reworded six phrases across sibling blocks, including a `<recommendation>` rationale that had assumed the pre-override outcome. That rewording is not a capability the review skill defines — its reconcile step permits only delete-when-a-decision-covers, dedup, and flag — so the correction was incidental. No sweep-vs-sweep contradiction has been recorded in any milestone; the recorded failure is recommendation-vs-override.

### Documentation and build surfaces

`CLAUDE.md` carries the invariants the goal reverses or extends: the `recommend-all-open-questions` bullet (parallel dispatch, embed-at-end, recommendation independence), the `shared/answer-procedure.md` bullet (fold-then-remove, two-outcome cascade), the `answer-all-open-questions-with-recommendation` bullet (most-significant-first proxy), and the dispatched-agent-return bullet (the gate's test list). `README.md`'s `## Skill reference` documents each skill's behaviour. The Antigravity transpiler copies `skills/`, `agents/`, and `shared/` verbatim apart from path rewriting, so a new child element needs no build change.

## Decisions

## Out of Scope

## Open questions

<open-question id="Invalid dependency target handling" status="open">
  <question>When a returned `&lt;depends-on&gt;` element names a question id that matches no still-open sibling block, or an option that matches none of that sibling&apos;s embedded `&lt;alternative&gt;` ids, should the acceptance gate reject the return (taking the single repair attempt with a reason naming the failed test), or should the orchestrator drop the offending element and embed the rest?</question>
</open-question>
<open-question id="Forward dependency declaration" status="open">
  <question>When an agent finds its recommendation turns on a still-open sibling that has not yet been annotated in this run (the sibling comes later in the most-significant-first order), how should it declare that dependency: a `&lt;depends-on&gt;` carrying the option it assumed as its own guess, a `&lt;depends-on&gt;` with no option, or no element at all?</question>
</open-question>
<open-question id="Ambiguous manual agreement default" status="open">
  <question>When the cascade cannot tell whether a free-text manual answer invalidates the option a dependent&apos;s `&lt;depends-on&gt;` assumed, should it default to stripping the dependent (a spare re-recommendation) or to keeping it (risking a stale rationale being lifted later)?</question>
</open-question>
<open-question id="Stale tags after manual refresh" status="open">
  <question>When a block is regenerated by the recommend sweep after its children were deleted by hand, and its new recommendation names a different option than surviving dependents&apos; `&lt;depends-on&gt;` elements assumed, should the sweep strip and regenerate those dependents in the same run, leave their stale tags for the answer-time mismatch strip, or rewrite the tags in place?</question>
</open-question>
<open-question id="Cleared dependents console advisory" status="open">
  <question>When an answer strips or tidies dependent blocks, should the answer skills print the affected Short Titles as a git-absent advisory alongside the terse status line (a cue that a recommend re-run is due), or stay silent because the diff records the change?</question>
</open-question>
<open-question id="Depends-on child order and form" status="deferred">
  <question>Where among the block&apos;s children the `&lt;depends-on&gt;` elements sit and whether they are self-closing, given that extraction keeps only the region from the first `&lt;alternative` line through the last `&lt;/recommendation&gt;` line.</question>
</open-question>
<open-question id="Origin walk tie order" status="deferred">
  <question>How the answer sweep orders questions that share the same depth in the dependency graph, such as several origins with no dependencies.</question>
</open-question>
<open-question id="Discuss path dependency naming" status="deferred">
  <question>Whether the conversational discuss-open-question path, which renders no XML, names the sibling recommendations its inline recommendation builds on.</question>
</open-question>
<open-question id="Capture treatment of tag lines" status="deferred">
  <question>Whether the capture skill&apos;s diff read is updated to state explicitly that removed `&lt;depends-on&gt;` lines, both inside the answered block and as orphan lines from tidied or stripped siblings, contribute nothing to its record.</question>
</open-question>
