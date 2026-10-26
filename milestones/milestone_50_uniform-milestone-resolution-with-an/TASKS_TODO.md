# TASKS TODO

## Forward Milestone Directory To Completion Agent

`complete-all-tasks` passes the `<MILESTONE_DIR>` its step 0 resolved on every dispatch as a fixed `Milestone directory: <MILESTONE_DIR>` line in its prompt fence beside the task-name line, following the alternatives pass's fence; `core/agents/complete-task.md` documents that line as a prompt value the agent uses as given with no resolution of its own; `core/shared/complete-procedure.md` step 1 takes a supplied directory as given and runs the shared pointer procedure only when none is supplied, the inline `complete-task` skill's case; and the three hosts' `COMPLETE_TASK_DISPATCH` slot values stop saying the prompt "contains only the task name". This keeps both dispatch sites on one unconditional prompt shape so no agent can diverge from the directory the orchestrator commits for. Verified by reading the rendered fence, agent file, and procedure in each host tree and by `uv run scripts/build_hosts.py --check` passing after the `hosts/` rebuild.

---

## Spell The Flag In The Docs

In `docs/skill-reference.md`, each of the sixteen pointer-resolving skills' `###` headings spells `[--milestone <milestone_id>]` exactly as that skill's Usage fence does, the `specify-milestone-starting-state <milestone_id>` heading taking the optional form in place of the required id and the `capture-milestone-principle-updates <milestone_id>` heading staying as it is. In `docs/ways-of-using-cairn.md`, the Starting-a-milestone chain runs `/cairn:specify-milestone-starting-state` with no argument, `<milestone_id>` leaves the notation paragraph's placeholder list (five placeholders become four), the Setting-up chain's closing clause "with `<milestone_id>` the directory `define-milestone-goal` created" is dropped, and the page says nothing about the `--milestone` flag. Verified by a grep for `<milestone_id>` over `docs/ways-of-using-cairn.md` printing nothing and by each updated heading matching its skill's rendered Usage fence.

---

## Record Milestone Resolution In CLAUDE.md

`CLAUDE.md` gains one invariant recording the uniform resolution rule: every milestone-operating skill resolves through the shared pointer procedure by default or through one optional leading `--milestone <milestone_id>` override naming the exact directory, validated by the existence of its `requirements.md` with no fallback to the pointer and honoured when the pointer reads `none`, the flag-parsing rule stated once in the procedure with one clause at each positional-text skill's parse point, and `capture-milestone-principle-updates` the stated exception keeping its required positional id. In the same edit, the `finish-current-milestone` invariant is narrowed to say the pointer clear happens exactly when the pointer names the finished milestone, and the dispatch-prompt invariant names the milestone directory beside the task heading as `complete-all-tasks`' whole prompt. Verified by reading the three passages against the finished skills, procedure, and agent file.

---
