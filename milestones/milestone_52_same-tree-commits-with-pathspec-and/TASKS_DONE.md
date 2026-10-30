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

## Route The Batch Calls Through The Tool

Replace the inlined guard, `git add`, and `git commit` in the three question-document batch calls — the answer sweep's batched call in both its question and conflict sections, the recommendation pass's batch call for its annotation and ordering commits, and the alternatives pass's batch call — with the commit tool's command, each call capturing the tool's stdout and echoing its own landed-commit marker only when that capture is empty, with their prose and reporting steps following. These calls are where a completion agent's staged files could ride into a question commit, which the pathspec now prevents. Verified by `tests/test_sweep_batched_call.py` passing against the changed call under both interpreters and the rebuilt host trees passing `--check`.

**Verified:**

- The answer sweep's batched call, in both its question section and its conflict section, replaces the inlined `git status` guard, `git add`, and `git commit -q` with `out="$(python3 {{PLUGIN_ROOT}}/tools/commit.py --subject "Recommendation-answer: <Short Title>" --body "$pick" -- <MILESTONE_DIR>/open_questions.xml <MILESTONE_DIR>/requirements.md)"` and echoes `answer commit landed` only when `out` is empty, a failure still falling through to `stopped at`; the call's opening stranded-fold guard is unchanged and the two sections still differ only in the `fold`/`replace` line and its placeholder.
- The recommendation pass's batch call commits `Recommendation-annotation: <milestone_id>` (still conditioned on a non-empty `body`, the lifted lines as `--body`) and `Question-ordering: <milestone_id>` (subject-only) through the commit tool over `<MILESTONE_DIR>/open_questions.xml`, each capturing stdout in `out` and echoing `annotation commit landed` / `ordering commit landed` only when `out` is empty; a failed annotation commit still ends the call before the sort.
- The alternatives pass's batch call commits each accepted question through the commit tool, subject-only under `Alternatives-annotation: $t` over `<MILESTONE_DIR>/open_questions.xml`, capturing the tool's whole print in `out` and printing a failure as the Short Title, a tab, `commit failed:`, and the tool's `Error:` line; it echoes no landed-commit marker, since its status line is read from the closing `list --without-alternatives` check.
- No `git add` or `git commit` remains in the three skills in any rendered host tree (`hosts/claude`, `hosts/antigravity`, `hosts/codex/plugins/cairn`), each holding `tools/commit.py` in its call.
- The prose and reporting steps follow: each skill's intro names the commit tool as its only committer, each call's paragraph describes the tool's guard, path-scoped stage, pathspec commit keeping another run's staged change out, retry, and the captured `out` (with `pick`/`err`/`body` and `out` named as quoted per-call values); the sweep's stop paragraph, printed-outcome list, and stopped-at report pair the Short Title with the failing tool's `Error:` line (no multi-line git message); the recommendation pass's "Any other line" names the commit tool's `Error:` line; the alternatives pass tells a refused file (`Error:` after the tab) from a failed commit (`commit failed:` after the tab).
- Run hands-on from the rendered Claude Code tree in a scratch repository under bash 5, bash 3.2, zsh, and sh, with another change staged: every alternatives, recommendation, ordering, and answer commit carried only its own milestone paths and the staged change stayed staged; a refused file and a refused block printed their lines; a no-block recommendation call with the document already sorted printed and committed nothing; a pre-commit hook refusal printed `commit failed: Error: git commit exited 1: …` in the alternatives call, stopped the recommendation call before the sort with the tool's `Error:` line, and stopped the sweep with `stopped at` and the tool's `Error:` line.
- `tests/test_sweep_batched_call.py` passes against the changed call under both interpreters (6 passed each), and the full suites pass (`uv run pytest`: 1093 passed; `uv run --no-project --python 3.9 --with pytest pytest`: 1089 passed, 1 skipped).
- `uv run scripts/build_hosts.py` rebuilt the three host trees and `uv run scripts/build_hosts.py --check` passes.

---

## Route The Task-File Writer Calls Through The Tool

Replace the inlined guard, `git add`, and `git commit` in the inline `complete-task` skill's, `submit-task`'s, and `derive-tasks`' fixed calls with the commit tool's command chained behind their task-list tool call, each capturing the tool's stdout and echoing its landed-commit marker only when that capture is empty, with their prose following. Each task-file commit then carries exactly its own paths and survives another run's lock. Verified by the three rendered calls running as shown against a scratch repository and the rebuilt host trees passing `--check`.

**Verified:**

- The inline `complete-task` skill's fixed call chains `task_list.py move` behind `&&` with `out="$(python3 {{PLUGIN_ROOT}}/tools/commit.py --subject "Task-completion: <Task Title>" -- <recorded path 1> <recorded path 2> <MILESTONE_DIR>/TASKS_TODO.md <MILESTONE_DIR>/TASKS_DONE.md)"` and echoes `completion commit landed` only when `out` is empty, its inlined `git status` guard, `git add`, and `git commit -q` gone.
- `submit-task`'s fixed call chains `task_list.py insert` behind `&&` with `out="$(python3 {{PLUGIN_ROOT}}/tools/commit.py --subject "Task-submission: <New Task Title>" -- <MILESTONE_DIR>/TASKS_TODO.md)"` and echoes `submission commit landed` only when `out` is empty, its inlined guard, `git add`, and `git commit` gone.
- `derive-tasks`' fixed call chains `task_list.py initialize` behind `&&` with `out="$(python3 {{PLUGIN_ROOT}}/tools/commit.py --subject "Task-derivation: <milestone_id>" -- <MILESTONE_DIR>/TASKS_TODO.md)"` and echoes `derivation commit landed` only when `out` is empty, its inlined guard, `git add`, and `git commit` gone.
- No `git status`, `git add`, or `git commit` command remains in the three skills in any rendered host tree (`hosts/claude`, `hosts/antigravity`, `hosts/codex/plugins/cairn`), each call holding `tools/commit.py`; the prose keeps only `never git add -A`.
- The prose follows: each skill names the shared commit procedure's one command, the commit tool, with its subject, no body, and its own paths written literally; describes the tool's guard, path-scoped stage, pathspec commit keeping another run's staged change out, and lock retry; names `out` as one quoted value captured from the tool's stdout; lists the call's outcomes with the task-list tool's `Error:` line told from the commit tool's (naming the failing git command, carrying git's message); keys each no-op line on the commit tool finding the paths unchanged; scopes `submit-task`'s and `derive-tasks`' refusal stops to the task-list tool's `Error:` line; every fixed console line unchanged.
- The three rendered Claude Code calls, extracted from `hosts/claude/` and run as shown against scratch repositories under bash 5.3, bash 3.2, zsh, and sh with another run's change staged and an untracked file present: every derivation, submission, and completion commit carried exactly its own paths and the staged change stayed staged; a repeated derivation printed and committed nothing; a duplicate-title list and an unknown anchor printed one task-list `Error:` line and committed nothing; a completion with `.git/index.lock` held for one second landed with only its own paths; a pre-commit hook refusal printed only the commit tool's `Error: git commit exited 1: …` line, no marker, and committed nothing.
- `uv run scripts/build_hosts.py` rebuilt the three host trees and `uv run scripts/build_hosts.py --check` passes; `uv run pytest` (1093 passed) and `uv run --no-project --python 3.9 --with pytest pytest` (1089 passed, 1 skipped) pass.

---

## Test The Lock Retry Through One Fixed Call

Add one test that extracts the inline `complete-task` skill's fixed call from the rendered Claude Code tree — the one fixed call the parallel test leaves unrun — and runs it in a `tmp_path` repository in two cases: holding `.git/index.lock` and releasing it within the retry window, asserting the commit landed with only its own paths; and creating the lock and never removing it, asserting the call ends within a time limit a little above the retry bound, passes on git's `Unable to create '…/.git/index.lock'` message, and lands no commit. This is the milestone's deterministic proof of the retry, which the parallel test is not relied on for and which no other fixed call is run against a lock for. Verified by the test passing under both interpreters on the conftest git fixtures.

**Verified:**

- `tests/test_completion_call_lock_retry.py` extracts the inline `complete-task` skill's fixed call from the rendered Claude Code tree as the one fence of `hosts/claude/skills/complete-task/SKILL.md` holding the task-list tool's `move` (asserting it runs the commit tool once), fills its milestone directory, task title, bar bullets, and recorded paths, and runs it under `bash -c` in a `tmp_path` repository built on the conftest `repo`, `environment`, and `git` fixtures, with another run's change staged and an untracked file present.
- Held lock released within the retry window: the test holds `.git/index.lock`, waits until git's own trace (`GIT_TRACE` to a file) records a second `git add`, proving the first met the lock and was repeated, then releases it; the call exits 0 printing only `completion commit landed`, and one `Task-completion: Build The Parser First` commit lands carrying exactly the edited and created paths plus the two task files, the other run's staged change still staged and the untracked file untouched.
- Lock never released: the call ends after at least the retry window and within a limit of the window plus 3 seconds (under one more window), exits non-zero with empty stdout and exactly one commit-tool `Error: git add …` line on stderr carrying git's `Unable to create '…/.git/index.lock': File exists.` message, after exactly `commit.ATTEMPTS` traced adds and no `git commit`; no commit lands (HEAD unchanged, one commit in history), nothing of the call is staged, and the landed move stays in the tree.
- With the rendered tool's retry disabled (`ATTEMPTS = 1`, restored afterwards), both run cases fail, so the test proves the retry rather than passing vacuously.
- The test passes under both interpreters: `uv run pytest` (1096 passed) and `uv run --no-project --python 3.9 --with pytest pytest` (1092 passed, 1 skipped), the new file's 3 tests passing in each.

---

## Extend The Resumption Rule To Live Work

Rewrite the opening of step 3 of `core/shared/complete-procedure.md` so uncommitted changes in the tree are named as either a previous run's partial work or another run's live work, with the runner continuing from what bears on its task and leaving the rest untouched in both cases. Several `complete-all-tasks` runs may now share one working tree, so the rule must cover work that is in progress rather than abandoned. Verified by the rebuilt host trees passing `--check` with both runners' files still pointing at the unchanged step.

**Verified:**

- The opening of step 3 of `core/shared/complete-procedure.md` names uncommitted changes in the tree as either a previous run's partial work or another run's live work (a run still in progress sharing the tree)
- In both cases the runner continues from whatever bears on its task (reading it, continuing from it, carrying its paths in the running list) rather than redoing or reverting it, and leaves the rest untouched with its paths kept out of the running list
- Step numbering and headings are unchanged (steps 1-5, `### 3. Carry out the task`), and the runner files (`core/agents/complete-task.md`, `core/skills/complete-task/SKILL.md`) are unedited and still point at the procedure and its step 5
- `uv run scripts/build_hosts.py` rebuilt the three host trees and `uv run scripts/build_hosts.py --check` passes, with only the four `complete-procedure.md` copies changed

---

## Completion Agent Writes Its Path File

Change `core/agents/complete-task.md` so it takes a third prompt line, `Scratch directory: <scratch dir>`, stages nothing, and runs step 5 as one fixed shell call chaining the task-list tool's `move` with the write of the task's whole change set — the recorded created and edited paths plus `<MILESTONE_DIR>/TASKS_TODO.md` and `<MILESTONE_DIR>/TASKS_DONE.md`, one path per line — to a file of one fixed name per run inside that scratch directory, behind the move's `&&`, with its return protocol reworded to match. The orchestrator commits each task from that file, so the agent's return becomes a file as the alternatives agent's already is. Verified by `agy_tests/test_subagent_write_tools.py` updated to the three-line prompt and to the landed path file as its pass signal, and the rebuilt host trees passing `--check`.

**Verified:**

- `core/agents/complete-task.md` takes three prompt lines (the task name, `Milestone directory: <MILESTONE_DIR>`, and `Scratch directory: <scratch dir>`), its frontmatter description naming the scratch directory within the 25-word cap
- Its step 5 is one fixed shell call: the procedure's `move` with its quoted bar heredoc, then `&&` and `cat > "<scratch dir>/paths.txt"` with a quoted heredoc holding the recorded created and edited paths plus `<MILESTONE_DIR>/TASKS_TODO.md` and `<MILESTONE_DIR>/TASKS_DONE.md`, one path per line, under one fixed name per run taken from no task title
- The agent stages and commits nothing: its staging contract is replaced by a path-file contract with no `git add` or `git commit`, and its return protocol says `DONE` means the change set was written to the path file (no payload above it) and a `FAILED` writes no path file, stages and commits nothing, and keeps the resumable-tree promise
- The rendered call, run verbatim against the agy fixture milestone under bash and zsh, writes the path file and stages nothing; the commit tool's `--path-file` then commits exactly those three paths with another staged path left staged; a refused move writes no path file
- `agy_tests/test_subagent_write_tools.py` dispatches the agent with the three-line prompt and takes the landed `<scratch dir>/paths.txt` (exactly the deliverable and both task files, nothing else in the scratch directory, nothing staged or committed) as its pass signal; it compiles under 3.13 and 3.9 and passes in a simulated dispatch running the rendered Antigravity call, failing when the deliverable is left out (the live agy run was not made, since the installed copy differs from the built tree and replacing it is the user's act)
- `uv run scripts/build_hosts.py --check` passes with the three rebuilt host agent files, and both pytest runs pass (1096 passed; 1092 passed, 1 skipped)

---

## Orchestrator Commits Each Task From The Path File

Change `core/skills/complete-all-tasks/SKILL.md` and the three hosts' `COMPLETE_TASK_DISPATCH` slot values so the run creates its scratch directory once with `mktemp -d`, passes it on every dispatch as the fixed `Scratch directory:` prompt line, and replaces step 2c's whole-index guard and commit with one fixed call that commits through the commit tool with the agent's path file as its only pathspec and then moves that file into a `processed` subdirectory of the scratch directory under a name the call makes unique, deleting nothing; an absent or empty file after a `DONE` commits nothing, ends the run on a new fixed identifier-free stop line with the task name and whether the file was absent or empty below it, and the `Task run committed nothing — no task staged a change.` condition, its line, and its table row are retired so a run whose tasks all returned `DONE` always ends on `All tasks completed.`. Verified by the new stop line's row in `docs/skill-reference.md`'s fixed-lines table and the retired row gone with `tests/test_fixed_console_lines.py` passing, the rebuilt host trees passing `--check`, and the on-demand agy suite run for the Antigravity slot change.

**Verified:**

- `core/skills/complete-all-tasks/SKILL.md` step 2 runs `mktemp -d` once before the first dispatch, holds the path as `<scratch dir>`, written out in full in every later command, and deletes nothing in it.
- Every dispatch prompt carries the fixed third line `Scratch directory: <scratch dir>`, and the three hosts' `COMPLETE_TASK_DISPATCH` slot values name the task name, the milestone directory, and the scratch directory and nothing else.
- Step 2c is one fixed call that commits through the commit tool with `--path-file "<scratch dir>/paths.txt"` as its only pathspec under `Task-completion: <TASK_NAME>`, names no path itself, runs no git command of its own, and then moves the file into `<scratch dir>/processed/` under a `mktemp`-unique name, deleting nothing.
- An absent or empty path file after a `DONE` commits nothing and ends the run on the new fixed identifier-free stop line `Task run stopped — a completed task could not be committed.`, with the task name and `path file absent` or `path file empty` below it, leaving the tree as the agent left it.
- The `Task run committed nothing — no task staged a change.` condition, line, and table row are gone from `core/`, `hosts/`, `docs/`, `scripts/`, and `tests/`, and step 3 ends a run whose tasks all returned `DONE` on `All tasks completed.`.
- `docs/skill-reference.md`'s fixed-lines table carries the new stop row and no retired row, and `uv run pytest tests/test_fixed_console_lines.py` passes (165 passed).
- The rendered Claude Code call run in a scratch repository commits only the path file's paths while another staged change stays staged, prints nothing on a no-op, prints `path file absent` and `path file empty` in those cases, and leaves the fixed name absent after each read.
- `uv run scripts/build_hosts.py --check` passes, `uv run pytest` passes (1096 passed), and the 3.9 floor run passes (1092 passed, 1 skipped).
- `uv run pytest agy_tests` passes (3 passed) against the built `hosts/antigravity/` tree installed at `~/.gemini/config/plugins/cairn`.

---

## Add The Parallel Two-Milestone Completion Test

Add one test that extracts the completion agent's step-5 fixed call and the orchestrator's commit-from-file call from the rendered Claude Code tree and, for each of two fixture milestones seeded into one `tmp_path` repository through the conftest factory, makes the task's edits, runs the agent's call with that milestone's recorded paths substituted, then runs the orchestrator's call on the path file it left behind, running the two milestones' agent-then-orchestrator sequences concurrently and asserting each `Task-completion:` commit carries only its own paths; it writes no path file of its own and runs no inline `complete-task` call. It is the milestone's one simple proof that two runs can share a tree without one's files riding into the other's commit. Verified by the test passing under both interpreters.

**Verified:**

- `tests/test_parallel_completion.py` extracts the completion agent's step-5 fixed call (the one fence of `hosts/claude/agents/complete-task.md` holding the move, which chains it with the path-file write) and the orchestrator's commit-from-file call (the one fence of `hosts/claude/skills/complete-all-tasks/SKILL.md` running the commit tool) from the rendered Claude Code tree
- Two fixture milestones, `tests/fixtures/parallel_first/` and `tests/fixtures/parallel_second/`, are seeded into one `tmp_path` repository through the conftest `repo` factory
- For each milestone the test makes the task's edits, runs the agent's call with that milestone's recorded paths substituted, then runs the orchestrator's call on the path file the agent's call left behind, the two milestones' agent-then-orchestrator sequences running concurrently in two threads
- Each `Task-completion:` commit is asserted to carry exactly its own paths: its edited and created files and its milestone's two task files
- The test writes no path file of its own and runs no inline `complete-task` call
- The test passes under `uv run pytest` (pinned 3.13) and `uv run --no-project --python 3.9 --with pytest pytest`, the whole suite passing in both runs

---

## Update The Committing Invariants In CLAUDE.md

Revise the CLAUDE.md invariants to the mechanism as it now stands: the committing invariant places the commit mechanics in the commit tool rather than in `commit-procedure.md` and describes the orchestrator's commit-from-file in place of the index its agent staged, the rule that a tool touches no git is scoped to the document writers, the shell-literal invariant's sentence setting a commit tool aside is reworded, the return-contract and dispatch-prompt invariants record the completion agent's path file and the scratch directory passed on every dispatch, and the `tests/` layout line names the moved git fixtures and the two new tests. The invariants are where the rationale for these decisions lives, so a later editor must not restore the staging contract or the whole-index commit. Verified by reading each named invariant against the runtime files and tests it describes.

**Verified:**

- CLAUDE.md's committing invariant places the commit mechanics in `core/tools/commit.py` (guard, path-scoped `git add`, `git commit` with the paths as pathspec, the exit-128-only bounded retry, the exit-0 no-op line, the `out`-gated markers) with `core/shared/commit-procedure.md` reduced to the tool's one command, matching both files, and gives the rationale (the 2026-10-28 leak, the lock retry, why a tool) from the milestone's recorded answers
- The committing invariant describes `complete-all-tasks` committing each `DONE` task through the commit tool with `--path-file "<scratch dir>/paths.txt"` as its only pathspec, the absent/empty stop, the silent no-op skip, and the retired `Task run committed nothing` line, and states that neither the agent's staging contract nor the whole-index commit with its `git diff --cached --quiet` guard may be restored, matching `core/skills/complete-all-tasks/SKILL.md`
- The rule that a tool touches no git is scoped to the document writers (open-question, task-list, fold, milestone-definition tools) in the committing invariant, the task-list and fold tool invariants say "like every/the other document writer(s)", and the commit tool is named the one tool that runs git, matching the docstrings of `core/tools/commit.py`, `task_list.py`, and `requirements.py`
- The shell-literal invariant's commit-tool sentence is reworded (the rule stays prose because the commit tool, added for the pathspec, retry, and path-file read, is still invoked through a runner-written command line), and its git-specific statements now name the commit-tool command lines, the agent's path-file sentence, the captured `out`, and the orchestrator's commit-from-file call, matching the rendered fixed calls
- The return-contract invariant records the completion agent's path file (its contents, the fixed per-run name taken from no title, the move into `processed` under a `mktemp`-unique name, no write on `FAILED`), and the dispatch-prompt invariant records `complete-all-tasks` passing the heading, the milestone directory, and the scratch directory, with the `Scratch directory: <scratch dir>` line on every dispatch at both sites, matching `core/agents/complete-task.md`, both orchestrators' prompt fences, and the three `COMPLETE_TASK_DISPATCH` slot values
- The `tests/` layout line names the git-repository fixtures moved into `tests/conftest.py` (`environment`, `git`, `run_call`, the `repo` factory, beside `run_commit`) and the two new tests `test_completion_call_lock_retry.py` and `test_parallel_completion.py`, matching the tests directory
- No CLAUDE.md sentence still says an agent stages its change set or that an orchestrator commits the index its agent staged, other than as retired and not to be restored; `uv run scripts/build_hosts.py --check` passes and `uv run pytest` passes (1098 passed)

---

## Update The Docs For Same-Tree Commits

Update `docs/workflow.md`'s `## How skills commit`, the `complete-all-tasks` and `complete-task` entries of `docs/skill-reference.md`, `docs/design-claims.md`, and `docs/ways-of-using-cairn.md` to record the pathspec, the retry, and the commit-from-file mechanism, rewording design claim 12 from a clean tree after each skill to per-commit hygiene while claim 9 stays as written, and stating that the existing "Preparing the next milestone while the current one runs" chain no longer leaks a completion agent's files into the answer sweep's or an annotating pass's commit, with two `complete-all-tasks` runs sharing one tree left unstated and no new chain added. The docs cover only the same-tree concurrency they already describe. Verified by no doc still saying an agent stages or an orchestrator commits the staged index, and `tests/test_fixed_console_lines.py` passing.

**Verified:**

- `docs/workflow.md`'s `## How skills commit` records the pathspec (every skill-layer commit staged path-scoped and committed with its own paths as the commit's pathspec, so another run's staged or uncommitted changes stay out), the commit-from-file mechanism (`/complete-all-tasks` creating one `mktemp -d` scratch directory passed on every dispatch, each subagent writing its whole change set to one fixed-name path file and staging nothing, the orchestrator committing each task with that file as its only pathspec and moving it into `processed` under a unique name, an absent or empty file stopping the run resumably), and the retry (the commit tool, `tools/commit.py`, as the one home of the mechanics behind `commit-procedure.md`'s one command, repeating a git write only on exit 128, up to 16 attempts a quarter of a second apart, any other failure passed on at once); the task-derivation-and-completion phase paragraph no longer says the subagent stages
- `docs/skill-reference.md`'s `complete-all-tasks` entry records the scratch directory, the subagent's `<scratch dir>/paths.txt` path file with no staging, the orchestrator's one-call commit from that file through the commit tool with the paths as pathspec and the lock retry, the move into `processed`, and the absent/empty stop; its `complete-task` entry records the commit through the commit tool with the paths as pathspec and the lock retry; the batch-skill entries' stale "commit procedure's three steps itself", "git's message", and "git's success output silenced" wording now names the commit tool
- `docs/design-claims.md` claim 12 is reworded from a clean tree after each skill to per-commit hygiene (each commit records only its own paths through the commit tool's pathspec, the task subagent's path file, the lock retry), its metric counting commits with a path outside their own change set in place of dirty trees, with the intro's count of suite-run tests updated to match; claim 9 is unchanged
- `docs/ways-of-using-cairn.md`'s "Preparing the next milestone while the current one runs" paragraph states that the chain can run beside the current milestone's `complete-all-tasks` and that a completion subagent's files no longer ride into an annotating pass's commit or the answer sweep's, with no chain line added and two `complete-all-tasks` runs sharing one tree left unstated
- No file under `docs/`, nor `README.md` or `CONTRIBUTING.md`, still says an agent stages its change set or an orchestrator commits the staged index (checked by search for staging and index wording)
- `tests/test_fixed_console_lines.py` passes under both interpreters (165 passed each); `uv run pytest` passes (1098 passed) and `uv run scripts/build_hosts.py --check` passes

---
