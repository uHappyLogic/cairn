# Milestones

This file tracks milestone progress. It is the source of truth for which milestone is current.

Each milestone lives at `milestones/milestone_<N>_<slug>/` and contains:

- `requirements.md` — goal, relevant starting state, decisions, open questions
- `TASKS_TODO.md` — pending tasks ordered by priority (highest first)
- `TASKS_DONE.md` — completed tasks

## Current Milestone

Current milestone: none

## Milestone History

### Milestone 15 — Runtime layer de-duplication

- De-duplicated the whole 32-file runtime layer (`skills/*/SKILL.md`, `agents/*.md`, `shared/*.md`) across eleven per-file sweep tasks, removing 7,597 words (32,758 → 25,161, −23.2% of the layer) under the rule that a sentence may be cut only where its content survives earlier in the same file, in a referenced shared procedure, or in a `CLAUDE.md` invariant.
- Retired the `## Rules` heading across the layer (−3,221 words), relocating each surviving unique rule into the step it constrains or, for rules constraining the whole skill, into the file's opening description paragraph as prose.
- Moved editor-facing rationale out of the runtime files into the `CLAUDE.md` invariants (−2,772 words), trimmed cross-file narration of counterparts to the one sentence each contract needs (−1,303 words), and rendered the `recommend-open-question` agent's `<open-question>` XML sub-element template once instead of twice (−68 words).
- Consolidated the `CLAUDE.md` `## Invariants to preserve when editing skills` section in a single post-sweep pass — merging ten overlapping bullets and absorbing the relocated rationale (35 bullets / 4,839 words → 25 bullets / 5,255 words) — under its own constraint-preservation ledger.
- Recorded every cut in the pipeline's own `**Verified:**` channel, one ledger bullet per imperative removed or relocated naming where that imperative now survives, adding no separate checklist artifact under the milestone directory.
- Verified `README.md`'s skill reference and workflow prose against the swept layer and found no sweep-caused falsification, so `README.md` was left unedited; two pre-existing stale claims (`goto-next-milestone`'s arguments and `finish-current-milestone`'s next-step pointer) were recorded as follow-ups rather than fixed.
- Ran seven fresh-context whole-layer re-audits with fix tasks between them: the runtime layer returned zero lost constraints for the last five passes and zero residual restatements for the last three, while the remaining findings were false evidence inside `TASKS_DONE.md` ledger bullets — the milestone ends without a clean overall verdict, the queued eighth re-audit pass having been removed from the task list.
- Extended `scripts/migrate_skills_to_agy.py` to copy `shared/` into the generated Antigravity tree, mirroring its existing `agents/` copytree, and regenerated `.agents/plugins/cairn/` against the final layer, leaving the `${CLAUDE_PLUGIN_ROOT}` path rewrite as a recorded follow-up.

### Milestone 14 — Brief-level task pipeline

- Flattened the task pipeline to a single brief-level altitude: every entry in `TASKS_TODO.md` is now a `##` title plus a 1–3 sentence description and a trailing `---`, with no `Provides`/`Notes`/`Success` sections, whichever path authored it.
- Replaced `shared/submit-procedure.md` with `shared/task-format.md`, holding only the brief-level template and its four authoring guidelines — referenced via `${CLAUDE_PLUGIN_ROOT}` by both authoring runners (`derive-tasks` and the `submit-task` skill) and parsed by `shared/complete-procedure.md`.
- Made `derive-tasks` the single writer on the derivation path: it now writes its ordered briefs into `TASKS_TODO.md` itself, retiring the per-brief dispatch loop and deleting the `submit-task` agent, leaving `complete-task` as the plugin's only remaining skill+agent pair.
- Leaned down the `submit-task` skill to author the same brief-level format inline and own the position-anchored insertion itself, keeping its triage, position decision, and `Task-submission:` commit unchanged.
- Reworked `shared/complete-procedure.md` to be self-sufficient at brief altitude: it derives each task's acceptance bar from the description plus `requirements.md`, resolves cross-task references by reading prior tasks' live deliverables, and records the derived bar in the `TASKS_DONE.md` entry as a `**Verified:**` bullet list.
- Reconciled `CLAUDE.md` and `README.md` with the flattened design (layout, pipeline listing, skill reference, diagrams, and the derivation/altitude/template invariants) and regenerated the checked-in Antigravity plugin tree under `.agents/plugins/cairn/`.

### Milestone 13 — agy-integration-polish

- Updated the `scripts/migrate_skills_to_agy.py` script to strictly enforce YAML frontmatter (`name` and `description`) on legacy source skills, failing fast instead of injecting dummy fallbacks.
- Documented the local transpilation build step for Google Antigravity in both `CLAUDE.md` and a new development section in `README.md`.
- Updated the GitHub repository description to explicitly reflect dual-platform support for Claude Code and Google Antigravity.

### Milestone 12 — Work-Type-Agnostic Sweep

- Completed Cairn's transformation into a fully work-type-agnostic workflow, finishing what the Generic Naming Refactor (milestone 3) began by removing every remaining assumption that the user's own deliverable is software engineering.
- Neutralized the two SE-saturated shared task cores (`shared/complete-procedure.md`, `shared/submit-procedure.md`) — reframing insertion-points/assertions/exports/build-test language and replacing the Unity tower-defense worked example with a canonical work-type-neutral written-guide example ("Draft the Getting Started section of the user guide").
- Reframed the verification mechanism so a task is checked against its Success criteria however the project defines done, with a direct criterion-by-criterion inspection fallback when CLAUDE.md names no done-verification convention — no build assumed.
- Replaced the "You are a Software Engineer" agent personas and swept the code/codebase framing across the skill layer, plus replaced the recurring environment-context enumeration ("tech stack, build/test commands, MCP tools") with the neutral "the project's domain context, working conventions, available tools, and how work is verified as done" across its seven reader files and the CLAUDE.md invariant (retaining a generalized `/init` pointer).
- Neutralized all software/game illustrations (RailCameraSnapper, Cinemachine cameras, the Arc-drive/swing question titles, shooting-mechanic goal examples) to the one canonical "Getting-started section order" / user-guide worked example, reused consistently, and swept the plugin's own `README.md` and `CLAUDE.md` while keeping Cairn's operating mechanics (git commits, path-scoped staging, file names) exempt as plugin infrastructure.
- Proved success with two independent fresh-context re-audits — the first surfaced 7 residual findings closed by two follow-up tasks, and the final re-audit returned an explicit zero-findings verdict.

### Milestone 11 — Terse Skill Reporting

- Cut every file-mutating, committing skill's success-path console output to a single fixed terse status line carrying no identifier (e.g. "Milestone defined.", "All tasks completed.", "Recommendations embedded."), since the committed diff and `git log` are the durable record of what changed.
- Applied the terse cut across all skill groups: the milestone-lifecycle skills, the three answer skills, `review-milestone-requirements`, the task-level/capture skills, `finish-current-milestone`, and the four orchestrators (each of which now prints one line for the whole run with no per-item loop output).
- Preserved the genuinely git-absent, decision-critical advisories alongside the terse line — `review-milestone-requirements`' convergence verdict and still-open list, `derive-tasks`' untraceable-requirement flag, and the answer skills' newly-exposed-open-questions note.
- Gave each committing skill a distinct one-line no-op message for when its dirty-own-path guard fires, since git holds no durable record of a no-op, while leaving all failure and clean-stop paths' full explanatory messages intact.
- Retired `finish-current-milestone`'s runtime "Suggest the next steps" block — including its recommendation of `/capture-milestone-principle-updates` and its `/define-milestone-goal` pointer — with the finish→capture handoff kept only as documented workflow guidance.
- Added a standalone terse-success-reporting invariant to `CLAUDE.md` (its sole durable home, since there is deliberately no shared `report-procedure.md`) and reconciled `CLAUDE.md` and `README.md` so no passage claims a skill prints a prose success summary or a runtime next-step recommendation.

### Milestone 10 — Skill-Layer Commits

- Established committing as a property of the skill layer: every user-invoked skill that changes files commits exactly those changes path-scoped under a distinct function-derived subject prefix, while dispatched agents never commit and orchestrators commit their agents' work after they return.
- Created `shared/commit-procedure.md` as the single source of truth for the skill-layer commit step (path-scoped staging, dirty-own-path no-op guard, function-derived `<Marker>: <descriptor>` subject convention), referenced by all committing skills and orchestrators.
- Converted 11 previously non-committing or partially-committing skills to commit their changes: `define-milestone-goal`, `specify-milestone-starting-state`, `modify-milestone-goal`, `review-milestone-requirements`, `submit-task`, `complete-task`, `recommend-all-open-questions`, `finish-current-milestone`, `capture-milestone-principle-updates`, and `goto-next-milestone`.
- Moved the `answer-all-open-questions-with-recommendation` commit from the dispatched agent up to the orchestrator (per answer), preserving one-commit-per-answer while obeying the skill-layer rule that agents never commit.
- Unified the per-skill subject convention: `complete-all-tasks` now commits under a function-derived prefix with the task heading moved to the commit body, and `recommend-all-open-questions` commits once at the end instead of being deliberately non-committing.
- Updated `CLAUDE.md` and `README.md` to document the layer-based commit rule, retiring the old role-based committing-vs-staging invariant and the milestone-7 agent-commits divergence.

### Milestone 9 — Open-Question XML Format

- Converted the open-question representation in `requirements.md` from the one-line Markdown blockquote (with its embedded `>`-run recommendation sub-block) to a well-formed, indented `<open-question id="..." status="open|deferred">` XML block — `<question>`, one or more `<alternative id="...">` with child `<advantage>`/`<drawback>`, zero or more sibling `<applied-principle>`, and a `<recommendation option="...">` — consolidated under the single `## Open questions` section while the prose sections stay Markdown.
- Established the query-where-it-pays convention: `review-milestone-requirements` authors the XML block, and the open-question skills locate/extract/remove via a dependency-free line-oriented `awk`/`sed`/`grep` CLI keyed on the `<open-question …>` / `</open-question>` boundary lines (never `xmllint`), while cross-document work (reconciliation, cascade analysis) still reads the whole file.
- Rewired `shared/answer-procedure.md` (locate + whole-block remove) and `shared/answer-with-recommendation-procedure.md` (locate + single-element `<recommendation>` lift with reverse entity-substitution) to the CLI/XML idiom, keeping their SHORT TITLE + ANSWER / SHORT-TITLE-only input contracts unchanged.
- Taught the `recommend-open-question` agent to render alternatives/applied-principle/recommendation as `<open-question>` sub-elements, and rewired the `recommend-all-open-questions` and `answer-all-open-questions-with-recommendation` orchestrators plus `discuss-open-question` and the answer wrappers to the XML blocks (whole-block-replacement embedding, `<recommendation>`-element idempotency/gather keys).
- Pinned the block contract in `## Decisions`: single-line id-first double-quoted opening tag, uniform five-predefined-entity escaping, 2-space-per-level indentation, case-folded `id` matching, sibling `<applied-principle>` for provenance-free lift, and the `<recommendation option>` → `<alternative id>` link with the "`<option>` — `<rationale>`" lift mapping.
- Re-synced `CLAUDE.md` invariants and `README.md` (skill reference, the *Iterating milestone requirements* section prose and diagram, and the answer-principle-learning-loop bullet) to the XML format and the query-where-it-pays convention, with all skill/agent edits made through the `skill-creator` plugin.

### Milestone 8 — Principles As Recommendation Advisor

- Reframed the project-wide answering principles from a binding auto-answer engine into a recommendation advisor, deleting the `try-answer-all-questions-by-principle` orchestrator skill and its read-only `try-answer-question-by-principle` subagent so no auto-answer path remains.
- Made the shared recommendation core `shared/recommend-procedure.md` principle-aware: its grounding step reads the fixed-path store `milestones/answer_decision_principles.md` in place, and a bearing confirmed principle acts as a weighted advisory factor (strong default, merit-override-only-with-a-named-reason, never a veto) that is cited whenever it influenced the recommended pick.
- Taught the `recommend-open-question` agent to render each bearing principle as its own `> **Applied principle:** <Short Title>` line stacked above the last-line `> **Recommendation:**` anchor, keeping the lifted anchor provenance-free by construction.
- Scrubbed the now-dead auto-answer provenance vocabulary (`Principle-based-answer:` subject, `Answer-Principle:` trailer, capture's exclusion grep, the manual-vs-sweep discriminator, and the revert-then-re-answer wording) from the `skills/`, `agents/`, and `shared/` layer.
- Repointed the principle-store header to name the recommendation core as the consumer, leaving the four principle entries and their `*Origin:*` lines byte-for-byte unchanged.
- Synced `CLAUDE.md` and `README.md` (skill roster, layout, pipeline block, invariants, the answer-principle-learning-loop prose, and the *Iterating milestone requirements* Mermaid diagram) to the recommendation-advisor model.

### Milestone 7 — Answer Open Questions With Recommendation

- Extracted recommendation-recording out of `answer-open-question` into a new execution-neutral shared procedure `shared/answer-with-recommendation-procedure.md` that lifts a question's embedded `> **Recommendation:**` anchor (with a no-anchor guard) and composes over `shared/answer-procedure.md`, leaving that recording core's ANSWER-as-input contract unchanged.
- Added the `answer-open-question-with-recommendation` skill+agent pair over that procedure: the skill runs it inline and commits its own path-scoped answer, and the file-editing agent runs it in isolation, commits its own answer, and returns `DONE`/`FAILED` — a deliberate mutation-in-agent divergence from the read-only-subagent design of `try-answer-all-questions-by-principle`.
- Added the `answer-all-open-questions-with-recommendation` orchestrator that sweeps every open/deferred question carrying an embedded recommendation and dispatches the file-editing agent strictly sequentially (gather-once-most-significant-first + per-dispatch re-read/skip), where the agent — not the orchestrator — owns each one-commit-per-answer commit.
- Fixed the recommendation-answer commit subject to the distinct `Recommendation-answer: <Short Title>`, which matches neither `^Manual-answer:` nor `Principle-based-answer:` so finish-time principle capture never harvests it, and widened the documented "individual skills never commit" exception from one skill to two.
- Narrowed `answer-open-question` to literal-only, replacing its removed record-recommendation mode with a targeted redirect guard that recognizes the retired `record the recommendation` sentinel (exact whole-string) and cleanly stops, pointing the user at `/answer-open-question-with-recommendation`.
- Repointed every stale recommend-sweep consumer pointer (in `recommend-all-open-questions` and `recommend-open-question`) to the new consumer, and synced `CLAUDE.md` and `README.md` (skill reference, layout, pipeline block, invariants, and the *Iterating milestone requirements* Mermaid diagram edge) to the new machinery.

### Milestone 6 — Recommend Open Questions

- Added the `recommend-all-open-questions` orchestrator skill: a non-interactive, argument-free batch path that sweeps the current milestone's open/deferred questions and embeds an alternatives+recommendation sub-block beneath each unchanged one-line question header.
- Added its read-only `recommend-open-question` subagent — the non-interactive twin of `discuss-open-question` — dispatched once per question, which grounds in the live project and returns the recommendation sub-block for the orchestrator to embed (mutating nothing itself).
- Extracted the "alternatives + recommendation for one question" analytical core into the new execution-neutral `shared/recommend-procedure.md`, now referenced (never restated) by both `discuss-open-question` and the `recommend-open-question` agent.
- Made the recommend sweep mutate-but-do-not-commit (path-scoped `git add`, no clean-tree precondition) and idempotent — it skips any block already carrying a `> **Recommendation:**` anchor, with a delete-the-sub-block-and-re-run escape hatch instead of a refresh mode.
- Gave `answer-open-question` a record-recommendation mode: the reserved sentinel answer text `record the recommendation` (exact whole-string match) lifts a block's embedded recommendation as the answer, and stops without changes when no recommendation is present.
- Generalized `shared/answer-procedure.md`'s block-removal step to clear the entire contiguous blockquote run (header plus any embedded recommendation), with the bare one-line header as the degenerate case.
- Synced `README.md` and `CLAUDE.md` to the new recommend-sweep path (skill reference, requirements-loop diagram, layout, pipeline block, and invariants).

### Milestone 5 — Milestone-finish Principle Capture

- Moved answering-principle capture off the per-answer path to an optional, recommended end-of-milestone step.
- `/answer-open-question` now commits its own `requirements.md` edit (path-scoped `git add`, subject `Manual-answer: <Short Title>`, rationale in the body, no `Answer-Principle:` trailer) instead of leaving it staged and chaining to capture — a deliberate, documented exception to the "individual skills never commit" invariant.
- Added the new finish-time skill `capture-milestone-principle-updates` (authored via `/skill-creator:skill-creator`) that distills principles from a milestone's `Manual-answer:` commits into the principle store via a two-phase flow (internal cross-candidate dedup, then strongest-first per-candidate revise-vs-add against the live store); it is now the sole writer of `milestones/answer_decision_principles.md`.
- Made `/finish-current-milestone` recommend (never auto-run) `/capture-milestone-principle-updates` in its step 8, ordered before `/define-milestone-goal`.
- Retired the `try-capture-answer-principle` skill (on-demand per-answer capture) and the `reject-auto-answer` skill (its correction role replaced by the uniform "revert the auto-answer commit, then `/answer-open-question` to re-answer, principle reconciled at finish" flow), scrubbing every live cross-reference.
- Synced `CLAUDE.md` and `README.md` (including the per-phase Mermaid diagrams and the answer-principle-learning-loop prose) to the new capture model.

### Milestone 4 — README Pipeline Diagrams

- Replaced the single oversized Workflow pipeline Mermaid diagram in `README.md` with six smaller per-phase `flowchart TD` diagrams (setup, milestone init, requirements loop, automated derivation/completion, follow-up, ending), each in its own `###` subsection with short flow prose.
- Chained the per-phase diagrams via the shared parallelogram state seam nodes `D0`–`D5`, each internal seam node appearing in its two adjacent diagrams, with the cross-phase "next milestone" loop hosted on the receiving *Initializing a milestone* diagram.
- Trimmed every skill node to its bare skill name (no inline descriptions or `(optional)`/`(auto)` qualifiers), keeping the `## Skill reference` section as the single home for full descriptions.
- Retained per-diagram phase-colour styling for cross-diagram identity, kept the amber `state` styling and parallelogram shape on the seam nodes, flattened the former hexagon nodes to plain boxes, and dropped the stale `linkStyle` line tied to the old monolith's edge indices.
- Fixed the stale `## Self-dogfooding` reference from `milestone_01_public-release-prep` to the current `milestone_04_readme-pipeline-diagrams` — the milestone's single mandated polish edit.

### Milestone 3 — Generic Naming Refactor

- Retired coding-flavored vocabulary across the whole plugin so Cairn reads as a generic idea-to-done workflow, in a clean break with no aliases.
- Renamed the task-execution machinery from "implement" to "complete": `complete-all-tasks` (orchestrator), `complete-task` (skill + agent), and `shared/complete-procedure.md`, with the dispatch type-string updated to match.
- Dropped the redundant "backlog" noun: `submit-backlog-task` → `submit-task` (skill + agent), `discuss-new-backlog-task` → `discuss-new-task`, and renamed `populate-backlog` → `derive-tasks` to name that tasks derive from the requirements.
- Applied the fan-out naming grammar `<verb>-all-<plural-object>`, renaming the answer sweep `try-answer-questions-by-principle` → `try-answer-all-questions-by-principle` while keeping its read-only subagent singular.
- Renamed the `requirements.md` template headings `## Relevant implementation state` → `## Relevant starting state` (and its writer skill to `specify-milestone-starting-state`) and `## Implementation decisions` → `## Decisions`, updating every reader and writer.
- Swept residual generic "implementation"/"implement" prose out of the authoring, clarification, and open-questions skills, and re-synced `README.md` and `CLAUDE.md` with the new vocabulary.
- Added the manually-run `migrate-workspace` skill that upgrades an existing consuming workspace's `milestones/` artifacts to current conventions, with an extension point for future migrations.

### Milestone 2 — Answer Principle Learning Loop

- Added the project-wide answering-principle store `milestones/answer_decision_principles.md` (at the `milestones/` root, shared across all milestones) as the accumulating basis for autonomous question resolution.
- Extracted the answer-recording core into `shared/answer-procedure.md`, now the single source of truth referenced (never restated) by both `answer-open-question` and the sweep orchestrator.
- Added the `try-capture-answer-principle` skill, which extracts and user-confirms reusable answering principles after each manual answer and is the sole writer of the principle store.
- Renamed `answer-obvious-open-questions` → `try-answer-questions-by-principle`: an orchestrator that resolves open questions by candidate elimination against confirmed principles, committing one auto-answer per commit with the applied principle named in an `Answer-Principle:` trailer.
- Added the read-only `try-answer-question-by-principle` subagent that performs per-question candidate elimination and returns a structured verdict, leaving all document mutation and committing to the orchestrator.
- Added the `reject-auto-answer` skill to revert a bad auto-answer commit, reopen its question, and direct the user to re-capture the offending principle.
- Synced `README.md` (Mermaid workflow + per-skill reference) and `CLAUDE.md` (layout, skills overview, invariants) with the new principle-learning loop.

### Milestone 1 — Public Release Preparation

- Renamed the plugin from `workflow` to **Cairn** across the manifest and `CLAUDE.md`, with the tagline "Mark the path from idea to shipped."
- Moved the current-milestone pointer out of `CLAUDE.md` into a single grep-able `Current milestone:` line in `milestones/README.md`, now the sole source of truth.
- Added `shared/get-current-milestone.md` as the one shared snippet all readers use to resolve `<MILESTONE_DIR>`, and migrated every reader and writer skill/agent onto it.
- Adopted zero-padded two-digit milestone numbering (`milestone_01_…`) with the next number derived by scanning `milestones/`.
- Added an MIT `LICENSE` and `.claude-plugin/marketplace.json`, making the repo installable via `/plugin marketplace add uHappyLogic/cairn`.
- Rewrote `README.md` as a public, adoption-focused landing page with a Mermaid workflow flowchart and a banner image concept.

## Completed Milestones

| # | Title | Path |
|---|-------|------|
| 1 | Public Release Preparation | `milestones/milestone_01_public-release-prep/` |
| 2 | Answer Principle Learning Loop | `milestones/milestone_02_answer-principle-learning/` |
| 3 | Generic Naming Refactor | `milestones/milestone_03_generic-naming-refactor/` |
| 4 | README Pipeline Diagrams | `milestones/milestone_04_readme-pipeline-diagrams/` |
| 5 | Milestone-finish Principle Capture | `milestones/milestone_05_milestone-finish-principle-capture/` |
| 6 | Recommend Open Questions | `milestones/milestone_06_recommend-open-questions/` |
| 7 | Answer Open Questions With Recommendation | `milestones/milestone_07_answer-all-with-recommendation/` |
| 8 | Principles As Recommendation Advisor | `milestones/milestone_08_principles-recommendation-advisor/` |
| 9 | Open-Question XML Format | `milestones/milestone_09_open-question-xml-format/` |
| 10 | Skill-Layer Commits | `milestones/milestone_10_skill-layer-commits/` |
| 11 | Terse Skill Reporting | `milestones/milestone_11_terse-skill-reporting/` |
| 12 | Work-Type-Agnostic Sweep | `milestones/milestone_12_work-type-agnostic-sweep/` |
| 13 | agy-integration-polish | `milestones/milestone_13_agy-integration-polish/` |
| 14 | Brief-level task pipeline | `milestones/milestone_14_brief-level-task-pipeline/` |
| 15 | Runtime layer de-duplication | `milestones/milestone_15_runtime-layer-dedup/` |
