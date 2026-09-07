# Milestone 19: Principle Capture By Milestone

## Goal

Rework `capture-milestone-principle-updates` into an argument-driven harvester: it requires a milestone id, drops the last-completed-row resolution, and infers that milestone's decision history itself from the answer commits on its `requirements.md` across all three provenances (`Manual-answer:`, `Alternative-answer:`, `Recommendation-answer:`), reconstructing from each commit's diff the recommendation and cited principles the user saw against the answer they recorded. Manual and alternative answers are the override signal: at capture time the skill asks the user why the alternative was preferred (offering its own best guess) and distills from those overrides the compact, intuitive guideline the recommender lacked, so future recommendations are accepted more often and manual or alternative answers become rarer. The store may shrink as well as grow: current reasoning takes precedence over an existing entry it contradicts, with capture pruning, merging, or generalizing entries, salvaging what it can from a decommissioned rule, and keeping each entry as short as it can be while still reading as an intuitive rule.

## Relevant starting state

### The capture skill as it stands

`skills/capture-milestone-principle-updates/SKILL.md` is argument-free. Step 1 resolves `<MILESTONE_DIR>` from the last row of the `## Completed Milestones` table in `milestones/README.md`, explicitly not via `shared/get-current-milestone.md`, because it is documented as a post-finish follow-up run after the pointer is `none`. Step 2 walks only `git log --grep='^Manual-answer: ' -- <MILESTONE_DIR>/requirements.md` and reads commit bodies. Phase 1 extracts keep/eliminate directives, drops non-generalizable ones, and clusters survivors; phase 2 walks them strongest-first, re-reads the whole store before each write, and offers the user a revise-vs-add choice per candidate by semantic overlap. The store can only be added to or have a single entry revised in place — there is no prune, merge, or generalize move. It commits under `Principle-capture: <milestone_id>` via `shared/commit-procedure.md`, path-scoped to the store, and reports `Principles captured.` or a one-line no-op. Its frontmatter description already reads "from a just-finished milestone's recorded decisions"; sibling skills that take a milestone id (`specify-milestone-starting-state`, `derive-tasks`, `review-milestone-requirements`, `recommend-all-open-questions`, `modify-milestone-goal`) take it as the directory name, e.g. `milestone_12_user-guide`.

### The principle store

`milestones/answer_decision_principles.md` holds four entries (`Prefer domain-neutral terms`, `Drop-vs-replace by ambiguity`, `Mutate live machinery last`, `Name by distinctive function`), each a `### <Short Title>` heading, a one-paragraph keep/eliminate directive of roughly 80–120 words, and an optional `*Origin:*` line naming the originating question. There is no status field; presence means confirmed. Its header paragraph names the consumers and states the file is written only by `capture-milestone-principle-updates`. All four entries were written by the retired per-answer capture skill during milestones 2–3; the finish-time skill has never run — there are zero `Principle-capture:` commits in the history, and the store's last content change was the milestone-8 header repoint.

### Answer commits and what their bodies carry

Every recorded answer is one commit touching `<MILESTONE_DIR>/requirements.md`, under one of three subjects. The commit body differs by provenance:

- `Manual-answer: <Short Title>` (`answer-open-question`): the body is the decision's rationale when deliberation was in context, otherwise the literal answer text verbatim; the skill never prompts for a rationale.
- `Recommendation-answer: <Short Title>` (single skill and the sweep orchestrator): the body is the lifted `<option> — <rationale>` text, i.e. the recommend agent's reasoning.
- `Alternative-answer: <Short Title>` (`answer-open-question-with-alternative`): the body is the chosen alternative's `<id> — <what-it-is>` text, with `<advantage>`/`<drawback>` excluded. No user rationale is captured anywhere on this path.

Counts across the history: 17 `Manual-answer:` (13 of them in milestones 6–7, before the recommend sweep existed), 66 `Recommendation-answer:` (milestones 8–17), 4 `Alternative-answer:` (milestones 11, 14, 17). Milestones 1–5 and 18 carry no answer commits at all under these subjects. No `Revert` commits exist, so the documented revert-then-re-answer correction flow has never been exercised.

### What an answer commit's diff preserves

Because `shared/answer-procedure.md` folds the decision into `## Decisions` and then removes the whole `<open-question>` block, each answer commit's diff carries as removed lines the full block the user saw: the `<question>`, every `<alternative id="...">` with its what-it-is text and `<advantage>`/`<drawback>` children, any `<applied-principle>` citations, and the `<recommendation option="...">` element with its rationale; the added lines are the new `## Decisions` entry and any cascaded removals. Comparing the removed `<recommendation option>` against the subject/body therefore reveals whether an answer accepted or overrode the recommendation, and which principle was cited when it was overridden. Across all answer commits, 19 `<applied-principle>` citation lines have been removed this way. Blocks answered before the sweep annotated them (all pre-milestone-8 manual answers) carry only `<question>` and no analysis.

### How the store is consumed

`shared/recommend-procedure.md` reads the store in place during grounding and treats a bearing principle as a weighted advisory factor that must be cited; the `recommend-open-question` agent renders each citation as an `<applied-principle>` sibling of `<recommendation>`, never inside it, so lifted answers stay provenance-free. The consumer side has no notion of principle weight, age, or retirement beyond presence in the file.

### Documentation surfaces that state the current grep boundary

The rule that capture harvests only `Manual-answer:` bodies is restated in: `CLAUDE.md` (the workflow map entry, the recommendation/alternative-answer provenance bullet, the correction-loop bullet, the skill-layer-commit bullet's "Still true" sentence, and the finish/capture bullet describing last-row resolution), `README.md` (the `## How skills commit` paragraph, the principle-learning bullets, and the skill-reference entries for `answer-open-question`, `-with-recommendation`, `-with-alternative`, and capture itself), and the commit steps of the three answer skills (`answer-open-question` says the subject exists so capture can collect it; the other two say their subject is never harvested). `finish-current-milestone` states it never invokes capture. The generated Antigravity tree under `.agents/plugins/cairn/` mirrors the skill file and is regenerated by `scripts/migrate_skills_to_agy.py`.

## Decisions

## Out of Scope

## Open questions

<open-question id="Role of accepted recommendations" status="open">
  <question>What does capture do with a milestone&apos;s Recommendation-answer commits, where the user accepted the recommendation as-is: treat each as a confirmation that reinforces any principle the removed block cited and leave it at that, mine its rationale for new principle candidates exactly like a manual answer, or use it only to detect a store entry the accepted reasoning contradicts?</question>
</open-question>
<open-question id="Override rationale prompting scope" status="open">
  <question>When does capture ask the user why an answer overrode the recommendation: only for overrides whose commit body carries no user rationale (every Alternative-answer, and a cold Manual-answer that is just the literal answer), or for every override including a Manual-answer whose body already holds deliberated rationale, and does the user get a way to skip or answer all prompts at once?</question>
</open-question>
<open-question id="Store rewrite confirmation granularity" status="open">
  <question>Now that a pass may prune, merge, generalize, and shorten existing entries as well as add, how is the store change confirmed with the user: one candidate at a time with revise/add/prune/merge as per-candidate choices, or as a single proposed rewrite of the whole store shown as a diff and confirmed once?</question>
</open-question>
<open-question id="Non-override manual answers" status="open">
  <question>Does capture still distill candidates from a Manual-answer whose removed block carried no recommendation to override (every pre-sweep answer, and any question the sweep never annotated), using its body rationale alone as today, or does the reworked skill treat only overrides of a recommendation as principle sources?</question>
</open-question>
<open-question id="Milestone id argument shape" status="deferred">
  <question>Is the required argument the directory name (milestone_19_principle-capture-by-milestone, matching the sibling skills that take a milestone id), a bare number, or either?</question>
</open-question>
<open-question id="Unfinished milestone allowed" status="deferred">
  <question>May capture run against a milestone that is not yet listed in the Completed Milestones table, including the current one, or does it stop unless the milestone is finished?</question>
</open-question>
<open-question id="Repeat capture on same milestone" status="deferred">
  <question>What happens when capture is run again for a milestone that already has a Principle-capture commit: proceed and rely on store dedup, warn and ask before proceeding, or stop?</question>
</open-question>
<open-question id="Entry compactness bar" status="deferred">
  <question>Is the compactness of a store entry expressed as a concrete cap (a word limit per entry, a ceiling on entry count) or only as the qualitative &quot;as short as still reads as an intuitive rule&quot; bar, and does the optional Origin line survive?</question>
</open-question>
<open-question id="Salvage form for contradicted entries" status="deferred">
  <question>When current reasoning contradicts an existing entry that was cited and then overridden, what forms may the salvage take: narrow the entry&apos;s scope, generalize it so both cases fit, replace it, or delete it outright when nothing generalizes?</question>
</open-question>
<open-question id="Skill framing after decoupling" status="deferred">
  <question>With a required milestone id, is capture still documented as the optional post-finish follow-up in README.md and CLAUDE.md, or reframed as an on-demand skill runnable for any milestone at any time?</question>
</open-question>
