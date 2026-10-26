# Get Current Milestone (shared snippet)

This is the single source of truth for resolving `<MILESTONE_DIR>`. It takes one input, an
optional `--milestone <milestone_id>` override at the start of the skill's invocation text:
when given, it names the milestone directly and the current-milestone pointer is never read;
when absent, `<MILESTONE_DIR>` comes from the pointer.

## Recognizing the override

The override is present only when the first whitespace-separated token of the invocation
text is exactly `--milestone`. Its value, `<milestone_id>`, is the token right after it.
Strip those two tokens and the whitespace following them; what remains is the skill's own
positional text, read exactly as if the flag had never been written. Any other first token,
including a `--milestone` that appears later in the text, means there is no override, and the
whole invocation text is the skill's own. A leading `--milestone` with no token after it is an
override whose value matches no milestone.

A skill that reads positional text strips the flag by this rule at its own parse point; the
override found there is the input the resolution below uses.

## Resolving an override

When an override is given, resolve it here without reading `milestones/README.md`, so it is
honoured whatever the pointer reads, `none` included.

1. Take `<milestone_id>` verbatim as the exact milestone directory name under `milestones/`,
   e.g. `milestone_12_user-guide`, and form `milestones/<milestone_id>/`. No bare number is
   resolved to a directory, and no `milestones/` prefix or trailing slash is stripped: any
   other spelling is a value that matches no milestone.

2. If `milestones/<milestone_id>/requirements.md` exists, `<MILESTONE_DIR>` is
   `milestones/<milestone_id>/`.

3. Otherwise **stop without changing anything**, with no fallback to the pointer. Report the
   error line `Error: --milestone <milestone_id> matches no milestone directory`, the value
   exactly as given, followed by every `milestone_*` directory present under `milestones/`,
   one name per line, so the caller can retry with one of them. The error line and that list
   are the whole report.

## Resolving from the pointer

With no override:

1. In the workspace root `milestones/README.md`, find the one line whose prefix
   is `Current milestone:` (case-sensitive; the colon is load-bearing — this
   unique prefix is what distinguishes the machine pointer line from the section
   heading `## Current Milestone`).

2. Examine the value after the prefix:

   - If the value is the bare token `none` (no backticks) — `Current milestone: none`
     — there is no active milestone. Stop and report accordingly; do not attempt to
     read a milestone directory.

   - Otherwise the value is a backtick-quoted path, e.g.
     `` Current milestone: `milestones/milestone_01_public-release-prep/` ``.
     Extract the path inside the backticks; that path is `<MILESTONE_DIR>`, handed
     on as it stands with no existence check.

## Using `<MILESTONE_DIR>`

Use `<MILESTONE_DIR>` as the prefix for all milestone-relative file reads
(e.g. `<MILESTONE_DIR>/TASKS_TODO.md`, `<MILESTONE_DIR>/requirements.md`).
