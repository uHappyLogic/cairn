# TASKS TODO

## Add Override Input To Pointer Procedure

`core/shared/get-current-milestone.md` gains its one input, an optional leading `--milestone <milestone_id>` in the skill's invocation text: it states once the rule for recognizing the flag and separating it from the skill's own positional text, takes the value verbatim as the exact milestone directory name under `milestones/` (no bare-number resolution, no stripped `milestones/` prefix or trailing slash) to form `milestones/<milestone_id>/`, and resolves an override without reading the pointer, so it is honoured even when the pointer reads `none`. When `milestones/<milestone_id>/requirements.md` does not exist the procedure stops with no fallback to the pointer, on an error line naming the given value followed by a list of every `milestone_*` directory under `milestones/` and no pointer to `/define-milestone-goal`; with no override the pointer's path stays unchecked and is handed on exactly as today. Verified by reading the rendered procedure in each host tree and by `uv run scripts/build_hosts.py --check` passing after the `hosts/` rebuild.

---

## Uniform Resolution In Specify Starting State

`specify-milestone-starting-state` loses its required positional `<milestone_id>`: its Usage fence becomes `/specify-milestone-starting-state [--milestone <milestone_id>]` with the prose and example under it describing the optional override, and its step 1 follows the shared pointer procedure to resolve `<MILESTONE_DIR>` like the other pointer-resolving skills, dropping its own "milestone not found" stop and `/define-milestone-goal` pointer, with its commit PATHS and `Starting-state: <milestone_id>` subject taking the id from the last path component of the resolved directory. This brings the skill under the uniform resolution rule so the Starting-a-milestone chain resolves the milestone `goto-next-milestone` just activated, while `capture-milestone-principle-updates` stays untouched with its required positional id. Verified by reading the rendered skill in each host tree and by `uv run scripts/build_hosts.py --check` passing after the `hosts/` rebuild.

---

## Flag Clause In Positional-Text Skills

The nine skills whose invocation carries positional text of their own (`answer-open-question`, `answer-open-question-with-recommendation`, `answer-open-question-with-alternative`, `ask-in-milestone-context`, `discuss-new-task`, `discuss-open-question`, `modify-milestone-goal`, `submit-task`, `complete-task`) each show `[--milestone <milestone_id>]` ahead of their positional text in their Usage or Invocation fence, with the prose under it describing the optional override, and each carries one clause at its own parse point (its parse step, or its step 0 where it has none) telling the runner to strip a leading `--milestone` value by the shared procedure before reading the rest, so the flag is never folded into a Short Title, an answer, a goal, a task name, or a question. `ask-in-milestone-context`'s `none`-pointer fallback is worded to apply only when no override is given, since an override never reads the pointer. Verified by reading the nine rendered skills in each host tree and by `uv run scripts/build_hosts.py --check` passing after the `hosts/` rebuild.

---

## Flag In Argument-Free Skill Usage

The seven pointer-resolving skills that take no positional text (`answer-all-open-questions-with-recommendation`, `complete-all-tasks`, `derive-tasks`, `finish-current-milestone`, `provide-alternatives-to-all-open-questions`, `recommend-all-open-questions`, `review-milestone-requirements`) each show `[--milestone <milestone_id>]` in their Usage or Invocation fence, with prose under it describing the optional override in place of every "No arguments" line, and keep only their step-0 reference to the shared procedure with no parse clause of their own; `goto-next-milestone` and `init-milestone-base-workflow`, which are outside the rule, are left unchanged. Verified by confirming no "No arguments" line remains in those seven rendered skills in any host tree and by `uv run scripts/build_hosts.py --check` passing after the `hosts/` rebuild.

---

## Finish Under Milestone Override

`finish-current-milestone` honours a matching `--milestone` override whatever the pointer reads: its step-1 stop on a `none` pointer applies only when no override is given, and its pointer-clearing step becomes conditional, overwriting the `Current milestone:` line with `none` only when the pointer names the finished milestone, leaving a `none` pointer as `none` and a pointer naming a different milestone untouched, while the history entry, the Completed Milestones row, and the `Milestone-finish:` commit are written as today in every case. This is needed because finishing a milestone must never deactivate a different one. Verified by reading the rendered skill in each host tree and by `uv run scripts/build_hosts.py --check` passing after the `hosts/` rebuild.

---

## Forward Milestone Directory To Completion Agent

`complete-all-tasks` passes the `<MILESTONE_DIR>` its step 0 resolved on every dispatch as a fixed `Milestone directory: <MILESTONE_DIR>` line in its prompt fence beside the task-name line, following the alternatives pass's fence; `core/agents/complete-task.md` documents that line as a prompt value the agent uses as given with no resolution of its own; `core/shared/complete-procedure.md` step 1 takes a supplied directory as given and runs the shared pointer procedure only when none is supplied, the inline `complete-task` skill's case; and the three hosts' `COMPLETE_TASK_DISPATCH` slot values stop saying the prompt "contains only the task name". This keeps both dispatch sites on one unconditional prompt shape so no agent can diverge from the directory the orchestrator commits for. Verified by reading the rendered fence, agent file, and procedure in each host tree and by `uv run scripts/build_hosts.py --check` passing after the `hosts/` rebuild.

---

## Spell The Flag In The Docs

In `docs/skill-reference.md`, each of the sixteen pointer-resolving skills' `###` headings spells `[--milestone <milestone_id>]` exactly as that skill's Usage fence does, the `specify-milestone-starting-state <milestone_id>` heading taking the optional form in place of the required id and the `capture-milestone-principle-updates <milestone_id>` heading staying as it is. In `docs/ways-of-using-cairn.md`, the Starting-a-milestone chain runs `/cairn:specify-milestone-starting-state` with no argument, `<milestone_id>` leaves the notation paragraph's placeholder list (five placeholders become four), the Setting-up chain's closing clause "with `<milestone_id>` the directory `define-milestone-goal` created" is dropped, and the page says nothing about the `--milestone` flag. Verified by a grep for `<milestone_id>` over `docs/ways-of-using-cairn.md` printing nothing and by each updated heading matching its skill's rendered Usage fence.

---

## Record Milestone Resolution In CLAUDE.md

`CLAUDE.md` gains one invariant recording the uniform resolution rule: every milestone-operating skill resolves through the shared pointer procedure by default or through one optional leading `--milestone <milestone_id>` override naming the exact directory, validated by the existence of its `requirements.md` with no fallback to the pointer and honoured when the pointer reads `none`, the flag-parsing rule stated once in the procedure with one clause at each positional-text skill's parse point, and `capture-milestone-principle-updates` the stated exception keeping its required positional id. In the same edit, the `finish-current-milestone` invariant is narrowed to say the pointer clear happens exactly when the pointer names the finished milestone, and the dispatch-prompt invariant names the milestone directory beside the task heading as `complete-all-tasks`' whole prompt. Verified by reading the three passages against the finished skills, procedure, and agent file.

---
