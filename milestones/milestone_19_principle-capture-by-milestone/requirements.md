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

### Store rewrite confirmation

The store change is confirmed as a whole-store rewrite, once, at commit time. After the per-override rationale prompts, capture composes the entire proposed store — adds, revisions, prunes, merges, generalizations, and shortenings applied together — and writes it directly to `milestones/answer_decision_principles.md` in place, printing no diff and no store content to the conversation. The user reviews the working-tree change with `git diff` and requests changes in conversation; the skill re-edits the file in place each round. The single confirmation gates the commit, not the write: on acceptance the skill commits the store path-scoped under `Principle-capture:`, and on explicit rejection it restores the store from `HEAD` and takes the existing no-op path. This replaces the former per-candidate write-confirmation invariant.

### Repeat capture guard

A repeat run of capture against a milestone that already has a `Principle-capture:` commit warns and confirms rather than stopping or silently re-walking. The `Principle-capture: <milestone_id>` commit subject is the record that a milestone was ingested: before the commit walk, capture greps the history for that exact subject, anchored on both ends, and on a hit prints a one-line notice naming the prior commit and asks once whether to proceed; with no hit it runs unchanged. No empty commit is written to record a no-op run, so a prior run that changed nothing (an empty commit range, a composed store identical to `HEAD`, or a rejected rewrite) is not detected; this gap is accepted as harmless.

### Milestone id argument shape

The required argument is the milestone directory name under `milestones/` (e.g. `milestone_19_principle-capture-by-milestone`), exactly as `specify-milestone-starting-state` takes it, resolved as `milestones/<milestone_id>/` with a clean stop when that directory has no `requirements.md`. The value is consumed verbatim in three places: the path-scoped git-log prefix, the `Principle-capture: <milestone_id>` commit subject, and the repeat-capture guard's anchored grep for that exact subject. No bare-number form is accepted and no number-to-directory resolution exists.

## Out of Scope

## Open questions

<open-question id="Role of accepted recommendations" status="open">
  <question>What does capture do with a milestone&apos;s Recommendation-answer commits, where the user accepted the recommendation as-is: treat each as a confirmation that reinforces any principle the removed block cited and leave it at that, mine its rationale for new principle candidates exactly like a manual answer, or use it only to detect a store entry the accepted reasoning contradicts?</question>
  <alternative id="Confirmation only">
    Each Recommendation-answer commit whose removed block carried an &lt;applied-principle&gt; citation counts as one user confirmation of that store entry, recorded as reinforcement evidence and nothing more; commits that cited no principle are ignored.
    <advantage>Cheapest possible role that still respects the goal&apos;s framing — the override commits stay the only teaching signal, and a cited-and-accepted entry gets a concrete shield against being pruned or narrowed in the same pass.</advantage>
    <drawback>The store has no weight or age field, so outside the prune step the reinforcement is inert, and a recommendation that overrode a bearing principle on merit and was accepted leaves that stale entry standing even though the goal says current reasoning takes precedence.</drawback>
  </alternative>
  <alternative id="Mine like manual">
    Treat every Recommendation-answer body as a rationale to extract keep/eliminate candidates from, exactly as phase 1 does for a Manual-answer body.
    <advantage>Harvests the largest pool by far (66 of the 87 answer commits) and never lets a genuinely generalizable rationale go uncaptured just because the user accepted it.</advantage>
    <drawback>Those bodies are the recommender&apos;s own reasoning, so they can only teach the recommender what it already knows — the goal targets the guideline the recommender lacked — while flooding the store rewrite the user reviews with agent-authored candidates the user never deliberated, the exact provenance the distinct subject was created to keep out.</drawback>
  </alternative>
  <alternative id="Contradiction detection only">
    Read each accepted rationale solely to check whether it contradicts an existing store entry — most sharply when the recommender overrode a bearing principle for a stated reason and the user accepted — and feed any hit into the prune, narrow, or generalize path; cited-and-accepted entries get no special standing.
    <advantage>Directly serves the shrink-as-well-as-grow half of the goal by surfacing exactly the entries whose accepted counter-reasoning proves them wrong or too broad.</advantage>
    <drawback>Discards the reinforcement signal, so the same pass can prune or narrow an entry that was cited and accepted this very milestone, and contradiction hits require the user to adjudicate agent-authored reasoning that nobody deliberated.</drawback>
  </alternative>
  <alternative id="Evidence for existing entries">
    Use accepted recommendations only as evidence about entries already in the store — a removed &lt;applied-principle&gt; citation reinforces that entry and shields it from pruning in the same pass, and an accepted rationale that contradicts an entry flags it for the prune, narrow, or generalize path — but never mine them for new candidates.
    <advantage>Covers both things an accepted recommendation can actually tell capture (which entries still earn their place, which the recommender has already outgrown) from the same per-commit diff read the goal already requires, while keeping the override commits the sole source of new principles.</advantage>
    <drawback>Capture must reconstruct and read every Recommendation-answer diff, not just the override ones, and a flagged contradiction still asks the user to weigh a rationale they only rubber-stamped.</drawback>
  </alternative>
  <recommendation option="Evidence for existing entries">An accepted recommendation carries the recommender&apos;s own reasoning, so it can never supply the guideline the recommender lacked, but it is the only evidence the shrink half of the goal has for which store entries still earn their place and which the recommender has already outgrown — and the goal already requires reading every answer commit&apos;s diff, so both signals come for free.</recommendation>
</open-question>
<open-question id="Override rationale prompting scope" status="open">
  <question>When does capture ask the user why an answer overrode the recommendation: only for overrides whose commit body carries no user rationale (every Alternative-answer, and a cold Manual-answer that is just the literal answer), or for every override including a Manual-answer whose body already holds deliberated rationale, and does the user get a way to skip or answer all prompts at once?</question>
  <alternative id="Prompt only rationale-less overrides, with batch controls">
    Capture prompts for the override reason only where the commit body carries no user rationale — every Alternative-answer, and a Manual-answer whose body is the bare literal answer with no stated reason (the same &quot;bare cold answer&quot; test phase 1 already applies) — reading a deliberated Manual-answer body as the user&apos;s own answer to the why; each prompt shows the skill&apos;s best guess and can be skipped, and the run opens with a one-shot choice to accept every guess or skip every prompt.
    <advantage>Never asks the user to re-explain, weeks later and from memory, a reason they already wrote in context, so prompts scale with the actual rationale gap (four of the seven historical overrides) and the argument-driven backfill run over an old milestone stays workable via skip-all or accept-all-guesses.</advantage>
    <drawback>Cold-vs-deliberated is a judgment the skill makes over body text, so a thin-but-real rationale can be misread as deliberated and its true why never asked for; the mitigation is that the body still surfaces in the rewritten entry the user reviews with git diff before the rewrite is committed.</drawback>
  </alternative>
  <alternative id="Prompt only rationale-less overrides, per-prompt skip only">
    Same gap-only scope, but the only control is skipping an individual prompt — no up-front accept-all or skip-all, on the argument that the prompt set is already small.
    <advantage>Least machinery: no batch mode to specify, and every retained override reason is one the user actually looked at rather than bulk-accepted.</advantage>
    <drawback>A retroactive run over a milestone the user no longer remembers becomes a sequence of prompts that each end in skip, and there is no way to say &quot;use your guesses&quot; once for the whole run even though the whole-store rewrite is confirmed once before commit anyway.</drawback>
  </alternative>
  <alternative id="Prompt every override, body as prefilled guess">
    Capture prompts on every override regardless of provenance, using an existing Manual-answer body as the prefilled guess the user confirms or corrects, with the same skip and batch controls.
    <advantage>Uniform and classification-free: no cold-vs-deliberated call, and the user gets to sharpen a body that justified the answer without specifically saying why the recommendation lost.</advantage>
    <drawback>Turns the harvester&apos;s highest-quality inputs into redundant interruptions — the user is asked to re-confirm at capture time what they deliberated and wrote when the context was fresh, which is exactly when their memory is weakest and the body is strongest.</drawback>
  </alternative>
  <recommendation option="Prompt only rationale-less overrides, with batch controls">A deliberated Manual-answer body is the user&apos;s override reason already, so prompting is worth it only where no reason exists (Alternative-answers and cold literal answers); the one-shot accept-all/skip-all breaks the tie against per-prompt-skip-only because the skill is now runnable against any past milestone, where the user often cannot answer from memory and every guess still lands in a working-tree rewrite the user reviews with git diff before it is committed.</recommendation>
</open-question>
<open-question id="Non-override manual answers" status="open">
  <question>Does capture still distill candidates from a Manual-answer whose removed block carried no recommendation to override (every pre-sweep answer, and any question the sweep never annotated), using its body rationale alone as today, or does the reworked skill treat only overrides of a recommendation as principle sources?</question>
  <alternative id="Overrides only">
    Treat only answers whose removed block carried a recommendation the user departed from as principle sources, and skip any Manual-answer whose block had no recommendation (every pre-sweep answer and any question the sweep never annotated).
    <advantage>Every candidate is a demonstrated recommender gap, so the diff-comparison and why-prompt machinery applies uniformly and the store only grows where the recommender was provably wrong.</advantage>
    <drawback>It discards the richest deliberated rationale in the history (8 of the 17 manual answers, and the whole current store came from such answers) and makes a discuss-then-answer decision invisible to capture, even though a decision the recommender never got to weigh in on is still a rule it lacks.</drawback>
  </alternative>
  <alternative id="Rationale-alone distill">
    Keep a Manual-answer with no recommendation in its removed block as a principle source and distill candidates from its body rationale alone, exactly as the current phase-1 extraction does, while the override-specific comparison and prompting apply only where a recommendation existed.
    <advantage>No user-deliberated rationale is thrown away, the eligibility rule stays simple (a body with reasoning is a source), and the existing non-generalizable filter already drops bare cold answers so the class adds no noise.</advantage>
    <drawback>These candidates lack the proof that the recommender would have gotten it wrong, so some may restate a rule the recommender already reaches, working against the compactness aim unless the store-side dedup and generalize moves hold them in check.</drawback>
  </alternative>
  <alternative id="Prompt as null override">
    Treat a Manual-answer with no recommendation as an override of a null recommendation: capture asks the user what guideline the answer encodes, offering its best guess distilled from the body, instead of extracting from the body alone.
    <advantage>One user-confirmed candidate path for every non-accepted answer, so the guideline is stated in the intuitive form the store wants rather than reverse-engineered from prose.</advantage>
    <drawback>It multiplies prompts on precisely the answers whose bodies already carry the fullest rationale, making a milestone with many pre-sweep or discussed answers tedious to capture for little added signal.</drawback>
  </alternative>
  <recommendation option="Rationale-alone distill">A manual answer with no recommendation is a decision the recommender never got to make, so its rationale is exactly the guideline it lacks; overrides are the sharper signal, not the only one, and the override distinction should shape the comparison and prompting steps, never source eligibility.</recommendation>
</open-question>
<open-question id="Unfinished milestone allowed" status="deferred">
  <question>May capture run against a milestone that is not yet listed in the Completed Milestones table, including the current one, or does it stop unless the milestone is finished?</question>
  <alternative id="Any defined milestone">
    Capture accepts any milestone id whose milestones/&lt;milestone_id&gt;/requirements.md exists, the current milestone included, with the path-scoped git log as the only boundary and no check against the Completed Milestones table.
    <advantage>Matches the goal exactly (argument-driven, last-completed-row resolution dropped) and the sibling milestone-id skills&apos; existence-only validation; because every answer commit lands during the requirements phase, the history is already complete before derive-tasks runs, so finish status carries no information the harvest needs and a user can capture as soon as the questions converge.</advantage>
    <drawback>A run against a milestone still mid-requirements harvests a partial history, so any answers recorded afterwards need a later pass to be considered.</drawback>
  </alternative>
  <alternative id="Finished milestones only">
    Capture resolves the id to a directory but stops with a clean-stop message unless that path appears as a row in the Completed Milestones table of milestones/README.md.
    <advantage>Guarantees the answer history is frozen when harvested, so one capture per milestone is by construction the whole story.</advantage>
    <drawback>Reintroduces the finish coupling the goal removes and adds a second README-table lookup to keep in sync, while blocking legitimate runs for no gain: finishing never adds answer commits, so the guard checks a state unrelated to what it protects.</drawback>
  </alternative>
  <alternative id="Advisory on unresolved questions">
    Capture runs against any defined milestone but, when that requirements.md still carries status=&quot;open&quot; blocks, prints a one-line advisory that the answer set may still grow and asks whether to proceed.
    <advantage>Keeps the flexibility of the existence-only rule while keying the warning on the signal that actually predicts more answers (unresolved questions) rather than the unrelated finish state.</advantage>
    <drawback>Adds an interactive gate for a condition git already makes harmless (a later pass simply re-walks the same path), and it fires on exactly the new use case the rework enables, so it reads as noise more often than as a real warning.</drawback>
  </alternative>
  <recommendation option="Any defined milestone">The harvest is a path-scoped git log bounded only by the file&apos;s existence and every answer commit lands before derive-tasks, so a finished-only stop guards a state that never changes the harvest and would reintroduce the finish coupling the goal drops; validate the id by directory existence exactly as the sibling milestone-id skills do.</recommendation>
</open-question>
<open-question id="Entry compactness bar" status="deferred">
  <question>Is the compactness of a store entry expressed as a concrete cap (a word limit per entry, a ceiling on entry count) or only as the qualitative &quot;as short as still reads as an intuitive rule&quot; bar, and does the optional Origin line survive?</question>
  <alternative id="Qualitative bar only">
    Keep the goal&apos;s &quot;as short as it can be while still reading as an intuitive rule&quot; as the sole compactness standard, with no per-entry word limit and no entry-count ceiling, and keep the optional *Origin:* line exactly as the 4a schema has it today.
    <advantage>Never forces a lossy truncation of a rule that genuinely needs a condition or corollary (the 125-word Mutate live machinery last entry) and changes nothing in the schema the four existing entries already satisfy.</advantage>
    <drawback>Gives the reworked skill no trigger for its new shorten move — with only a judgment call to lean on, a pass has no way to tell which entries are over the bar, so entries drift longer and the store the recommender reads on every question grows unchecked.</drawback>
  </alternative>
  <alternative id="Soft target plus qualitative bar">
    State a numeric target as a heuristic — a directive of roughly 40–80 words, flagged for shortening when it exceeds about 100 — while the qualitative bar stays the deciding test, no ceiling on entry count (prune and merge by contradiction and overlap are the count control), and *Origin:* survives as an optional single-line pointer.
    <advantage>Gives the skill a concrete flag that fires the shorten move on the entries that need it (one of the four today) while the qualitative bar still lets a rule keep the clause it needs, and the one-line Origin preserves the originating case that a revise-vs-salvage judgment and a human auditor rely on.</advantage>
    <drawback>Two bars instead of one — a runner must hold both the number and the judgment, and a target phrased as &quot;roughly&quot; can be argued past in either direction when an entry sits near it.</drawback>
  </alternative>
  <alternative id="Hard caps, Origin dropped">
    Enforce a fixed per-entry word limit and a fixed ceiling on entry count as pass/fail checks in the skill, mirroring the 25-word frontmatter-description cap, and drop the *Origin:* line since git history now carries the provenance.
    <advantage>Deterministic and greppable — a pass either satisfies the limits or does not, so the store can never bloat and the recommender&apos;s grounding cost is bounded by construction.</advantage>
    <drawback>A rule whose condition does not fit the limit gets truncated or split into two shallower entries, and a count ceiling forces an unrelated prune whenever a genuinely new principle arrives at capacity — the cap decides what survives, not the reasoning the goal says takes precedence.</drawback>
  </alternative>
  <alternative id="Qualitative bar, Origin dropped">
    Keep the qualitative bar as the only standard and remove the *Origin:* line, relying on the answer commits&apos; diffs (which the reworked capture reconstructs anyway) as the sole record of where a principle came from.
    <advantage>Shortest possible entries — every line the recommender reads is directive, none is provenance.</advantage>
    <drawback>The originating case is what lets capture judge whether current reasoning contradicts an entry or merely narrows it, and a store entry with no pointer forces a git archaeology pass to recover it every time an entry is revised, salvaged, or audited by a human.</drawback>
  </alternative>
  <recommendation option="Soft target plus qualitative bar">A numeric target the skill can act on, held under the qualitative bar so a rule keeps the clause it needs, is what turns the goal&apos;s new shorten move into something a pass actually fires; Origin survives as one line because the originating case is what a salvage-vs-revise judgment reads, and an entry-count ceiling is unnecessary once prune and merge by contradiction already bound the store.</recommendation>
</open-question>
<open-question id="Salvage form for contradicted entries" status="deferred">
  <question>When current reasoning contradicts an existing entry that was cited and then overridden, what forms may the salvage take: narrow the entry&apos;s scope, generalize it so both cases fit, replace it, or delete it outright when nothing generalizes?</question>
  <alternative id="Full salvage ladder">
    All four forms are permitted, attempted in a fixed preference order — narrow the entry&apos;s scope clause, generalize it so both the accepted citations and the override fit, replace it with a fresh directive when its premise is wrong, and delete only when nothing survives — with the chosen form visible in the working-tree diff the user reviews before the rewrite is committed.
    <advantage>Preserves the most validated knowledge: the store&apos;s entries already open with an explicit &quot;When a question…&quot; scope clause, so a single override usually only proves the rule mis-scoped rather than wrong, and the ladder lets capture keep what the entry&apos;s prior accepted citations confirmed while still honoring the goal&apos;s &quot;salvage what it can&quot; and &quot;shrink as well as grow&quot; mandate.</advantage>
    <drawback>Four candidate moves per contradicted entry is the most judgment per entry, and repeated narrowing across milestones can accrete exception clauses that push the entry past the compactness bar unless each step is held to the shortest entry that still predicts both cases.</drawback>
  </alternative>
  <alternative id="Narrow or delete">
    The salvage is binary: carve the overriding case out of the entry&apos;s scope clause, or remove the entry; no generalizing or replacing.
    <advantage>Simplest and most deterministic — each edit is a small, recognizable diff to an existing entry, and the entry keeps its title, origin, and tie-breakers.</advantage>
    <drawback>A single override almost never licenses deletion, so in practice every contradiction becomes another &quot;except when…&quot; clause, which is the exact bloat the goal&apos;s compactness aim forbids, and the form cannot express the case where the override reveals the deeper rule the old entry was only an instance of.</drawback>
  </alternative>
  <alternative id="Replace outright">
    A contradicted entry is decommissioned and a new entry is written from the override&apos;s rationale, so the store always reflects the newest reasoning.
    <advantage>Clean: no accreted exceptions, no stale tie-breakers, and the newest deliberated reasoning wins unambiguously, matching &quot;current reasoning takes precedence.&quot;</advantage>
    <drawback>Over-weights one decision against a history of confirmed acceptances — entries such as Name by distinctive function have been cited and accepted many times — so it throws away validated scope and worked examples that the override never disputed.</drawback>
  </alternative>
  <alternative id="Generalize or delete">
    Capture must restate the entry so both the original cases and the override fit, and deletes it when no such restatement exists; narrowing and replacing are not offered.
    <advantage>Every surviving entry is the most reusable rule the evidence supports, with no case-specific carve-outs.</advantage>
    <drawback>Forced generalization tends toward vagueness (&quot;prefer the better-fitting option&quot;) that fails the &quot;reads as an intuitive rule&quot; test, and it excludes the most common honest outcome — the principle is right in its domain and simply did not apply here — which narrowing expresses in one clause.</drawback>
  </alternative>
  <recommendation option="Full salvage ladder">Allow all four forms in the order narrow, generalize, replace, delete, because the store&apos;s entries already carry explicit scope clauses that make narrowing the natural first move while the goal explicitly asks capture to prune, merge, generalize and salvage what it can; when two forms fit equally, the tie-break is whichever yields the shortest entry that still predicts both the prior accepted citations and the override.</recommendation>
</open-question>
<open-question id="Skill framing after decoupling" status="deferred">
  <question>With a required milestone id, is capture still documented as the optional post-finish follow-up in README.md and CLAUDE.md, or reframed as an on-demand skill runnable for any milestone at any time?</question>
  <alternative id="Keep post-finish framing">
    Keep documenting capture in README.md and CLAUDE.md as the optional follow-up run after /finish-current-milestone, updating only the resolution sentence to say the milestone comes from the required id argument instead of the last Completed Milestones row.
    <advantage>Smallest documentation change, and the finish moment stays the one canonical cue for when to run it, which is exactly when a milestone&apos;s answer set is guaranteed complete.</advantage>
    <drawback>The docs would describe a constraint the skill no longer has: a required id is the whole point of decoupling, so framing it as post-finish-only hides the legitimate backfill run over milestones 6-18, which is the first real use the store will ever get.</drawback>
  </alternative>
  <alternative id="Reframe as on-demand skill">
    Move capture out of the Ending a milestone stage into the on-demand family beside /ask-in-milestone-context, documented as runnable for any milestone id at any time with no reference to finish.
    <advantage>Documentation matches the actual contract exactly, and backfilling the never-populated store across earlier milestones becomes discoverable rather than something a reader has to infer is allowed.</advantage>
    <drawback>Loses the pipeline cue that tells a user when to run it, so capture is easy to forget entirely or to run on a milestone whose answers are still being recorded, harvesting a partial decision history.</drawback>
  </alternative>
  <alternative id="On-demand contract, finish as natural moment">
    Document the contract as on-demand (any milestone id, any time, backfill explicitly allowed) while keeping its home in the Ending a milestone stage with the existing dashed optional edge, stating finish as the natural moment because the answer set is complete then, never as a precondition.
    <advantage>States the true contract and keeps the when-to-run cue, mirroring how README already places the on-demand /ask-in-milestone-context inside a stage with an any-time note.</advantage>
    <drawback>Two framings in one entry can read as hedging, and every surface must say post-finish is a convention rather than a precondition or the CLAUDE.md invariants drift back toward the pointer-none design.</drawback>
  </alternative>
  <recommendation option="On-demand contract, finish as natural moment">The required id makes the contract on-demand by construction and the store&apos;s first real run is a backfill, but finish remains the one moment a milestone&apos;s answer set is complete, so the docs keep that as the natural trigger while never stating it as a precondition.</recommendation>
</open-question>
