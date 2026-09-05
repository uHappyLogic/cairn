# Milestone 17: Versioning And Release Tooling

## Goal

Put cairn's own versioning on a rail: add a version script under `scripts/` that writes a given `MAJOR.MINOR.PATCH` literal into every in-repo place a version belongs — auditing the repo first to decide that full set and adding a version to surfaces that carry none today, starting with the generated Antigravity manifest — and a maintainer-only release skill under `.claude/skills/` that takes the version as its argument, runs the script, regenerates the Antigravity tree, commits, pushes, tags, and creates the GitHub release with notes it composes from the changes since the last release (the `milestones/README.md` history entries added since the last release, cross-checked against the commit range). The script only edits files and never touches git or `gh`; the skill owns every git and `gh` step, refuses to run on a dirty working tree, and pushes any local commits before it pushes the tag. Neither artifact ships to consuming projects or falls under the plugin's runtime-layer skill invariants, the going-forward tag format is bare `MAJOR.MINOR.PATCH`, and the legacy `v.0.9.x` tags are left untouched.

## Relevant starting state

### Version-bearing surfaces

The only in-repo file that carries a plugin version today is `.claude-plugin/plugin.json` (`"version": "0.9.9"`). It was hand-aligned with the release tag in commit `503cb27` (`Manifest-version: align plugin.json with release tag 0.9.9`); before that it had read `1.0.0` since milestone 3 and never tracked releases. `.claude-plugin/marketplace.json` carries no version at all — its single `plugins[]` entry has only `name`, `source`, and `description`. `pyproject.toml` (`cairn-tooling`, `version = "0.1.0"`) versions the transpilation tooling, not the plugin, and has never moved. `README.md` embeds no version literal; its release badge (`img.shields.io/github/v/release/uHappyLogic/cairn?…&display_name=tag`) reads the latest GitHub release tag live. A repo-wide grep for `0.9.` and `"version"` outside `milestones/` and `.git/` hits only `plugin.json`.

### Generated Antigravity tree and transpiler

`scripts/migrate_skills_to_agy.py` is the only script under `scripts/`, run as `uv run scripts/migrate_skills_to_agy.py` (Python 3.13 via `.python-version`, `pyyaml` the sole dependency). On every run it **rewrites** `.agents/plugins/cairn/plugin.json` from a hard-coded dict — `$schema`, `name`, and `description: "Ported plugin for cairn"` — with no version key, so any version added to that manifest by hand is lost on the next regeneration; the version must come from the script itself. It also deletes and recopies `skills/` (skipping any directory whose name ends in `-workspace`), `agents/`, and `shared/` into the tree. The generated tree (32 files) is **checked in**, and the last two milestones each closed with a regeneration commit, so "regenerate the Antigravity tree" already has an established place in the finish ritual but no automation.

### Tags and GitHub releases

Ten tags exist across three formats: `v.0.9.0` through `v.0.9.6` (dotted legacy), `v0.9.7`, and bare `0.9.8` and `0.9.9` — the goal's bare `MAJOR.MINOR.PATCH` format is already in use for the last two. Each tag has a matching GitHub release on `uHappyLogic/cairn` (latest `0.9.9`, created 2026-09-04, not draft or prerelease). The `0.9.8` and `0.9.9` release bodies follow one hand-written shape: one `## <Milestone title> (milestone <N>)` section per milestone finished since the prior release, each a bulleted summary, closing with a `**Full Changelog**: …/compare/<prev>...<new>` link. Release `0.9.9` covered milestones 15 and 16 (80 commits from `0.9.8`); its bullets are condensed rewrites of the corresponding `milestones/README.md` history entries, not verbatim copies. `gh` 2.96.0 is installed and authenticated to `uHappyLogic` over SSH; the `origin` remote is `git@github.com:uHappyLogic/cairn.git`. There is no release automation: `.github/` holds only the README banner image, and no workflow files exist.

### Milestone history as release-note source

`milestones/README.md` carries a `## Milestone History` section with one `### Milestone <N> — <Title>` entry per finished milestone (newest first, bulleted), plus the `## Completed Milestones` table (`# | Title | Path`) that `finish-current-milestone` appends to. Each history entry lands in exactly one `Milestone-finish: milestone_<NN>_<slug>` commit touching `milestones/README.md`, so "history entries added since the last release" is recoverable as the `Milestone-finish:` commits in `<last-tag>..HEAD`, and cross-checkable by diffing the `### Milestone` headings of that file at the two ends of the range. Since `0.9.9` there are three commits and no finished milestone: the `Manifest-version:` bump plus milestone 17's definition and activation.

### Maintainer-only skill location

`.claude/` contains only `settings.json` (enabling the `skill-creator` plugin) and `settings.local.json`; there is no `.claude/skills/` directory, so the release skill will be the first project-local skill. The plugin's shipped skills all live under `skills/` (21 directories), which the transpiler copies into the Antigravity tree and which the `CLAUDE.md` runtime-layer invariants govern; `.claude/skills/` is outside both. `AGENTS.md` is a symlink to `CLAUDE.md`, so it needs no separate maintenance.

### Commit conventions relevant to the release path

Every committing skill stages path-scoped and commits under a `<Marker>: <descriptor>` subject via `shared/commit-procedure.md`, which also supplies the dirty-own-path no-op guard. The working tree is clean at `c91eb5a`, and the one prior version bump used the ad-hoc subject `Manifest-version:`. Commits authored through Claude carry a `Co-Authored-By:` trailer in the body.

## Decisions

### Version surface set

The version script writes every version literal in the repo — four surfaces: `.claude-plugin/plugin.json`, the generated `.agents/plugins/cairn/plugin.json`, a `version` field on the single `plugins[]` entry in `.claude-plugin/marketplace.json` (which carries none today), and `pyproject.toml`, whose `cairn-tooling` version moves off its independent `0.1.0` onto the plugin version so the whole repo carries one number. A release therefore bumps every version literal in the tree, leaving no per-file judgement call about which surfaces are in scope.

### Generated manifest version source

The transpiler reads `.claude-plugin/plugin.json` at generation time and copies its `version` value into the dict it writes to `.agents/plugins/cairn/plugin.json`, so the version script writes only the source manifest. This keeps a single source of truth and makes the generated tree correct for every regeneration path, including a bare standalone `uv run scripts/migrate_skills_to_agy.py`, without ordering the version script and the transpiler against each other.

### Release process documentation

The release procedure is documented in exactly one place — the release skill's own `SKILL.md` under `.claude/skills/` — and nowhere else; discovery is via the slash-command list. Neither `CLAUDE.md` nor `README.md` gains a release paragraph, so the executable steps have a single source of truth with no prose copy to drift.

### Release skill name

The release skill is named `release-plugin`, living at `.claude/skills/release-plugin/SKILL.md` and invoked as `/release-plugin <MAJOR.MINOR.PATCH>`. The name keeps the verb-object grammar every shipped skill uses while its object noun states the distinctive responsibility — releasing the versioned plugin, not the separately-versioned Python tooling.

### Last release anchor

The skill identifies the last release as the nearest tag reachable from HEAD, resolved with `git describe --tags --abbrev=0` and used as the literal tag string for both the `<last-tag>..HEAD` commit range and the compare-link endpoint. Both jobs the anchor serves are ancestry questions, so no version string is ever parsed or compared and the mixed legacy tag formats are irrelevant to it; resolution stays local, with no network or `gh` dependency.

### Release preconditions scope

The release skill applies four hard pre-flight stops before it commits, tags, or pushes anything: the tracked working tree is clean, HEAD is on `main`, `main` is not behind `origin/main` (checked after a fetch), and there are no untracked files under the transpiler's source paths `skills/`, `agents/`, and `shared/`. Untracked files elsewhere in the repo are tolerated, since path-scoped staging cannot pick them up. Each of the four blocks a route by which unmerged or uncommitted content would reach a published tag, and the scoped untracked check keeps the gate from firing on files that are harmless by construction.

### Version argument validation

The release skill hard-refuses the version argument on all three grounds before it touches anything: a malformed literal, a version whose tag already exists (exact-name lookup against local and remote tags), and a version not strictly greater than the resolved last release, compared as a numeric tuple rather than by tag-name sort. All three checks run pre-mutation, where the cost of a bad version is an error message rather than reverting a pushed commit and deleting a published release; a maintainer who genuinely needs a non-monotonic or backfill release uses the manual tag path outside the skill.

### Empty release range behavior

When no `Milestone-finish:` commit falls in the range since the last release, the release skill stops before any mutating step, states plainly that no milestone was finished since that release, shows the commit-range-derived notes it would publish in place of the usual history-entry sections, and proceeds only on explicit maintainer confirmation. An empty history range is ambiguous between a forgotten `/finish-current-milestone` and a deliberate version-only patch release, and only the maintainer can tell the two apart, so the degraded note source stays possible but becomes an explicit choice rather than a blanket refusal or a silent fallback.

## Out of Scope

## Open questions

<open-question id="Pre-publish confirmation" status="open">
  <question>Does the release skill pause to show the maintainer the composed release notes and the version before it pushes, tags, and creates the GitHub release, or does it run unattended end to end once invoked?</question>
  <alternative id="Confirm once before publishing">
    The skill does all local work unattended — runs the version script, regenerates the Antigravity tree, composes the notes, makes the release commit — then stops once to show the maintainer the version and the full composed release body, and pushes, tags, and creates the GitHub release only on approval.
    <advantage>Places the single gate exactly at the reversible/irreversible boundary: everything before it is a local commit the maintainer can amend or reset, everything after it is a public tag and release, and it gates the one artifact no precondition can validate mechanically — an LLM-composed notes body that condenses milestone history rather than copying it.</advantage>
    <drawback>The skill is no longer a single fire-and-forget command: it cannot run non-interactively (a CI job or a headless invocation), and it costs the maintainer one review turn on every release even when the notes are obviously fine.</drawback>
  </alternative>
  <alternative id="Fully unattended">
    Once invoked with a version, the skill runs end to end with no pause, relying on its argument validation and its preconditions (clean tree, version format, release range) as the only gates before it pushes, tags, and publishes.
    <advantage>One command produces a finished release, keeping the skill scriptable and matching the plugin&apos;s existing unattended orchestrators (`complete-all-tasks`, `recommend-all-open-questions`) that dispatch and commit without asking.</advantage>
    <drawback>The generated notes body reaches a public GitHub release before any human reads it, and correcting it means editing or deleting a published release — a class of error the preconditions structurally cannot catch, unlike the mechanical checks they do cover.</drawback>
  </alternative>
  <alternative id="Publish as draft for out-of-band review">
    The skill runs unattended through push, tag, and `gh release create --draft`, then reports the draft URL and leaves the maintainer to review and publish the release in the GitHub UI.
    <advantage>Keeps the invocation itself interaction-free while still putting a human between composition and publication, and the review happens where the notes actually render.</advantage>
    <drawback>The tag and the release commit are already pushed before anyone looks, so the review can no longer prevent the irreversible part; it also splits ownership of a step the goal assigns wholly to the skill, leaving every release in a half-finished state that depends on a manual follow-up outside the tool.</drawback>
  </alternative>
  <alternative id="Confirm at every mutating step">
    The skill pauses for approval before each state-changing action in turn — the release commit, the branch push, the tag push, and the release creation.
    <advantage>Maximum control and precise failure isolation: the maintainer can stop at whichever step first looks wrong and knows exactly how far the run got.</advantage>
    <drawback>Four prompts for one workflow trains the maintainer to rubber-stamp them, which defeats the review that matters; the early steps are locally revertible anyway, so gating them buys control that costs more attention than it protects.</drawback>
  </alternative>
  <recommendation option="Confirm once before publishing">One gate at the point where a local, revertible commit becomes a public tag and release is the least interaction that still lets a human veto generated release notes before they are permanent.</recommendation>
</open-question>
<open-question id="Release commit subject" status="deferred">
  <question>What Marker-colon-descriptor commit subject does the release commit carry for the version bump plus regenerated Antigravity tree, and is its path set exactly those files?</question>
  <alternative id="Release marker, single commit">
    One commit under the subject `Release: MAJOR.MINOR.PATCH`, staging exactly the files the version script wrote plus the regenerated `.agents/plugins/cairn/` tree, named explicitly per `shared/commit-procedure.md`.
    <advantage>The marker names the commit&apos;s distinctive responsibility — it is the one commit a release run creates and the point the tag lands on — and the version literal as descriptor makes `git log --oneline` read as a release history; it also explains why 32 regenerated files ride along, which a bare version bump would not.</advantage>
    <drawback>`Release:` is a bare marker where every existing cairn marker is a two-word `Object-function` compound (`Task-derivation:`, `Milestone-finish:`), and it names an operation broader than the commit itself, since the tag and the GitHub release are separate acts the commit does not contain.</drawback>
  </alternative>
  <alternative id="Version-bump marker, single commit">
    One commit under `Version-bump: MAJOR.MINOR.PATCH` over the same path set, continuing the shape of the one-off `Manifest-version:` bump in `503cb27`.
    <advantage>Literally accurate about what the commit changes, and its compound `Object-function` shape matches the established marker family exactly.</advantage>
    <drawback>&quot;Bump&quot; states the generic mechanism rather than the distinctive function, and it understates the commit — the regenerated Antigravity tree is not a version bump, so a reader seeing the whole generated tree in a `Version-bump:` diff has to reconstruct why.</drawback>
  </alternative>
  <alternative id="Split bump and regeneration">
    Two commits per release — the version-bearing files under one subject, the regenerated `.agents/plugins/cairn/` tree under a separate regeneration subject.
    <advantage>Each commit&apos;s diff is self-consistent and the generated-tree churn stays out of the version diff, matching the existing finish-ritual habit of a standalone regeneration commit.</advantage>
    <drawback>Breaks the one-release-one-commit mapping the tag depends on: the tag can only point at one of the two, and a run that dies between them leaves a repo whose checked-in generated tree and manifest version disagree.</drawback>
  </alternative>
  <applied-principle>Name by distinctive function</applied-principle>
  <recommendation option="Release marker, single commit">One commit under `Release: MAJOR.MINOR.PATCH`, path-scoped to exactly the version-script-written files plus the regenerated `.agents/plugins/cairn/` tree (never `git add -A`) — the marker names why the commit exists rather than the mechanism it uses, and keeping it a single commit keeps the tag pointing at one complete, self-consistent release state.</recommendation>
</open-question>
<open-question id="Partial failure resumption" status="deferred">
  <question>If a step fails after the release commit exists (push, tag push, or release creation), what state does the skill leave behind, and can a re-run with the same version resume from it?</question>
  <alternative id="Idempotent resume">
    Each post-commit step becomes check-then-do — is the version commit present, is the branch pushed, does the tag exist and point at that commit, does the GitHub release exist — so a re-run with the same version skips what already succeeded and continues from the first incomplete step, stopping only when it finds an artifact that exists but disagrees.
    <advantage>One command recovers from any post-commit failure, and every check is a cheap query (`git rev-parse`, `git ls-remote --tags`, `gh release view`) the skill already partly needs to push local commits before the tag.</advantage>
    <drawback>Every step gains detection plus a mismatch guard, and a resume that misreads state (tag pushed, branch since amended) could publish a release against a tree the maintainer no longer expects.</drawback>
  </alternative>
  <alternative id="Stop and report">
    The skill leaves whatever succeeded exactly as it stands, prints which steps completed and the literal git/gh commands to finish by hand, and a same-version re-run is simply refused by its own tag-exists precondition.
    <advantage>No state-detection machinery at all — the failure message is the entire recovery mechanism, matching the plugin&apos;s established clean-stop-and-point pattern.</advantage>
    <drawback>Recovery is manual and unrehearsed in exactly the situation — a half-published release — where getting it wrong is most costly.</drawback>
  </alternative>
  <alternative id="Rollback on failure">
    On any post-commit failure the skill unwinds its own work — deleting the local and, if pushed, the remote tag and resetting the release commit — so the repo returns to its pre-release state and a plain re-run starts clean.
    <advantage>Only one entry state ever exists, so the happy path stays the only path and no resume branching is needed.</advantage>
    <drawback>Unwinding already-pushed refs is destructive and can itself fail, making the failure handler the riskiest part of the skill.</drawback>
  </alternative>
  <recommendation option="Idempotent resume">The post-commit steps are each checkable with a one-line git or gh query, so check-then-do makes &quot;re-run with the same version&quot; the whole recovery story, with a stop-on-mismatch guard covering the cases where resuming would be wrong.</recommendation>
</open-question>
<open-question id="Stale generated tree handling" status="deferred">
  <question>If regenerating the Antigravity tree changes files beyond the manifest version because a runtime edit was never regenerated, does the release commit absorb those changes or does the skill stop and report?</question>
  <alternative id="Absorb silently">
    The skill regenerates the Antigravity tree as a normal step and folds whatever it produces — manifest version plus any files a missed regeneration left behind — into the release commit without comment.
    <advantage>Simplest possible rule with no conditional branch: the shipped tree is guaranteed to match the source at the tag, every time, and a mechanical catch-up never interrupts a release.</advantage>
    <drawback>A large drift lands in the release commit with nothing in the console or the release notes hinting that this release also shipped previously-unregenerated runtime edits.</drawback>
  </alternative>
  <alternative id="Absorb and report">
    The skill regenerates, folds the full result into the release commit, and prints a one-line advisory naming the drift (that files beyond `.agents/plugins/cairn/plugin.json` changed, and how many) before it proceeds.
    <advantage>Keeps the release unblocked and the shipped tree correct while making the one fact git alone would not surface — that this release absorbed a stale-tree catch-up — visible to the maintainer at the moment it happens.</advantage>
    <drawback>The advisory is informational only, so a maintainer who wanted to inspect the drift before it was committed must still revert or amend after the fact.</drawback>
  </alternative>
  <alternative id="Stop and report">
    The skill regenerates, compares the result against the checked-in tree, and aborts before any commit when anything beyond the manifest version changed, telling the maintainer to run `uv run scripts/migrate_skills_to_agy.py`, commit that separately, and re-invoke.
    <advantage>The release commit stays minimal and auditable by construction, and the catch-up regeneration gets its own reviewable commit with honest provenance.</advantage>
    <drawback>Blocks a release on a purely mechanical, deterministic condition the skill just fixed in its own working tree, forcing the maintainer to re-run the identical command by hand and start over.</drawback>
  </alternative>
  <alternative id="Separate regeneration commit">
    The skill regenerates and, when the diff exceeds the manifest version, commits the catch-up as its own commit ahead of the release commit, leaving the release commit to carry only the version bump and manifest.
    <advantage>Nothing blocks and the git history stays honest — the drift is separable and revertible on its own, and the release commit reads as exactly one thing.</advantage>
    <drawback>Adds conditional commit machinery and a second commit subject to a skill whose commit shape is otherwise fixed, for a distinction that matters only in the rare stale case.</drawback>
  </alternative>
  <recommendation option="Absorb and report">The generated tree is a pure deterministic derivative of `skills/`, `agents/`, and `shared/` — regenerating it can only ever produce what the already-committed sources say, so there is nothing to review and nothing to lose by absorbing it, and the skill&apos;s clean-working-tree precondition means the whole diff is self-generated and unambiguous; the printed advisory covers the one thing the commit alone would not tell the maintainer.</recommendation>
</open-question>
<open-question id="Release note fidelity" status="deferred">
  <question>Are the release notes the history entries&apos; bullets verbatim, or condensed rewrites matching the shape of the existing 0.9.8 and 0.9.9 release bodies?</question>
  <alternative id="Verbatim transplant">
    The skill copies each `### Milestone &lt;N&gt; — &lt;Title&gt;` entry&apos;s bullets out of `milestones/README.md` unchanged into the release body, rewriting only the heading into the `## &lt;Title&gt; (milestone &lt;N&gt;)` form and appending the Full Changelog link.
    <advantage>Fully deterministic and cheap — the release note is a mechanical extraction, so it never invents, omits, or softens a claim, and the published notes provably match the project&apos;s own history record.</advantage>
    <drawback>The history entries are an internal engineering record and carry bullets a consumer-facing release note should not: process meta-commentary (re-audit pass counts, ledger channels, no-op falsification passes), which is exactly the material the hand-written 0.9.8 and 0.9.9 bodies dropped.</drawback>
  </alternative>
  <alternative id="Condensed rewrite">
    The skill composes the release body by rewriting each milestone&apos;s history bullets down to the user-facing changes, matching the shape the existing 0.9.8 and 0.9.9 bodies already set — one `## &lt;Title&gt; (milestone &lt;N&gt;)` section per milestone, a short bulleted summary, then the Full Changelog compare link.
    <advantage>It reproduces the established, already-published house style exactly, and it is the only option that can drop milestone-internal process bullets and merge overlapping ones — the transformation the 0.9.9 body demonstrably applied (eight history bullets condensed to six, self-critical and no-op bullets cut).</advantage>
    <drawback>The body is model-composed prose rather than a mechanical copy, so it is reproducible only up to the quality of that composition pass and can drift in tone or drop a genuinely user-visible change without any automatic check catching it.</drawback>
  </alternative>
  <alternative id="Filtered verbatim">
    The skill copies bullets verbatim but applies a stated selection rule — keep bullets describing a change to the shipped plugin, drop bullets describing only the milestone&apos;s own process — so the text is never rewritten, only chosen.
    <advantage>Keeps the extraction&apos;s no-invention guarantee while removing the worst of the internal-record noise, giving most of the condensation benefit at a fraction of the composition risk.</advantage>
    <drawback>The keep/drop rule is a judgement call in disguise and does not survive contact with the real entries — milestone 15&apos;s and 16&apos;s bullets mix shipped changes with process detail inside single sentences, which selection alone cannot separate, and verbatim bullets are written at internal-record length and density.</drawback>
  </alternative>
  <recommendation option="Condensed rewrite">The two already-published release bodies are themselves condensed rewrites with a different heading form and the milestone-internal bullets cut, so matching that shape keeps the release series consistent and keeps engineering-process detail out of a consumer-facing note; what would flip this is wanting the release body diffable against `milestones/README.md`.</recommendation>
</open-question>
<open-question id="Cross-check mismatch handling" status="deferred">
  <question>When the history entries added since the last release disagree with the commit range (a finish commit with no matching entry, or the reverse), does the skill stop, warn and continue, or reconcile automatically?</question>
  <alternative id="Stop and report">
    The skill treats any cross-check disagreement as a precondition failure: before it commits, pushes, tags, or creates the release it prints both sides of the mismatch (finish commits in the range with no matching history entry, and history entries with no matching finish commit), changes nothing, and exits so the maintainer can fix the source and re-run.
    <advantage>It catches an incomplete release-note set before the one artifact that cannot be quietly re-cut — a pushed tag and a published GitHub release — exists, and it matches the posture the goal already gives this skill for the dirty-working-tree case, where an anomalous starting state means refuse rather than proceed.</advantage>
    <drawback>A benign mismatch — a rebased or amended finish commit, a hand-written history entry — blocks the release until the maintainer edits `milestones/README.md`, and a skill taking only the version as its argument offers no override to push past it.</drawback>
  </alternative>
  <alternative id="Warn and continue">
    The skill composes the notes from the history entries regardless, prints the discrepancies as an advisory, and proceeds through the commit, push, tag, and release steps.
    <advantage>It never blocks a release on a discrepancy that is usually benign, while still putting the mismatch in front of the maintainer.</advantage>
    <drawback>The warning scrolls past in the very run that publishes, so a genuinely missing entry becomes a published release with a whole milestone absent from its notes — repairable only by editing the release after the fact.</drawback>
  </alternative>
  <alternative id="Reconcile automatically">
    The skill fills the gaps itself: for a finish commit with no history entry it synthesizes a note section from that commit&apos;s range, and it keeps an entry that has no matching finish commit, without maintainer involvement.
    <advantage>It always produces complete-looking notes with no interruption to the release run.</advantage>
    <drawback>It papers over the real defect — the missing entry stays missing in `milestones/README.md`, the durable history — and publishes machine-synthesized prose that will not match the hand-written shape of the 0.9.8 and 0.9.9 bodies.</drawback>
  </alternative>
  <alternative id="Asymmetric guard">
    The skill splits the two directions: a finish commit with no history entry stops the run, while a history entry with no matching finish commit only warns and continues.
    <advantage>It blocks exactly the direction that can silently drop a milestone from the notes, and lets the direction that is almost always a rebase artifact through.</advantage>
    <drawback>It turns a one-sentence guard into a two-case rule that a maintainer must remember, and the extra-entry direction can also mean a fabricated or duplicated entry — which it then publishes.</drawback>
  </alternative>
  <recommendation option="Stop and report">Stop before any git or `gh` mutation and report both sides, because the release is the one irreversible artifact in the run while the cost of a false stop is a single README edit and a re-run — and if the extra-entry direction proves routinely benign in practice, that is the signal to relax the guard into the asymmetric form.</recommendation>
</open-question>
