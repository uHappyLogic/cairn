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
