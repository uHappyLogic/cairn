# Ways of using Cairn

How to chain Cairn's skills as headless command lines, one goal per section: each way below is a heading naming the goal, one or two sentences on when to run it and what it leaves behind, and the chain as one fenced block whose every line is a complete invocation. Each line names its host binary and, on Claude Code, its model and effort, so a chain mixes hosts, models, and effort levels line by line; the legend states what each setting does, and what a setting buys is left to the [design claims](design-claims.md). Every skill commits what it changes under its own subject (see [how skills commit](workflow.md#how-skills-commit)), so the git log records each run whichever host or model made it. The phases these chains walk are in [workflow.md](workflow.md), and what each skill does is in the [skill reference](skill-reference.md).

## Notation and flags

Every line is one headless run, `claude -p "/cairn:<skill>"` on Claude Code, `agy -p "/cairn:<skill>"` on Antigravity, or `codex exec '$cairn:<skill>'` on Codex, where `/cairn:<skill>` is the skill's slash command under the plugin's `cairn:` namespace, `$cairn:<skill>` is the same skill under Codex's `$` sigil (single-quoted so the shell passes the `$` through as written), and the process exits when the skill finishes. Angle brackets mark the only text you substitute; every other token runs as written. The page uses six placeholders: `<goal>` is the milestone's goal description, exactly as the skill reference spells it in `define-milestone-goal --at <scope> <overall_goal_description>`, written as plain prose with no double quote since it sits inside the line's quoted prompt (no single quote on a Codex line, whose prompt is single-quoted); `<scope>` is the directory holding the core of the milestone's work, relative to the project root and `.` for the root, the value of that skill's required `--at` flag, as `discuss-milestone-goal` proposes it; `<path>` is the milestone's repo-relative path, trailing slash included, exactly as the definition tool printed it (for example `milestones/user-guide/` for a milestone defined `--at .`, or `packages/api/milestones/rate-limits/` for one defined `--at packages/api`), the value of the required leading flag the skill reference spells as `--milestone <path>`; `<Short Title>` is an open question's Short Title and `<Alternative Id>` the `id` of one of its embedded alternatives, the two halves the skill reference spells as `answer-open-question-with-alternative --milestone <path> <question_name>. <alternative id>`; and `<answer text>` is your own answer to a question, which `answer-open-question --milestone <path> <question_name>` takes after the Short Title and a period, written as plain prose under the same quoting rule as `<goal>`.

Every line after a definition line names its milestone by `--milestone <path>`, first, before any text of the skill's own, because no milestone is current: nothing stores one and no line picks one, so every chain below is written for one milestone's path and runs the same whether that milestone is the only live one or one of several. The definition line's `Milestone-definition: <path>` commit subject records the path the later lines take (`git log -1 --format=%s` right after that line), and a line whose `--milestone` is missing or names no live milestone stops with nothing changed and lists every live milestone's path to retry with.

The headless flags:

- `--dangerously-skip-permissions` auto-approves every tool-permission request so a headless run never waits on a prompt; it exists on Claude Code and Antigravity under this one name, and its Codex counterpart is `--dangerously-bypass-approvals-and-sandbox`, which also lifts Codex's sandbox.
- `--model` selects the model for the run: on Claude Code it takes a family alias such as `sonnet`, `opus`, or `fable`, which `claude --help` defines as the latest model of that family (so the chains name families, not releases, and go stale only when a family changes), on Antigravity it takes a model id from the `agy models` list or that id's base model name without its trailing effort level, which `--effort` then chooses or, left out, falls to the model's default, and on Codex its counterpart is `-m`.
- `--effort` sets the reasoning effort for the run: the values it takes are the ones that host's own `--help` lists (`claude --help`, `agy --help`), and on Antigravity a model may offer only some of them, a run naming one it lacks stopping with the levels it has; Codex has no effort flag.
- `--add-dir` adds one more directory to the run's workspace; it exists on all three hosts under this one name, and no line on this page carries it, because every line runs from the project root and each host, `agy` included, takes the run's working directory as its workspace and works on the project from there, while the plugin loads from its installed location (on Antigravity the global `~/.gemini/config/plugins/cairn`), never from the working directory.

To move a line between Claude Code and Antigravity, change the binary (`claude` to `agy`, or back), give `--model` and `--effort` values that host accepts or omit both to run at its defaults, as every `agy` line on this page does, and keep `--dangerously-skip-permissions` as it stands. To move a line to Codex, change the binary to `codex exec` (dropping `-p`), drop `--model` and `--effort` to run at the account's defaults, as every `agy` line already does, replace `--dangerously-skip-permissions` with `--dangerously-bypass-approvals-and-sandbox`, and rewrite `"/cairn:<skill>"` to `'$cairn:<skill>'`.

## Setting up a project

Run this once per project, in a fresh git repository: the bootstrap line adds the milestone workflow guidance to `CLAUDE.md` and commits it under `Workflow-bootstrap: milestones`, then the definition line creates the first milestone at `<scope>/milestones/<slug>/`, creating the scope's `milestones/` container with it, and commits it under `Milestone-definition: <path>`; the [Starting a milestone](#starting-a-milestone) chain runs next on that `<path>`. Two preconditions come before the chain rather than in it: `git init` in the project root, since every line commits and the definition line stops before writing anything outside a git work tree, and one `/init` run, whose `CLAUDE.md` environment context the later skills read and which the bootstrap sweeps into its own commit.

```sh
claude -p "/cairn:init-milestone-base-workflow" --dangerously-skip-permissions --model "sonnet" --effort medium;
claude -p "/cairn:define-milestone-goal --at <scope> <goal>" --dangerously-skip-permissions --model "sonnet" --effort medium;
```

## Starting a milestone

Run this once a milestone is defined, on the `<path>` its definition line recorded: it writes the milestone's starting state, surfaces the first review pass's open questions, embeds a set of alternatives on each, and picks a recommendation from every set. No other milestone has to be finished first, and nothing else readies this one, since every line names the milestone it works on. The alternatives line runs on `opus` at `--effort high`, one subagent per question, and the recommend line on `fable` at `--effort xhigh`, one inline pass over the whole set.

```sh
claude -p "/cairn:specify-milestone-starting-state --milestone <path>" --dangerously-skip-permissions --model "fable" --effort xhigh;
claude -p "/cairn:review-milestone-requirements --milestone <path>" --dangerously-skip-permissions --model "fable" --effort xhigh;
claude -p "/cairn:provide-alternatives-to-all-open-questions --milestone <path>" --dangerously-skip-permissions --model "opus" --effort high;
claude -p "/cairn:recommend-all-open-questions --milestone <path>" --dangerously-skip-permissions --model "fable" --effort xhigh;
```

## Answering the questions that matter to you

Run this once [Starting a milestone](#starting-a-milestone) has put a recommendation on every question and you have read the annotated set: one answer line per decision you make yourself, in the first form to record an alternative you name by its id, the recommended one or another, and in the second to record an answer in your own words where no alternative fits, each clearing the picks on other questions it undermines; the recommend line then picks again for exactly the questions so cleared, the next line records every remaining recommendation, and the last two derive the task list and complete it, so the milestone needs you at the keyboard once, between the two chains, and leaves the ordered task list completed. The answer lines run on `fable` at `--effort high`, each inline over one question; the recommend line on `fable` at `--effort xhigh` and the sweep line on `fable` at `--effort high`, each one inline pass over the whole set; and the last two lines as in [Executing tasks](#executing-tasks).

```sh
claude -p "/cairn:answer-open-question-with-alternative --milestone <path> <Short Title>. <Alternative Id>" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:answer-open-question --milestone <path> <Short Title>. <answer text>" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:recommend-all-open-questions --milestone <path>" --dangerously-skip-permissions --model "fable" --effort xhigh;
claude -p "/cairn:answer-all-open-questions-with-recommendation --milestone <path>" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:derive-tasks --milestone <path>" --dangerously-skip-permissions --model "fable" --effort xhigh;
claude -p "/cairn:complete-all-tasks --milestone <path>" --dangerously-skip-permissions --model "opus" --effort high;
```

## Running a mixed-agent requirements review

Repeat this pass until `review-milestone-requirements` reports convergence: each pass reconciles the open questions against the recorded decisions and surfaces new gaps, embeds alternatives on every question that lacks them and a recommendation on every question that lacks one, and records each recommendation as a decision. The host changes between the review line and the alternatives line, so one agent surfaces the questions and another annotates them; the alternatives line runs on `opus` at `--effort high`, and the recommend line on `fable` at `--effort xhigh` and the answer line on `fable` at `--effort high`, each one inline pass over the whole set; swapping every line to one host by the legend's rule gives the single-host form of the same pass.

```sh
agy -p "/cairn:review-milestone-requirements --milestone <path>" --dangerously-skip-permissions
claude -p "/cairn:provide-alternatives-to-all-open-questions --milestone <path>" --dangerously-skip-permissions --model "opus" --effort high;
claude -p "/cairn:recommend-all-open-questions --milestone <path>" --dangerously-skip-permissions --model "fable" --effort xhigh;
claude -p "/cairn:answer-all-open-questions-with-recommendation --milestone <path>" --dangerously-skip-permissions --model "fable" --effort high;
```

## Putting more intelligence into a stuck milestone

Run this when the review loop has not converged after passes at the settings above: it records the recommendations already embedded, runs one more review, alternatives, recommend, and answer pass — the review line on `opus` at `--effort max`, the alternatives line on `opus` at `--effort high`, and the recommend line on `fable` at `--effort xhigh` and both answer lines on `fable` at `--effort high`, each one inline pass over the whole set — then derives the task list and completes it in the same chain, with no stop between.

```sh
claude -p "/cairn:answer-all-open-questions-with-recommendation --milestone <path>" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:review-milestone-requirements --milestone <path>" --dangerously-skip-permissions --model "opus" --effort max;
claude -p "/cairn:provide-alternatives-to-all-open-questions --milestone <path>" --dangerously-skip-permissions --model "opus" --effort high;
claude -p "/cairn:recommend-all-open-questions --milestone <path>" --dangerously-skip-permissions --model "fable" --effort xhigh;
claude -p "/cairn:answer-all-open-questions-with-recommendation --milestone <path>" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:derive-tasks --milestone <path>" --dangerously-skip-permissions --model "fable" --effort xhigh;
claude -p "/cairn:complete-all-tasks --milestone <path>" --dangerously-skip-permissions --model "opus" --effort high;
```

## Executing tasks

Run this once a review pass has left every open question carrying a recommendation: the first line records those recommendations as decisions, on `fable` at `--effort high`, the recommend line's model one effort level lower, one inline pass over the whole set; `derive-tasks` writes the task list, and `complete-all-tasks` works through it, one commit per task. `complete-all-tasks` is the heaviest run and can stop at the host account's usage limit, which is what each comment line waits out; because every task commits on its own and a failed task's partial work is continued rather than redone, running the line again continues from the remaining tasks.

```sh
# wait until your account's usage window has reset
claude -p "/cairn:answer-all-open-questions-with-recommendation --milestone <path>" --dangerously-skip-permissions --model "fable" --effort high;
claude -p "/cairn:derive-tasks --milestone <path>" --dangerously-skip-permissions --model "fable" --effort xhigh;
claude -p "/cairn:complete-all-tasks --milestone <path>" --dangerously-skip-permissions --model "opus" --effort high;
# wait until your account's usage window has reset
claude -p "/cairn:complete-all-tasks --milestone <path>" --dangerously-skip-permissions --model "opus" --effort high;
```

## Preparing another milestone while one runs

Run this when you want a second milestone's questions ready while another milestone is still executing: it defines the second milestone at its own `<scope>` and runs [Starting a milestone](#starting-a-milestone)'s lines on its `<path>`, so the starting state, the first review pass's open questions, their alternatives, and a recommendation on each are committed for it while the other milestone's chains run unchanged on their own path. It is no special case of either chain: no milestone is current, so two chains in one project differ only in the path every line carries, and each line below takes the second milestone's `<path>`, the one its own definition line recorded. The starting state describes the project as it stands when the line runs, so rerun that line, and the review after it, if the milestone still executing changes what it describes. The chain can run while the other milestone's `complete-all-tasks` is still working in the same tree: a completion subagent stages nothing, leaving its edits uncommitted until its orchestrator commits that task from the path file it wrote, and every commit names its own paths as its pathspec, so a completion subagent's files never ride into an annotating pass's commit, nor into the answer sweep's when you go on to record this milestone's recommendations with `answer-all-open-questions-with-recommendation --milestone <path>`; a git write that meets the other run's lock is repeated for a few seconds rather than failing at once. The tree is dirty while both run, and each commit still carries only its own paths. The second milestone's tasks wait at the scope gate: while the milestone still executing is started and its scope is the second's, encloses it, or lies beneath it, `derive-tasks --milestone <path>` stops on the gate's fixed line, the holder's path below it, until that milestone is finished, while two milestones in disjoint scopes derive and complete their tasks at once.

```sh
claude -p "/cairn:define-milestone-goal --at <scope> <goal>" --dangerously-skip-permissions --model "sonnet" --effort medium;
claude -p "/cairn:specify-milestone-starting-state --milestone <path>" --dangerously-skip-permissions --model "fable" --effort xhigh;
claude -p "/cairn:review-milestone-requirements --milestone <path>" --dangerously-skip-permissions --model "fable" --effort xhigh;
claude -p "/cairn:provide-alternatives-to-all-open-questions --milestone <path>" --dangerously-skip-permissions --model "opus" --effort high;
claude -p "/cairn:recommend-all-open-questions --milestone <path>" --dangerously-skip-permissions --model "fable" --effort xhigh;
```

## Finishing a milestone

Run this when the milestone's `TASKS_TODO.md` is empty and no open question stands: it removes the milestone's directory in one `Milestone-finish: <path>` commit whose body is the milestone's summary, its title line, a blank line, and its accomplishment bullets, and updates `CLAUDE.md` in the same commit for lasting changes. Nothing is cleared, since nothing was current: the milestone's files stand at that commit's parent, the plugin's milestones tool prints the summary back as the milestone's record, and reverting the commit makes the milestone live again.

```sh
claude -p "/cairn:finish-milestone --milestone <path>" --dangerously-skip-permissions --model "sonnet" --effort medium;
```
