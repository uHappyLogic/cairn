# TASKS DONE

## Add Git Work-Tree Prerequisite Check

Add to `core/skills/init-milestone-base-workflow/SKILL.md` a git prerequisite check that runs first, ahead of the Python check, on every invocation before state detection: one `git rev-parse --is-inside-work-tree` probe of the workspace root that passes anywhere inside a git work tree (a subdirectory of a larger repository, or a fresh repository with no commits, with no top-level advisory) and otherwise stops before any write with its own four-part message in the Python check's shape (a git work tree at the workspace root looked for; the `git` executable missing or the directory not a work tree found; install git or run `git init` in the workspace root as the fitting remedy; a re-run completes the bootstrap with nothing to undo), never prompting and never running `git init` itself, with the opening paragraph presenting the git check as the first thing the skill does. The check is what lets the commit step the next task adds assume a work tree. Verified by reading the rendered skill for the step order and the two separate stops, and by `uv run scripts/build_hosts.py --check` passing with the rebuilt `hosts/` trees committed alongside.

**Verified:**

- `core/skills/init-milestone-base-workflow/SKILL.md` step 1 is "Check the git prerequisite", ahead of step 2 "Check the Python prerequisite" and step 3 "Detect existing state", and states it runs on every invocation, including a re-run on an already-bootstrapped project.
- The git check is a single `git rev-parse --is-inside-work-tree` probe in the workspace root that passes on `true`, anywhere inside a work tree (a subdirectory of a larger repository, or a fresh repository with no commits), with no top-level match required and no advisory printed.
- On failure the git check stops before any write, prompts for nothing, never runs `git init`, and prints its own four-part message: a git work tree at the workspace root looked for; the `git` executable missing or the directory not a work tree found; install git or run `git init` in the workspace root as the fitting remedy; a re-run completes the bootstrap with nothing to undo.
- The git and Python stops are separate: the git stop says a project failing both learns about Python on the next run, and the Python check keeps its own four-part stop, now continuing to step 3 on success.
- The opening paragraph presents the git work-tree check as the first thing the skill does, followed by the Python check.
- `uv run scripts/build_hosts.py` rebuilt `hosts/claude/` and `hosts/antigravity/`, whose rendered skills carry the same step order and stops, and `uv run scripts/build_hosts.py --check` passed.

---

## Commit Bootstrap Scaffold Through Shared Procedure

Retire the "It does not commit — staging is left to the user" exemption in `core/skills/init-milestone-base-workflow/SKILL.md` by adding a commit step after the `CLAUDE.md` step that follows `{{PLUGIN_ROOT}}/shared/commit-procedure.md` with PATHS of `milestones/README.md` always plus `CLAUDE.md` only on runs where the skill created or appended to it (keyed on the edit being made, never by diffing), the constant subject-only SUBJECT `Workflow-bootstrap: milestones` and no BODY, handing the paths over unchanged so uncommitted changes already present in them are swept into the commit with no pre-write status probe, stop, confirmation, hunk-level staging, or advisory. This closes the milestone's goal that every file-changing skill commits its own paths. Verified by reading the rendered skill against `define-milestone-goal` step 5 and `finish-current-milestone` step 8 for shape, and by `uv run scripts/build_hosts.py --check` passing with the rebuilt `hosts/` trees committed alongside.

**Verified:**

- The opening paragraph of `core/skills/init-milestone-base-workflow/SKILL.md` no longer says "It does not commit — staging is left to the user" and instead states that the skill commits the files it created or edited as one path-scoped commit.
- A new step 7 "Commit the bootstrap" sits after step 6 (the `CLAUDE.md` step) and before the renumbered step 8 "Confirm", and follows `{{PLUGIN_ROOT}}/shared/commit-procedure.md`, carrying out its steps itself.
- Its PATHS are always `milestones/README.md`, plus `CLAUDE.md` only on runs where step 6 created it or appended the `## Milestone Workflow` section, keyed on whether the edit was made and never on diffing or inspecting content.
- Its SUBJECT is the constant `Workflow-bootstrap: milestones`, and it supplies no BODY, so the commit is subject-only.
- The step hands the paths over unchanged, so uncommitted changes already present in them are swept into the commit, with no status probe beforehand, no stop, no confirmation, no hunk-level staging, and no advisory.
- Read against `define-milestone-goal` step 5 and `finish-current-milestone` step 8, the step has the same shape: the "Read and follow the shared commit procedure" opener, the PATHS and SUBJECT bullets, the conditional-inclusion sentence modelled on the finish step, and the closing "The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit." line.
- `uv run scripts/build_hosts.py` rebuilt `hosts/claude/` and `hosts/antigravity/`, whose rendered skills carry step 7 with each host's resolved commit-procedure path, and `uv run scripts/build_hosts.py --check` passed.

---

## Replace Bootstrap Report With Terse Lines

Replace the multi-line confirmation in `core/skills/init-milestone-base-workflow/SKILL.md` with the reporting shape the other setup skills use: on success exactly one fixed identifier-free status line, `Workflow bootstrapped.`, and on the already-initialized stop one distinct no-op line, cutting the created-versus-preserved itemization, the pointer-initialized line, the numbered next steps, and the suggestion to run `/init` (including the one in the `CLAUDE.md` step), so the skill prints no next-step or handoff pointer. The commit diff now shows which files were created or appended to, which is why the itemization goes. Verified by reading the rendered skill and by `uv run scripts/build_hosts.py --check` passing with the rebuilt `hosts/` trees committed alongside.

**Verified:**

- Step 8 "Confirm" of `core/skills/init-milestone-base-workflow/SKILL.md` prints, on the success path, exactly one fixed identifier-free status line `Workflow bootstrapped.` and nothing else.
- The already-initialized stop in step 3 prints one distinct no-op line, `Workflow already bootstrapped — nothing changed.`, and nothing else.
- The created-versus-preserved itemization (including step 5's "Report that the file was preserved"), the pointer-initialized line, and the numbered next steps are gone from the skill.
- The suggestion to run `/init` is gone, including the one in the `CLAUDE.md` step (step 6), and the skill prints no next-step or handoff pointer; a grep of the rendered skills for "suggest", "next step", "recommend", "preserved", and "initialized to" finds nothing.
- `uv run scripts/build_hosts.py` rebuilt `hosts/claude/` and `hosts/antigravity/`, whose rendered skills carry the same step 3 and step 8 lines, and `uv run scripts/build_hosts.py --check` passed.

---

## Update Invariant And Docs For Committing Bootstrap

Update every statement in `CLAUDE.md`, `docs/workflow.md`, `docs/design-claims.md`, and `docs/skill-reference.md` that the bootstrap does not commit or that Python is the workflow's one runtime prerequisite: the pipeline tag "non-committing" and the "one non-committing exemption" clause of the committing invariant, the exemption paragraph and the "one runtime prerequisite" wording in `docs/workflow.md`, design claim 12's "two exceptions" sentence (which drops to the one failed-run exception), and the skill-reference entry, so each now records git as a second prerequisite checked first, the `Workflow-bootstrap: milestones` commit, and the terse report. The criterion is the decision, not a hand list, so grep for further statements rather than stopping at the sites named. Verified by a repository-wide grep finding no remaining claim, outside the historical `CHANGELOG.md` entries and `milestones/`, that the bootstrap leaves files uncommitted or staged or that Python is the one prerequisite.

**Verified:**

- `CLAUDE.md`'s pipeline listing tags `init-milestone-base-workflow` with the git work-tree check first, then python3 ≥ 3.9, then the scaffold, and `commits under Workflow-bootstrap: milestones`, replacing "non-committing".
- The "Committing is a property of the skill layer" invariant in `CLAUDE.md` drops "the one non-committing exemption" clause and states there is no exemption: the bootstrap checks for a git work tree first (git as the second prerequisite beside Python), commits subject-only under `Workflow-bootstrap: milestones`, and sweeps uncommitted changes already in its paths into that commit by design.
- `docs/workflow.md`'s One-time setup paragraph names two runtime prerequisites, git first then Python 3.9+, and says the bootstrap commits under `Workflow-bootstrap: milestones`; the How skills commit exemption paragraph is replaced by a statement that the bootstrap is no exception (git check first, commit with no body, pre-existing uncommitted changes in its paths swept in).
- `docs/design-claims.md` claim 12 says the work tree is clean after each skill "with one exception", the failed-run partial work, with the bootstrap sentence removed.
- The `docs/skill-reference.md` entry records both prerequisites (git checked first by one `git rev-parse --is-inside-work-tree` probe with its remedy, then Python), the `Workflow-bootstrap: milestones` subject-only commit and its paths, and the terse report (`Workflow bootstrapped.` on success, `Workflow already bootstrapped — nothing changed.` on the no-op stop, no itemization or next-step pointer).
- A repository-wide grep (excluding `.git`, `milestones/`, and `CHANGELOG.md`) for "non-committing", "one runtime prerequisite", "does not commit", "staging is left", "leaves its changes", "two exceptions", "exemption", and "changes staged" finds no remaining claim that the bootstrap leaves files uncommitted or staged, the only `CLAUDE.md` hit being the sentence denying the exemption; the one remaining "one runtime prerequisite" wording is in `README.md` and its two `scripts/hosts/*/README.md` copies (and their rendered `hosts/*/README.md`), which the following task "Record Git As Second README Prerequisite" owns.
- `uv run scripts/build_hosts.py --check` passes (no file under `core/` or `scripts/hosts/` changed).

---

## Record Git As Second README Prerequisite

Reword the "one runtime prerequisite" paragraph in `README.md` and its two host copies under `scripts/hosts/*/README.md` so git (a work tree at the project root) stands beside Python 3.9 as a second prerequisite that `/init-milestone-base-workflow` checks first, and rebuild `hosts/` so the rendered host READMEs match. Verified by the three sources agreeing and by `uv run scripts/build_hosts.py --check` passing with the rebuilt trees committed alongside.

**Verified:**

- `README.md`'s Installation paragraph no longer says "one runtime prerequisite"; it names two runtime prerequisites, **git** (the project root inside a git work tree that every skill commits into) and a **Python 3.9 or later** interpreter answering as `python3`, and says `/init-milestone-base-workflow` checks both once per project, git first, stopping with the remedy when either is missing.
- `scripts/hosts/claude/README.md` and `scripts/hosts/antigravity/README.md` carry the identical reworded paragraph, so the three sources agree; the literal `3.9` stays in each.
- `uv run scripts/build_hosts.py` rebuilt `hosts/claude/README.md` and `hosts/antigravity/README.md` with the same paragraph, and `uv run scripts/build_hosts.py --check` passed.
- A repository-wide grep (excluding `.git`, `milestones/`, and `CHANGELOG.md`) for "one runtime prerequisite" and "one prerequisite" finds nothing.

---
