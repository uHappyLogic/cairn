# Check the Scope Gate (shared snippet)

This is the single source of truth for the scope gate, the check that lets only one started
milestone at a time take task work in a scope. Its one input is the resolved
`<MILESTONE_DIR>`. Every runner that enters a task into a milestone's list or completes one
runs it as a step of its own, before its work, at the point its own file names. The check
changes nothing.

## What a held scope means

A milestone's scope is the directory holding its `milestones/` container. A milestone is
started when it is live — its directory still stands in the working tree — and tasks were
entered into its task list at some time, which the log shows as its `TASKS_TODO.md` changed
after the commit that defined it. It stays started until `/finish-milestone` removes its
directory, also after every one of its tasks is completed. A milestone that is only defined,
or that is still deciding its questions, is not started.

Another started milestone **holds** this milestone's scope when its scope is the same
directory, a directory that contains this one, or a directory under this one. Milestones in
disjoint scopes never hold each other's. While another milestone holds the scope, no task of
this milestone enters its list and none is completed: the run waits until every holder is
finished.

## Running the gate

Run, from the workspace root, the plugin's milestones tool:

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/milestones.py gate <MILESTONE_DIR>
```

It prints the path of every milestone holding the scope, one per line, and nothing when none
does, exiting 0 either way; when it cannot check — a shallow clone, whose truncated log can
read a started milestone as unstarted, or a path with no `milestones/` container — it prints
one `Error: <reason>` line on stderr instead, with a non-zero exit.

- **The call printed nothing, on either stream, and exited 0** — the scope is free: go on to
  the runner's next step.
- **Anything else** — **stop without changing anything**. Report the fixed line
  `Scope gate closed — the scope is held or could not be checked.` first, then below it the
  paths the call printed, verbatim, or, when the call failed, its one `Error: <reason>` line
  from stderr. Those lines are the whole report: the run can be repeated once every holder is
  finished, or once the cause the `Error:` line names is fixed.
