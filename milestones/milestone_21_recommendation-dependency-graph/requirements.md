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

## Out of Scope

## Open questions

<open-question id="Invalid dependency target handling" status="open">
  <question>When a returned `&lt;depends-on&gt;` element names a question id that matches no still-open sibling block, or an option that matches none of that sibling&apos;s embedded `&lt;alternative&gt;` ids, should the acceptance gate reject the return (taking the single repair attempt with a reason naming the failed test), or should the orchestrator drop the offending element and embed the rest?</question>
  <alternative id="Gate rejection">
    Add a seventh acceptance-gate test that resolves every returned `&lt;depends-on&gt;` against the still-open sibling blocks and the target sibling&apos;s embedded `&lt;alternative id&gt;` lines, and treat a miss like any other structural miss — a reason string naming the failed test, then the single repair attempt, and a skip of that question alone only on a second failure.
    <advantage>It is the exact analog of existing gate test 6 (an `option` value matching no `&lt;alternative&gt;` id) and keeps one uniform per-return judging pipeline: no orchestrator-side branch that edits a return, and a typo&apos;d id or option is precisely what the aimed same-session `SendMessage` repair fixes cheaply with the agent&apos;s analysis intact.</advantage>
    <drawback>The gate must reach outside the return into the document for the first time (grepping the sibling&apos;s block region for its `&lt;alternative id&gt;` lines), and one bad tag can cost an otherwise-sound recommendation its embed if the repair also fails.</drawback>
  </alternative>
  <alternative id="Drop the element">
    The orchestrator accepts the return, deletes the offending `&lt;depends-on&gt;` line, and embeds the remaining children, extending the salvage precedent extraction already set.
    <advantage>No otherwise-valid recommendation is ever lost to a bad tag, and it costs no repair round-trip.</advantage>
    <drawback>It silently discards a declared coupling while the rationale that rests on it stays embedded — reinstating exactly the undeclared-coupling failure this milestone exists to eliminate — and makes the orchestrator a rewriter of returns rather than a verbatim embedder.</drawback>
  </alternative>
  <alternative id="Embed unvalidated">
    Add no gate test at all: embed the tag as returned and let answer time absorb it, since a tag naming no existing question never matches anything and a wrong-option tag simply fails the agreement comparison and conservatively strips its dependent.
    <advantage>Cheapest change — the gate, the repair path, and the orchestrator&apos;s embed step all stay byte-for-byte as they are.</advantage>
    <drawback>The committed `requirements.md` carries a false structural claim with no detection anywhere, and a wrong-option tag guarantees a spurious strip-and-regenerate later, which is a silent correctness debt paid at the least visible moment.</drawback>
  </alternative>
  <recommendation option="Gate rejection">A dependency tag is a structural claim the orchestrator can verify from data it already holds, so it belongs in the gate beside test 6 — one judging path, an aimed repair, and no orchestrator branch that rewrites a return or embeds an unverified claim.</recommendation>
</open-question>
<open-question id="Ambiguous manual agreement default" status="open">
  <question>When the cascade cannot tell whether a free-text manual answer invalidates the option a dependent&apos;s `&lt;depends-on&gt;` assumed, should it default to stripping the dependent (a spare re-recommendation) or to keeping it (risking a stale rationale being lifted later)?</question>
  <alternative id="Strip on doubt">
    Treat an inconclusive judgment as a mismatch: strip the dependent&apos;s embedded children (transitively, as a disagreeing answer already does) and leave the bare block for the next recommend sweep to regenerate.
    <advantage>It keeps one hard invariant — an embedded recommendation in the document is never inconsistent with what `## Decisions` now records — and the recovery path is cheap and already specified: the answer sweep&apos;s per-question re-check already treats a block whose `&lt;recommendation&gt;` is gone as a benign skip, and a re-run of `/recommend-all-open-questions` regenerates exactly the un-annotated set.</advantage>
    <drawback>It spends a recommendation dispatch that may have been unnecessary, and discards any hand-edits made to that dependent&apos;s children, since the documented refresh path is regeneration rather than repair.</drawback>
  </alternative>
  <alternative id="Keep on doubt">
    Treat an inconclusive judgment as agreement: leave the dependent&apos;s children intact (removing or keeping its `&lt;depends-on&gt;` tag as the agreement path does) and let a later pass catch any staleness.
    <advantage>It preserves work and avoids churn — no wasted dispatch, no block temporarily unanswerable via `/answer-open-question-with-recommendation`, and no loss of hand-edited rationale.</advantage>
    <drawback>A rationale built on an assumption the manual answer actually invalidated stays liftable, so the failure mode is a silently wrong recorded decision that only revert-then-re-answer fixes — and that capture then reads as accepted-recommendation evidence; the milestone-19 history shows this exact class of stale sibling rationale surviving an override and being corrected only incidentally by a review pass.</drawback>
  </alternative>
  <alternative id="Ask on doubt">
    Resolve the ambiguity by asking: on an inconclusive judgment, name the dependent and its assumed option and take a single strip-or-keep confirmation from the user.
    <advantage>The one party who knows what the free-text answer meant decides, so neither wrong default is taken.</advantage>
    <drawback>It puts interaction into `shared/answer-procedure.md`, which is execution-neutral and prompts nowhere today, and adds per-dependent friction to every ambiguous manual answer for a call the cascade can make safely by default.</drawback>
  </alternative>
  <recommendation option="Strip on doubt">The costs are asymmetric — an extra dispatch is cheap, self-healing, and already tolerated by both sweeps, while a kept stale rationale becomes a wrong recorded decision that only a revert can undo — so doubt should resolve toward the recoverable failure.</recommendation>
</open-question>
<open-question id="Cleared dependents console advisory" status="open">
  <question>When an answer strips or tidies dependent blocks, should the answer skills print the affected Short Titles as a git-absent advisory alongside the terse status line (a cue that a recommend re-run is due), or stay silent because the diff records the change?</question>
  <alternative id="Stay silent">
    The answer skills print nothing new: the strip or tidy is recorded in the answer commit&apos;s own diff (removed `&lt;alternative&gt;` / `&lt;applied-principle&gt;` / `&lt;recommendation&gt;` / `&lt;depends-on&gt;` child lines inside the surviving sibling blocks), and each cleared block re-surfaces as an un-annotated open question on the next `/review-milestone-requirements` or `/recommend-all-open-questions` pass.
    <advantage>It is the only option that passes the terse-reporting rule&apos;s two-part test — the change is git-recorded, not git-absent, and it forces no decision (the recommend sweep&apos;s idempotent skip means a re-run annotates precisely the cleared set by construction) — and it matches two standing precedents: the recommend sweep&apos;s silent extraction/repair recovery, and this answer sweep&apos;s existing explicit rule not to enumerate recommendation-less questions because &quot;they remain visible as `&lt;open-question&gt;` blocks in `requirements.md` and via re-running `/review-milestone-requirements`&quot;.</advantage>
    <drawback>A user who has just answered learns nothing at that moment about which sibling recommendations went stale, and must read the diff or wait for the next review pass to see the blast radius of a wide transitive strip.</drawback>
  </alternative>
  <alternative id="Advisory in single-question skills">
    Each of the three single-question answer skills (`answer-open-question`, `-with-recommendation`, `-with-alternative`) prints the affected Short Titles alongside its terse status line, in the slot already occupied by the newly-exposed-open-questions advisory.
    <advantage>It gives the immediate re-run cue at the one moment the user is looking — the answer they just recorded — using an advisory slot that already exists in all three skills, so the reporting step needs no new shape.</advantage>
    <drawback>It is a re-narration of the commit&apos;s own diff, which is exactly what the terse-reporting rule collapses, and its length is unbounded — a transitive strip across several dependents prints a growing list after every answer.</drawback>
  </alternative>
  <alternative id="Advisory in the answer sweep only">
    The single-question skills stay silent; only `answer-all-open-questions-with-recommendation` reports at end of run, listing the gathered questions it skipped because a mid-sweep strip removed their `&lt;recommendation&gt;` element.
    <advantage>It targets the one case where the user could plausibly be misled — a multi-answer run whose single terse line would otherwise imply every gathered question was answered, when a routine strip turned some into benign skips.</advantage>
    <drawback>It directly contradicts that sweep&apos;s existing do-not-enumerate rule, and the information is not actually missing: the sweep commits once per answer under `Recommendation-answer: &lt;Short Title&gt;`, so `git log` already names exactly which gathered questions were recorded and which were not.</drawback>
  </alternative>
  <alternative id="Count-only line">
    A fixed one-line addition stating how many dependent blocks were cleared or tidied, with no Short Titles.
    <advantage>Output stays bounded no matter how wide the cascade, while still flagging that a recommend re-run is due.</advantage>
    <drawback>A bare count is not actionable — the user must open the diff anyway to learn which blocks were hit — so it costs a console line without removing a lookup, and it still narrates the diff.</drawback>
  </alternative>
  <recommendation option="Stay silent">Clearing a dependent is fully recorded in the answer commit&apos;s diff and leaves the block in exactly the un-annotated state the next review or recommend pass surfaces by construction, so it fails both halves of the git-absent-and-decision-critical advisory test and an advisory would contradict the answer sweep&apos;s existing rule against enumerating recommendation-less questions.</recommendation>
</open-question>
<open-question id="Depends-on child order and form" status="deferred">
  <question>Where among the block&apos;s children the `&lt;depends-on&gt;` elements sit and whether they are self-closing, given that extraction keeps only the region from the first `&lt;alternative` line through the last `&lt;/recommendation&gt;` line.</question>
  <alternative id="Inside region, self-closing">
    Self-closing `&lt;depends-on question=&quot;…&quot; option=&quot;…&quot;/&gt;` elements sit as direct children strictly inside the extraction region — after the alternatives and any `&lt;applied-principle&gt;` elements, immediately before `&lt;recommendation&gt;` — so the child order is alternatives, applied-principles, depends-on, recommendation.
    <advantage>Requires no change to the pipeline&apos;s start/end anchors or to gate tests 1 and 2: the region still opens on `&lt;alternative` and closes on `&lt;/recommendation&gt;`, every tag is one atomic greppable line in the same boundary-line CLI idiom as `&lt;applied-principle&gt;`, and both attributes yield to one attribute-name-anchored regex, which is exactly what the cascade&apos;s tag-matching and capture&apos;s diff read need.</advantage>
    <drawback>The declarations sit in the middle of the children rather than at the top, so a reader scanning a block for its assumptions must know the order to find them, and a new self-closing form enters a vocabulary whose every existing element is paired.</drawback>
  </alternative>
  <alternative id="Leading, extraction widened">
    The `&lt;depends-on&gt;` elements are the block&apos;s first children, ahead of the alternatives, with extraction&apos;s start anchor and acceptance-gate test 1 widened to accept a leading `&lt;depends-on` line before the first `&lt;alternative` line.
    <advantage>Dependencies read first, before the analysis that rests on them — the most legible order for a human scanning a block, and it matches how the goal describes a declaration as a property of the whole block.</advantage>
    <drawback>It loosens the one guarantee the milestone-19 failure was fixed by: the region no longer provably starts at `&lt;alternative`, and any leading tag an agent renders slightly wrong (or that a repaired return omits) is silently truncated by extraction rather than caught, turning a declared dependency into an undeclared one — the precise failure mode the graph exists to prevent.</drawback>
  </alternative>
  <alternative id="Nested in recommendation">
    The elements are nested inside the `&lt;recommendation&gt;` element as its children, so the assumption travels with the assertion that made it.
    <advantage>The dependency can never be orphaned from the recommendation it qualifies, and no new sibling child kind is added to the block&apos;s vocabulary.</advantage>
    <drawback>It contradicts the deliberate rule that keeps `&lt;applied-principle&gt;` a sibling and never a child of `&lt;recommendation&gt;`, and it breaks the recommendation lift: the answer path takes that element&apos;s text verbatim as the recorded decision prose, so nested tags would have to be stripped out and would otherwise leak assumption provenance into `## Decisions`.</drawback>
  </alternative>
  <alternative id="Paired, option as text">
    A paired form carrying the assumed option as element text — `&lt;depends-on question=&quot;…&quot;&gt;Option&lt;/depends-on&gt;` — placed in the same in-region position as the first alternative.
    <advantage>It mirrors `&lt;applied-principle&gt;`, the closest existing precedent for an atomic citation-like child, and introduces no self-closing syntax into a vocabulary that has none.</advantage>
    <drawback>The two halves of one fact then need two different read rules — an attribute-name-anchored regex plus a text read — where the self-closing two-attribute form needs only the former, and it diverges from the `&lt;depends-on question=&quot;Short Title&quot; option=&quot;Option&quot;/&gt;` form the milestone goal already states.</drawback>
  </alternative>
  <recommendation option="Inside region, self-closing">Placing the tags strictly inside the existing extraction region keeps the shape-checked return pipeline, its two boundary tests, and the whole-block removal untouched, and the self-closing two-attribute form matches the goal while keeping each declaration one greppable line with both fields readable by the same attribute regex; if legibility later outweighs that, the tie-breaker is whether a reader or the pipeline is the primary consumer of child order — and today it is the pipeline.</recommendation>
</open-question>
<open-question id="Origin walk tie order" status="deferred">
  <question>How the answer sweep orders questions that share the same depth in the dependency graph, such as several origins with no dependencies.</question>
  <alternative id="Document order">
    Within a depth level, walk the tied questions in the order their `&lt;open-question&gt;` blocks appear in the `## Open questions` section, which is the order the boundary-line CLI already enumerates.
    <advantage>Fully deterministic and free: same-depth questions are mutually independent by construction (if A declares `&lt;depends-on&gt;` on B then A sits deeper than B), so every tie-break yields an equally valid topological order and the cheapest one costs nothing in correctness while making the walk reproducible run to run.</advantage>
    <drawback>Document order is authoring order appended by `review-milestone-requirements`, so it carries no semantic weight — the first tied question answered is arbitrary rather than the most consequential.</drawback>
  </alternative>
  <alternative id="Significance judgment">
    Keep the existing sweep&apos;s "loosely most-significant → least" heuristic as the within-depth tie-break, applying judgment only among questions the graph leaves unordered.
    <advantage>Preserves the current skill&apos;s ordering language verbatim and offers a hedge against coupling a question failed to declare, by tending to answer foundational questions first anyway.</advantage>
    <drawback>Reintroduces per-run judgment into a step the dependency graph exists to make structural — the significance ordering was explicitly the proxy adopted because "no structural signal exists for the order", and an undeclared coupling between two tied questions is precisely the defect `&lt;depends-on&gt;` is meant to surface, not to paper over.</drawback>
  </alternative>
  <alternative id="Fan-out count">
    Order tied questions by how many dependents declare a `&lt;depends-on&gt;` on them, most-depended-upon first.
    <advantage>Structural rather than judgmental, and answers the question whose cascade touches the most dependents earliest.</advantage>
    <drawback>Buys nothing — every tied question is answered in the same single pass regardless of order, and no cascade outcome changes — while adding a whole-graph fan-out computation to the gather step and still needing a further fallback for equal counts, so it relocates the tie instead of resolving it.</drawback>
  </alternative>
  <alternative id="Leave unspecified">
    State that same-depth order is immaterial and let the runner walk ties in any order.
    <advantage>Honest about the fact that ties are genuinely unordered, and adds the least spec surface to the ordering step.</advantage>
    <drawback>An unspecified order in a runtime file invites the runner to improvise a different sequence each run, which contradicts the deterministic gather the boundary-line CLI is used for and leaves a reader of the step with no instruction to follow.</drawback>
  </alternative>
  <recommendation option="Document order">Same-depth questions cannot depend on one another, so tie order can never change a cascade outcome — that makes the only real criteria determinism and cost, and document order is already what the boundary-line CLI hands the gather step for free, while retiring the significance proxy the graph was built to replace.</recommendation>
</open-question>
<open-question id="Discuss path dependency naming" status="deferred">
  <question>Whether the conversational discuss-open-question path, which renders no XML, names the sibling recommendations its inline recommendation builds on.</question>
  <alternative id="Disclosure duty in shared core">
    Replace the retired &quot;never treat another question&apos;s recommendation as an input&quot; clause in `shared/recommend-procedure.md` step 1 with a caller-neutral duty — when the recommendation leans on a still-open sibling&apos;s recommendation, name that sibling and the option assumed — leaving each caller to render it its own way (`&lt;depends-on&gt;` in the agent, prose in the discussion).
    <advantage>One edit in the file where the retired clause already lives keeps the core from going silent on cross-question coupling, and mirrors the established split exactly: the core already says &quot;cite the principle it leaned on&quot; while the agent owns the `&lt;applied-principle&gt;` markup.</advantage>
    <drawback>The execution-neutral core must state the duty without the sweep mechanics that give it teeth (the acceptance gate and the answer-time cascade), so a reader of the core alone sees a disclosure obligation with no visible enforcement.</drawback>
  </alternative>
  <alternative id="Prose naming in discuss skill">
    Leave the core silent on the duty and author a naming rule in `skills/discuss-open-question/SKILL.md` itself, alongside its own &quot;what would change your mind&quot; layer.
    <advantage>Keeps the sweep-shaped dependency vocabulary entirely out of the neutral core, and puts the prose form next to the conversational layer that would surface it to the user.</advantage>
    <drawback>Duplicates in a skill what the core already covers for its other caller, and the core — which both callers read — would say nothing at all about cross-question coupling once the independence clause is removed from it.</drawback>
  </alternative>
  <alternative id="Discuss path untouched">
    Treat the dependency declaration as agent-and-XML-only: `discuss-open-question` is left byte-for-byte unchanged and names no sibling recommendation.
    <advantage>Smallest change surface, and honest that the discussion has no machine consumer for a declaration — the conversation is live, so the user can interrogate any assumption directly.</advantage>
    <drawback>Retiring the independence clause from the shared core silently grants the discuss path the coupling ability with no disclosure duty whatever, so an inline recommendation can rest on an unstated assumption about a sibling — the milestone-19 undeclared-coupling failure this milestone exists to fix, reproduced on the conversational path.</drawback>
  </alternative>
  <recommendation option="Disclosure duty in shared core">Yes — it names them, via a caller-neutral duty written into the core in place of the retired independence clause, because that is where both callers already learn the obligation and where each caller&apos;s own rendering (XML vs. prose) is already the established division of labor.</recommendation>
</open-question>
<open-question id="Capture treatment of tag lines" status="deferred">
  <question>Whether the capture skill&apos;s diff read is updated to state explicitly that removed `&lt;depends-on&gt;` lines, both inside the answered block and as orphan lines from tidied or stripped siblings, contribute nothing to its record.</question>
  <alternative id="No change">
    Leave the capture skill&apos;s diff read exactly as it is, relying on its reconstruct list being a closed enumeration — `&lt;question&gt;`, `&lt;alternative&gt;`, `&lt;applied-principle&gt;`, `&lt;recommendation&gt;` — so any child element it does not name contributes nothing by omission.
    <advantage>Zero runtime prose growth, and it is already true: nothing in the read tells a runner to look at an unlisted element, so `&lt;depends-on&gt;` is inert without a word being written.</advantage>
    <drawback>It answers only the easy half. The cascade&apos;s new tidy and strip outcomes remove lines from siblings that stay in the document, so the diff now carries removed `&lt;recommendation option&gt;` and `&lt;alternative id&gt;` lines belonging to no removed block — exactly the tokens the reconstruct and agreement steps key on — and the starting state records that removed lines belonging to no removed block are not addressed by that read.</drawback>
  </alternative>
  <alternative id="Orphan-line scoping">
    Reword the existing disambiguating sentence (&quot;any other removed block in the same diff is a cascaded sibling … contributes nothing&quot;) so it covers removed lines belonging to no removed block as well: only lines within the answered block&apos;s `-&lt;open-question id=&quot;…&quot;` … `-&lt;/open-question&gt;` boundaries feed the record.
    <advantage>One reworded sentence at the exact point of use closes the real gap, and it is element-agnostic — it holds for `&lt;depends-on&gt;` orphans and for stripped siblings&apos; `&lt;recommendation&gt;`/`&lt;alternative&gt;` orphans alike, so it will not need revisiting when another child element is added.</advantage>
    <drawback>It never names `&lt;depends-on&gt;`, so an editor grepping the repo for that tag to confirm every skill&apos;s treatment of it finds nothing in capture and must infer the coverage from the scoping rule.</drawback>
  </alternative>
  <alternative id="Name depends-on explicitly">
    Add prose that names `&lt;depends-on&gt;` outright, stating that such lines contribute nothing both inside the answered block and as orphans from tidied or stripped siblings — the literal update the question proposes.
    <advantage>Maximally unambiguous about the one element the milestone introduces, and it makes capture&apos;s treatment of the tag greppable by name alongside the skills that do act on it.</advantage>
    <drawback>It is an element-specific negative clause — the start of a per-element &quot;ignore this&quot; list every future child element must be added to — and it addresses the weaker hazard while saying nothing about the orphan `&lt;recommendation&gt;`/`&lt;alternative&gt;` lines a strip leaves behind, which are the lines that could actually flip an agreement classification.</drawback>
  </alternative>
  <alternative id="Capture as evidence">
    Make `&lt;depends-on&gt;` a positive input to capture: reconstruct the answered block&apos;s dependency tags as part of what the user saw, and read a strip cascade as evidence about the recommendations it invalidated.
    <advantage>The assumed-option tag is genuine context that stood in the block at answer time, and an override that invalidated dependents is arguably stronger evidence than one that did not.</advantage>
    <drawback>It expands capture&apos;s scope well past the milestone goal for no principle it could not already distill — new principles come from override reasoning and deliberated bodies, and a dependency tag is the recommender&apos;s own assumption, which the accepted-recommendation rule already bars as a principle source.</drawback>
  </alternative>
  <recommendation option="Orphan-line scoping">Rewording the one existing scoping sentence to cover orphan removed lines fixes the gap the cascade actually opens — stripped siblings&apos; `&lt;recommendation&gt;`/`&lt;alternative&gt;` lines outside any removed block — and subsumes the `&lt;depends-on&gt;` case for free, without starting a per-element exclusion list.</recommendation>
</open-question>
