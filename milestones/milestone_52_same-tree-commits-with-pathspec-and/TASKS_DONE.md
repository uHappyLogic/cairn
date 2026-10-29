# TASKS DONE

## Move Git Test Helpers Into Conftest

Move the `environment`, `repo`, `git`, and `run_call` helpers of `tests/test_sweep_batched_call.py` into `tests/conftest.py` — `environment` as a fixture, `git` and `run_call` as module-level helpers or fixtures returning them, and `repo` generalized into a factory fixture taking which fixture milestones to seed, on the pattern of the existing `milestone_dir` and `task_list_dir` factories — keeping the sweep-specific seeding in the sweep test, rewriting that test to use them, and leaving `test_sweep_compact_view.py` untouched. The commit tool's tests, the lock retry test, and the parallel test that follow all build git repositories on these fixtures, so they need one home before the first of them is written. Verified by both pytest runs passing with the batched-call test's assertions unchanged.

**Verified:**

- `tests/conftest.py` defines the `environment` fixture moved from the sweep test: the Claude Code tree's plugin-root variable exported to `hosts/claude`, a `python3` wrapper for the suite's interpreter on `PATH`, `PYTHONDONTWRITEBYTECODE`, and git isolated (`GIT_CONFIG_NOSYSTEM`, `/dev/null` global config, own `HOME`) with a fixed author and committer identity.
- `tests/conftest.py` holds `git` and `run_call` as the module-level helpers `run_git` and `run_bash`, with fixtures `git` and `run_call` returning them, keeping the moved signatures and behaviour.
- `tests/conftest.py` holds a `repo` factory fixture, on the pattern of `milestone_dir` and `task_list_dir`, taking a mapping of destination paths to the fixture milestones to seed plus optional extra files, and making one `Initial commit` holding them.
- `tests/test_sweep_batched_call.py` defines none of `environment`, `repo`, `git`, or `run_call`; its own `repo` fixture overrides the conftest factory with only the sweep-specific seeding (the golden `sweep` milestone at its milestone path and the unrelated tracked `README.md`), and every test assertion is unchanged.
- `tests/test_sweep_compact_view.py` is untouched.
- `uv run pytest` passes (1056 passed) and `uv run --no-project --python 3.9 --with pytest pytest` passes (1052 passed, 1 skipped), all six batched-call tests passing in both.

---

## Add The Commit Tool And Its Tests

Add the new stdlib-only, self-contained commit tool under `core/tools/` that the `## Decisions` entries Commit tool and Path file specify: given paths (as arguments, or read line-exact from a path file, one per line, an empty list refused), a subject, and an optional body, it runs the dirty-own-path guard, the path-scoped `git add`, and `git commit` with the paths as its pathspec, repeating a git write only when git exits with 128 — about ten to twenty times with a fixed pause of a quarter to half a second between attempts, a fractional sleep inside the tool, one constant schedule with no override — passing exit 1 on at once, exiting 0 with its fixed no-op line on stdout when nothing changed, printing nothing when a commit lands, and keeping exit 1 with one `Error:` line on stderr for refusals and a git failure after the last retry. Every skill-layer commit in this milestone runs through it, so it lands before any caller changes. Verified by its subprocess contract and parity tests on the conftest git fixtures under both interpreters, its line in CLAUDE.md's repository layout, and a rebuilt `hosts/` tree passing `--check`.

**Verified:**

- `core/tools/commit.py` exists as a stdlib-only (argparse, os, subprocess, sys, time) self-contained tool importing no sibling and no importlib (`tests/test_commit_parity.py`), holding no `{{` and naming no host, and the rebuild renders it byte-identical into `hosts/claude/tools/`, `hosts/antigravity/tools/`, and `hosts/codex/plugins/cairn/tools/` (`cmp` against `core/tools/commit.py`).
- It takes `--subject SUBJECT`, an optional `--body BODY` (an empty or whitespace-only body makes a subject-only commit), and the paths either as `PATH` arguments or through `--path-file FILE`, read line-exact (split at newlines only, each line taken whole, a line holding nothing skipped, the last line needing no newline); an empty path list, an empty path argument, an empty or multi-line subject, and a missing, non-UTF-8, or path-less path file are refused with exit 1 and one `Error:` line before any git command runs, and paths given both ways is argparse's exit 2 (`tests/test_commit_contract.py`).
- It runs the dirty-own-path guard `git status --porcelain -- PATH...` (optional locks off, never repeated), the path-scoped `git add -- PATH...`, and `git commit -m SUBJECT [-m BODY] -- PATH...` with the paths as its pathspec, every path read literally: the commit carries only the named paths while another staged change stays staged, other edits and untracked files stay in the tree, new, modified, and deleted paths are recorded, paths resolve relative to the working directory, and a glob character names one file only (`tests/test_commit_pathspec.py`).
- A git write repeats only when git exits 128, on one constant schedule of 16 attempts (15 repeats) with a fixed 0.25-second `time.sleep` between two, a window of 3.75 seconds, with no option to override it: a lock released within the window lets the commit land with only its own paths, a lock never released ends after exactly 16 `git add` attempts within the window plus margin with git's `Unable to create '…/.git/index.lock'` message folded into one `Error:` line and no commit, the commit write is repeated on 128 too, and a pre-commit hook's exit 1 is passed on at once after one attempt (`tests/test_commit_retry.py`, logging the real attempts through a git wrapper).
- A no-op exits 0 printing exactly `Nothing committed — none of the paths changed.` on stdout with nothing staged or committed, a landed commit prints nothing, and refusals and git failures (a non-repository, git missing from PATH, a refused commit) are exit 1 with exactly one `Error:` line on stderr and no traceback (`tests/test_commit_contract.py`).
- The tests build their repositories on the conftest git fixtures (`repo`, `environment`, `git`, plus the new `run_commit` fixture and `COMMIT_TOOL` constant in `tests/conftest.py`), and `uv run pytest` passes (1093 passed) and `uv run --no-project --python 3.9 --with pytest pytest` passes (1089 passed, 1 skipped).
- CLAUDE.md's repository layout carries a `core/tools/commit.py` line describing the commit tool and its contract.
- `uv run scripts/build_hosts.py --check` passes after the rebuild.

---

## Reduce The Commit Procedure To The Tool

Rewrite `core/shared/commit-procedure.md` so its three steps become the commit tool's one fixed command over PATHS, SUBJECT, and BODY, and update the eleven skills that follow it by reference so each runs that command as its one git tool call and reads the tool's printed line directly to choose its no-op line. This moves the commit mechanics into the tool for every skill that never inlined them. Verified by the procedure showing the one command, each of the eleven skills reading the tool's line for its no-op, and the rebuilt host trees passing `--check`.

**Verified:**

- `core/shared/commit-procedure.md` keeps its PATHS, SUBJECT, and optional BODY inputs and reduces its procedure to the one commit-tool command `python3 {{PLUGIN_ROOT}}/tools/commit.py --subject "<SUBJECT>" --body "<BODY>" -- <PATHS>` (the `--body` left out for a subject-only commit), run as the step's one git tool call with every path its own argument after `--` and none held in a shell variable, and no git command of the runner's own beside it (no status check, no `git add`, no `git commit`, no `--allow-empty`).
- The procedure states the tool's three outcomes as the caller reads them: nothing printed is a landed commit, exactly `Nothing committed — none of the paths changed.` on stdout is the no-op from which the caller chooses its own no-op line, and one `Error:` line on stderr is a failure with nothing committed, passed on to the caller.
- Each of the eleven skills that follow the procedure by reference (`answer-open-question`, `answer-open-question-with-alternative`, `answer-open-question-with-recommendation`, `capture-milestone-principle-updates`, `define-milestone-goal`, `finish-current-milestone`, `goto-next-milestone`, `init-milestone-base-workflow`, `modify-milestone-goal`, `review-milestone-requirements`, `specify-milestone-starting-state`) runs the procedure's one commit-tool command as its step's one git tool call, no longer says "carrying out its steps yourself" or that the procedure owns the guard, and keys its no-op line on the commit tool printing `Nothing committed — none of the paths changed.`; capture maps that line after an accepted rewrite to its existing `the store already holds what the milestone teaches` line and keeps its rejection path off the tool entirely.
- `uv run scripts/build_hosts.py` rebuilt the three host trees and `uv run scripts/build_hosts.py --check` passes; `uv run pytest` (1093 passed) and `uv run --no-project --python 3.9 --with pytest pytest` (1089 passed, 1 skipped) pass.

---
