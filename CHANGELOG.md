# Changelog

Each entry is the notes of that version's [GitHub release](https://github.com/uHappyLogic/cairn/releases), verbatim, newest first.

## 1.5.1 — 2026-09-18

### Changes since 1.5.0

- Each distribution repository's tree now carries `.github/workflows/traffic-badges.yml`, a scheduled GitHub Actions workflow (daily at 03:17 UTC, plus manual dispatch) that records the repository's unique views and unique clones as badge SVGs on a `traffic-data` branch. It runs only in `uHappyLogic/cairn-<host>` and is inert in an installed copy of the plugin.
- The distribution READMEs and `CONTRIBUTING.md` pointers scope their generated-do-not-edit claim to `main` and name `traffic-data` as the one branch no release touches; the Antigravity install note now reads that `main` advances only by release snapshots.
- The host build's unfilled-placeholder check ignores a `{{` inside a GitHub Actions `${{ … }}` expression, so a workflow template can be rendered into a host tree while a bare `{{VERSION}}`, `{{NAME}}`, or `{{PLUGIN_ROOT}}` slot still fails the build.
- The maintainer-only `/release-plugin` skill now states that every placeholder is substituted braced, after an unbraced `$COMMIT:refs/heads/main` under zsh made the 1.5.0 distribution push land nothing on its first attempt.
- Nothing in the plugin runtime — skills, agents, shared procedures — changes in this release.

**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/1.5.0...1.5.1

## 1.5.0 — 2026-09-17

### Repo Hygiene Surface (milestone 24)

- A GitHub Actions drift-gate workflow runs `uv run scripts/build_hosts.py --check` on every push and pull request, with both actions pinned to full commit SHAs, and the README carries a CI badge reporting its status on `main`.
- Root `CONTRIBUTING.md` spells out the proposal-first contributor workflow — the maintainer reserves a milestone on `main` with `/define-milestone-goal`, the contributor runs it in a fork from `/goto-next-milestone` through `/finish-current-milestone`, and the pull request lands as a merge commit — and now holds the build-loop `## Development` section moved out of the README, which keeps a short `## Contributing` routing section in its place.
- Root `SECURITY.md` directs vulnerability reports to GitHub private vulnerability reporting, and root `CODE_OF_CONDUCT.md` adopts Contributor Covenant 2.1; both stay root-only and are never rendered into a host tree.
- Three YAML issue forms (bug, feature, milestone proposal) and a pull-request template replace blank issues, with questions routed to the newly enabled Discussions Q&A category.
- Every distribution repository now carries a `CONTRIBUTING.md` pointer sending visitors to `uHappyLogic/cairn` for issues, pull requests, and vulnerability reports.
- Root `CHANGELOG.md` holds every release's notes, backfilled from all sixteen GitHub releases, and each release now prepends its entry inside the `Release: <VERSION>` commit so the changelog and the release pages carry identical text.

### Multi-Host Core And Dist Repos (milestone 23)

- The runtime layer — 21 skills, 3 agents, 7 shared procedures — is authored once, host-neutrally, under `core/`: every cross-reference uses the `{{PLUGIN_ROOT}}` placeholder and no `core/` file names a host.
- Each host is a declarative definition directory `scripts/hosts/<host>/` (a `settings.toml` beside its manifest and README templates), and `uv run scripts/build_hosts.py [<host> ...] [--check]` renders every host from `core/` through a full validation gate, with `--check` as the byte-for-byte drift gate; `scripts/migrate_skills_to_agy.py` is gone.
- The committed `hosts/claude/` and `hosts/antigravity/` trees are pure build output; the root `skills/`, `agents/`, `shared/`, and `.agents/` trees and the root `.claude-plugin/plugin.json` are removed, and the monorepo marketplace points at `./hosts/claude`.
- A root `VERSION` file is the single source of truth for the plugin version; `set_version.py` writes it with its three mirrored surfaces and never touches `hosts/`, whose manifests the build renders from it.
- Each release now publishes every `hosts/<host>/` tree verbatim into its distribution repository — `uHappyLogic/cairn-claude` and `uHappyLogic/cairn-antigravity` — as one commit tagged with the release version, plus a GitHub release carrying the same notes.
- `README.md`'s Installation section is one subsection per host: `uHappyLogic/cairn-claude` is the recommended Claude Code install source (with a migration note for installs pinned to `uHappyLogic/cairn`), and Antigravity installs from an archive extract.

**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/1.4.0...1.5.0

## 1.4.0 — 2026-09-15

### Drop Open-Question Status (milestone 22)

- The `status` attribute is gone from `<open-question>` blocks: the opening tag is now exactly `<open-question id="Short Title">`, and every locate and gather extracts the `id` attribute alone.
- `review-milestone-requirements` no longer triages findings as Blocking or Deferred: every gap it surfaces is one ordinary question block, and it reports convergence simply when no `<open-question>` block remains — the same condition `derive-tasks` requires.
- `derive-tasks` lost its deferred pass-through, so no runtime control flow branches on a question's status anymore.
- Every "open or deferred" / "whatever its status" qualifier was swept from the shared procedures, both sweeps, the single-question skills, and both agents; the boundary-line CLI, entity unescaping, case-folding, cascade, and `<depends-on>` reconciliation behave exactly as before.
- `capture-milestone-principle-updates` still reads historical answer commits whose removed lines carry `status="…"`, absorbing them through its id-anchored locate with no extra handling.
- `README.md` and `CLAUDE.md` describe only the status-free form, and the Antigravity tree under `.agents/plugins/cairn/` was regenerated to match.

**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/1.3.0...1.4.0

## 1.3.0 — 2026-09-10

### Recommendation Dependency Graph (milestone 21)

- `/recommend-all-open-questions` now dispatches strictly sequentially in most-significant-first order and embeds each accepted return before the next dispatch, so a later recommendation may build on sibling recommendations already embedded — retiring the recommendation-independence rule that forbade it.
- A recommendation that leans on an already-annotated sibling declares it as a self-closing `<depends-on question="…" option="…"/>` child, placed after the alternatives and applied-principles and immediately before `<recommendation>`; a coupling on a not-yet-annotated sibling is expressed as prose instead, so no option is ever guessed.
- The sweep's acceptance gate gained a seventh test resolving every returned `<depends-on>` one hop against the still-present annotated sibling blocks and their `<alternative id>` values — the first test to read the live document — with a miss taking the ordinary reason-string-plus-one-repair path and the orchestrator never dropping or rewriting a returned element.
- Answering now reconciles surviving dependents: the matching `<depends-on>` tag is removed when the recorded option agrees with what the dependent assumed, and the dependent's embedded children are stripped transitively when it disagrees, is in doubt, or the target was removed with no option recorded — strip-on-doubt, because an extra dispatch is cheap while a stale rationale becomes a wrong decision.
- The shared recording procedure's input contract widened to three fields with an optional **RECORDED OPTION**, whose presence selects exact-id comparison over judgment; the two lifting callers pass the id they already hold and `/answer-open-question` explicitly passes nothing.
- `/answer-all-open-questions-with-recommendation` walks the dependency graph by depth from its origins — unresolvable edges dropped, same-depth ties in document order, a stranded cycle broken by promoting its document-order-first member — replacing the "loosely most-significant-first" significance proxy with a deterministic, total walk.
- `/review-milestone-requirements` strips the embedded children of every dependent of a block it prunes or dedups, transitively and without recording any decision, giving an option-less removal the same treatment the answer cascade gives a mismatch.
- `/capture-milestone-principle-updates`' diff read is scoped to the answered block's own boundaries by one element-agnostic rule, so the orphan lines the cascade's tidy and strip outcomes leave in surviving siblings no longer feed the record.

**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/1.2.0...1.3.0

## 1.2.0 — 2026-09-08

### Recommend Agent Return Robustness (milestone 20)

- `/recommend-all-open-questions` no longer drops a valid recommendation because the agent wrapped it in surrounding prose: every return is now judged through one pipeline — an explicit `FAILED:` verdict read from the last line before anything else, extraction of the region from the first `<alternative` line through the last `</recommendation>` line, then a single acceptance gate.
- That gate combines the two boundary tests with four line-greps in the boundary-line CLI idiom — no wrapper or `<question>` line, exactly one `<recommendation` opening line, at least one `<alternative id` line, and an `option` value matching one of those alternative ids — so it needs no XML parser and no second control path.
- Any extraction or gate miss now takes exactly one aimed repair attempt before a question is skipped: the same agent session is continued where the host allows it, otherwise one fresh re-dispatch carries the same prompt plus a shape reminder. Only a second failure leaves a block un-annotated.
- The `recommend-open-question` agent's rendering step became a draft → self-check → emit step tested against those same two shape tests, replacing its accumulated list of prohibitions.
- Reporting stays terse: a recommendation recovered by extraction or by the repair is reported exactly like a clean one, and only questions still skipped after the repair reach the advisory.

**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/1.1.1...1.2.0

## 1.1.1 — 2026-09-07

### Principle Capture By Milestone (milestone 19)

- `/capture-milestone-principle-updates` now takes a required `<milestone_id>` argument, so any milestone — current, unfinished, or long finished — can be harvested on demand, backfill included.
- Its commit walk covers all three answer provenances (`Manual-answer:`, `Alternative-answer:`, `Recommendation-answer:`), reconstructing from each commit's diff the recommendation and cited principles the user saw against the decision actually recorded.
- Manual and alternative overrides are now the sole source of new principles — prompted for an override reason with a best guess where the commit body records none, behind a one-shot accept-all / skip-all / review-one-at-a-time choice — while accepted recommendations are read as evidence only, reinforcing cited entries and flagging contradicted ones.
- The per-candidate confirm-and-write loop is replaced by a single whole-store rewrite, so `milestones/answer_decision_principles.md` may shrink as well as grow through prunes, merges, generalizations, and shortenings under a soft 40–80-word compactness bar; a contradicted entry is salvaged through a fixed narrow → generalize → replace → delete ladder.
- Two start-of-run guards were added, each a one-line notice plus a single proceed confirmation: a repeat-capture guard, and a dirty-store guard that makes the working-tree file the rewrite baseline so hand-edits survive.
- A single confirmation now gates the commit rather than the write: the rewrite lands in the working tree for `git diff` review, rejection restores the pre-write snapshot, and the `Principle-capture:` commit carries one body line per store change.
- Running capture at milestone finish is now documented as a convention, never a precondition — `finish-current-milestone` never invokes it.

**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/1.1.0...1.1.1

## 1.1.0 — 2026-09-05

### Agent Layer Improvements (milestone 18)

- Removed every pinned `model: opus` from the plugin — the three agents and the two skills that carried it — so dispatched agents and skills now inherit the session's model instead of forcing Opus.
- Recolored the three agents `red` (`complete-task`), `yellow` (`answer-open-question-with-recommendation`), and `blue` (`recommend-open-question`) so no two share a color and all three stay distinguishable on a grayscale display.
- Hardened `/recommend-all-open-questions`: the `recommend-open-question` agent now returns `FAILED: <reason>` on failure, and the sweep shape-checks every return before embedding, skipping a failed or malformed one (block left untouched, skipped questions reported) instead of splicing prose into `requirements.md` as XML.
- Orchestrators now address their agents by namespaced registry name (`cairn:complete-task`, `cairn:recommend-open-question`, `cairn:answer-open-question-with-recommendation`), and the recommend sweep passes the milestone directory to its agent so it grounds itself in that milestone's `requirements.md` directly.
- Made a failed or interrupted `complete-task` run resumable: partial work is left uncommitted in the tree and the next run continues from it rather than promising an untouched tree it could never guarantee.
- The two file-editing agents now stage their own change set path-scoped and return a bare `DONE`/`FAILED: <reason>`; `/complete-all-tasks` and `/answer-all-open-questions-with-recommendation` commit that staged index, keeping one commit per task or answer.
- Answer recording now folds the decision into `## Decisions` before removing the `<open-question>` block, so an interruption between the two edits can no longer silently lose a question.
- The Antigravity build now rewrites every `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference to `.agents/plugins/cairn/shared/<name>.md`, so the generated tree's shared-procedure references resolve under Antigravity instead of pointing nowhere.

**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/1.0.1...1.1.0

## 1.0.1 — 2026-09-05

### Versioning And Release Tooling (milestone 17)

- Added `scripts/set_version.py`, a one-argument `MAJOR.MINOR.PATCH` script that writes every in-repo version literal — `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `pyproject.toml`, and `uv.lock` — in a single all-or-nothing pass, never touching git, `gh`, or the generated tree.
- Taught `scripts/migrate_skills_to_agy.py` to read the source manifest's version at generation time and copy it into the generated `.agents/plugins/cairn/plugin.json`, so the Antigravity manifest carries a version on every regeneration path while `.claude-plugin/plugin.json` stays the single source of truth.
- Added a maintainer-only `/release-plugin <MAJOR.MINOR.PATCH>` skill as the sole documented home of the release procedure, gated behind four hard pre-flight stops (clean tracked tree, HEAD on `main`, `main` not behind `origin/main`, no untracked sources) and three pre-mutation version refusals (malformed literal, an existing tag, a version not strictly greater than the last release).
- Made the skill compose its own release notes from the `Milestone-finish:` commits since the last release, cross-checked against the `### Milestone` headings added to `milestones/README.md` over the same range, stopping on a mismatch in either direction and falling back to commit-derived notes — on explicit confirmation only — when no milestone was finished.
- Standardised a release on the bare `MAJOR.MINOR.PATCH` tag and exactly one path-scoped `Release: <VERSION>` commit, followed by a single pre-publish pause and check-then-do branch push, tag push, and `gh` release creation, so a re-run with the same version resumes from the first incomplete step instead of duplicating work.

**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/0.9.9...1.0.1

## 0.9.9 — 2026-09-04

### Frontmatter description diet (milestone 16)

- Cut all 24 plugin frontmatter descriptions (21 `skills/*/SKILL.md`, 3 `agents/*.md`) to a **single independent clause of 25 words or fewer** naming only what that skill or agent does — the always-on description budget drops from 1,411 words to 452 (−68%), and the longest single description from 149 words to 23.
- Restructured the six heaviest descriptions from scratch and shortened the nine mid-weight ones, deleting their trigger-phrase lists, mechanics, commit subjects, sequencing, cross-skill references, "Use when…" framing, and design provenance outright — a description is a routing label, never a record, so nothing cut was relocated.
- Compressed the three agent descriptions into that same shape while keeping each invocation contract as a short clause naming what the prompt carries (the task's heading text, the question's Short Title).
- Enforced two machine-checkable bars across the set: no semicolon or colon in any description, and every raw frontmatter loads under `yaml.safe_load` with its `description:` line left unquoted — so the transpiler's re-quoting fallback survives as an unexercised net.
- Extended `CLAUDE.md`'s **Skill Frontmatter** invariant into the single home of every rule governing the frontmatter `description` key.
- Regenerated the checked-in Antigravity tree at `.agents/plugins/cairn/`, with each of the 24 generated files byte-identical to its source.

### Runtime layer de-duplication (milestone 15)

- De-duplicated the whole 32-file runtime layer (`skills/*/SKILL.md`, `agents/*.md`, `shared/*.md`) across eleven per-file sweeps, removing 7,597 words (32,758 → 25,161, −23.2%) under the rule that a sentence may be cut only where its content survives earlier in the same file, in a referenced shared procedure, or in a `CLAUDE.md` invariant.
- Retired the `## Rules` heading across the layer (−3,221 words), relocating each surviving rule into the step it constrains or into the file's opening description paragraph.
- Moved editor-facing rationale out of the runtime files into the `CLAUDE.md` invariants (−2,772 words) and trimmed cross-file narration of counterparts to the one sentence each contract needs (−1,303 words).
- Consolidated the `CLAUDE.md` invariants section in a single post-sweep pass, merging ten overlapping bullets (35 bullets → 25).
- Ran seven fresh-context whole-layer re-audits with fix tasks between them; the runtime layer returned zero lost constraints for the last five passes and zero residual restatements for the last three.
- Extended `scripts/migrate_skills_to_agy.py` to copy `shared/` into the generated Antigravity tree, so every `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference resolves to a file that is present.

**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/0.9.8...0.9.9

## 0.9.8 — 2026-09-01

### Brief-level task pipeline (milestone 14)

- Flattened the task pipeline to a single **brief-level altitude**: every entry in `TASKS_TODO.md` is a `##` title plus a 1–3 sentence description and a trailing `---`, with no `Provides`/`Notes`/`Success` sections, whichever path authored it.
- Replaced `shared/submit-procedure.md` with `shared/task-format.md`, holding only the brief-level template and its four authoring guidelines — referenced by both authoring runners (`derive-tasks` and the `submit-task` skill) and parsed by `shared/complete-procedure.md`.
- Made `derive-tasks` the single writer on the derivation path: it writes its ordered briefs into `TASKS_TODO.md` itself, retiring the per-brief dispatch loop and deleting the `submit-task` agent — leaving `complete-task` as the plugin's only remaining skill+agent pair.
- Leaned down the `submit-task` skill to author the same brief-level format inline and own the position-anchored insertion itself, keeping its triage, position decision, and `Task-submission:` commit unchanged.
- Reworked `shared/complete-procedure.md` to be self-sufficient at brief altitude: it derives each task's acceptance bar from the description plus `requirements.md`, resolves cross-task references by reading prior tasks' live deliverables, and records the derived bar in the `TASKS_DONE.md` entry as a `**Verified:**` bullet list.
- Reconciled `CLAUDE.md` and `README.md` with the flattened design and regenerated the checked-in Antigravity plugin tree under `.agents/plugins/cairn/`.

**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/0.9.7...0.9.8

## 0.9.7 — 2026-07-27

**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/0.9.6...0.9.7

## 0.9.6 — 2026-07-15

## 0.9.5 — 2026-07-03

**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/0.9.4...0.9.5

## 0.9.4 — 2026-07-02

**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/0.9.3...0.9.4

## 0.9.3 — 2026-06-23

**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/0.9.2...0.9.3

## 0.9.2 — 2026-06-16

**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/0.9.1...0.9.2

## 0.9.1 — 2026-06-12

**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/0.9.0...0.9.1

## 0.9.0 — 2026-06-12

**Full Changelog**: https://github.com/uHappyLogic/cairn/commits/0.9.0
