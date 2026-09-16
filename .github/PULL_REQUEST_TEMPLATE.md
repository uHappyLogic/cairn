Milestone: `milestone_<N>_<slug>` <!-- the reserved id: the directory name the maintainer's `Milestone-definition:` commit created on `main` -->
Closes #<proposal issue>

## Finished-milestone checklist

The reviewer confirms the branch carries what a finished contributor milestone leaves in the tree — the one check CI does not make.

- [ ] `milestones/<id>/requirements.md` carries no `<open-question>` block.
- [ ] `milestones/<id>/TASKS_TODO.md` carries no task section.
- [ ] `milestones/<id>/TASKS_DONE.md` carries every task, each with its `**Verified:**` bullets.
- [ ] `milestones/README.md` carries the milestone's history entry, and its `Current milestone:` line reads `none`.
- [ ] The branch carries one `Milestone-finish: <id>` commit.
- [ ] `CLAUDE.md` is touched only for lasting changes.
- [ ] `hosts/` is rebuilt — the `drift-gate` status check passes on this pull request.
