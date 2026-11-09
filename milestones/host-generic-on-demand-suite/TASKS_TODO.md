# TASKS TODO

## Stop Counting Subagent Status Checks As Dispatches

On Antigravity the alternatives-agent dispatch test failed intermittently (2 passed and 1 failed under `uv run pytest host_tests --host antigravity` in the release pre-flight task's verification, after a 3-passed run in the task before it), because Antigravity's entry in `host_tests/conftest.py` counts a `manage_subagents` call as a dispatch, so a dispatching session that checks on or waits for the subagent it started is read as making a second dispatch, where the starting suite counted the dispatch tests' dispatches from `subagent` steps only. Make the entry count only a call that starts a subagent as a dispatch and a status, wait, or listing call on an already-started subagent as none, keeping every record assertion and adding no host-specific branch to the tests. It is verified by the parser yielding one dispatch on a recorded run that holds a `manage_subagents` call, and by `uv run pytest host_tests --host antigravity` passing all three tests.

---
