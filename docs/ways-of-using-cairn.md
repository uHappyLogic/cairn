# Ways of using Cairn

How to chain Cairn's skills as headless command lines, one goal per section: each way below is a heading naming the goal, one or two sentences on when to run it and what it leaves behind, and the chain as one fenced block whose every line is a complete invocation. Each line names its host binary and, on Claude Code, its model and effort, so a chain mixes hosts, models, and effort levels line by line; the legend states what each setting does, and what a setting buys is left to the [design claims](design-claims.md). Every skill commits what it changes under its own subject (see [how skills commit](workflow.md#how-skills-commit)), so the git log records each run whichever host or model made it. The phases these chains walk are in [workflow.md](workflow.md), and what each skill does is in the [skill reference](skill-reference.md).

## Notation and flags

Every line is one headless run, `claude -p "/cairn:<skill>"` on Claude Code or `agy -p "/cairn:<skill>"` on Antigravity, where `/cairn:<skill>` is the skill's slash command under the plugin's `cairn:` namespace and the process exits when the skill finishes. Angle brackets mark the only text you substitute; every other token runs as written. The page uses two placeholders: `<milestone_id>` is the milestone's directory name under `milestones/`, exactly as the skill reference spells it in `specify-milestone-starting-state <milestone_id>`, and `<project-root>` is the absolute path of the repository the run works in.

The flags on the lines:

- `--dangerously-skip-permissions` auto-approves every tool-permission request so a headless run never waits on a prompt; it exists on both hosts under this one name.
- `--model` selects the model for the run: on Claude Code it takes a family alias such as `opus` or `fable`, which `claude --help` defines as the latest model of that family (so the chains name families, not releases, and go stale only when a family changes), and on Antigravity it takes a model id from the `agy models` list.
- `--effort` sets the reasoning effort for the run: `low`, `medium`, `high`, `xhigh`, or `max` on Claude Code and `low`, `medium`, or `high` on Antigravity, each list as that host's `--help` gives it.
- `--add-dir` adds one more directory to the run's workspace; it exists on both hosts, and the Antigravity lines pass the project root through it.

To move a line to the other host, change the binary (`claude` to `agy`, or back), give `--model` and `--effort` values that host accepts or omit both to run at its defaults, as every `agy` line on this page does, keep `--dangerously-skip-permissions` as it stands, and carry `--add-dir "<project-root>"` on every `agy` line as the lines below do.

## Starting a milestone

Run this once a milestone is defined and the previous one is finished, so the current-milestone pointer reads `none`: it activates the milestone, writes its starting state, surfaces the first review pass's open questions, and embeds a recommendation on each. The same chain also ran with `--model "opus"` on every line and `--effort max` on the last three.

```sh
claude -p "/cairn:goto-next-milestone" --dangerously-skip-permissions --model "opus" --effort high;
claude -p "/cairn:specify-milestone-starting-state <milestone_id>" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:review-milestone-requirements" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:recommend-all-open-questions" --dangerously-skip-permissions --model "opus" --effort xhigh;
```

## Running a mixed-agent requirements review

Repeat this pass until `review-milestone-requirements` reports convergence: each pass reconciles the open questions against the recorded decisions and surfaces new gaps, embeds a recommendation on every question that lacks one, and records each recommendation as a decision. The host changes between the review line and the recommend line, so one agent surfaces the questions and another recommends on them; swapping every line to one host by the legend's rule gives the single-host form of the same pass.

```sh
agy -p "/cairn:review-milestone-requirements" --add-dir "<project-root>" --dangerously-skip-permissions
claude -p "/cairn:recommend-all-open-questions" --dangerously-skip-permissions --model "opus" --effort max;
claude -p "/cairn:answer-all-open-questions-with-recommendation" --dangerously-skip-permissions --model "opus" --effort high;
```

## Putting more intelligence into a stuck milestone

Run this when the review loop has not converged after passes at the settings above: it records the recommendations already embedded, runs one more review, recommend, and answer pass with every line on `opus` at `--effort max` for the review and recommend lines and `xhigh` for the answer lines, then derives the task list and completes it in the same chain, with no stop between.

```sh
claude -p "/cairn:answer-all-open-questions-with-recommendation" --dangerously-skip-permissions --model "opus" --effort xhigh;
claude -p "/cairn:review-milestone-requirements" --dangerously-skip-permissions --model "opus" --effort max;
claude -p "/cairn:recommend-all-open-questions" --dangerously-skip-permissions --model "opus" --effort max;
claude -p "/cairn:answer-all-open-questions-with-recommendation" --dangerously-skip-permissions --model "opus" --effort xhigh;
claude -p "/cairn:derive-tasks" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:complete-all-tasks" --dangerously-skip-permissions --model "opus" --effort xhigh;
```

## Executing tasks

Run this once a review pass has left every open question carrying a recommendation: the first line records those recommendations as decisions, `derive-tasks` writes the task list, and `complete-all-tasks` works through it, one commit per task. `complete-all-tasks` is the heaviest run and can stop at the host account's usage limit, which is what each comment line waits out; because every task commits on its own and a failed task's partial work is continued rather than redone, running the line again continues from the remaining tasks.

```sh
# wait until your account's usage window has reset
claude -p "/cairn:answer-all-open-questions-with-recommendation" --dangerously-skip-permissions --model "opus" --effort high;
claude -p "/cairn:derive-tasks" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:complete-all-tasks" --dangerously-skip-permissions --model "opus" --effort xhigh;
# wait until your account's usage window has reset
claude -p "/cairn:complete-all-tasks" --dangerously-skip-permissions --model "opus" --effort xhigh;
```

## Finishing a milestone

Run this when `TASKS_TODO.md` is empty: it records the milestone's completion summary in `milestones/README.md`, clears the current-milestone pointer to `none`, and updates `CLAUDE.md` for lasting changes, leaving the repository ready for the next `goto-next-milestone`.

```sh
claude -p "/cairn:finish-current-milestone" --dangerously-skip-permissions --model "opus" --effort high;
```
