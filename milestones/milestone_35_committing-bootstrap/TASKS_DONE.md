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
