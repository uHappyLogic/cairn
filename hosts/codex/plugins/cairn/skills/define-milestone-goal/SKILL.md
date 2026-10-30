---
name: define-milestone-goal
description: Create a new milestone directory with its three starting files from the provided goal description.
---

# define-milestone-goal

Creates a new milestone directory at `<scope>/milestones/<slug>/`, under the `milestones/` container of the scope you name, holding the three files every milestone starts with — `requirements.md`, `open_questions.xml`, and `TASKS_TODO.md` — all created by the plugin's milestone-definition tool, which also derives the directory name from the title and creates the container when it is missing. Your only work is choosing the milestone's title, handing the tool's output to the commit procedure, and reporting the result; the files are filled in by the skills that follow (`/specify-milestone-starting-state`, `/review-milestone-requirements`, etc.). Defining a milestone does not activate it: this skill never updates `AGENTS.md` or `milestones/README.md`, which change only when the milestone becomes the *current* active one via `/goto-next-milestone`.

## Usage

```
/define-milestone-goal --at <scope> <overall_goal_description>
```

- `--at <scope>`: required, with no default — the directory holding the core of the milestone's work, relative to the workspace root, `.` for the root. Use the directory `/discuss-milestone-goal` proposed, as given; it must already exist.
- `<overall_goal_description>`: a clear description of what the milestone should accomplish. Use `/discuss-milestone-goal` first if the goal is still vague.

**Example:**
```
/define-milestone-goal --at docs add a getting-started guide that walks a new user through their first session
```

## Workflow

### 0. Read the scope

The flag is present only when the first whitespace-separated token of the invocation text is exactly `--at`. Its value, `<scope>`, is the token right after it; strip those two tokens and the whitespace following them, and what remains is `<overall_goal_description>`. Take `<scope>` verbatim: normalizing it, and refusing a scope that is absolute, climbs out of the workspace root, or is not an existing directory, is the tool's. When the first token is anything else, or `--at` has no token after it, **stop without changing anything** and report the fixed line `Milestone not defined — no --at scope was given.` first, with the usage line `/define-milestone-goal --at <scope> <overall_goal_description>` below it.

### 1. Choose the title

Read `<overall_goal_description>` and choose a short title that names the milestone's objective (e.g. `Getting-started guide` for the example above). The tool derives the directory name from the title's first words, so lead with the words that identify the milestone.

### 2. Create the milestone

From the workspace root, run the tool once, passing the scope and the title each as one quoted argument and `<overall_goal_description>` unchanged on standard input through a **quoted-delimiter heredoc** (`<<'EOF'`, so nothing inside is expanded; pick a delimiter line the goal text does not contain):

```
python3 ${PLUGIN_ROOT}/tools/define_milestone.py --at "<scope>" --title "<title>" <<'EOF'
<overall_goal_description>
EOF
```

On success the tool prints exactly two lines: the commit subject, then the milestone's path, in its canonical repo-relative form with its trailing slash. Hold both unchanged for step 3; compose, reword, and re-derive neither.

If the call fails — the shell cannot find `python3`, or the tool exits non-zero with one `Error: <reason>` line on stderr — stop here and report it in full: the fixed line `Milestone not defined — the definition tool failed.` first, then the shell's or the tool's line verbatim below it (a missing interpreter is the Python 3.9+ prerequisite `/init-milestone-base-workflow` checks for). The tool leaves nothing behind on failure, so there is nothing to clean up and nothing to commit.

### 3. Commit the new milestone

Read and follow the shared commit procedure at `${PLUGIN_ROOT}/shared/commit-procedure.md`, running its one commit-tool command yourself as this step's one git tool call. Supply it these two inputs, both exactly as the tool printed them in step 2:

- **PATHS** — the milestone path, the tool's second line; the directory holds exactly the three files the tool just created.
- **SUBJECT** — the tool's first line.

The commit tool runs the dirty-own-path guard, the path-scoped staging, and the commit.

### 4. Confirm

On the success path — the commit in step 3 recorded the new milestone — print exactly one fixed terse status line and nothing else:

```
Milestone defined.
```

Do not add the created directory path, the title, the goal text, or a next-step pointer.

If instead the step-3 commit tool printed `Nothing committed — none of the paths changed.` (nothing under the milestone directory changed, so nothing was committed), do not print the terse line — print this one fixed line and nothing else:

```
Milestone not committed — its directory held no uncommitted file.
```
