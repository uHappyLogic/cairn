# Milestone 24: Repo Hygiene Surface

## Goal

Give the cairn repository the hygiene surface a first-time visitor scans for. Add a GitHub Actions workflow that runs `uv run scripts/build_hosts.py --check` on every push and pull request, with a CI badge beside the release badge; a root `CONTRIBUTING.md` (edit `core/`, rebuild, invariants live in `CLAUDE.md`), `SECURITY.md`, `CODE_OF_CONDUCT.md`, bug and feature issue templates, and a pull-request template; a `CONTRIBUTING.md` template in each host definition that renders into the host tree and points contributors at the root repository; an in-repo `CHANGELOG.md` backfilled from every existing GitHub Release and thereafter maintained by `/release-plugin`, which prepends each release's composed notes and stages the file in the `Release: <VERSION>` commit so the changelog, the monorepo release, and the distribution releases carry identical notes; and Discussions enabled on the root repository. `FUNDING.yml` and release cadence are out of scope.

## Relevant starting state

### GitHub repository surface

`.github/` exists but holds only `assets/readme/cairn-banner.png` — no `workflows/`, no `ISSUE_TEMPLATE/`, no `PULL_REQUEST_TEMPLATE.md`. GitHub's community-profile API for `uHappyLogic/cairn` scores the repository 42%: `license` and `readme` present; `code_of_conduct`, `contributing`, `issue_template`, and `pull_request_template` missing. Repository settings: issues enabled, wiki enabled (unused), Discussions disabled; both distribution repositories (`uHappyLogic/cairn-claude`, `uHappyLogic/cairn-antigravity`) have issues disabled by design. `README.md` opens with the banner and a centered `<p>` holding exactly two shields.io badges — the release badge (`github/v/release/uHappyLogic/cairn`, tag display) and a static MIT license badge — and has no Contributing, Security, or Changelog section.

### Continuous integration

No CI exists. The repository's only automated check is `uv run scripts/build_hosts.py --check` — the drift gate that renders every host from `core/`, runs the full validation set, compares byte-for-byte against the committed `hosts/<host>/` trees, writes nothing, and exits non-zero listing differing paths — and today it runs only by hand or as pre-flight gate 2e of `/release-plugin`. Tooling is `uv` with Python `>=3.11` (`.python-version` pins `3.13`), one dependency (`pyyaml`) pinned in `uv.lock`, and `pyproject.toml` marked `package = false`; the drift gate also asserts the root `.claude-plugin/marketplace.json` entry equals `VERSION`.

### Host definitions and template rendering

Each host is a definition directory `scripts/hosts/<host>/` whose every file other than `settings.toml` is a template rendered to the same relative path in `hosts/<host>/`, with `{{VERSION}}` filled from the root `VERSION` and `{{NAME}}` from `plugin_name` (`scripts/build_hosts.py`, `render_host`). Claude's templates are `README.md`, `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json`; Antigravity's are `README.md` and `plugin.json`. `LICENSE` is not a template — the build copies the root file by a dedicated code path — so a new text template with no slots would render unchanged and pass the gate's `unfilled-placeholder` check. Both distribution `README.md` templates already carry a "Generated — do not edit" paragraph directing issues and pull requests to `uHappyLogic/cairn`, and a `## Source` section linking the release tag and noting that the release page carries the notes.

### Release skill and release notes

`.claude/skills/release-plugin/SKILL.md` is the maintainer-only release procedure. Step 5 composes `<RELEASE_BODY>` in context and mutates nothing: one `## <Title> (milestone <N>)` section per `Milestone-finish:` commit in `<LAST_TAG>..HEAD` (highest number first, bullets condensed from that milestone's `milestones/README.md` history entry), closed by a `**Full Changelog**: …/compare/<LAST_TAG>...<VERSION>` line; an empty range instead builds a `## Changes since <LAST_TAG>` section behind a maintainer confirmation. Step 6 runs `set_version.py`, rebuilds, stages exactly `VERSION`, `pyproject.toml`, `uv.lock`, `.claude-plugin/marketplace.json`, and `hosts/` path-scoped, records the one `Release: <VERSION>` commit, and verifies `git status --porcelain --untracked-files=no` is empty; step 6 is skipped whole on a resumption (HEAD subject already `Release: <VERSION>`). The skill (step 6b) and `CLAUDE.md`'s Development section both state that the release commit "changes version slots and nothing else, by construction", resting on pre-flight 2a (clean tracked tree) and 2e (drift gate). The notes exist only in context until step 8c writes them to a temp file for `gh release create --notes-file`; each distribution repository's release carries the identical body, and its `Release:` commit body links to the monorepo release page for notes. Step 7 shows `<VERSION>` and the full `<RELEASE_BODY>` as the run's single pause, after the commit.

### Existing release history

Sixteen GitHub releases exist, tagged bare `0.9.0` through `1.4.0`, published 2026-06-12 through 2026-09-15, each titled by its tag. The eight bodies `0.9.0`–`0.9.7` carry only the `**Full Changelog**` compare link (`0.9.0`'s points at `/commits/0.9.0`); the eight from `0.9.8` on carry milestone sections in the step-5 shape (`0.9.9` has two). Publish dates are available via `gh release list --json tagName,publishedAt`. No `CHANGELOG.md` exists anywhere in the repository.

### Contribution-relevant documentation

`README.md`'s `## Development` section already documents the core-once-rebuild model, the three `build_hosts.py` invocations, the `VERSION`/`set_version.py` rule, the distribution repositories, and the directory-marketplace developer install; `## Self-dogfooding` notes that `milestones/` holds the project's own live workflow artifacts. The design invariants a contributor must preserve live in `CLAUDE.md` (~100 KB, also reachable as the `AGENTS.md` symlink) under "Invariants to preserve when editing skills". Commits follow function-derived `<Marker>: <descriptor>` subjects. `LICENSE` is MIT; no security-contact or conduct text exists in any file.

## Decisions

### Contributor workflow

An outside contribution is proposal-first, then a contributor-run milestone on a maintainer-reserved slot. A substantive change is proposed as an issue or Discussion; acceptance is the maintainer running `/define-milestone-goal` on `main` with the accepted proposal and activating it with `/goto-next-milestone` once the current-milestone pointer is free. The contributor branches from that commit and runs the full requirements-and-task pipeline through `/finish-current-milestone` in a fork, and the pull request is merged with a merge commit — squash merges are disabled on the repository — so the milestone commits survive for release notes and for `/capture-milestone-principle-updates`, which the maintainer runs after the merge. There is no plain-pull-request tier: small fixes are filed as issues for the maintainer to make.

## Out of Scope

## Open questions

<open-question id="CI trigger scope">
  <question>Should the drift-gate workflow run on pushes to every branch or only to main (plus every pull request), and should it be path-filtered to the build inputs (core/, scripts/, hosts/, VERSION, the root marketplace) or run on every change?</question>
  <alternative id="Every push and pull request, unfiltered">
    A workflow triggered by push and pull_request with no branch or path filter, so the gate runs on every commit reaching any branch of the root repository, on every pull request, and on each release tag push.
    <advantage>It is the literal contract of the goal (every push and pull request) in the smallest possible workflow with nothing to curate: no filter list can fall out of step with what build_hosts.py reads, every pull request, including a docs-only one, gets a status from the repository&apos;s single automated check, and the badge reflects the latest commit on main rather than the last relevant one.</advantage>
    <drawback>Most runs re-verify an unchanged build: 33 of the last 40 commits are the milestone workflow&apos;s own milestones/-only commits touching nothing the build reads, and a same-repository branch with an open pull request runs twice per push, though each run is about half a minute of checkout and uv setup around a 0.2-second gate on a public repository where Actions minutes cost nothing.</drawback>
  </alternative>
  <alternative id="Main pushes plus pull requests">
    The conventional GitHub layout: push restricted to the main branch plus every pull_request, with no path filter.
    <advantage>It removes the push-plus-pull-request double run and the tag-push run, so every commit is checked exactly once at the point it matters, when it lands on main or is proposed against it.</advantage>
    <drawback>In 568 commits the maintainer has opened no pull request and lands side branches by fast-forward, so a side-branch push gets no run and drift is first reported by the badge turning red on main after it has landed, exactly when a visitor sees it; it also narrows the goal&apos;s own wording (every push) to save a handful of free runs.</drawback>
  </alternative>
  <alternative id="Path-filtered to build inputs">
    Push and pull_request triggers carrying a paths filter that names the build inputs, so a commit touching none of them starts no run at all.
    <advantage>It cuts the runs to the commits that can actually change the render, about one in six on this history, and keeps the Actions tab free of no-op runs for the milestone workflow&apos;s own commits.</advantage>
    <drawback>The list must mirror the exact input set of build_hosts.py and its runner (core/, scripts/, hosts/, VERSION, LICENSE, the root marketplace, pyproject.toml, uv.lock, .python-version, and the workflow file itself); the question&apos;s own five-item list already omits LICENSE, which the build copies into every host tree, and the uv environment files, so the filter becomes a hand-maintained second copy of the build&apos;s inputs, the very drift the gate exists to catch, and a path-skipped workflow reports no status, so any future required-check branch protection blocks a docs-only pull request until a no-op twin workflow is added.</drawback>
  </alternative>
  <recommendation option="Every push and pull request, unfiltered">The gate reads core/, scripts/hosts/, VERSION, LICENSE, and the root marketplace and finishes in 0.2 seconds inside a half-minute free job, so filtering buys nothing measurable while a paths list would be a hand-maintained second copy of the build&apos;s input set (the question&apos;s own list already omits LICENSE and the uv files) and a skipped run leaves a pull request with no status; every push and pull request is the goal&apos;s literal wording, the maintainer pushes straight to main with no pull-request history to double-run, and the two-event trigger has nothing to curate.</recommendation>
</open-question>
<open-question id="Contributing vs Development overlap">
  <question>Does the root CONTRIBUTING.md absorb the README Development section (with the README linking out to it), or summarize the contributor path and link to the README section that stays authoritative?</question>
</open-question>
<open-question id="README links to hygiene files">
  <question>Beyond the CI badge, should README.md gain a Contributing section or links to CONTRIBUTING.md, SECURITY.md, CHANGELOG.md, and Discussions, or stay untouched?</question>
</open-question>
<open-question id="Conduct text and contact">
  <question>Which code-of-conduct text is adopted (Contributor Covenant 2.1, the GitHub-recognized default, or 3.0), and which contact address does its enforcement clause name?</question>
  <alternative id="Covenant 2.1 with the commit author address">
    CODE_OF_CONDUCT.md is Contributor Covenant 2.1 verbatim, its single [INSERT CONTACT METHOD] slot filled with kosiak.lukasz@gmail.com, the author address every one of the 568 commits already carries.
    <advantage>It is the current 2.x text and the one GitHub&apos;s content detection labels Contributor Covenant on the Community Standards page (a 2.1 file resolves to key contributor_covenant where a 3.0 file resolves to Other), it has exactly one slot to fill, and the address named already exists, is read, and is public on every commit page of the repository, so the file needs no new mailbox and no authored enforcement text.</advantage>
    <drawback>A personal gmail address lands in a rendered file that crawlers and harvesters index, the exposure Security reporting channel&apos;s recommendation leaves out of SECURITY.md, and 2.1 is no longer the newest Covenant (3.0 shipped in July 2025), so a visitor who checks the Covenant site sees a superseded version.</drawback>
  </alternative>
  <alternative id="Covenant 2.1 with a dedicated conduct address">
    The same 2.1 text with the slot filled by a purpose-made address on a domain the maintainer controls (the profile links busyminds.io) or a separate mailbox created for reports.
    <advantage>It keeps the personal inbox out of the rendered file, gives conduct mail a channel that can be forwarded or rotated without touching the file, and is the address SECURITY.md could later name as its fallback.</advantage>
    <drawback>No such mailbox verifiably exists today (the GitHub profile lists no email and busyminds.io exposes no contact), so the file names an address whose creation and monitoring happen outside the repository, and for a one-maintainer project with no community incidents an alias nobody checks is worse than a personal address somebody reads.</drawback>
  </alternative>
  <alternative id="GitHub picker text (Covenant 2.0)">
    The text GitHub&apos;s codes_of_conduct API serves and its template chooser draws on, which is Contributor Covenant 2.0, with the same single slot filled with the author address.
    <advantage>Zero authoring: gh api codes_of_conduct/contributor_covenant returns the body ready to write, and GitHub detects it as Contributor Covenant exactly as it does 2.1.</advantage>
    <drawback>It adopts a text its publisher replaced in 2021 (2.1 adds caste and color to the pledge and changes little else) to save one download, so the file opens with an outdated version line for anyone who knows the Covenant.</drawback>
  </alternative>
  <alternative id="Covenant 3.0 with the commit author address">
    The July 2025 rewrite from the Organization for Ethical Source, with its two [NOTE] slots (means of reporting, and the remedies and enforcement process) authored and the author address named as the reporting channel.
    <advantage>It is the current text from the Covenant&apos;s stewards, with clearer and less US-centric language, the neutral Community Moderators role, and the restorative Addressing and Repairing Harm section that new adopters are moving to.</advantage>
    <drawback>GitHub&apos;s detection does not recognise it (the Covenant&apos;s own repository and changesets&apos; 3.0 file both show as Other on the Community Standards page, though the presence check still passes), its text carries a CC BY-SA 4.0 share-alike line beside an otherwise MIT repository, and its two NOTE slots ask for authored reporting and remedy prose rather than one address, more customisation than a repository with no community incidents has facts for.</drawback>
  </alternative>
  <recommendation option="Covenant 2.1 with the commit author address">2.1 is the text GitHub labels Contributor Covenant (a 3.0 file resolves to Other) and the current 2.x version, with one slot to fill instead of 3.0&apos;s two authored notes; the contact has to be an email because GitHub offers no private conduct channel (issues and Discussions are public, private vulnerability reporting is for security), and the only address that verifiably exists and is read is the author address already on all 568 commits and every commit page of the repository, so naming it adds crawler indexing of a rendered file but no new information; choose the dedicated address instead only if a monitored mailbox on a maintainer-controlled domain already exists, since creating one for a repository with no community yet is an inbox nobody checks.</recommendation>
</open-question>
<open-question id="Security reporting channel">
  <question>Does SECURITY.md direct reports to GitHub private vulnerability reporting (which must be enabled on the repository), to an email address, or both, and which versions does it declare supported?</question>
  <alternative id="GitHub private reporting only">
    SECURITY.md directs reports to the root repository&apos;s Report a vulnerability form (github.com/uHappyLogic/cairn/security/advisories/new), the milestone enables private vulnerability reporting on uHappyLogic/cairn with one gh api --method PUT call beside the Discussions enable, no email address appears in the file, and the supported-versions table names the latest release only, noting that every fix ships as a new release from main to both distribution repositories.
    <advantage>A report lands as a draft advisory inside the repository that owns the fix, with a private thread, an optional private fork for the patch, and a publish-with-CVE step, and nothing new is published about the maintainer: the GitHub profile lists no email today and no file in the repository carries contact text, so the file stays a link plus a policy.</advantage>
    <drawback>The link only works once private reporting is actually enabled (it is disabled on all three repositories today), a reporter needs a GitHub account, and the distribution repositories keep no Report a vulnerability button of their own, so a user who lands on cairn-claude first reaches the form only through that README&apos;s existing redirect to the root repository.</drawback>
  </alternative>
  <alternative id="Email address only">
    SECURITY.md names an email address as the sole reporting channel (the git author address that every one of the 568 commits already carries, or a dedicated one) with the same latest-release-only support declaration, and no repository setting changes.
    <advantage>It works for a reporter with no GitHub account, needs no settings toggle, and can share one address with the code-of-conduct enforcement clause if Conduct text and contact settles on an email.</advantage>
    <drawback>It publishes a personal address in the one file every scanner and spam harvester reads (the profile publishes none today, and a gmail inbox cannot tell a report from noise), and each report arrives as unstructured mail outside the repository: no private thread, no advisory record, no fix-then-publish flow, all of which the maintainer then rebuilds by hand.</drawback>
  </alternative>
  <alternative id="Private reporting with email fallback">
    Private reporting is enabled and named first, and the file adds an email address as a fallback for reporters who cannot use the GitHub form, with the same latest-release-only declaration.
    <advantage>Neither reporter class is turned away, and the file reads as the fullest conventional policy.</advantage>
    <drawback>It pays both costs at once for a repository with zero advisories and one maintainer: the address is published anyway, reports can arrive through two channels the maintainer must watch and reconcile, and the fallback line is the one part of the file that depends on how Conduct text and contact chooses its enforcement contact, so writing it now means choosing that address here first.</drawback>
  </alternative>
  <recommendation option="GitHub private reporting only">Private reporting is one gh api --method PUT toggle of the same kind as the Discussions enable the goal already includes, and it puts each report where the fix happens, as a draft advisory with a private thread and a publish step, instead of in a gmail inbox; the maintainer publishes no email today and a fallback address is a one-line addition if Conduct text and contact settles on one, so nothing is lost by leaving it out now; and the supported-versions clause has one honest value because the sixteen releases are strictly linear, the release skill publishes only main&apos;s HEAD, and both patch releases (1.0.1, 1.1.1) landed on the newest minor, so the table names the latest release only and states that every fix ships as a new release to both distribution repositories.</recommendation>
</open-question>
<open-question id="Issue template format">
  <question>Are the bug and feature templates YAML issue forms with structured fields (host, cairn version, skill invoked) or Markdown templates with free-text sections?</question>
  <alternative id="YAML issue forms">
    Two issue forms, .github/ISSUE_TEMPLATE/bug-report.yml and feature-request.yml, each with name, description, and labels (bug and enhancement, both already present on the repository) over a body of typed fields: the bug form a host dropdown (Claude Code, Antigravity), a cairn version input, a skill-invoked input, a what-happened textarea, and a console-output textarea with render set to shell, the first four marked required; the feature form a summary input and two textareas for the workflow gap and the proposed behaviour.
    <advantage>A required field can be neither left empty nor deleted, so every bug report arrives carrying the three facts a cairn reproduction turns on (which of the two host trees, which of the sixteen releases, which of the 21 skills) under fixed ### headings in a plain-Markdown body; the host dropdown mirrors the two definition directories under scripts/hosts/, and the transcript textarea renders as a code block without the reporter knowing any Markdown.</advantage>
    <drawback>The gh CLI does not detect YAML forms (its template lookup matches only .md files, and cli/cli issue 5865, Support for issue forms, has been open since 2022), so gh issue create, the tool at hand for cairn&apos;s agent-host audience, offers no template and files a blank body unless run with --web; and any dropdown that enumerated the skills would be a hand-maintained copy of core/skills/ the build never validates, in a history that has already renamed seven skills.</drawback>
  </alternative>
  <alternative id="Markdown templates">
    Two Markdown templates, .github/ISSUE_TEMPLATE/bug_report.md and feature_request.md, each with YAML front matter (name, about, title, labels) over a body of ### sections whose HTML-comment prompts ask for host, cairn version, skill invoked, steps, expected and actual behaviour, and console output.
    <advantage>It works in every entry path: the web chooser, gh issue create (which lists the template and pre-fills the body from it), and any editor, and each template is one plain text file to author, read, and diff.</advantage>
    <drawback>Nothing is enforced: the pre-filled sections are editable text a reporter deletes or leaves as the placeholder comment, so host, version, and skill arrive as prose when they arrive at all and must be asked for in a follow-up comment, while the community-profile check counts the template folder the same for either format, so the file earns nothing a form does not.</drawback>
  </alternative>
  <alternative id="Form for bugs, Markdown for features">
    A YAML form for the bug report, where the structured fields pay, and a Markdown template for the feature request, which is prose.
    <advantage>Each template takes the format its content wants: enforced facts for a reproduction, free text for a proposal.</advantage>
    <drawback>Two authoring formats for two files, and the gh CLI then sees only the .md file, so its chooser offers the feature template and a blank issue alone and a bug filed from the terminal starts from the feature body or nothing; a form whose body is a single textarea is exactly as free as a Markdown template, so the split saves no freedom and costs the uniformity.</drawback>
  </alternative>
  <recommendation option="YAML issue forms">Host, cairn version, and skill invoked are the three facts a cairn bug cannot be reproduced without and exactly what free text loses, and required form fields are the only mechanism that guarantees them on a repository with no issues yet and no triage history to fall back on; keep the host as a two-value dropdown mirroring scripts/hosts/ and the version and skill as free-text inputs so no field enumerates the 21 skills a list would have to track; the one cost is the gh CLI gap, which a reporter crosses with gh issue create --web and which a Markdown template only papers over since gh pre-fills sections it does not enforce, so choose Markdown only if terminal-filed issues are expected to be the main channel.</recommendation>
</open-question>
<open-question id="Blank issues and contact links">
  <question>Should an ISSUE_TEMPLATE config.yml disable blank issues and route questions to a Discussions category once Discussions is enabled?</question>
</open-question>
<open-question id="Changelog entry heading form">
  <question>Does each CHANGELOG.md entry follow Keep a Changelog conventions (a bracketed version heading with date, reference-style compare links, an Unreleased section) or a plain version-and-date heading over the release body verbatim?</question>
  <alternative id="Full Keep a Changelog">
    The file follows the format whole: a title and adherence note, an Unreleased section, one bracketed version heading with an ISO date per release, each body re-sorted into Added / Changed / Deprecated / Removed / Fixed / Security subsections, and a reference-style link list at the bottom resolving every bracketed version to its compare URL.
    <advantage>It is the one changelog format a first-time visitor and changelog tooling recognise on sight, with a per-release date, a category breakdown, and a linked compare range in a fixed place.</advantage>
    <drawback>Its substance, the category subsections, cannot be the release body: the composed notes are one milestone section per finished milestone (eight sectioned bodies from 0.9.8 to 1.4.0, 0.9.9 with two), so either step 5 of /release-plugin is rewritten to compose in categories, changing the published series shape and the milestones/README.md-to-notes mapping, or the changelog entry becomes a second, hand-categorised rendering that the goal&apos;s identical-notes clause forbids; the eight link-only bodies have nothing to categorise, and the Unreleased section and bottom link list are two more slots the release skill must edit and a resumption must re-verify.</drawback>
  </alternative>
  <alternative id="Keep a Changelog frame over verbatim body">
    Borrow the format&apos;s skeleton only: an Unreleased section, bracketed version headings with the date, and the bottom reference-link list, with each entry&apos;s body being the release body verbatim (milestone sections plus the Full Changelog line).
    <advantage>The file&apos;s outline reads as the recognised format at a glance without changing a word of what the release notes say.</advantage>
    <drawback>It announces a format it does not follow (no category subsection under any heading), the compare link appears twice per entry (the bracketed heading&apos;s reference and the body&apos;s own Full Changelog line), the verbatim body&apos;s ## milestone sections sit level with the version headings unless demoted, the Unreleased section stays empty forever because nothing writes to it between releases (notes are composed from milestone history at release time and the finish skill ships to consuming projects), and every release turns the one prepend into three edits: insert the entry under Unreleased, retarget the Unreleased compare endpoint, and add the new version&apos;s reference link.</drawback>
  </alternative>
  <alternative id="Plain version-date heading over verbatim body">
    A title, a one-line note that each entry is that release&apos;s notes verbatim, newest first, and per release a plain heading of the form ## &lt;VERSION&gt; — &lt;YYYY-MM-DD&gt; (the em-dash style of the milestones/README.md history headings) directly over the release body, whose milestone sections sit at ### so they nest under it; no Unreleased section and no reference links, the body&apos;s Full Changelog line being the compare link.
    <advantage>The release write is one prepend below the title with no other slot in the file, the entry is byte-identical to the body written to the three release pages, and the backfill is a loop over gh release view --json body with the publishedAt date as each heading&apos;s date.</advantage>
    <drawback>It is not the recognised format, so a visitor gets no Added/Changed breakdown and no Unreleased preview, and the nesting costs one shape change: step 5 composes milestone sections at ### from this release on (the eight existing sectioned bodies are demoted once in the backfill), so release pages from here on render those sections one level smaller than 0.9.8 through 1.4.0 do.</drawback>
  </alternative>
  <recommendation option="Plain version-date heading over verbatim body">The goal fixes the entry body as the release&apos;s composed notes, identical across the changelog and the three release pages, which rules out the categorised body that is Keep a Changelog&apos;s substance and leaves only its skeleton to borrow, and that skeleton costs more than it reads: an Unreleased section nothing fills between releases, a reference-link list duplicating the body&apos;s own Full Changelog line, and three edits per release in place of one prepend; a plain ## &lt;VERSION&gt; — &lt;YYYY-MM-DD&gt; heading over the verbatim body keeps the release write to one prepend and the backfill to a gh release view loop with publishedAt dates, and composing the milestone sections at ### (demoted once in the backfill) is the one adjustment that makes the outline nest while keeping the entry byte-identical to the body, which is also what a later reread from the file needs if Release body source of truth settles on reading the body back from CHANGELOG.md.</recommendation>
</open-question>
<open-question id="Link-only release backfill">
  <question>For the eight releases 0.9.0 through 0.9.7 whose bodies are only the compare link, does the backfill carry those bodies verbatim or reconstruct condensed notes from the milestone history and commit ranges?</question>
  <alternative id="Verbatim carry">
    Each early entry is the plain version-date heading over the body exactly as gh release view returns it: the single Full Changelog line for seven releases (0.9.0&apos;s pointing at /commits/0.9.0) and nothing at all under 0.9.6, whose published body is empty.
    <advantage>It is the goal&apos;s literal source (backfilled from every existing GitHub Release) and the only option under which the identical-notes clause and the file&apos;s own one-line verbatim note hold for all sixteen entries without an exception, so the backfill stays one uniform gh release view loop with publishedAt dates, and every entry records what the release said when it shipped rather than what a later reader composed about it.</advantage>
    <drawback>Half the file (June 12 to July 27, thirteen finished milestones) tells a visitor nothing beyond a commit range, 0.9.6 comes over as a bare heading, and the condensed per-milestone story for that period is reachable only through milestones/README.md&apos;s history entries, not from the changelog itself.</drawback>
  </alternative>
  <alternative id="Reconstruct in the changelog only">
    Compose each early entry in the step-5 shape from the history entries the step-5b heading diff attributes to that tag pair (milestone 1 for 0.9.1, 2 for 0.9.2, 3 to 6 for 0.9.4, 7 and 8 for 0.9.5, 9 to 11 for 0.9.6, 12 and 13 for 0.9.7), a commit-range summary for 0.9.0 (24 commits, including the pre-milestone origin) and 0.9.3 (16 commits, no entry added), each closed by the existing compare link, leaving the release pages untouched.
    <advantage>The changelog reads uniformly end to end in the shape the later eight already use, and the milestone-to-release mapping is deterministic because all thirteen history entries stand unchanged at HEAD.</advantage>
    <drawback>Eight entries no longer match their release page, so the goal&apos;s identical-notes clause and the file&apos;s verbatim note each need a carved-out exception, and the notes are a September rewrite of June and July work with no release-time provenance that a reader cannot tell apart from notes that shipped, two of them resting on condensed commit subjects alone.</drawback>
  </alternative>
  <alternative id="Reconstruct and republish">
    The same reconstruction, followed by gh release edit &lt;tag&gt; --notes-file on each of the eight monorepo releases so that page and entry carry identical text.
    <advantage>Identity holds for every entry by construction and the published series becomes sixteen sectioned bodies of one shape, which is the consistency step 5 already aims at going forward.</advantage>
    <drawback>It rewrites eight published release pages, the artifact the release skill treats as irreversible and the goal names as the backfill&apos;s source rather than its target, through a one-time mutating operation outside /release-plugin, replacing the honest at-the-time record with retro-composed text while carrying the same condensation labor as reconstructing in the changelog alone.</drawback>
  </alternative>
  <depends-on question="Changelog entry heading form" option="Plain version-date heading over verbatim body"/>
  <recommendation option="Verbatim carry">The goal names the existing releases as the backfill&apos;s source and requires the changelog and the release pages to carry identical notes, which under the plain heading over the verbatim body is a single gh release view loop that holds for all sixteen entries with no exception; reconstructing turns eight entries into a September rewrite the reader cannot distinguish from shipped notes, and the only way to reconstruct without breaking identity is to rewrite eight published release pages, which is the one thing that should break the tie (choose republishing only if the maintainer wants those pages rewritten); the compare link still gives each early entry its commit range and milestones/README.md already holds the condensed per-milestone story.</recommendation>
</open-question>
<open-question id="Release body source of truth">
  <question>Once /release-plugin writes the changelog entry, does the publish step read the release body from the committed CHANGELOG.md entry (so a resumption rereads it instead of recomposing) or keep the in-context body, and does pre-flight guard against an entry for the release version already being present?</question>
  <alternative id="Committed entry is the source">
    Once the Release commit exists, the release body is defined as the entry for &lt;VERSION&gt; extracted from HEAD:CHANGELOG.md (the lines under its ## &lt;VERSION&gt; heading up to the next ## heading, blank lines trimmed), so step 7 shows and step 8 publishes that text on a fresh run and a resumption alike; step 5 composes only on a fresh run, and a pre-mutation gate beside the tag-existence check requires that no entry for &lt;VERSION&gt; exists on a fresh run and that exactly one exists at HEAD on a resumption.
    <advantage>The notes gain the durability every other release artifact already has: the Release commit is what step 8 resumes from, so a resumption publishes the committed text instead of a fresh condensed rewrite, closing the gap where a run that fails between 8c and 8d today recomposes at step 5 and can hand the distribution releases notes that differ from the monorepo release already created; identity between the changelog and the three release pages then holds by construction, the step-7 pause shows exactly what git records, and the guard turns a stale unpublished Release commit buried below HEAD, which would otherwise gain a duplicate entry in a commit that succeeds, into a pre-flight stop.</advantage>
    <drawback>It adds one extraction rule the skill must state exactly (heading line to next ## heading, milestone sections already at ###), and a resumption now skips step 5 whole, so its cross-check and empty-range confirmation are not re-run on recovery and rest on the committed entry as the evidence they passed.</drawback>
  </alternative>
  <alternative id="In-context body throughout">
    Step 5 stays the only source of the body: step 6 additionally prepends it to CHANGELOG.md and stages that path, a resumption recomposes it as today, and no new gate reads the changelog, the existing clean-tree, tag-existence, and HEAD-subject checks being relied on.
    <advantage>The smallest edit to the skill: one prepend and one staged path in step 6, with every step that reads &lt;RELEASE_BODY&gt; and the whole resumption story left untouched.</advantage>
    <drawback>Recomposition is a condensed rewrite, not a deterministic function, so on a resumption the body shown at step 7 and published to any release page not yet created can differ from the committed entry and from a page an earlier run already created, which is exactly the identical-notes clause the goal adds; and a Release commit for &lt;VERSION&gt; declined at step 7 and later buried under other commits (HEAD subject no longer matches, no tag exists) passes every existing gate, where today it stops at step 6d with nothing to commit but with the changelog it commits a second &lt;VERSION&gt; entry.</drawback>
  </alternative>
  <alternative id="Reread only on resumption">
    A fresh run carries the composed body in context from step 5 through step 8 as today, while a resumption skips step 5 and extracts the body from the committed entry; only the fresh-run half of the guard (no entry for &lt;VERSION&gt; yet) is added.
    <advantage>The fresh run has nothing between compose and publish: no extraction rule stands between what step 5 built, what step 7 shows, and what 8c writes, and the file read is confined to the recovery path.</advantage>
    <drawback>One value gets two sources, and the extraction runs only on the rare resumption, so a defect in it (or a prepend that placed the entry wrongly) surfaces exactly when recovering from a failure, while a fresh run never confirms that the text it committed is the text it published.</drawback>
  </alternative>
  <depends-on question="Changelog entry heading form" option="Plain version-date heading over verbatim body"/>
  <recommendation option="Committed entry is the source">The goal already puts the entry in the Release commit before anything is published, which makes it the one version-controlled copy of the notes and the natural thing a check-then-do resumption reads back, so the changelog and the three release pages stay identical even when a run fails between creating them (today a resumption recomposes a condensed rewrite at step 5 and can publish differing distribution notes); under the plain heading form the extraction is a fixed line range with the body byte-identical to the entry, and the guard is one grep beside the tag check that flips on resumption, turning the duplicate-entry commit a stale unpublished Release commit would otherwise produce into a pre-flight stop.</recommendation>
</open-question>
<open-question id="Unused wiki tab">
  <question>Should the unused wiki be disabled on the root repository so a visitor sees no empty Wiki tab, or be left enabled?</question>
</open-question>
<open-question id="Squash merge setting">
  <question>Is disabling squash merges on the root repository, which the contributor-workflow decision requires so a contributor milestone&apos;s Milestone-finish: and answer commit subjects survive the merge, a task of this milestone alongside enabling Discussions, or a repository setting the maintainer flips by hand outside any task?</question>
</open-question>
<open-question id="Proposal intake route">
  <question>Is the proposal that precedes a contributor-run milestone filed through a dedicated proposal issue form beside the bug and feature templates, through a Discussions category once Discussions is enabled, or through the feature template as it stands?</question>
</open-question>
<open-question id="CONTRIBUTING.md handoff wording">
  <question>Does the root CONTRIBUTING.md spell out the proposal-then-reserved-milestone handoff step by step (propose, maintainer defines and activates the milestone on main, branch from that commit, run the pipeline through /finish-current-milestone, merge commit), or state the contract in a sentence and point at the README workflow documentation for the steps?</question>
</open-question>
<open-question id="Pull-request template milestone field">
  <question>Does the pull-request template ask for the reserved milestone id and the proposal it was accepted in, so a reviewer can check the branch carries that milestone&apos;s artifacts, or stay a generic checklist (rebuilt hosts/ trees, --check green, CLAUDE.md invariants preserved)?</question>
</open-question>
