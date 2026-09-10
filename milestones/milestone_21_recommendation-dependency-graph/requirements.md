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

### Stale tags after manual refresh

When a block whose embedded children were deleted by hand is regenerated by the recommend sweep and its new recommended option differs from what surviving dependents' `<depends-on>` elements assumed, the sweep leaves those dependents exactly as they are — it does not strip and re-dispatch them, does not rewrite their `option` values, and prints no mismatch advisory. Reconciliation happens only in the answer-time cascade, which compares each dependent's assumed option against the option actually recorded, never against its target's live recommendation. A `<depends-on>` therefore records what a dependent assumed rather than a pointer that must track its target, so the strip is already correct in both branches without the annotate-only sweep gaining any cascade machinery or the outer re-gather loop it deliberately lacks; a dependent the user also wants regenerated is covered by the same hand-clear escape hatch just used on the target.

### Forward dependency declaration

A `<depends-on>` element is emitted only for a sibling that already carries embedded children in the block the agent read, so every dependency tag names an existing question and an existing `<alternative>` id by construction. A recommendation that turns on a still-open sibling not yet annotated in this run declares no element at all and expresses the coupling as prose inside the affected `<drawback>` or the rationale: no option is ever guessed, and there is no option-less tag form. That keeps the acceptance gate's option-matching test, the answer-time agree/disagree comparison, and the transitive strip to one uniform case. The residual risk is accepted — answering such a later sibling strips nothing and a stale rationale may still be lifted, guarded only by that prose.

### Invalid dependency target handling

A returned `<depends-on>` element naming a question id that matches no still-open sibling block, or an option matching none of that sibling's embedded `<alternative>` ids, is a gate failure rather than something the orchestrator edits away. The acceptance gate gains a seventh test that resolves every returned `<depends-on>` against the still-open sibling blocks and the target sibling's embedded `<alternative id>` lines — reaching outside the return into the document for the first time — and a miss is treated exactly like any other structural miss: a reason string naming the failed test, the single repair attempt, and a skip of that question alone only on a second failure. The orchestrator therefore never deletes or rewrites a returned element and never embeds an unverified structural claim, keeping one uniform per-return judging pipeline.

### Depends-on child order and form

The `<depends-on>` elements are self-closing `<depends-on question="…" option="…"/>` tags placed as direct children strictly inside the existing extraction region — after the alternatives and any `<applied-principle>` elements, immediately before `<recommendation>` — so a block's child order is alternatives, applied-principles, depends-on, recommendation. Sitting wholly within the region leaves the return pipeline's extraction anchors, its two boundary shape tests, and the whole-block removal untouched, and the self-closing two-attribute form keeps each declaration a single greppable line whose `question` and `option` fields are both readable by one attribute-name-anchored regex. Child order is settled in favour of the pipeline, which is its primary consumer, rather than a reader scanning the block.

### Ambiguous manual agreement default

Strip on doubt — the costs are asymmetric — an extra dispatch is cheap, self-healing, and already tolerated by both sweeps, while a kept stale rationale becomes a wrong recorded decision that only a revert can undo — so doubt should resolve toward the recoverable failure. When the cascade's judgment of whether a free-text manual answer invalidates the option a dependent's `<depends-on>` assumed is inconclusive, it treats that as a mismatch: the dependent's embedded children are stripped transitively, exactly as a disagreeing answer strips them, and the bare block is left for the next recommend sweep to regenerate.

### Cleared dependents console advisory

When recording an answer strips or tidies a dependent block's embedded children, the answer skills print nothing beyond their existing output. The change is fully recorded in the answer commit's own diff, and each cleared block is left in exactly the un-annotated state the next `/review-milestone-requirements` or `/recommend-all-open-questions` pass surfaces by construction, so such a note fails both halves of the git-absent-and-decision-critical advisory test. Printing one would also contradict the answer sweep's existing rule against enumerating recommendation-less questions.

### Origin walk tie order

The answer sweep walks questions that share the same depth in the dependency graph in document order — the order their `<open-question>` blocks appear in the `## Open questions` section, which is what the boundary-line CLI already hands the gather step. Same-depth questions cannot depend on one another, so tie order can never change a cascade outcome; determinism and cost are therefore the only real criteria, and document order costs nothing while retiring the "loosely most-significant first" significance proxy the dependency graph was built to replace.

### Discuss path dependency naming

The conversational `discuss-open-question` path does name the sibling recommendations its inline recommendation builds on, via a caller-neutral disclosure duty written into `shared/recommend-procedure.md` step 1 in place of the retired independence clause: when a recommendation leans on a still-open sibling's recommendation, name that sibling and the option assumed. Each caller renders that duty its own way — `<depends-on>` elements in the agent, prose in the discussion — which is the established division of labor already used for principles, where the core states the citation obligation and the agent owns the `<applied-principle>` markup. The core carries the duty without the sweep mechanics that give it teeth (the acceptance gate and the answer-time cascade), so a reader of the core alone sees the obligation without its enforcement; that is accepted.

### Capture treatment of tag lines

Capture's diff read is updated by rewording its one existing disambiguating sentence so the scoping rule covers removed lines belonging to no removed block as well as whole cascaded sibling blocks: only lines within the answered block's `-<open-question id="…">` … `-</open-question>` boundaries feed the record. That closes the gap the cascade's tidy and strip outcomes actually open — orphan `<recommendation option>` and `<alternative id>` lines removed from siblings that stay in the document, which are exactly the tokens the reconstruct and agreement steps key on — and subsumes the `<depends-on>` case for free. The reworded sentence stays element-agnostic and never names `<depends-on>`, so no per-element "ignore this" list is started and the rule holds unchanged as further child elements are added.

## Out of Scope

## Open questions

<open-question id="Cascade option input contract" status="open">
  <question>How does the shared answer procedure obtain the recorded option id and the exact-versus-judgment comparison mode for its dependency cascade, given that its inputs today are only the Short Title and the answer text?</question>
</open-question>
<open-question id="Dependency cycle handling" status="open">
  <question>A block whose children were hand-cleared and regenerated after its former dependents can declare a dependency back on one of them, forming a cycle; is such a cycle rejected at the acceptance gate or tolerated, and how does the answer sweep then order the members of a cycle?</question>
</open-question>
<open-question id="Deferred siblings as targets" status="open">
  <question>Does a still-open sibling, as a valid &lt;depends-on&gt; target and in the acceptance gate&apos;s resolution test, mean any block still present under the Open questions section including status=&quot;deferred&quot; ones, or only status=&quot;open&quot; blocks?</question>
</open-question>
<open-question id="Dangling dependency tags" status="open">
  <question>When a target block is removed by a path that records no option, such as the cascade removing a mooted entry or a review pass pruning or deduplicating it, what happens to the &lt;depends-on&gt; elements in surviving siblings that point at it: strip those dependents, remove just the elements, or leave them in place?</question>
</open-question>
<open-question id="Unresolvable target walk placement" status="open">
  <question>How does the answer sweep place a gathered question whose &lt;depends-on&gt; target is not in the gathered set because the target block is gone or carries no recommendation: record it as an origin in this sweep, or leave it unanswered until its target has been recommended and answered?</question>
</open-question>
<open-question id="Recommend sweep significance ordering" status="deferred">
  <question>On what basis does the recommend sweep rank questions most-significant-first before dispatching sequentially: the gathered question texts alone, or a whole-document read of requirements.md, which the gather step today deliberately avoids?</question>
</open-question>
