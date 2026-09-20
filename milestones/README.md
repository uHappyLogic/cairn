# Milestones

This file tracks milestone progress. It is the source of truth for which milestone is current.

Each milestone lives at `milestones/milestone_<N>_<slug>/` and contains:

- `requirements.md` — goal, relevant starting state, decisions, open questions
- `TASKS_TODO.md` — pending tasks ordered by priority (highest first)
- `TASKS_DONE.md` — completed tasks

## Current Milestone

Current milestone: none

## Milestone History

### Milestone 26 — README landing page

- Root `README.md` is now a landing page: its first screen is the release/CI/license badges and the centered three-repository adoption table (one-sentence caption, no `## Adoption` heading) above `# Cairn`, the bold tagline, the host-neutral one-liner "Milestone-driven development for your coding agent — any kind of work, one milestone at a time.", one simplified mermaid loop diagram (define → review → recommend → answer → derive → complete, plus a dashed answer → review return edge labelled "until no open questions remain", under the phase diagrams' shared theme block), and per-host `## Installation`, with the 4.7 MB banner and the `.github/assets/` directory deleted.
- Below the fold, `## Why Cairn?` reads host-neutrally ("Cairn gives your coding agent…"), a new `## Design principles` block presents claims 11, 2 (carrying claim 12's provenance subject), and 5 as their verbatim claim lines linked to the claims page over one design sentence each, and the tail runs `## How it works` (closing with links to both docs pages), `## Self-dogfooding`, `## Contributing`, `## Migrating from the old marketplace` (the pre-1.5.0 note demoted to an appendix reached from one bold pointer line in the Claude Code subsection), `## License`.
- A new `docs/` directory holds `docs/workflow.md` (the six phase sections with their mermaid diagrams, `## How skills commit`, and `## The answer-principle-learning loop` promoted to a sibling `##` section) and `docs/skill-reference.md` (the 23 per-skill and per-agent entries, with milestone 15's two stale entries — the argument-free `goto-next-milestone` and `finish-current-milestone`'s closing sentence — corrected in the move), every heading's text kept so the old README anchors survive path-prefixed.
- `docs/design-claims.md` commits the 19 design claims from the untracked `temp/` note word for word in Simplified Technical English, changing only the frame: a one-paragraph orienting intro for a repository reader, the closing note trimmed to the claims-17–19 sentence, and claim 12's clean-tree sentence corrected for the non-committing bootstrap skill and the partial-work-stays rule.
- Both distribution README templates under `scripts/hosts/*/README.md` share the landing shape — a centered two-badge strip of that repository's unique-views and unique-clones badges above `# Cairn for <Host>`, the same one-liner verbatim, the generated note's `traffic-data` sentence disclosing that the workflow's own daily fetch counts as one unique clone a day, and the host's installation section (the Claude one split exactly like the root's, with the migration note in its own section) over the `## Source` and `## License` tail, with no diagram, no "Why Cairn?" text, and no design-principles block — and `hosts/` is rebuilt with `uv run scripts/build_hosts.py --check` passing.
- `CLAUDE.md`'s repository layout describes the finished landing page and carries entries for the three `docs/` pages, its Skill Frontmatter invariant and `## Development` prose name `docs/skill-reference.md` and the first-screen adoption table as the new homes, and `CONTRIBUTING.md`'s Workflow pipeline link points at `docs/workflow.md#workflow-pipeline`, so no link in the repository targets a moved README section.

### Milestone 25 — Traffic Adoption Badges

- `README.md` carries a new `## Adoption` section between `## Skill reference` and `## Contributing`: a pipe table with one linked row per repository (`uHappyLogic/cairn`, `cairn-claude`, `cairn-antigravity`) and two badge columns (unique views, unique clones), each badge served from that repository's `traffic-data` branch and linked to it, under a caption dating the counts from 2026-09-04, explaining that unique counts sum each day's uniques, and disclosing the workflow's own daily clone plus the monorepo's CI checkouts.
- Every repository runs the same `traffic-badges` workflow daily at 03:17 UTC — `permissions: {}`, two steps of `albertoarena/github-traffic-badge` pinned to its `v1.1.4` commit SHA writing `views-unique.svg` and `clones-unique.svg` to the `traffic-data` branch — as three hand-kept copies: the monorepo's under `.github/workflows/` and one template per host under `scripts/hosts/<host>/.github/workflows/`, rendered into `hosts/<host>/` and shipped as inert cargo in installed trees behind a leading runs-only-in-its-distribution-repository comment.
- The build's `unfilled-placeholder` gate now matches `(?<!\$)\{\{` — a `{{` not immediately preceded by `$` — so GitHub Actions `${{ … }}` expressions pass in rendered workflow files while bare `{{VERSION}}`/`{{NAME}}`/`{{PLUGIN_ROOT}}` slots still fail, with no path-scoped exemption or new definition key.
- Both distribution README templates, both `CONTRIBUTING.md` pointers, and the root README's Installation line scope their build-output claims to `main` and name the `traffic-data` branch as the one thing in each distribution repository no build renders and no release touches.
- Release 1.5.1 was cut mid-milestone to publish the workflow templates into both distribution repositories through the documented release route, so their `main` advanced only by a release snapshot.
- The fine-grained token was extended in place with Contents read-and-write on the three repositories, stored as the `TRAFFIC_TOKEN` secret on each with `gh secret set`, and its local copy at `temp/PAT` deleted, so the token now exists only in GitHub's write-only secret store.
- One `workflow_dispatch` per repository seeded every `traffic-data` branch (14 days of `totals.json` from 2026-09-04) before the README referenced a badge, and all six badge URLs return HTTP 200.
- Read-only `gh api` readings, dated in `requirements.md`, show the action author's own repository still `active` on nothing but the daily bot push at day 75 and 77 past its last human commit, and both distribution repositories advancing `pushed_at` with public `PushEvent`s on `refs/heads/traffic-data` after their first scheduled runs — the evidence that the daily push keeps the cron workflows clear of GitHub's 60-day inactivity disable.

### Milestone 24 — Repo Hygiene Surface

- A GitHub Actions drift-gate workflow at `.github/workflows/drift-gate.yml` runs `uv run scripts/build_hosts.py --check` on every push and pull request with no branch or path filter, both actions pinned to full commit SHAs, and the README badge row carries a third shields.io CI badge beside the release badge.
- Root `CONTRIBUTING.md` spells out the proposal-first contributor workflow — the maintainer reserves a milestone with `/define-milestone-goal` on `main` without activating it, the contributor runs it in a fork from `/goto-next-milestone` through `/finish-current-milestone`, syncing from `main` by merge only while its pointer reads `none`, and the pull request lands as a merge commit followed by `/capture-milestone-principle-updates` — and carries the build-loop `## Development` section moved whole out of the README, whose slot now holds a short `## Contributing` routing section.
- Root `SECURITY.md` directs vulnerability reports to GitHub private vulnerability reporting only, with a supported-versions table naming the latest release, and root `CODE_OF_CONDUCT.md` is Contributor Covenant 2.1 verbatim; both stay root-only, never rendered into a host tree.
- `.github/ISSUE_TEMPLATE/` holds three YAML issue forms — bug (required host dropdown, cairn version, and skill invoked), feature, and milestone proposal — beside a `config.yml` that disables blank issues and routes questions to the Discussions Q&A category, and `.github/PULL_REQUEST_TEMPLATE.md` asks for the reserved milestone id and the proposal issue over a seven-item finished-milestone checklist.
- Each host definition under `scripts/hosts/<host>/` carries a `CONTRIBUTING.md` template rendered into its host tree, so every distribution repository points visitors at the root repository for issues, pull requests, and vulnerability reports.
- Root `CHANGELOG.md` is backfilled from all sixteen GitHub releases verbatim under `## <VERSION> — <YYYY-MM-DD>` headings (the eight sectioned release pages demoted to `###` sections so every entry equals its page body byte for byte), and `/release-plugin` now prepends each release's entry inside the `Release: <VERSION>` commit, gates on that entry in pre-flight, publishes the committed entry to every release page on fresh runs and resumptions alike, and amends the unpushed commit to revise the notes at its pause.
- Repository settings on `uHappyLogic/cairn` now have Discussions and private vulnerability reporting enabled and squash merges and the wiki disabled, each read back and recorded in the settings task's Verified bullets.

### Milestone 23 — Multi-Host Core And Dist Repos

- The runtime layer is authored once, host-neutrally, under `core/` (21 skills, 3 agents, 7 shared procedures): every cross-reference uses the `{{PLUGIN_ROOT}}` placeholder, the 24 Claude-specific resolve hints are deleted, and no `core/` file names a host — the repair step, dispatch sites, and init template are keyed on capabilities and the plugin's own namespace, while the agents' Claude-only `color` key stays in `core/` and is stripped by data.
- Each host is a declarative definition directory `scripts/hosts/<host>/` — a `settings.toml` under one shared key set beside manifest and README templates with `{{VERSION}}`/`{{NAME}}` slots — and `scripts/build_hosts.py [<host> ...] [--check]` renders every selected host from `core/` through a full validation gate (no host name in `core/`, frontmatter and 25-word descriptions, no `{{`, no foreign or dangling plugin-root literal, no stripped key, every version slot equal to `VERSION`), swapping trees in only when all pass; `--check` is the byte-for-byte drift gate and `scripts/migrate_skills_to_agy.py` is gone.
- The committed `hosts/claude/` and `hosts/antigravity/` trees are pure build output; the root `skills/`, `agents/`, `shared/`, and `.agents/` trees and the root `.claude-plugin/plugin.json` are removed, and the monorepo marketplace points at `./hosts/claude`.
- A root `VERSION` file is the single source of truth for the plugin version: `set_version.py` writes it with its three mirrored surfaces (`.claude-plugin/marketplace.json`, `pyproject.toml`, `uv.lock`) and never touches `hosts/`, whose manifest and README version slots the build renders from it.
- The release skill runs the `--check` drift gate and a per-host `gh repo view` existence pre-flight (printing the exact `gh repo create`/`gh repo edit` commands when a repository is missing), stages `hosts/` with the version surfaces so the Release commit changes only version slots, and in step 8d publishes each `hosts/<host>/` tree into `uHappyLogic/cairn-<host>` as one `git commit-tree` commit atomically pushed to `main` and the `<VERSION>` tag, followed by a distribution GitHub release carrying the monorepo's notes.
- The distribution repositories `uHappyLogic/cairn-claude` and `uHappyLogic/cairn-antigravity` exist — public, deliberately empty so the first publish becomes their root commit, with topics set and issues, wiki, and projects disabled so feedback routes to `uHappyLogic/cairn`.
- `README.md`'s Installation section is one subsection per host plus the shared bootstrap steps, with `cairn-claude` as the recommended Claude Code install source, a migration note for installs pinned to `uHappyLogic/cairn`, and an archive-extract path for Antigravity, each subsection word-for-word identical to its distribution README template.
- `CLAUDE.md` and `README.md` describe the `core/` → `scripts/hosts/` → `hosts/` model throughout, and the four stale `migrate-workspace` references are deleted.

### Milestone 22 — Drop Open-Question Status

- The `status` attribute is gone from `<open-question>` blocks: the opening boundary tag is now exactly `<open-question id="Short Title">`, and every locate and gather states its `id="([^"]*)"` extraction plainly, without the attribute-order justification the second attribute once required.
- `review-milestone-requirements` authors every finding it surfaces as one ordinary three-line block — the Blocking/Deferred triage, the deferred template, and the "low-risk-to-reverse" threshold were deleted with no reworded don't-raise rule in their place — and its convergence verdict, like the `derive-tasks` precondition, is now simply "no `<open-question>` block remains".
- The deferred pass-through in `derive-tasks` was removed, so no runtime control flow branches on the attribute anymore.
- Every "open or deferred", "whatever its `status`", and "reads no `status`" qualifier was swept from `shared/`, the two sweeps, the single-question skills, and both agents, leaving the boundary-line CLI, entity unescaping, case-folding, cascade, and `<depends-on>` reconciliation unchanged.
- `capture-milestone-principle-updates` keeps its pre-XML blockquote-form note (with its second marker corrected to `> **Open question — …:**`) as the one runtime survivor of the word "Deferred", relying on its id-anchored locate to absorb `status="…"` on historical removed lines without a note.
- `README.md` and `CLAUDE.md` describe only the current form — delete-only, with no retirement invariant or "do not reintroduce" sentence — and finished milestones' records were left as written; the Antigravity tree under `.agents/plugins/cairn/` was regenerated status-free.

### Milestone 21 — Recommendation Dependency Graph

- `recommend-all-open-questions` now dispatches strictly sequentially in most-significant-first order and embeds each accepted return before the next dispatch, so a later recommendation may build on sibling recommendations already embedded — retiring the recommendation-independence rule that forbade it.
- A recommendation that leans on an already-annotated sibling must declare it as a self-closing `<depends-on question="…" option="…"/>` child, placed after the alternatives and applied-principles and immediately before `<recommendation>`; a coupling on a not-yet-annotated sibling is expressed as prose instead, so no option is ever guessed.
- The sweep's acceptance gate gained a seventh test that resolves every returned `<depends-on>` one hop against the still-present annotated sibling blocks and their `<alternative id>` values — the first test to read the live document — with a miss taking the ordinary reason-string-plus-one-repair path and the orchestrator never dropping or rewriting a returned element.
- `shared/answer-procedure.md`'s cascade now reconciles surviving dependents: the matching `<depends-on>` tag is removed when the recorded option agrees with what the dependent assumed, and the dependent's embedded children are stripped transitively when it disagrees, is in doubt, or the target was removed with no option recorded — strip-on-doubt, because an extra dispatch is cheap while a stale rationale becomes a wrong decision.
- Its input contract widened to three fields with an optional **RECORDED OPTION**, whose presence selects exact-id comparison over judgment; the two lifting callers pass the id they already hold and `answer-open-question` explicitly passes nothing.
- `answer-all-open-questions-with-recommendation` now walks the dependency graph by depth from its origins — unresolvable edges dropped, same-depth ties in document order, a stranded cycle broken by promoting its document-order-first member — replacing the "loosely most-significant-first" significance proxy with a deterministic, total walk.
- `review-milestone-requirements` strips the embedded children of every dependent of a block it prunes or dedups, transitively and without recording any decision, giving an option-less removal the same treatment the answer cascade gives a mismatch.
- `capture-milestone-principle-updates`' diff read was scoped to the answered block's own boundaries with one element-agnostic sentence, so the orphan lines the cascade's tidy and strip outcomes leave in surviving siblings no longer feed the record.
- `CLAUDE.md` and `README.md` record the retirement of recommendation independence and the new dependency-graph behaviour across both sweeps; the Antigravity tree under `.agents/plugins/cairn/` was regenerated.

### Milestone 20 — Recommend Agent Return Robustness

- The `recommend-all-open-questions` sweep now judges each agent return through one per-return pipeline — a last-line `FAILED:` verdict tested before anything else, extraction of the region from the first `<alternative` line through the last `</recommendation>` line, then a single acceptance gate — so surrounding text is stripped rather than dropping a valid recommendation with it.
- That acceptance gate combines the two boundary tests with four line-greps in the boundary-line CLI idiom (no wrapper or `<question>` line, exactly one `<recommendation` opening line, at least one `<alternative id` line, and an entity-unescaped case-folded `option` matching one of those ids), needing no XML parser and no second control path.
- Every extraction or gate miss now takes exactly one repair attempt before any skip: continue the same agent session via `SendMessage` where the host allows it, otherwise one fresh re-dispatch with the same prompt plus the shape reminder — the branch the Antigravity build takes — with repairs issued on arrival while other dispatches are in flight and a per-question repair-spent marker holding the attempt to one.
- The corrective message is a fixed one-paragraph template rendered once in the skill with a single slot, filled with the same failed-test reason string the gate derives, quoting both shape tests verbatim and never quoting the offending prose back.
- `agents/recommend-open-question.md` step 4 was rewritten from the ground up as a draft → self-check → emit step whose only test list is those two shape tests, dropping the accumulated prohibition list whole while step 3's rendering specification stays byte-for-byte untouched.
- Console reporting stays terse: a question annotated only after extraction or after the repair gets no mention at all, and only questions still skipped after the repair path reach the step-6 advisory and the step-5 all-skipped no-op wording.
- `CLAUDE.md` and `README.md` record the deliberate reversal of the "discarded whole, never salvaged" rule with its evidence and a do-not-restore instruction, plus the scope boundary leaving `complete-task`, `answer-open-question-with-recommendation` and their orchestrators byte-for-byte untouched; the Antigravity tree under `.agents/plugins/cairn/` was regenerated.

### Milestone 19 — Principle Capture By Milestone

- `capture-milestone-principle-updates` now takes a required `<milestone_id>` argument, validated only by the existence of `milestones/<milestone_id>/requirements.md`, replacing the last-row-of-Completed-Milestones resolution so any milestone — current, unfinished, or long finished — can be harvested on demand.
- Its commit walk covers all three answer provenances (`Manual-answer:`, `Alternative-answer:`, `Recommendation-answer:`) and reconstructs from each commit's diff the recommendation, cited principles, and alternatives the user saw, classifying every commit by agreement against the removed recommendation and by deliberated-vs-bare body.
- Manual and alternative overrides are the sole source of new principles, prompted for an override reason with a best guess where the body records none behind a one-shot accept-all/skip-all/review choice, while accepted recommendations are evidence only — reinforcing cited entries and flagging contradicted ones.
- The per-candidate confirm-and-write loop was replaced by one whole-store rewrite composed in place over the working-tree baseline, so the store may shrink as well as grow through prunes, merges, generalizations, and shortenings under a soft 40–80-word compactness bar.
- A contradicted entry is salvaged through a fixed ladder — narrow, generalize, replace, delete only when nothing survives — tie-broken by the shortest entry that still predicts both the prior citations and the override, with reinforced entries shielded.
- Two start-of-run guards were added, each a one-line notice plus a single proceed confirmation: a repeat-capture guard grepping for the exact `Principle-capture: <milestone_id>` subject, and a dirty-store guard that makes the working-tree file the rewrite baseline.
- A single confirmation now gates the commit rather than the write, with a pre-write snapshot restored on rejection (never `HEAD`) and an explicit exit that skips `shared/commit-procedure.md`, and the `Principle-capture:` commit carries one body line per store change composed at commit time.
- `README.md`, `CLAUDE.md`, and the three answer skills were updated to record capture as an on-demand, milestone-id-driven harvester over all three provenances, with the finish-time run phrased as a convention and never a precondition.

### Milestone 18 — Agent Layer Improvements

- Dropped the pinned `model: opus` frontmatter line from the three `agents/*.md` files and the two skills that carried it (`answer-open-question-with-recommendation`, `answer-open-question-with-alternative`), so nothing in the plugin pins a model and every dispatched agent inherits the session model.
- Recolored the agents `red` (`complete-task`), `yellow` (`answer-open-question-with-recommendation`), and `blue` (`recommend-open-question`) — three distinct, luminance-separated values that stay tellable apart on a grayscale display, replacing the old `green`/`green`/`teal` set.
- Closed the recommend sweep's return-contract gap: `recommend-open-question` returns `FAILED: <reason>` on failure, and `recommend-all-open-questions` shape-checks every return (first text `<alternative`, last text `</recommendation>`) and skips rather than splices a malformed or failed one, leaving that block untouched and printing the skipped Short Titles with reasons as a git-absent advisory.
- Orchestrators now address dispatched agents by their namespaced registry name (`cairn:complete-task`, `cairn:recommend-open-question`, `cairn:answer-open-question-with-recommendation`), phrased descriptively at the dispatch site, and the recommend dispatch prompt carries `<MILESTONE_DIR>` so the agent grounds itself by reading that milestone's `requirements.md` instead of the orchestrator feeding it surrounding context.
- Replaced `complete-task`'s unimplementable untouched-tree-on-failure promise with a resumable contract: a failed or interrupted run leaves its partial work uncommitted, and `shared/complete-procedure.md`'s carry-out step treats already-uncommitted changes as a previous run's partial work to continue from rather than redo.
- The two file-editing agents path-scope `git add` their own change set and return a bare `DONE`/`FAILED: <reason>` with no hand-back payload; `complete-all-tasks` and `answer-all-open-questions-with-recommendation` commit that staged index, the latter lifting the `<recommendation>` text for its commit body during its pre-dispatch re-check while the block still stands.
- Reordered `shared/answer-procedure.md` so the decision is folded into `## Decisions` before the `<open-question>` block is removed, so an interruption between the two edits leaves a recoverable superset instead of a silently lost question.
- `scripts/migrate_skills_to_agy.py` now rewrites every `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference in the generated tree to `.agents/plugins/cairn/shared/<name>.md` and drops the `echo "$CLAUDE_PLUGIN_ROOT"` resolve hint, closing the milestone-15 follow-up under which those references resolved nowhere under Antigravity.

### Milestone 17 — Versioning And Release Tooling

- Added `scripts/set_version.py`, a one-argument `MAJOR.MINOR.PATCH` version script that writes every in-repo version literal — `.claude-plugin/plugin.json`, a new `version` field on `.claude-plugin/marketplace.json`'s single `plugins[]` entry, `pyproject.toml`, and `uv.lock`'s matching `cairn-tooling` line — and never touches git, `gh`, or the generated tree.
- Taught `scripts/migrate_skills_to_agy.py` to read the source manifest's version at generation time and copy it into the generated `.agents/plugins/cairn/plugin.json`, so the generated manifest carries a version on every regeneration path while `.claude-plugin/plugin.json` stays the single source of truth.
- Added the maintainer-only release skill at `.claude/skills/release-plugin/SKILL.md`, invoked as `/release-plugin <MAJOR.MINOR.PATCH>` — the sole documented home of the release procedure, outside the shipped `skills/` tree and the plugin's runtime-layer invariants.
- Gated a release behind four hard pre-flight stops (clean tracked tree, HEAD on `main`, `main` not behind `origin/main`, no untracked files under `skills/`, `agents/`, or `shared/`) and three pre-mutation version refusals (malformed literal, a tag that already exists locally or remotely, and a version not strictly greater than the last release compared as a numeric tuple).
- Gave the skill a note-composition step that derives release notes from the `Milestone-finish:` commits since the last release, cross-checks them against the `### Milestone` headings added to `milestones/README.md` over the same range and stops on a mismatch in either direction, and on an empty range shows commit-range-derived notes and proceeds only on explicit confirmation.
- Made the local half of a release exactly one `Release: <VERSION>` commit staged path-scoped over the version script's and the transpiler's write sets, followed by a single pre-publish pause showing the full composed body before the check-then-do branch push, bare `MAJOR.MINOR.PATCH` tag, and `gh` release creation, so a re-run with the same version resumes from the first incomplete step.

### Milestone 16 — Frontmatter Description Diet

- Cut all 24 plugin frontmatter descriptions (21 `skills/*/SKILL.md`, 3 `agents/*.md`) to a single independent clause of 25 words or fewer naming only what that skill or agent does, taking the always-on description budget from 1,411 words to 452 (−68%) and the longest single description from 149 words to 23.
- Restructured the six heaviest descriptions from scratch and shortened the nine mid-weight ones, deleting their trigger-phrase lists, mechanics, commit subjects, sequencing, cross-skill references, "Use when…" framing, and design provenance outright — descriptions are routing labels, never a record, so nothing cut was relocated.
- Audited the six descriptions already at or under the cap to the same bar, leaving byte-for-byte unchanged the three that carried no mechanics, sequencing, cross-skill reference, or banned punctuation.
- Compressed the three agent descriptions into that same one-clause shape while keeping each invocation contract as a short clause naming what the prompt carries (the task's heading text, the question's Short Title), and deleted the separate "dispatched by X, not called directly by the user" note.
- Enforced two machine-checkable bars across the set — no semicolon or colon in any description, and every raw frontmatter loads under `yaml.safe_load` with its `description:` line left unquoted — so the transpiler's re-quoting fallback survives as an unexercised net (`review-milestone-requirements` was the one file that tripped it).
- Extended `CLAUDE.md`'s **Skill Frontmatter** invariant into the single home of every rule governing the frontmatter `description` key, and revised milestone 15's runtime-prose bullet so it no longer exempts descriptions as "the triggering surface" — no new standalone invariant bullet was added.
- Ran the bounded falsification-only pass over `README.md`'s `## Skill reference` and `CLAUDE.md`'s workflow map and recorded it as a no-op: the rewrites changed one `description:` line per file and no skill or agent body, so no claim on either surface was falsified (`goto-next-milestone`'s stale README entry remains the pre-existing follow-up milestone 15 recorded).
- Regenerated the checked-in Antigravity tree at `.agents/plugins/cairn/` in a single closing run of `scripts/migrate_skills_to_agy.py`, with each of the 24 generated files byte-identical to its source and no transpiler source touched.

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
| 16 | Frontmatter Description Diet | `milestones/milestone_16_frontmatter-description-diet/` |
| 17 | Versioning And Release Tooling | `milestones/milestone_17_versioning-release-tooling/` |
| 18 | Agent Layer Improvements | `milestones/milestone_18_agent-layer-improvements/` |
| 19 | Principle Capture By Milestone | `milestones/milestone_19_principle-capture-by-milestone/` |
| 20 | Recommend Agent Return Robustness | `milestones/milestone_20_recommend-agent-return-robustness/` |
| 21 | Recommendation Dependency Graph | `milestones/milestone_21_recommendation-dependency-graph/` |
| 22 | Drop Open-Question Status | `milestones/milestone_22_drop-open-question-status/` |
| 23 | Multi-Host Core And Dist Repos | `milestones/milestone_23_multi-host-core-and-dist-repos/` |
| 24 | Repo Hygiene Surface | `milestones/milestone_24_repo-hygiene-surface/` |
| 25 | Traffic Adoption Badges | `milestones/milestone_25_traffic-adoption-badges/` |
| 26 | README landing page | `milestones/milestone_26_readme-landing-page/` |
