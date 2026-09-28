# Milestone 36: Non-interactive milestone activation

## Goal

`/goto-next-milestone` runs without asking anything. It activates the lowest-numbered milestone directory that isn't listed in `## Milestone History`. It stops only in two cases: the `Current milestone:` pointer doesn't read `none` (it tells you to run `/finish-current-milestone`), or no undone milestone exists (it tells you to run `/define-milestone-goal`). The single-candidate confirmation and the multiple-candidate choice are removed, the terse `Milestone activated.` line stays, and `docs/skill-reference.md`, `docs/ways-of-using-cairn.md` and the rebuilt host trees are updated to match.

## Relevant starting state

### The `goto-next-milestone` skill

The skill lives at `core/skills/goto-next-milestone/SKILL.md` and takes no arguments. Its step 1 reads the `Current milestone:` line of `milestones/README.md` and stops with a pointer at `/finish-current-milestone` when the value is not `none`. Its step 2 collects every `milestone_<N>_<slug>/` directory under `milestones/`, subtracts the ones listed in `## Milestone History`, and branches three ways on the remainder: zero candidates stops with a pointer at `/define-milestone-goal`, one candidate confirms the path and title with the user before proceeding, and multiple candidates lists them and asks the user which to activate, with the zero-stripped integer rule for the number stated only inside that third branch. Steps 3 to 5 overwrite the pointer line, commit `milestones/README.md` through `{{PLUGIN_ROOT}}/shared/commit-procedure.md` under `Milestone-activation: milestone_<number>_<slug>`, and print the fixed `Milestone activated.` line, with a distinct no-change line when the dirty-own-path guard fires. The file's last change was a milestone-11 `Tasklist-completion:` commit that added the terse reporting; the candidate logic has not changed since.

### How `milestones/README.md` records done milestones

`## Milestone History` entries are headed `### Milestone N — Title` with accomplishment bullets, prepended by `/finish-current-milestone` step 5; they carry the integer number and the title, never the directory name. The same finish step appends a `| N | Title | <backticked path> |` row, the path spelled `milestones/milestone_<NN>_<slug>/`, to the `## Completed Milestones` table, which is the only place in the README that pairs a done milestone with its directory path. The bootstrap skill's README template keeps both sections and notes that the table is written by `/goto-next-milestone`, a stale attribution since the finish skill writes it. Pre-split milestones 1 to 27 appear in both structures like every other milestone. `core/shared/get-current-milestone.md` defines the pointer format the skill overwrites: `Current milestone: none` bare, or a backticked `milestones/milestone_<NN>_<slug>/` path.

### Milestone directory naming

`/define-milestone-goal` names directories `milestone_<NN>_<slug>` with `<NN>` zero-padded to two digits, takes the next number as max-plus-one over existing directories, and refuses a number already taken under any slug, so numbers are unique and monotone. It never touches the pointer, so a defined milestone is a candidate until activated and finished.

### Documentation naming the skill

`docs/skill-reference.md` has one `goto-next-milestone` entry (a scan for a defined-but-not-active directory, pointer update, no files created, runnable only after the finish) and mentions the skill again in the `finish-current-milestone` entry. `docs/ways-of-using-cairn.md` opens its "Starting a milestone" chain with `claude -p "/cairn:goto-next-milestone"` under `--dangerously-skip-permissions`, describes it as activating the milestone once the pointer reads `none`, and its "Setting up a project" chain hands off to that chain with the pointer at `none`; neither passage mentions the confirmation or choice prompts. `docs/workflow.md` says the skill advances the pointer, and `docs/design-claims.md` does not name it. `core/skills/finish-current-milestone`, `define-milestone-goal`, `ask-in-milestone-context`, and `init-milestone-base-workflow` each mention the skill once as the activation step, none describing its prompts.

### Host build output

Both `hosts/claude/skills/goto-next-milestone/SKILL.md` and `hosts/antigravity/skills/goto-next-milestone/SKILL.md` are byte-for-byte renders of the core file differing only in the `{{PLUGIN_ROOT}}` substitution, checked by `uv run scripts/build_hosts.py --check` in CI. No test covers skill prose; the pytest suite covers only the open-question tool.

### Other interactive prompts in the skill layer

Besides this skill's two prompts, only `answer-open-question-with-alternative` (asks why an alternative was preferred when no rationale is given) and `capture-milestone-principle-updates` (one confirmation gating its commit) ask the user anything on a success path; every other file-changing skill runs to its commit without a question.

## Decisions

## Out of Scope

