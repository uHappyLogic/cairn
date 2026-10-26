# Ways of using Cairn

How to chain Cairn's skills as headless command lines, one goal per section: each way below is a heading naming the goal, one or two sentences on when to run it and what it leaves behind, and the chain as one fenced block whose every line is a complete invocation. Each line names its host binary and, on Claude Code, its model and effort, so a chain mixes hosts, models, and effort levels line by line; the legend states what each setting does, and what a setting buys is left to the [design claims](design-claims.md). Every skill commits what it changes under its own subject (see [how skills commit](workflow.md#how-skills-commit)), so the git log records each run whichever host or model made it. The phases these chains walk are in [workflow.md](workflow.md), and what each skill does is in the [skill reference](skill-reference.md).

## Notation and flags

Every line is one headless run, `claude -p "/cairn:<skill>"` on Claude Code, `agy -p "/cairn:<skill>"` on Antigravity, or `codex exec '$cairn:<skill>'` on Codex, where `/cairn:<skill>` is the skill's slash command under the plugin's `cairn:` namespace, `$cairn:<skill>` is the same skill under Codex's `$` sigil (single-quoted so the shell passes the `$` through as written), and the process exits when the skill finishes. Angle brackets mark the only text you substitute; every other token runs as written. The page uses four placeholders: `<goal>` is the milestone's goal description, exactly as the skill reference spells it in `define-milestone-goal <overall_goal_description>`, written as plain prose with no double quote since it sits inside the line's quoted prompt (no single quote on a Codex line, whose prompt is single-quoted); `<Short Title>` is an open question's Short Title and `<Alternative Id>` the `id` of one of its embedded alternatives, the two halves the skill reference spells as `answer-open-question-with-alternative <question_name>. <alternative id>`; and `<answer text>` is your own answer to a question, which `answer-open-question <question_name>` takes after the Short Title and a period, written as plain prose under the same quoting rule as `<goal>`.

The headless flags:

- `--dangerously-skip-permissions` auto-approves every tool-permission request so a headless run never waits on a prompt; it exists on Claude Code and Antigravity under this one name, and its Codex counterpart is `--dangerously-bypass-approvals-and-sandbox`, which also lifts Codex's sandbox.
- `--model` selects the model for the run: on Claude Code it takes a family alias such as `opus` or `fable`, which `claude --help` defines as the latest model of that family (so the chains name families, not releases, and go stale only when a family changes), on Antigravity it takes a model id from the `agy models` list or that id's base model name without its trailing effort level, which `--effort` then chooses or, left out, falls to the model's default, and on Codex its counterpart is `-m`.
- `--effort` sets the reasoning effort for the run: the values it takes are the ones that host's own `--help` lists (`claude --help`, `agy --help`), and on Antigravity a model may offer only some of them, a run naming one it lacks stopping with the levels it has; Codex has no effort flag.
- `--add-dir` adds one more directory to the run's workspace; it exists on all three hosts under this one name, and no line on this page carries it, because every line runs from the project root and each host, `agy` included, takes the run's working directory as its workspace and works on the project from there, while the plugin loads from its installed location (on Antigravity the global `~/.gemini/config/plugins/cairn`), never from the working directory.

To move a line between Claude Code and Antigravity, change the binary (`claude` to `agy`, or back), give `--model` and `--effort` values that host accepts or omit both to run at its defaults, as every `agy` line on this page does, and keep `--dangerously-skip-permissions` as it stands. To move a line to Codex, change the binary to `codex exec` (dropping `-p`), drop `--model` and `--effort` to run at the account's defaults, as every `agy` line already does, replace `--dangerously-skip-permissions` with `--dangerously-bypass-approvals-and-sandbox`, and rewrite `"/cairn:<skill>"` to `'$cairn:<skill>'`.

## Setting up a project

Run this once per project, in a fresh git repository: it bootstraps the workflow, committing `milestones/README.md` with the current-milestone pointer at `none` and the `CLAUDE.md` workflow guidance, then defines the first milestone and commits its directory without activating it, so the pointer still reads `none` and the [Starting a milestone](#starting-a-milestone) chain runs next. Two preconditions come before the chain rather than in it: `git init` in the project root, since the bootstrap stops before writing anything outside a git work tree, and one `/init` run, whose `CLAUDE.md` environment context the later skills read and which the bootstrap sweeps into its own commit.

```sh
claude -p "/cairn:init-milestone-base-workflow" --dangerously-skip-permissions --model "opus" --effort high;
claude -p "/cairn:define-milestone-goal <goal>" --dangerously-skip-permissions --model "opus" --effort high;
```

## Starting a milestone

Run this once a milestone is defined and the previous one is finished, so the current-milestone pointer reads `none`: it activates the lowest-numbered undone milestone without asking (the first line stops only if the pointer does not read `none` or no undone milestone exists), writes its starting state, surfaces the first review pass's open questions, embeds a set of alternatives on each, and picks a recommendation from every set. The alternatives line runs on `opus` at `--effort high`, one subagent per question, and the recommend line on `fable` at `--effort high`, one inline pass over the whole set.

```sh
claude -p "/cairn:goto-next-milestone" --dangerously-skip-permissions --model "opus" --effort high;
claude -p "/cairn:specify-milestone-starting-state" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:review-milestone-requirements" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:provide-alternatives-to-all-open-questions" --dangerously-skip-permissions --model "opus" --effort high;
claude -p "/cairn:recommend-all-open-questions" --dangerously-skip-permissions --model "fable" --effort high;
```

## Answering the questions that matter to you

Run this once [Starting a milestone](#starting-a-milestone) has put a recommendation on every question and you have read the annotated set: one answer line per decision you make yourself, in the first form to record an alternative you name by its id, the recommended one or another, and in the second to record an answer in your own words where no alternative fits, each clearing the picks on other questions it undermines; the recommend line then picks again for exactly the questions so cleared, the next line records every remaining recommendation, and the last two derive the task list and complete it, so the milestone needs you at the keyboard once, between the two chains, and leaves the ordered task list completed. The answer lines run on `fable` at `--effort high`, each inline over one question; the recommend and sweep lines on `fable` at `--effort high`, each one inline pass over the whole set; and the last two lines as in [Executing tasks](#executing-tasks).

```sh
claude -p "/cairn:answer-open-question-with-alternative <Short Title>. <Alternative Id>" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:answer-open-question <Short Title>. <answer text>" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:recommend-all-open-questions" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:answer-all-open-questions-with-recommendation" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:derive-tasks" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:complete-all-tasks" --dangerously-skip-permissions --model "opus" --effort xhigh;
```

## Running a mixed-agent requirements review

Repeat this pass until `review-milestone-requirements` reports convergence: each pass reconciles the open questions against the recorded decisions and surfaces new gaps, embeds alternatives on every question that lacks them and a recommendation on every question that lacks one, and records each recommendation as a decision. The host changes between the review line and the alternatives line, so one agent surfaces the questions and another annotates them; the alternatives line runs on `opus` at `--effort high`, and the recommend and answer lines on `fable` at `--effort high`, each one inline pass over the whole set; swapping every line to one host by the legend's rule gives the single-host form of the same pass.

```sh
agy -p "/cairn:review-milestone-requirements" --dangerously-skip-permissions
claude -p "/cairn:provide-alternatives-to-all-open-questions" --dangerously-skip-permissions --model "opus" --effort high;
claude -p "/cairn:recommend-all-open-questions" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:answer-all-open-questions-with-recommendation" --dangerously-skip-permissions --model "fable" --effort high;
```

## Putting more intelligence into a stuck milestone

Run this when the review loop has not converged after passes at the settings above: it records the recommendations already embedded, runs one more review, alternatives, recommend, and answer pass — the review line on `opus` at `--effort max`, the alternatives line on `opus` at `--effort high`, and the recommend line and both answer lines on `fable` at `--effort high`, each one inline pass over the whole set — then derives the task list and completes it in the same chain, with no stop between.

```sh
claude -p "/cairn:answer-all-open-questions-with-recommendation" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:review-milestone-requirements" --dangerously-skip-permissions --model "opus" --effort max;
claude -p "/cairn:provide-alternatives-to-all-open-questions" --dangerously-skip-permissions --model "opus" --effort high;
claude -p "/cairn:recommend-all-open-questions" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:answer-all-open-questions-with-recommendation" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:derive-tasks" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:complete-all-tasks" --dangerously-skip-permissions --model "opus" --effort xhigh;
```

## Executing tasks

Run this once a review pass has left every open question carrying a recommendation: the first line records those recommendations as decisions, on `fable` at `--effort high` like the recommend line that picked them, one inline pass over the whole set; `derive-tasks` writes the task list, and `complete-all-tasks` works through it, one commit per task. `complete-all-tasks` is the heaviest run and can stop at the host account's usage limit, which is what each comment line waits out; because every task commits on its own and a failed task's partial work is continued rather than redone, running the line again continues from the remaining tasks.

```sh
# wait until your account's usage window has reset
claude -p "/cairn:answer-all-open-questions-with-recommendation" --dangerously-skip-permissions --model "fable" --effort high;
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
