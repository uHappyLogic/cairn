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

### Cascade option input contract

The shared answer procedure's input contract widens from two fields to three: an optional **RECORDED OPTION** — the un-escaped option/alternative id the caller already lifted — joins SHORT TITLE and ANSWER, and its presence is itself the comparison-mode discriminator. Supplied means exact id comparison of the recorded option against each dependent's assumed option; absent means judgment of whether the ANSWER prose invalidates that assumption. Both lifting callers already hold the id at the moment they delegate (`shared/answer-with-recommendation-procedure.md`'s step 3 lift and `answer-open-question-with-alternative`'s inline lift), so passing it re-derives nothing and one optional field carries both the id and the mode without a second parameter; `answer-open-question` is documented as explicitly passing nothing rather than merely being unchanged. The anchor string `<option> — <rationale>` stays a caller-side rendering convention and never becomes a parse contract inside the execution-neutral core, and the discrimination mirrors the one capture already makes on an answer commit's diff.

### Deferred siblings as targets

A valid `<depends-on>` target is any `<open-question>` block still present under `## Open questions` that carries embedded children, regardless of its `status`: the acceptance gate's resolution test resolves the `question` attribute against that whole set without reading `status` at all, so a `status="deferred"` sibling the sweep annotated is a declarable target exactly like an open one. That keeps the resolution test a plain boundary-line grep over the block list the sweep already gathered and preserves the open-or-deferred uniformity the two sweeps' gathers, the CLI locate, and `shared/answer-procedure.md` all share, rather than making the gate the first mechanism on this path to branch on `status`. The residual — a deferred target may carry forward unanswered past `/derive-tasks`, leaving a declared dependency permanently unreconciled — is accepted as one the milestone already accepts elsewhere, and no advisory is added for it.

### Dangling dependency tags

When a target block is removed by a path that records no option — the cascade removing a mooted entry, or a `/review-milestone-requirements` pass pruning or deduplicating it — the removal is treated uniformly as a mismatch: every surviving sibling whose `<depends-on>` pointed at that block has its embedded children stripped transitively, leaving the bare block for the next recommend sweep to regenerate. A removal that records no option is exactly the inconclusive comparison this milestone already decided to resolve by stripping, so it routes into the existing disagreeing-answer branch rather than adding a third cascade outcome, and the review skill gains the same dependent-stripping step on its prune and dedup paths. The cost is real blast radius from an option-less removal into sweep output — several blocks' children may clear at once, forcing a re-run — and is accepted as the recoverable failure over a stale rationale surviving as lift-able.

## Out of Scope

## Open questions

<open-question id="Dependency cycle handling" status="open">
  <question>A block whose children were hand-cleared and regenerated after its former dependents can declare a dependency back on one of them, forming a cycle; is such a cycle rejected at the acceptance gate or tolerated, and how does the answer sweep then order the members of a cycle?</question>
  <alternative id="Tolerate, document-order entry">
    The acceptance gate gains no cycle test, and the answer sweep&apos;s origin walk handles a stranded set — questions none of whose targets are yet answered — by promoting its document-order-first member to an origin and continuing the depth walk from there.
    <advantage>It costs one sentence in the walk step and nothing anywhere else: the gate stays the line-oriented CLI check it was deliberately confined to, the seventh test&apos;s one-hop resolution is unchanged, and the tie-break rule already decided for same-depth questions (document order) is simply reused as the entry rule, so the sweep stays deterministic and total for any graph shape.</advantage>
    <drawback>The promoted member is answered before the sibling whose option it assumed, so its rationale may be stale when recorded — the same residual risk already accepted under &quot;Forward dependency declaration&quot;, here shrunk to one question per cycle because answering it immediately strips or tidies the rest of the cycle.</drawback>
  </alternative>
  <alternative id="Reject at the gate">
    The gate gains a further test that follows the target sibling&apos;s own &lt;depends-on&gt; elements transitively and rejects any returned element that closes a cycle back on the question under dispatch, taking the single repair attempt and then the per-question skip.
    <advantage>The embedded graph is acyclic by construction, so the answer sweep&apos;s origin walk needs no special case at all and every question is answered strictly after the sibling it assumed.</advantage>
    <drawback>It turns a gate held to line-greps and one-hop attribute resolution into a transitive reachability walk over the whole questions section — a second control path the gate was explicitly designed to avoid — and its likely outcome is a skipped, un-annotated block, defeating the hand-clear refresh that created the situation.</drawback>
  </alternative>
  <alternative id="Agent-side prohibition">
    The recommend agent is told not to declare a dependency on a sibling that already depends on the question it is recommending, with the gate and the answer sweep both left unchanged.
    <advantage>It is the cheapest possible change — one clause in the agent&apos;s rendering step — and needs no new machinery in either sweep.</advantage>
    <drawback>It is unenforced, which is precisely what the acceptance gate exists to correct: a return that ignores the clause passes the gate, gets embedded, and strands the answer sweep with no rule for what to do — the failure is merely moved past every checkpoint.</drawback>
  </alternative>
  <alternative id="Tolerate, defer cycle members">
    The gate tolerates cycles, and the answer sweep leaves every member of a cycle unanswered, reporting them as questions it could not order.
    <advantage>No question is ever answered against an unvalidated assumption, and the deferral is visible rather than silent.</advantage>
    <drawback>A pair of questions produced by an ordinary hand-clear refresh becomes permanently unanswerable by the sweep until a human breaks the cycle by hand, contradicting the self-healing, strip-and-regenerate pattern every other branch of this design uses.</drawback>
  </alternative>
  <recommendation option="Tolerate, document-order entry">A cycle is only reachable through the hand-clear escape hatch, is coherent under the already-decided reading of &lt;depends-on&gt; as a record of what a dependent assumed rather than a live pointer, and dissolves at the first answer&apos;s cascade — so a one-sentence deterministic entry rule reusing the decided document-order tie-break beats adding a transitive graph walk to a gate kept deliberately parser-free, and its one stale-rationale risk is the recoverable kind this milestone has twice chosen to accept.</recommendation>
</open-question>
<open-question id="Unresolvable target walk placement" status="open">
  <question>How does the answer sweep place a gathered question whose &lt;depends-on&gt; target is not in the gathered set because the target block is gone or carries no recommendation: record it as an origin in this sweep, or leave it unanswered until its target has been recommended and answered?</question>
  <alternative id="Origin by dropped edge">
    Build the dependency graph only over the gathered set: each &lt;depends-on&gt; is resolved against that set, an edge whose target is absent or recommendation-less is dropped, and a question left with no resolvable edges is an origin walked in document order among the other origins.
    <advantage>Keeps the walk one uniform graph build with no new outcome class, no deadlock, and no orchestrator mutation — every gathered question is still recorded, preserving the sweep&apos;s existing contract that a gathered block always gets answered, and the depth-tie rule already decided (document order) applies unchanged.</advantage>
    <drawback>The question&apos;s recorded answer may lift a rationale resting on an assumption nothing in the sweep can verify, and a wrong recorded decision is undone only by reverting its commit — the asymmetric cost the strip-on-doubt decision named.</drawback>
  </alternative>
  <alternative id="Hold until target resolved">
    Leave such a question unanswered in this sweep — neither origin nor descendant — so it is recorded only after a later run has regenerated and answered its target, making the dependency reconcilable by the cascade as designed.
    <advantage>Never records a decision on an assumption the cascade could not check, so the graph&apos;s whole purpose — no dependent answered before its target — holds without exception.</advantage>
    <drawback>Adds a gathered-but-unanswered outcome the sweep does not have today (needing its own report line despite terse reporting), and when the target was removed for good — pruned or deduped by a review pass, or mooted by a cascade — the question is unanswerable by the sweep forever, with hand-editing the only escape.</drawback>
  </alternative>
  <alternative id="Strip and defer">
    Treat the unresolvable edge like a disagreeing cascade: clear the question&apos;s embedded children and leave the bare block for the next recommend sweep to regenerate against the current document, instead of answering it this run.
    <advantage>Resolves the doubt toward the recoverable failure — the question is re-recommended with fresh grounding rather than recorded on an unverifiable assumption — and is self-healing across a recommend-then-answer cycle.</advantage>
    <drawback>Gives the answer orchestrator a mutation it has never had (a strip to stage and commit outside any answer, under some new subject), and cuts against the already-recorded decision that a dependent whose target was hand-cleared is left exactly as it is.</drawback>
  </alternative>
  <recommendation option="Origin by dropped edge">A &lt;depends-on&gt; records what a dependent assumed rather than a live pointer, and only a recorded option can reconcile it, so an edge to a target this sweep will never answer carries nothing to act on — dropping it costs no machinery, deadlocks nothing, and leaves exactly the residual stale-rationale risk the forward-declaration decision already accepted.</recommendation>
</open-question>
<open-question id="Recommend sweep significance ordering" status="deferred">
  <question>On what basis does the recommend sweep rank questions most-significant-first before dispatching sequentially: the gathered question texts alone, or a whole-document read of requirements.md, which the gather step today deliberately avoids?</question>
  <alternative id="Gathered texts only">
    Rank the surviving questions by judgment over exactly what step 1&apos;s boundary-line gather already yields — each block&apos;s id, status, and &lt;question&gt; text — with no additional reading of requirements.md by the orchestrator.
    <advantage>Costs nothing beyond the gather the sweep already performs, and preserves the sweep&apos;s stated design property that the orchestrator never reads the whole file to assemble context — the subagent, not the orchestrator, is the one that grounds in the document.</advantage>
    <drawback>Question texts alone are a thin signal for foundationality, so the ranking will sometimes place a dependent ahead of its target, leaving that coupling to the prose fallback instead of a &lt;depends-on&gt; element.</drawback>
  </alternative>
  <alternative id="Whole-document read">
    Have the orchestrator read requirements.md in full — Goal, Relevant starting state, Decisions, and every block — and rank the questions against that whole picture before dispatching.
    <advantage>Gives the richest available basis for judging which questions are foundational, maximizing how many real couplings get declared as structured &lt;depends-on&gt; elements rather than falling back to prose.</advantage>
    <drawback>Reverses an explicit design property of this sweep — the gather is deliberately CLI-only precisely so the orchestrator&apos;s context stays small across a long sequential run — and buys accuracy on a heuristic whose misses are already an accepted, self-healing risk.</drawback>
  </alternative>
  <alternative id="Goal-slice hybrid">
    Rank from the gathered question texts plus one bounded extra slice of requirements.md — the &#35;&#35; Goal section, and optionally &#35;&#35; Decisions — sliced by the same line-oriented CLI rather than read whole.
    <advantage>Adds the milestone&apos;s root context, which is the single most useful signal for what &quot;foundational&quot; means here, at a bounded and deterministic reading cost rather than a whole-file one.</advantage>
    <drawback>Introduces a second reading rule into a gather step whose whole virtue is being one uniform CLI pass, and the added precision is spent on a ranking that is loose by construction anyway.</drawback>
  </alternative>
  <alternative id="Document order">
    Drop significance ranking entirely and dispatch in the document order the gather already hands back, mirroring the tie order the answer sweep just adopted.
    <advantage>Fully deterministic, free, and consistent with the sibling decision that retired the &quot;loosely most-significant first&quot; proxy elsewhere in this milestone.</advantage>
    <drawback>Contradicts the milestone Goal&apos;s explicit &quot;most-significant-first order&quot; and would require a goal revision; unlike the answer sweep it has no dependency graph to fall back on, since the graph is what this sweep produces, so ordering here is the only lever that exists.</drawback>
  </alternative>
  <recommendation option="Gathered texts only">Rank from what the gather already holds: the ordering is a best-effort heuristic whose misses are absorbed by the accepted prose fallback, so it does not justify breaking the sweep&apos;s deliberate no-whole-document-read property, and it matches the same loose-judgment ordering the answer sweep already documents.</recommendation>
</open-question>
