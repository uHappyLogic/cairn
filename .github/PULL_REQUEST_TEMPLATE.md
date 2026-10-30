Milestone: `milestone_<N>_<slug>` <!-- the reserved id: the directory name the maintainer's `Milestone-definition:` commit created on `main` -->
Closes #<proposal issue>

## Finished-milestone checklist

The reviewer confirms the branch carries what a finished contributor milestone leaves in the tree — the one check CI does not make.

- [ ] `milestones/<id>/requirements.md` carries no `<open-question>` block.
- [ ] `milestones/<id>/TASKS_TODO.md` carries no task section.
- [ ] `milestones/README.md` carries the milestone's history entry, and its `Current milestone:` line reads `none`.
- [ ] The branch carries one `Task-completion: <task heading>` commit per completed task, each with the task's verified `- ` bullets as its body (`python3 core/tools/milestones.py tasks milestones/<id> --with-body` lists them).
- [ ] The branch carries one `Milestone-finish: <id>` commit.
- [ ] `CLAUDE.md` is touched only for lasting changes.
- [ ] `hosts/` is rebuilt — the `drift-gate` status check passes on this pull request.
