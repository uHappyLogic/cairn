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

## Out of Scope

## Open questions

<open-question id="Generated manifest version source" status="open">
  <question>Since the transpiler rewrites the Antigravity manifest from a hard-coded dict on every run, how does that generated manifest get its version — does the transpiler read it from `.claude-plugin/plugin.json` at generation time, take it as an argument, or does the version script write the generated file directly with the transpiler preserving it?</question>
  <alternative id="Transpiler reads plugin.json">
    The transpiler reads `.claude-plugin/plugin.json` at generation time and copies its `version` value into the dict it writes to `.agents/plugins/cairn/plugin.json`, so the version script writes only the source manifest.
    <advantage>Keeps exactly one version-bearing source of truth and makes the generated manifest correct after any transpiler run — including a bare `uv run scripts/migrate_skills_to_agy.py` — regardless of whether the version script ran first, last, or at all.</advantage>
    <drawback>The transpiler gains a read dependency on the Claude-side manifest and needs a defined behavior when that file or its `version` key is missing, and the version script no longer literally writes the generated surface, satisfying the goal indirectly.</drawback>
  </alternative>
  <alternative id="Version passed as transpiler argument">
    The transpiler takes the version as a command-line argument (e.g. `--version 1.0.0`) and emits whatever it is given, with the release skill or version script supplying it.
    <advantage>Makes the version an explicit input the caller controls, leaving the transpiler with no knowledge of any other manifest and no file-reading fallback logic.</advantage>
    <drawback>The habitual bare invocation documented in `CLAUDE.md` now either fails or needs a default, which is precisely the drift the milestone is trying to eliminate, and it moves correctness into whichever caller remembers to pass the flag.</drawback>
  </alternative>
  <alternative id="Transpiler preserves generated version">
    The version script writes the version directly into `.agents/plugins/cairn/plugin.json`, and the transpiler is changed to merge rather than overwrite — reading any existing generated manifest and carrying its `version` key forward.
    <advantage>The version script literally writes every version-bearing surface, matching the goal&apos;s framing of the generated manifest as one of the files it edits.</advantage>
    <drawback>It makes the generated tree partly stateful — a regeneration into a fresh or deleted `.agents/` tree silently produces a version-less manifest — which contradicts the tree&apos;s defining property of being fully reproducible from source.</drawback>
  </alternative>
  <alternative id="Version script edits transpiler literal">
    The version script rewrites the version literal inside `scripts/migrate_skills_to_agy.py` itself, and the transpiler emits that hard-coded value on every run.
    <advantage>Every surface the version script touches is a uniform literal-in-file edit, and regeneration reproduces the version deterministically with no cross-file read and no argument.</advantage>
    <drawback>It makes executable source a version-bearing surface edited by another script, which is fragile to reformatting and leaves the transpiler carrying a version it does not own.</drawback>
  </alternative>
  <recommendation option="Transpiler reads plugin.json">Deriving the generated manifest&apos;s version from `.claude-plugin/plugin.json` at generation time keeps a single source of truth and makes the generated tree correct for every regeneration path, including a bare standalone run, without ordering the version script and the transpiler against each other.</recommendation>
</open-question>
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
<open-question id="Empty release range behavior" status="open">
  <question>When no milestone history entry has been added since the last release (only non-finish commits in the range), does the release skill refuse to release, or compose the notes from the commit range alone?</question>
  <alternative id="Refuse to release">
    The skill treats a range with zero `Milestone-finish:` commits as a clean stop: it reports the empty history range, names the last release tag, and exits before any commit, push, tag, or `gh release` step.
    <advantage>Guarantees every published release body is composed from curated `milestones/README.md` history entries, and catches the most likely cause of an empty range in this repo — a maintainer who ran the release before `/finish-current-milestone` — at the only moment it is still cheap to fix.</advantage>
    <drawback>Blocks a legitimate version-only or fix-only patch release outright; the repo already has exactly that shape today (`503cb27` plus milestone 17&apos;s definition and activation sit between `0.9.9` and HEAD with no finished milestone), leaving the maintainer to tag and write the release by hand.</drawback>
  </alternative>
  <alternative id="Commit-range fallback">
    When no history entry was added since the last release, the skill silently falls back to composing the notes from the commit range alone, summarizing the `&lt;Marker&gt;: &lt;descriptor&gt;` subjects in that range and closing with the usual `**Full Changelog**` compare link.
    <advantage>Costs nothing extra to build and never blocks a release — the commit range is already being read for the goal&apos;s cross-check, and the house commit-subject convention makes those subjects self-describing enough to summarize.</advantage>
    <drawback>Publishes a release whose body silently departs from the established `## &lt;Milestone title&gt; (milestone &lt;N&gt;)` shape with no maintainer signal, so a forgotten `/finish-current-milestone` yields a permanently mis-shaped public release rather than an error.</drawback>
  </alternative>
  <alternative id="Confirmed commit-range fallback">
    The skill detects the empty history range, stops to state plainly that no milestone was finished since the last release, shows the commit-range-derived notes it would publish, and proceeds only on explicit maintainer confirmation.
    <advantage>Keeps the deliberate patch release possible while making the degraded, uncurated note source an explicit maintainer choice, so the forgot-to-finish mistake still gets caught without hard-coding a refusal the repo&apos;s own release history would already have tripped.</advantage>
    <drawback>Introduces an interactive stop on this path, so the release skill cannot run fully unattended in the one case where a human is most likely absent, and it adds a second notes-composition shape the skill must maintain.</drawback>
  </alternative>
  <recommendation option="Confirmed commit-range fallback">An empty history range is ambiguous between a forgotten milestone finish and a deliberate patch release, and only the maintainer can tell them apart, so the skill should surface the degraded note source and let that call be made rather than guessing with a blanket refusal or a silent fallback.</recommendation>
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
<open-question id="Last release anchor" status="deferred">
  <question>How does the skill identify the last release given the mixed legacy tag formats — the latest tag reachable from HEAD, the GitHub latest release, or the highest version-sorted tag?</question>
  <alternative id="Reachable tag from HEAD">
    Anchor on the nearest tag reachable from HEAD via `git describe --tags --abbrev=0`, taking whatever literal tag string it returns as the previous release.
    <advantage>It is format-agnostic by construction — it never parses or compares version strings, so the `v.0.9.x` / `v0.9.7` / bare `0.9.x` split is simply invisible to it — and it answers the ancestry question the skill actually has, since both uses of the anchor (the `&lt;last-tag&gt;..HEAD` commit range for the `Milestone-finish:` cross-check, and the `compare/&lt;prev&gt;...&lt;new&gt;` link endpoint) are about history, not about which number is biggest; verified on this repo today it returns `0.9.9`, and it needs no network.</advantage>
    <drawback>It trusts the local repo alone: a tag pushed from another machine and not yet fetched, or a tag that exists locally but was never published as a GitHub release, would silently anchor the range to the wrong point, and it reports nothing when HEAD has no reachable tag beyond a bare failure.</drawback>
  </alternative>
  <alternative id="GitHub latest release">
    Anchor on the publishing system of record, reading the latest release&apos;s tag with `gh release list --limit 1 --json tagName -q &apos;.[0].tagName&apos;` (or the `releases/latest` API).
    <advantage>It names what was actually published rather than what happens to be tagged locally — the same thing the README release badge already displays — and is equally format-agnostic, so the skill&apos;s notion of &quot;last release&quot; matches the page the notes will be posted next to.</advantage>
    <drawback>It adds a network and auth dependency to a step that is otherwise purely local, and GitHub&apos;s &quot;latest&quot; is chosen by publish date or an explicit flag with no guarantee the tag is an ancestor of HEAD, so the derived commit range can be wrong or empty even when the call succeeds.</drawback>
  </alternative>
  <alternative id="Highest version-sorted tag">
    Normalize the legacy prefixes off every tag, version-sort the results, and take the highest, mapping back to the original tag string for the compare link.
    <advantage>It depends on neither history topology nor the network, so it still yields the semantically highest version after a rebase, a shallow clone, or a tag made on a side branch.</advantage>
    <drawback>The naive form is demonstrably wrong on this repo — `git tag --sort=-v:refname` ranks `v0.9.7` above `0.9.9` because of the prefix split — so it requires bespoke normalization plus a name-mapping step back to the literal tag, the most code of any option, and &quot;highest version&quot; is not the same question as &quot;last released&quot; anyway.</drawback>
  </alternative>
  <alternative id="Reachable tag verified against GitHub">
    Take `git describe --tags --abbrev=0` as the anchor, then compare it against the latest GitHub release tag and stop with a report if the two disagree.
    <advantage>It keeps the ancestry-correct local anchor while catching the one failure mode that anchor cannot see — a release published elsewhere, or a local tag never released — before the skill composes notes against a wrong range.</advantage>
    <drawback>It reintroduces the network dependency into anchor resolution and adds a second stop condition to a skill that already carries several preconditions, for a mismatch that a single-maintainer repo with linear history rarely produces.</drawback>
  </alternative>
  <recommendation option="Reachable tag from HEAD">Both jobs the anchor serves are ancestry questions, and `git describe --tags --abbrev=0` answers them in one local command that never parses a version string, so the three legacy tag formats cost nothing — it already returns `0.9.9` correctly here, whereas version-sorting returns `v0.9.7` and needs bespoke normalization to fix.</recommendation>
</open-question>
<open-question id="Version argument validation" status="deferred">
  <question>Beyond requiring a bare MAJOR.MINOR.PATCH literal, does the skill also refuse a version that is not strictly greater than the last release or that already exists as a tag?</question>
  <alternative id="Format only">
    The skill validates only that the argument is a bare MAJOR.MINOR.PATCH literal and otherwise trusts the maintainer, letting git and gh surface a duplicate tag or a downgrade as a natural failure.
    <advantage>Smallest possible validation surface — one regex, no dependency on resolving a last-release anchor, and no rule that could ever wrongly block a deliberate release.</advantage>
    <drawback>The natural failure arrives too late: by the time `git tag` rejects an existing name the skill has already written the version into the files, committed, and pushed, leaving a published commit stamped with a version that will never be released and requiring a manual revert to clean up.</drawback>
  </alternative>
  <alternative id="Format and tag collision">
    Beyond the literal, the skill refuses a version whose tag already exists (an exact-name lookup against local and remote tags), but applies no ordering rule.
    <advantage>Catches the one genuinely destructive case before any file, commit, or push happens, at the cost of a single exact-match tag lookup that is immune to the repo&apos;s mixed `v.0.9.x` / `v0.9.7` / bare tag formats.</advantage>
    <drawback>A transposition or downgrade typo that names an unused version — `0.9.10` typed as `0.9.1`&apos;s successor, or `1.0.0` typed as `0.1.0` — passes every check and is only visible after the GitHub release has published and demoted the latest-release badge.</drawback>
  </alternative>
  <alternative id="Full precondition check">
    The skill hard-refuses on all three grounds before it touches anything: malformed literal, a version that already exists as a tag, and a version not strictly greater than the resolved last release.
    <advantage>All three failure modes are caught pre-mutation, where the cost is an error message rather than a revert of a pushed commit and a deleted GitHub release, and the ordering check is the only guard against the typo class that a tag-existence check cannot see.</advantage>
    <drawback>The ordering check needs a resolved last-release anchor and numeric-tuple comparison (the legacy prefixed tags make naive `-v:refname` sorting put `v0.9.7` above `0.9.9`), and it hard-blocks any out-of-order or backfill release without an in-skill escape hatch.</drawback>
  </alternative>
  <alternative id="Ordering as override prompt">
    Format and tag collision are hard refusals, but a non-increasing version only produces a warning the maintainer must explicitly confirm before the skill proceeds.
    <advantage>Keeps the typo caught at the moment it matters while leaving a deliberate out-of-order release possible without editing or bypassing the skill.</advantage>
    <drawback>Adds an interactive branch to a validation step whose whole value is being unattended and deterministic, and a confirmation prompt in the same run as the release itself is exactly the prompt a maintainer clicks through, so it degrades to no check at all.</drawback>
  </alternative>
  <recommendation option="Full precondition check">Every check is cheap and runs before the first mutation, and this skill spends one argument across file edits, a commit, a push, a tag, and a published GitHub release in one irreversible sweep — so a version caught late costs a revert and a force-push while catching it costs a tag lookup and a tuple comparison; a maintainer who genuinely needs a non-monotonic release still has the manual tag path outside the skill.</recommendation>
</open-question>
<open-question id="Release preconditions scope" status="deferred">
  <question>Besides a clean tracked working tree, does the skill also require being on the main branch, having no untracked files, and not being behind origin before it proceeds?</question>
  <alternative id="Clean tree only">
    The skill checks only that tracked files are unmodified, exactly as the goal states, and proceeds regardless of branch, upstream position, or untracked files.
    <advantage>Smallest possible gate: nothing beyond the already-decided requirement, no extra git commands, and no precondition that can block a legitimate release on an unrelated local condition.</advantage>
    <drawback>The two failure modes git does not warn about land badly — a release cut from a feature branch tags and publishes unmerged work silently, and a HEAD behind origin only fails at the push, after the release commit already exists, which is precisely the partial state the skill would then have to unwind.</drawback>
  </alternative>
  <alternative id="Branch and sync gate">
    Adds two pre-flight hard stops to the clean-tracked-tree check — HEAD is on main, and after a fetch main is not behind origin/main — while tolerating untracked files anywhere.
    <advantage>Blocks exactly the conditions that are either invisible to git (wrong branch) or detected too late to be cheap (behind origin), using two commands run before any commit, tag, or push exists.</advantage>
    <drawback>Leaves one real hole: the transpiler copies `skills/`, `agents/`, and `shared/` off disk, so a wholly-untracked new skill directory is swept into the regenerated Antigravity tree and published in the release commit even though it was never committed as source.</drawback>
  </alternative>
  <alternative id="Scoped untracked gate">
    The Branch and sync gate plus one more scoped check — no untracked files under the transpiler&apos;s source paths (`skills/`, `agents/`, `shared/`) — with untracked files elsewhere in the repo tolerated.
    <advantage>Closes the only route by which uncommitted content reaches a published artifact, at the cost of a single path-scoped status command, without ever firing on scratch files, local notes, or build leftovers that the path-scoped release commit could not have picked up anyway.</advantage>
    <drawback>A fourth condition to specify, explain, and keep aligned with the transpiler&apos;s copy list — if that list ever grows a directory, the check silently stops covering it.</drawback>
  </alternative>
  <alternative id="Strict full clean">
    Requires all four: on main, not behind origin, no modified tracked files, and no untracked files anywhere in the repo.
    <advantage>Gives the strongest single guarantee — the released tree is byte-identical to what origin/main holds plus the version bump — and is stated in one sentence with no carve-outs to reason about.</advantage>
    <drawback>Blocks releases on conditions that cannot affect the release at all, since staging is path-scoped, so any stray untracked file forces the maintainer to clean or stash unrelated work and trains them toward bypassing the gate.</drawback>
  </alternative>
  <recommendation option="Scoped untracked gate">Require clean tracked tree, on main, and not behind origin as hard pre-flight stops, plus no untracked files under `skills/`, `agents/`, and `shared/` — each of the four blocks a way unmerged or uncommitted content reaches a published tag, and the scoping keeps the untracked check from firing on files that path-scoped staging already makes harmless.</recommendation>
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
<open-question id="Release skill name" status="deferred">
  <question>What is the release skill named and invoked as, given it takes the version as its sole argument?</question>
  <alternative id="release-plugin">
    A verb-object kebab-case name matching the shipped grammar exactly, invoked as `/release-plugin 1.0.0` from `.claude/skills/release-plugin/SKILL.md`.
    <advantage>It reads in the same verb-object shape as every one of the 21 shipped skills (`derive-tasks`, `finish-current-milestone`, `submit-task`), and its object noun is the repo&apos;s established word for the versioned artifact (`.claude-plugin/`, `plugin.json`), so it names precisely what is being released and distinguishes it from the independently-versioned `cairn-tooling` `pyproject.toml`.</advantage>
    <drawback>Two words where one might do, and &quot;plugin&quot; is a slightly redundant qualifier inside a repo that is nothing but a plugin.</drawback>
  </alternative>
  <alternative id="release">
    The bare name with the object dropped, invoked as `/release 1.0.0`.
    <advantage>Shortest possible thing to type for the one maintainer who will ever run it, and the version argument makes the intent unmistakable at the call site.</advantage>
    <drawback>It is the only skill in the repo that is not verb-object, and as a maximally generic slash-command token it is the name most likely to collide with a skill from another plugin loaded in the same maintainer session.</drawback>
  </alternative>
  <alternative id="cut-release">
    The standard release-engineering idiom as verb-object, invoked as `/cut-release 1.0.0`.
    <advantage>&quot;Cut a release&quot; is the phrase maintainers already use for exactly this end-to-end act, so the name needs no explanation.</advantage>
    <drawback>&quot;Cut&quot; is release-tooling jargon that appears nowhere else in the repo&apos;s vocabulary, and its object &quot;release&quot; names the event rather than the artifact, which breaks the object-noun consistency the other skill names keep.</drawback>
  </alternative>
  <alternative id="publish-release">
    Verb-object naming the publication step, invoked as `/publish-release 1.0.0`.
    <advantage>&quot;Publish&quot; names the irreversible, outward-facing half of the job — push, tag, GitHub release — which is the part a maintainer most needs the name to warn them about.</advantage>
    <drawback>It understates the skill&apos;s full responsibility: it also writes the version literals, regenerates the Antigravity tree, and commits, so the name describes only the last stage of what it does.</drawback>
  </alternative>
  <applied-principle>Name by distinctive function</applied-principle>
  <applied-principle>Drop-vs-replace by ambiguity</applied-principle>
  <recommendation option="release-plugin">It keeps the verb-object grammar every shipped skill uses while its object noun states the distinctive responsibility — releasing the versioned plugin, not the separately-versioned Python tooling — which neither the bare verb nor the event-noun variants convey.</recommendation>
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
<open-question id="Release process documentation" status="deferred">
  <question>Where is the maintainer-facing release procedure documented — the Development section of CLAUDE.md, README.md, or only the skill itself?</question>
  <alternative id="Skill only">
    The release procedure lives entirely in `.claude/skills/&lt;release-skill&gt;/SKILL.md` and nowhere else; discovery is via the slash-command list.
    <advantage>Single source of truth with zero drift risk — the steps are read by whoever executes them, exactly like every other cairn skill, and a change to the process is one edit.</advantage>
    <drawback>Nothing in `CLAUDE.md` or `README.md` records that releases are automated at all, so an agent reasoning about the repo (or the maintainer months later) has no signpost to the skill and may hand-cut a release the way `503cb27` was done.</drawback>
  </alternative>
  <alternative id="CLAUDE.md pointer">
    The skill holds the full procedure; `CLAUDE.md`&apos;s `## Development` section gains a short paragraph naming the release skill, its version argument, and the surfaces it touches — a signpost, not a restatement of the steps.
    <advantage>Puts the release path where this repo&apos;s maintainer-facing acts already live (the `## Development` transpile note, the `migrate-workspace` catalog registration rule), so the agent operating in this repo finds it, while the executable steps stay unduplicated in the skill.</advantage>
    <drawback>Adds a second place that must be touched when the release flow changes, and `CLAUDE.md` is loaded into every session in this repo, so the paragraph costs context on every run regardless of relevance.</drawback>
  </alternative>
  <alternative id="README Development">
    The procedure is documented in `README.md`&apos;s `## Development` section, next to the existing `uv run scripts/migrate_skills_to_agy.py` build step.
    <advantage>Sits beside the one other maintainer-only repo command already documented there, and is visible to outside contributors browsing the project on GitHub.</advantage>
    <drawback>`README.md` is the consuming-project user&apos;s doc — an installer of the plugin can never cut a cairn release (it needs `gh` auth to `uHappyLogic`), so the section becomes noise for its primary audience, and the agent that actually runs the skill does not read `README.md` by default.</drawback>
  </alternative>
  <alternative id="Both CLAUDE.md and README">
    Mirror a short release note in both `CLAUDE.md`&apos;s and `README.md`&apos;s `## Development` sections, as the Antigravity transpilation step is mirrored today.
    <advantage>Matches the existing precedent exactly — the one comparable maintainer-only command is already written in both places — so it needs no new judgment about which file wins.</advantage>
    <drawback>Triples the surfaces that drift when the release flow changes (skill plus two prose copies), and the existing mirrored transpile text has already diverged in wording between the two files, showing the duplication is not maintained in practice.</drawback>
  </alternative>
  <recommendation option="CLAUDE.md pointer">The executable steps belong only in the skill, but a repo whose agent-facing conventions live in `CLAUDE.md` needs the release path signposted there — a short `## Development` paragraph naming the skill, its version argument, and the surfaces it writes; `README.md` stays a user-and-contributor doc, since only the maintainer can release.</recommendation>
</open-question>
