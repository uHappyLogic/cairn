# Milestone 35: Committing Bootstrap

## Goal

Retire the bootstrap's non-committing exemption so that every file-changing Cairn skill commits its own paths and a headless chain leaves no uncommitted files behind. init-milestone-base-workflow gains a git work-tree prerequisite check beside its Python check, stopping before it writes anything when the project is not a git repository, and commits the files it created or edited (milestones/README.md, and CLAUDE.md when it touched it) through the shared commit procedure under its own function-derived subject. The invariant in CLAUDE.md, the exemption paragraph in docs/workflow.md, and the skill reference are updated to match. The benchmark harness side of G04 is out of scope.

## Relevant starting state

### The bootstrap skill

`core/skills/init-milestone-base-workflow/SKILL.md` runs six steps: a Python prerequisite check (step 1), state detection (step 2), creation of `milestones/` and `milestones/README.md` (steps 3–4), ensuring `CLAUDE.md` carries the `## Milestone Workflow` section (step 5), and a free-form confirmation report (step 6). Step 1 is the template for a prerequisite check: it runs on every invocation before state detection, stops before any write on failure, and prints one message with what it looked for, what it found, the remedy, and that a re-run completes the bootstrap. Step 2 stops without changing anything when `milestones/`, `milestones/README.md`, and its `Current milestone:` line all already exist. Step 5 edits `CLAUDE.md` only when it lacks the section (creating the file when absent, appending otherwise), so whether `CLAUDE.md` was touched is known at edit time. The opening paragraph states "It does not commit — staging is left to the user", and step 6 is a multi-line report (items created vs. preserved, pointer initialized, next steps), not the one fixed terse line the other committing skills print. The skill is rendered byte-identically into `hosts/claude/` and `hosts/antigravity/`; any edit under `core/` requires `uv run scripts/build_hosts.py` and the rebuilt trees committed alongside, gated by `--check` in `.github/workflows/drift-gate.yml`.

### The shared commit procedure and its consumers

`core/shared/commit-procedure.md` takes PATHS (named by the caller without content inspection), SUBJECT (`<Marker>: <descriptor>`), and optional BODY, then runs a dirty-own-path guard via `git status --porcelain -- <PATHS>`, a path-scoped `git add`, and `git commit`. It assumes it is running inside a git work tree; nothing in `core/` checks for one (no `git rev-parse`, no "not a git repository" prose anywhere in the runtime files). Sixteen skills reference it; the bootstrap is the only file-changing skill that does not. Two consumers show the shapes this milestone needs: `define-milestone-goal` step 5 commits files it just created under `Milestone-definition: <milestone_id>`, and `finish-current-milestone` step 8 commits `milestones/README.md` always and `CLAUDE.md` "only on passes where step 7 actually edited it", keyed on whether the edit was made, never by diffing. Both end with a step that prints exactly one fixed terse status line on success and one distinct line when the guard fired. The git log carries no marker for the bootstrap yet; existing setup markers are `Milestone-definition:`, `Milestone-activation:`, `Milestone-finish:`, and `Starting-state:`.

### Where the exemption is recorded

The exemption is stated in five places, and they do not agree on what the bootstrap leaves behind. `CLAUDE.md` line 51 tags the skill "non-committing" in the pipeline listing and line 95 (the "Committing is a property of the skill layer" invariant) names it "the one non-committing exemption (a consuming project may not be a git repo)". `docs/workflow.md` line 166 says it "leaves its changes **staged** for you instead" because the project "may not be a git repo or may want its own commit boundaries". `docs/design-claims.md` claim 12 says the work tree is clean after each skill "with two exceptions", the bootstrap "does not commit and leaves its changes staged for the user" and a failed run's partial work. The SKILL.md itself says staging is left to the user, so the skill neither commits nor stages today. `docs/skill-reference.md` lines 5–7 describe the Python check and the scaffold and say nothing about committing. `README.md` line 54 and its two copies under `scripts/hosts/*/README.md` name Python 3.9 as Cairn's "one runtime prerequisite"; git is not listed as a prerequisite anywhere.

### Headless chains

`docs/ways-of-using-cairn.md` states that every skill commits what it changes under its own subject and contains no chain line invoking `init-milestone-base-workflow`; every documented chain starts from an already-bootstrapped repository. The bootstrap is therefore the only skill a headless run could invoke that leaves files uncommitted.

### Known gap

No file in the repository references G04; the identifier lives outside the repo, so the in-scope boundary the goal draws against it has no in-repo anchor.

## Decisions

## Out of Scope

