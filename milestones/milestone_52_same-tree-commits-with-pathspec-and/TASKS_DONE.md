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
