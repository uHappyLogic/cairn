# TASKS DONE

## Add Override Input To Pointer Procedure

`core/shared/get-current-milestone.md` gains its one input, an optional leading `--milestone <milestone_id>` in the skill's invocation text: it states once the rule for recognizing the flag and separating it from the skill's own positional text, takes the value verbatim as the exact milestone directory name under `milestones/` (no bare-number resolution, no stripped `milestones/` prefix or trailing slash) to form `milestones/<milestone_id>/`, and resolves an override without reading the pointer, so it is honoured even when the pointer reads `none`. When `milestones/<milestone_id>/requirements.md` does not exist the procedure stops with no fallback to the pointer, on an error line naming the given value followed by a list of every `milestone_*` directory under `milestones/` and no pointer to `/define-milestone-goal`; with no override the pointer's path stays unchecked and is handed on exactly as today. Verified by reading the rendered procedure in each host tree and by `uv run scripts/build_hosts.py --check` passing after the `hosts/` rebuild.

**Verified:**

- `core/shared/get-current-milestone.md` states one input, an optional leading `--milestone <milestone_id>` in the skill's invocation text, with the rule for recognizing it (first whitespace-separated token exactly `--milestone`, value the next token) and for separating it from the skill's own positional text (both tokens stripped, the rest read as if the flag were never written) stated once, in its `## Recognizing the override` section.
- The override value is taken verbatim as the exact directory name under `milestones/` to form `milestones/<milestone_id>/`, with no bare-number resolution and no stripped `milestones/` prefix or trailing slash.
- An override is resolved without reading `milestones/README.md`, so it is honoured whatever the pointer reads, `none` included.
- When `milestones/<milestone_id>/requirements.md` does not exist the procedure stops without changing anything and with no fallback to the pointer, on the error line `Error: --milestone <milestone_id> matches no milestone directory` naming the given value, followed by every `milestone_*` directory under `milestones/`, and with no pointer to `/define-milestone-goal`.
- With no override the pointer steps are unchanged and the extracted path is handed on as `<MILESTONE_DIR>` with no existence check.
- The rendered procedure in `hosts/claude/shared/`, `hosts/antigravity/shared/`, and `hosts/codex/plugins/cairn/shared/` is byte-identical to the core file and was read to carry the override input.
- `uv run scripts/build_hosts.py --check` passes (exit 0) after the `hosts/` rebuild.

---

## Uniform Resolution In Specify Starting State

`specify-milestone-starting-state` loses its required positional `<milestone_id>`: its Usage fence becomes `/specify-milestone-starting-state [--milestone <milestone_id>]` with the prose and example under it describing the optional override, and its step 1 follows the shared pointer procedure to resolve `<MILESTONE_DIR>` like the other pointer-resolving skills, dropping its own "milestone not found" stop and `/define-milestone-goal` pointer, with its commit PATHS and `Starting-state: <milestone_id>` subject taking the id from the last path component of the resolved directory. This brings the skill under the uniform resolution rule so the Starting-a-milestone chain resolves the milestone `goto-next-milestone` just activated, while `capture-milestone-principle-updates` stays untouched with its required positional id. Verified by reading the rendered skill in each host tree and by `uv run scripts/build_hosts.py --check` passing after the `hosts/` rebuild.

**Verified:**

- `core/skills/specify-milestone-starting-state/SKILL.md`'s Usage fence reads `/specify-milestone-starting-state [--milestone <milestone_id>]`, with the prose under it describing the optional leading override (no argument fills the current milestone; `--milestone <milestone_id>` names another by its exact directory name under `milestones/`) and an example using the flag; no required positional `<milestone_id>` remains.
- Its step 1 follows `{{PLUGIN_ROOT}}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`, like the other pointer-resolving skills, and carries no "milestone not found" stop and no `/define-milestone-goal` pointer.
- Its step 2 reads `<MILESTONE_DIR>/requirements.md`, its commit PATHS is `<MILESTONE_DIR>/requirements.md`, and its SUBJECT stays `Starting-state: <milestone_id>`, with `<milestone_id>` stated to be the last path component of the resolved `<MILESTONE_DIR>`.
- `core/skills/capture-milestone-principle-updates/SKILL.md` is unchanged, keeping its required positional id.
- The rendered skill in `hosts/claude/skills/`, `hosts/antigravity/skills/`, and `hosts/codex/plugins/cairn/skills/` was read and carries the new Usage, step 1, and commit inputs, with each host's plugin root substituted.
- `uv run scripts/build_hosts.py --check` passes (exit 0) after the `hosts/` rebuild.

---

## Flag Clause In Positional-Text Skills

The nine skills whose invocation carries positional text of their own (`answer-open-question`, `answer-open-question-with-recommendation`, `answer-open-question-with-alternative`, `ask-in-milestone-context`, `discuss-new-task`, `discuss-open-question`, `modify-milestone-goal`, `submit-task`, `complete-task`) each show `[--milestone <milestone_id>]` ahead of their positional text in their Usage or Invocation fence, with the prose under it describing the optional override, and each carries one clause at its own parse point (its parse step, or its step 0 where it has none) telling the runner to strip a leading `--milestone` value by the shared procedure before reading the rest, so the flag is never folded into a Short Title, an answer, a goal, a task name, or a question. `ask-in-milestone-context`'s `none`-pointer fallback is worded to apply only when no override is given, since an override never reads the pointer. Verified by reading the nine rendered skills in each host tree and by `uv run scripts/build_hosts.py --check` passing after the `hosts/` rebuild.

**Verified:**

- Each of the nine core skills (`answer-open-question`, `answer-open-question-with-recommendation`, `answer-open-question-with-alternative`, `ask-in-milestone-context`, `discuss-new-task`, `discuss-open-question`, `modify-milestone-goal`, `submit-task`, `complete-task`) shows `[--milestone <milestone_id>]` directly after the skill name and ahead of its positional text in its Usage or Invocation fence.
- The prose under each of those fences describes the optional leading override: it names the milestone by its exact directory name under `milestones/`, e.g. `milestone_12_user-guide`, in place of the current-milestone pointer.
- Each of the nine carries one clause at its own parse point (`answer-open-question` step 1's split; `answer-open-question-with-alternative`'s Invocation split rule; step 0 of `ask-in-milestone-context`, `discuss-new-task`, `discuss-open-question`, `modify-milestone-goal`, and `submit-task`; the milestone-finding step 1 of `answer-open-question-with-recommendation`; step 1 of `complete-task`) telling the runner to first strip a leading `--milestone <milestone_id>` by the rule in `get-current-milestone.md` and read only the rest as its Short Title, answer, goal text, issue description, task name, or question.
- `ask-in-milestone-context`'s `none`-pointer fallback opens "If no override was given and the pointer is `none`" and states that an override never reads the pointer, so the fallback never applies to one.
- The nine rendered skills in `hosts/claude/skills/`, `hosts/antigravity/skills/`, and `hosts/codex/plugins/cairn/skills/` were read and carry the fence, the override prose, the strip clause, and (for `ask-in-milestone-context`) the reworded fallback, with each host's plugin root substituted.
- `uv run scripts/build_hosts.py --check` passes (exit 0) after the `hosts/` rebuild.

---

## Flag In Argument-Free Skill Usage

The seven pointer-resolving skills that take no positional text (`answer-all-open-questions-with-recommendation`, `complete-all-tasks`, `derive-tasks`, `finish-current-milestone`, `provide-alternatives-to-all-open-questions`, `recommend-all-open-questions`, `review-milestone-requirements`) each show `[--milestone <milestone_id>]` in their Usage or Invocation fence, with prose under it describing the optional override in place of every "No arguments" line, and keep only their step-0 reference to the shared procedure with no parse clause of their own; `goto-next-milestone` and `init-milestone-base-workflow`, which are outside the rule, are left unchanged. Verified by confirming no "No arguments" line remains in those seven rendered skills in any host tree and by `uv run scripts/build_hosts.py --check` passing after the `hosts/` rebuild.

**Verified:**

- Each of the seven core skills (`answer-all-open-questions-with-recommendation`, `complete-all-tasks`, `derive-tasks`, `finish-current-milestone`, `provide-alternatives-to-all-open-questions`, `recommend-all-open-questions`, `review-milestone-requirements`) shows `/<skill> [--milestone <milestone_id>]` in its Usage or Invocation fence.
- The prose under each of those fences describes the optional leading override (with no argument the skill works on the current milestone; `--milestone <milestone_id>` names another by its exact directory name under `milestones/`, e.g. `milestone_12_user-guide`, in place of the current-milestone pointer), replacing every "No arguments" / "Takes no arguments" line, and the two annotating passes' opening "**argument-free**" now reads "takes **no Short Title**".
- Each of the seven keeps only its step-0 (for `finish-current-milestone`, step-1) reference to `get-current-milestone.md` and carries no parse clause of its own (no "strip a leading" clause in any of them).
- `goto-next-milestone` and `init-milestone-base-workflow` are unchanged in `core/` and in every host tree.
- No "No arguments", "Takes no arguments", or "argument-free" line remains in those seven rendered skills under `hosts/claude/skills/`, `hosts/antigravity/skills/`, or `hosts/codex/plugins/cairn/skills/`, each of which carries the new fence once.
- `uv run scripts/build_hosts.py --check` passes (exit 0) after the `hosts/` rebuild.

---

## Finish Under Milestone Override

`finish-current-milestone` honours a matching `--milestone` override whatever the pointer reads: its step-1 stop on a `none` pointer applies only when no override is given, and its pointer-clearing step becomes conditional, overwriting the `Current milestone:` line with `none` only when the pointer names the finished milestone, leaving a `none` pointer as `none` and a pointer naming a different milestone untouched, while the history entry, the Completed Milestones row, and the `Milestone-finish:` commit are written as today in every case. This is needed because finishing a milestone must never deactivate a different one. Verified by reading the rendered skill in each host tree and by `uv run scripts/build_hosts.py --check` passing after the `hosts/` rebuild.

**Verified:**

- `core/skills/finish-current-milestone/SKILL.md` step 1 resolves `<MILESTONE_DIR>` through `get-current-milestone.md` from a leading `--milestone <milestone_id>` override when given, states a matching override is honoured whatever the pointer reads (`none` included), and applies its "no active milestone to finish" stop only when no override was given and the pointer is `none`.
- Step 6 is conditional: it overwrites the `Current milestone:` line with `Current milestone: none` only when the line's backtick-quoted path names the finished milestone's directory `<MILESTONE_DIR>` (always so with no override), leaves a `none` line as `none`, and leaves a line naming a different milestone untouched.
- Step 6 states steps 5 and 8 run as written in every case, so the history entry, the Completed Milestones row, and the `Milestone-finish: milestone_<NN>_<slug>` commit of `milestones/README.md` are unchanged; the intro and step 8's PATHS note describe the pointer clear as happening only when the pointer names the finished milestone.
- The rendered skill in `hosts/claude/`, `hosts/antigravity/`, and `hosts/codex/plugins/cairn/` carries the same wording, read after the rebuild.
- `uv run scripts/build_hosts.py --check` passes (exit 0) after the `hosts/` rebuild.

---

## Forward Milestone Directory To Completion Agent

`complete-all-tasks` passes the `<MILESTONE_DIR>` its step 0 resolved on every dispatch as a fixed `Milestone directory: <MILESTONE_DIR>` line in its prompt fence beside the task-name line, following the alternatives pass's fence; `core/agents/complete-task.md` documents that line as a prompt value the agent uses as given with no resolution of its own; `core/shared/complete-procedure.md` step 1 takes a supplied directory as given and runs the shared pointer procedure only when none is supplied, the inline `complete-task` skill's case; and the three hosts' `COMPLETE_TASK_DISPATCH` slot values stop saying the prompt "contains only the task name". This keeps both dispatch sites on one unconditional prompt shape so no agent can diverge from the directory the orchestrator commits for. Verified by reading the rendered fence, agent file, and procedure in each host tree and by `uv run scripts/build_hosts.py --check` passing after the `hosts/` rebuild.

**Verified:**

- `core/skills/complete-all-tasks/SKILL.md` step 2b's prompt fence carries a fixed `Milestone directory: <MILESTONE_DIR>` line after the `Complete the task named: "<TASK_NAME>"` line, blank-line separated as in the alternatives pass's fence, and the sentence below the fence says every dispatch carries it, holding the `<MILESTONE_DIR>` step 0 resolved from an override or the pointer.
- `core/agents/complete-task.md` gains an `## Inputs` section documenting the task-name line and the `Milestone directory:` line as its two prompt values, the directory used as given as the supplied directory the procedure's step 1 takes, never resolved by the agent; its description names the milestone directory beside the heading text (25-word cap and frontmatter checks pass in the build).
- `core/shared/complete-procedure.md` step 1 takes a runner-supplied milestone directory as given as `<MILESTONE_DIR>` and follows `get-current-milestone.md` only when none is supplied, the inline `complete-task` skill's case, with any held `--milestone` override as that procedure's input.
- The three hosts' `scripts/hosts/<host>/slots/COMPLETE_TASK_DISPATCH.md` values say the prompt carries the task name and the milestone directory and nothing else, substituting `<MILESTONE_DIR>` with the directory resolved in step 0; a grep for "only the task name", "heading text as the prompt", and "The task name is given" over `core`, `scripts`, `hosts`, and `agy_tests` prints nothing.
- After `uv run scripts/build_hosts.py`, the rendered `skills/complete-all-tasks/SKILL.md` fence, `agents/complete-task.md` Inputs section, and `shared/complete-procedure.md` step 1 read as above in `hosts/claude`, `hosts/antigravity`, and `hosts/codex/plugins/cairn`, and `uv run scripts/build_hosts.py --check` passes.
- `agy_tests/test_subagent_write_tools.py` dispatches the completion agent with the new two-line prompt (task heading plus seeded milestone directory), and `uv run pytest` (891 passed) and the 3.9 floor run (887 passed, 1 skipped) both pass.

---

## Spell The Flag In The Docs

In `docs/skill-reference.md`, each of the sixteen pointer-resolving skills' `###` headings spells `[--milestone <milestone_id>]` exactly as that skill's Usage fence does, the `specify-milestone-starting-state <milestone_id>` heading taking the optional form in place of the required id and the `capture-milestone-principle-updates <milestone_id>` heading staying as it is. In `docs/ways-of-using-cairn.md`, the Starting-a-milestone chain runs `/cairn:specify-milestone-starting-state` with no argument, `<milestone_id>` leaves the notation paragraph's placeholder list (five placeholders become four), the Setting-up chain's closing clause "with `<milestone_id>` the directory `define-milestone-goal` created" is dropped, and the page says nothing about the `--milestone` flag. Verified by a grep for `<milestone_id>` over `docs/ways-of-using-cairn.md` printing nothing and by each updated heading matching its skill's rendered Usage fence.

**Verified:**

- In `docs/skill-reference.md`, the `###` headings of the sixteen pointer-resolving skills (`review-milestone-requirements`, `discuss-open-question`, `answer-open-question`, `answer-open-question-with-recommendation`, `answer-open-question-with-alternative`, `answer-all-open-questions-with-recommendation`, `modify-milestone-goal`, `provide-alternatives-to-all-open-questions`, `recommend-all-open-questions`, `derive-tasks`, `discuss-new-task`, `submit-task`, `complete-all-tasks`, `complete-task`, `ask-in-milestone-context`, `finish-current-milestone`) each spell `[--milestone <milestone_id>]` once, directly after the skill name and before any positional text, exactly as the first `/<skill>` line of that skill's rendered `hosts/claude/skills/<skill>/SKILL.md` Usage fence does (checked programmatically for all sixteen).
- The `specify-milestone-starting-state` heading reads `specify-milestone-starting-state [--milestone <milestone_id>]`, the optional form in place of the required id, matching its rendered Usage fence.
- The `capture-milestone-principle-updates <milestone_id>` heading is unchanged.
- In `docs/ways-of-using-cairn.md`, the Starting-a-milestone chain line runs `claude -p "/cairn:specify-milestone-starting-state"` with no argument.
- The notation paragraph says "The page uses four placeholders" and lists `<goal>`, `<Short Title>`, `<Alternative Id>`, and `<answer text>`, with the `<milestone_id>` clause removed.
- The Setting-up chain's paragraph ends "the [Starting a milestone](#starting-a-milestone) chain runs next.", the clause "with `<milestone_id>` the directory `define-milestone-goal` created" dropped.
- `grep -n '<milestone_id>' docs/ways-of-using-cairn.md` prints nothing, and `grep -n -- '--milestone' docs/ways-of-using-cairn.md` prints nothing, so the page says nothing about the flag.

---

## Record Milestone Resolution In CLAUDE.md

`CLAUDE.md` gains one invariant recording the uniform resolution rule: every milestone-operating skill resolves through the shared pointer procedure by default or through one optional leading `--milestone <milestone_id>` override naming the exact directory, validated by the existence of its `requirements.md` with no fallback to the pointer and honoured when the pointer reads `none`, the flag-parsing rule stated once in the procedure with one clause at each positional-text skill's parse point, and `capture-milestone-principle-updates` the stated exception keeping its required positional id. In the same edit, the `finish-current-milestone` invariant is narrowed to say the pointer clear happens exactly when the pointer names the finished milestone, and the dispatch-prompt invariant names the milestone directory beside the task heading as `complete-all-tasks`' whole prompt. Verified by reading the three passages against the finished skills, procedure, and agent file.

**Verified:**

- `CLAUDE.md` `## Invariants` gains one new bullet recording the uniform resolution rule: the seventeen milestone-operating skills (the sixteen pointer-resolving ones plus `specify-milestone-starting-state`) resolve `<MILESTONE_DIR>` through `core/shared/get-current-milestone.md`, from the pointer by default or from one optional leading `--milestone <milestone_id>` override, matching the 17 skills whose Usage and `docs/skill-reference.md` headings spell `[--milestone <milestone_id>]`.
- The invariant states the override's value form (exact directory name, verbatim, no bare-number resolution or stripped prefix/slash), its validation by the existence of `milestones/<milestone_id>/requirements.md`, the miss stopping on an `Error:` line plus the `milestone_*` listing with no fallback to the pointer, and the override honoured when the pointer reads `none`, matching the live `get-current-milestone.md`.
- The invariant states the flag-parsing rule once in the procedure with one clause at each positional-text skill's parse point, matching the nine skills carrying a strip clause (`answer-open-question`, its two lifting variants, `ask-in-milestone-context`, `complete-task`, `discuss-new-task`, `discuss-open-question`, `modify-milestone-goal`, `submit-task`) and the argument-free skills carrying none.
- The invariant names `capture-milestone-principle-updates` as the stated exception keeping its required positional id, matching its SKILL.md (no `--milestone` mention, `requirements.md` existence test, `milestone_*` listing).
- The `finish-current-milestone` invariant is narrowed: the pointer is cleared to `none` exactly when it names the finished milestone, a `none` pointer stays `none` and one naming another milestone is left untouched, the `none` stop applies only without an override, and history, table row, and commit are written in every case, matching the live skill's steps 1 and 6.
- The dispatch-prompt invariant names the resolved `<MILESTONE_DIR>` beside the task's `##` heading as `complete-all-tasks`' whole prompt and the agent's use of it as given, matching the skill's prompt fence, the `complete-task` agent's `## Inputs`, `complete-procedure.md` step 1, and the three `COMPLETE_TASK_DISPATCH` slot values.
- `uv run scripts/build_hosts.py --check` passes after the edit.

---
