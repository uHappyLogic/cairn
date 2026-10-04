# Milestone 42: Stale picks as undeclared dependents

## Goal

When a question is answered by hand (`/answer-open-question` or `/answer-open-question-with-alternative`), the runner names the standing recommendations on other open questions that the answer undermines, and the open-question tool's `remove` reconciles them as dependents of the answered question in the same write as the `<depends-on>`-tagged ones, transitively and keeping their alternatives, so the answer sweep cannot record a pick formed without that answer. Picks the answer does not bear on are left standing, and doubt strips. The milestone also decides whether `/modify-milestone-goal` clears the picks a revision undermines, and implements that if so.

The change is measured by replaying historical stale-pick cases, counting both the stale picks it clears and the unaffected picks it leaves standing. The replay runs outside the repository's tracked files, and no committed artifact carries historical data from it beyond aggregate results.

Out of scope: the answer sweep and `/answer-open-question-with-recommendation`, which both stay as they are, including the sweep's fold-time contradiction rule and its advisory; the recommendation pass and its disclosure duty; conflicts between picks of the same recommendation pass; hand edits to `requirements.md` outside the skills.

## Relevant starting state

### The tool's `remove` and its dependent reconciliation

`core/tools/open_questions.py` exposes `remove MILESTONE_DIR SHORT_TITLE [--option RECORDED_OPTION]`, which takes exactly one Short Title. `remove_question` deletes the block and finds its dependents only through `dependents_of`, that is, the blocks carrying a `<depends-on>` tag whose `question` names the removed id. With `--option`, a dependent whose every such tag carries that option loses just those tags; every other dependent, and every dependent when no option is given, goes through `strip_recommendation` (its `<recommendation>`, `<depends-on>`, and `<applied-principle>` children deleted, its `<alternative>` children kept). The strip is transitive over the dependents of each stripped block, and the whole reconciliation is one write. The call has no argument that names a further block to reconcile, and it prints nothing on success, although `remove_question` returns the stripped ids.

### The tool's `strip --recommendation`

`strip [--recommendation] MILESTONE_DIR SHORT_TITLE [SHORT_TITLE ...]` accepts several Short Titles and, with the flag, applies the same `strip_recommendation` primitive to each. It is not transitive: every other block is left untouched, including a `<depends-on>` tag that names a stripped block. `walk` ignores a tag naming an absent or recommendation-less block, and such a tag is reconciled only when the block it names is later answered. The recommendation pass documents this call as the escape hatch for forcing a fresh pick.

### The shared answer core

`core/shared/answer-procedure.md` records one answer in five steps: locate, analyse, fold, remove, cascade. Its `locate` call prints only the answered block, and no step reads the other blocks or their standing recommendations. The analyse step asks whether the answer makes another entry moot, forces its answer, or contradicts something already written; the only cascade that follows from it is step 5, a bare `remove` per mooted entry. Step 4 owns the `--option` decision: the caller's RECORDED OPTION verbatim, or for a literal answer one prose verdict on whether the answer plainly settles on one of the block's own alternatives, passing nothing on doubt. The core is followed by the two hand-answer skills, by `answer-with-recommendation-procedure.md`, and through that by the answer sweep.

### The two hand-answer skills

`core/skills/answer-open-question/SKILL.md` parses a literal answer, passes no RECORDED OPTION, follows the answer core, and commits `open_questions.xml` and `requirements.md` under `Manual-answer: <Short Title>`. `core/skills/answer-open-question-with-alternative/SKILL.md` lifts the named alternative with `lift --alternative`, passes its id as RECORDED OPTION, follows the same core, and commits the same two paths under `Alternative-answer: <Short Title>`. The alternative skill tells its runner never to read `open_questions.xml` itself, and the literal skill states that every read and write of it in the core is a tool call. Neither skill sees a standing recommendation on any block but the answered one. `discuss-open-question` offers `/answer-open-question` when the user lands on an answer, naming the matching alternative id when there is one, and advises running `/modify-milestone-goal` first when a deliberation also moves the goal.

### `modify-milestone-goal`

`core/skills/modify-milestone-goal/SKILL.md` edits the `## Goal` section only and commits `requirements.md` alone under `Goal-revision: <milestone_id>`. Its impact step already reads `open_questions.xml` whole, for reasoning only, and works out which open questions the new goal settles, opens, or makes irrelevant, but writes nothing from that analysis and prints none of it. `CLAUDE.md` records this as an invariant (act-only, never cascades, points at review), and `docs/skill-reference.md` describes the skill the same way.

### How a pick is declared dependent, and what happens to a standing pick

`core/shared/recommend-procedure.md` requires a pick that leans on a sibling settling on a particular alternative to disclose it, and `recommend-all-open-questions` renders each disclosure as `<depends-on question option/>`; `embed --recommendation` validates that every tag resolves to another block and one of its alternative ids. That tag is the only record of what a pick assumed. The recommendation pass gathers with `list --without-recommendation`, so a block carrying a pick is never re-picked on a later run, while a stripped block re-enters the next run. The answer sweep records every standing pick as given; a stripped block fails its `lift` and is skipped silently. `derive-tasks` has the precondition that no open question remains.

### Other callers of the cascade

`review-milestone-requirements` removes a pruned or duplicate block with a bare `remove`, which strips every tagged dependent transitively. `capture-milestone-principle-updates` reconstructs an answer from the answered block's removed diff lines only, so recommendation lines stripped from other blocks in an answer commit do not enter its record.

### Invariants and documentation that describe the cascade

`CLAUDE.md` holds the rationale under "One reconciliation engine, strip on doubt": `remove --option` is the only reconciliation, the option id is never derived by parsing the answer, the cascade never clears an `<alternative>`, there is no separate `reconcile` subcommand, and stripped dependents get no console advisory. `docs/skill-reference.md` describes the dependent reconciliation in its entries for both hand-answer skills, and `docs/design-claims.md` states it in claims 6 and 16. Runtime files state the tool's contract in at most one sentence per site and write every tool command out in full.

### Tests and build

`tests/test_remove.py` holds 48 tests of the removal cascade and `tests/test_strip.py` covers both strip forms, over the golden fixtures under `tests/fixtures/`. A tool change is run under both pytest invocations listed in `CLAUDE.md`, and any change under `core/` is followed by `uv run scripts/build_hosts.py`, with the rebuilt `hosts/` trees committed alongside it. The judgment a skill's prose asks for has no automated test in the repository.

### Replay material

The repository holds no replay or benchmark harness. `temp/` is git-ignored and currently holds notes only, among them an uncommitted analysis of answer-sweep runs across local projects that use the workflow; in aggregate it found the stale-pick pattern in eight runs, fourteen pick-versus-decision pairs, most of them in private repositories. An uncommitted idea note there describes the shape of an earlier one-off check: scratch clones fetched at the parent of a historical commit, with the skill under test run headless against a chosen plugin tree.

## Decisions

### Undermined-pick judgment home

The step that names the standing picks an answer undermines lives in a new shared procedure under `core/shared/` that both hand-answer skills follow in place of the answer core directly: it performs the judgment, then delegates to `core/shared/answer-procedure.md`, handing it the named Short Titles as a new optional input that the core's step 4 passes through to `remove`. `answer-with-recommendation-procedure.md` passes nothing for that input, so the core stays a pass-through recorder that gains one input and no branch, and the two answer paths are each a composing procedure over the same recording core.

### Undermined pick test

A standing pick is undermined when its recommended alternative, as that alternative's what-it-is text reads, can no longer be carried out alongside the recorded decision, or when the one-line rationale of its `<recommendation>` element states or plainly presupposes something the answer changed (a fact about the project, a constraint, a sibling's expected outcome), so that the stated reason no longer holds as written even though the option itself could still be carried out. The test reads the option text and the rationale text against the answer and what it directly entails; whether the rationale rests on the changed thing is judged in prose, and doubt strips. The runner does not re-form the recommender's judgment over the other blocks' sets.

### Unknown named dependent

`remove` resolves every Short Title it is given as an undermined dependent before it changes anything. A title matching no block, and equally the answered block's own title named among its dependents, stops the call on one `Error:` line naming that title (and, for an unknown one, the ids the document holds), with exit status 1 and the document byte-for-byte unchanged: nothing is removed and no dependent is reconciled. The runner corrects the list and runs the same call again.

### Named dependent without a pick

A block named as an undermined dependent that exists but carries no `<recommendation>` element is accepted, and the call makes its one write. The named block goes through the same per-block strip primitive as every other dependent, which reports no change when the block holds nothing of the recommendation half, so the block is left exactly as it stands, alternatives included. Because nothing was deleted from it, it seeds no transitive strip: a block whose `<depends-on>` names it is left as it is. The removal of the answered block and the reconciliation of every other tagged or named dependent proceed in the same write, and the tool prints nothing.

### Cleared picks report

Both hand-answer skills keep their reporting step as it stands: the one fixed line `Answer recorded.` plus the existing advisory about new questions the answer may have raised, with nothing printed about any pick the write cleared, whether cleared by the runner's judgment, by a `<depends-on>` tag, or transitively. The answer commit's diff and the next run of the recommendation pass stay the only record; no line is added to the commit body, and the tool's print contract and the invariant that stripped dependents get no console advisory are left untouched.

### Replay result home

The replay task's **Verified:** bullets in the milestone's `TASKS_DONE.md` carry the aggregate counts (stale picks cleared, unaffected picks left standing, and whatever bar or margin applies). No file outside the milestone directory carries a figure: `docs/` and `CLAUDE.md` describe the new behaviour without numbers, and the finish summary in `milestones/README.md` may restate the counts in one bullet.

### Standing picks view

The hand-answer runner reads `<MILESTONE_DIR>/open_questions.xml` whole with the file-reading tool, for reasoning only, and judges the standing picks from that read, which shows every block with its `<alternative>`, `<applied-principle>`, `<depends-on>`, and `<recommendation>` children. The "never read or edit it yourself" sentence of `answer-open-question-with-alternative` and the "every read and write of it in the core is a tool call" statement of `answer-open-question` are reworded to the form the other inline skills carry: a whole read is for reasoning only, and every locate, list, lift, and write is a tool call. The tool is unchanged.

### Answer matching the standing pick

A match is no exemption. On every hand answer the runner performs the undermined-pick judgment over the other questions' standing picks against the recorded answer, whether or not the option it records is the one the answered block's own `<recommendation option>` names, through both the literal and the alternative skill, with no provenance condition. The answered block's own recommendation plays no part in deciding whether the judgment runs.

### Goal revision pick clearing

`/modify-milestone-goal` clears the standing picks a goal revision undermines. In the same run as the goal edit, the skill names the standing picks its impact analysis judges the revision undermines, from its whole read of `open_questions.xml`, and clears them with one `strip --recommendation` call over those Short Titles, keeping every `<alternative>`. A block whose `<depends-on>` names a cleared block keeps its pick and its tag, exactly as the tool's `strip` leaves it today, so the clearing is not transitive and the tool is unchanged. `open_questions.xml` joins `requirements.md` in the `Goal-revision:` commit.

## Out of Scope

