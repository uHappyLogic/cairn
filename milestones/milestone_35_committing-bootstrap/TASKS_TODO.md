# TASKS TODO

## Commit Bootstrap Scaffold Through Shared Procedure

Retire the "It does not commit — staging is left to the user" exemption in `core/skills/init-milestone-base-workflow/SKILL.md` by adding a commit step after the `CLAUDE.md` step that follows `{{PLUGIN_ROOT}}/shared/commit-procedure.md` with PATHS of `milestones/README.md` always plus `CLAUDE.md` only on runs where the skill created or appended to it (keyed on the edit being made, never by diffing), the constant subject-only SUBJECT `Workflow-bootstrap: milestones` and no BODY, handing the paths over unchanged so uncommitted changes already present in them are swept into the commit with no pre-write status probe, stop, confirmation, hunk-level staging, or advisory. This closes the milestone's goal that every file-changing skill commits its own paths. Verified by reading the rendered skill against `define-milestone-goal` step 5 and `finish-current-milestone` step 8 for shape, and by `uv run scripts/build_hosts.py --check` passing with the rebuilt `hosts/` trees committed alongside.

---

## Replace Bootstrap Report With Terse Lines

Replace the multi-line confirmation in `core/skills/init-milestone-base-workflow/SKILL.md` with the reporting shape the other setup skills use: on success exactly one fixed identifier-free status line, `Workflow bootstrapped.`, and on the already-initialized stop one distinct no-op line, cutting the created-versus-preserved itemization, the pointer-initialized line, the numbered next steps, and the suggestion to run `/init` (including the one in the `CLAUDE.md` step), so the skill prints no next-step or handoff pointer. The commit diff now shows which files were created or appended to, which is why the itemization goes. Verified by reading the rendered skill and by `uv run scripts/build_hosts.py --check` passing with the rebuilt `hosts/` trees committed alongside.

---

## Update Invariant And Docs For Committing Bootstrap

Update every statement in `CLAUDE.md`, `docs/workflow.md`, `docs/design-claims.md`, and `docs/skill-reference.md` that the bootstrap does not commit or that Python is the workflow's one runtime prerequisite: the pipeline tag "non-committing" and the "one non-committing exemption" clause of the committing invariant, the exemption paragraph and the "one runtime prerequisite" wording in `docs/workflow.md`, design claim 12's "two exceptions" sentence (which drops to the one failed-run exception), and the skill-reference entry, so each now records git as a second prerequisite checked first, the `Workflow-bootstrap: milestones` commit, and the terse report. The criterion is the decision, not a hand list, so grep for further statements rather than stopping at the sites named. Verified by a repository-wide grep finding no remaining claim, outside the historical `CHANGELOG.md` entries and `milestones/`, that the bootstrap leaves files uncommitted or staged or that Python is the one prerequisite.

---

## Record Git As Second README Prerequisite

Reword the "one runtime prerequisite" paragraph in `README.md` and its two host copies under `scripts/hosts/*/README.md` so git (a work tree at the project root) stands beside Python 3.9 as a second prerequisite that `/init-milestone-base-workflow` checks first, and rebuild `hosts/` so the rendered host READMEs match. Verified by the three sources agreeing and by `uv run scripts/build_hosts.py --check` passing with the rebuilt trees committed alongside.

---

## Add Project-Setup Chain To Headless Page

Add to `docs/ways-of-using-cairn.md` a project-setup section placed before "Starting a milestone" whose fenced block runs the bootstrap line and a `define-milestone-goal "<goal>"` line from a fresh git repository and hands off to the existing "Starting a milestone" chain, naming `git init` and `/init` in prose as preconditions rather than chain lines, and add the `<goal>` placeholder to the page's notation legend. This is the chain the committing bootstrap makes possible, since the page's premise is that every skill commits what it changes. Verified by reading the page: the section precedes "Starting a milestone", its lines follow the legend's notation, and the legend lists three placeholders.

---
