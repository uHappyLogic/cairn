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
