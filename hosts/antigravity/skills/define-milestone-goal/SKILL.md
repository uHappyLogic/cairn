---
name: define-milestone-goal
description: Create a new milestone directory with its four starting files from the provided goal description.
---

# define-milestone-goal

Creates a new milestone directory under `milestones/` holding the four files every milestone starts with — `requirements.md`, `open_questions.xml`, `TASKS_TODO.md`, and `TASKS_DONE.md` — all created by the plugin's milestone-definition tool, which also works out the milestone's number and directory name. Your only work is choosing the milestone's title, handing the tool's output to the commit procedure, and reporting the result; the files are filled in by the skills that follow (`/specify-milestone-starting-state`, `/review-milestone-requirements`, etc.). Defining a milestone does not activate it: this skill never updates `CLAUDE.md` or `milestones/README.md`, which change only when the milestone becomes the *current* active one via `/goto-next-milestone`.

## Usage

```
/define-milestone-goal <overall_goal_description>
```

- `<overall_goal_description>`: a clear description of what the milestone should accomplish. Use `/discuss-milestone-goal` first if the goal is still vague.

**Example:**
```
/define-milestone-goal add a getting-started guide that walks a new user through their first session
```

## Workflow

### 1. Choose the title

Read `<overall_goal_description>` and choose a short title that names the milestone's objective (e.g. `Getting-started guide` for the example above). The tool derives the directory name from the title's first words, so lead with the words that identify the milestone.

### 2. Create the milestone

From the workspace root, run the tool once, passing the title as one quoted argument and `<overall_goal_description>` unchanged on standard input through a **quoted-delimiter heredoc** (`<<'EOF'`, so nothing inside is expanded; pick a delimiter line the goal text does not contain):

```
python3 .agents/plugins/cairn/tools/define_milestone.py --title "<title>" <<'EOF'
<overall_goal_description>
EOF
```

On success the tool prints exactly two lines: the commit subject, then the milestone directory path. Hold both unchanged for step 3; compose, reword, and re-derive neither.

If the call fails — the shell cannot find `python3`, or the tool exits non-zero with one `Error: <reason>` line on stderr — stop here and report it in full, quoting the shell's or the tool's line verbatim (a missing interpreter is the Python 3.9+ prerequisite `/init-milestone-base-workflow` checks for). The tool leaves nothing behind on failure, so there is nothing to clean up and nothing to commit.

### 3. Commit the new milestone

Read and follow the shared commit procedure at `.agents/plugins/cairn/shared/commit-procedure.md`, carrying out its steps yourself. Supply it these two inputs, both exactly as the tool printed them in step 2:

- **PATHS** — the milestone directory path, the tool's second line; the directory holds exactly the four files the tool just created.
- **SUBJECT** — the tool's first line.

The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit.

### 4. Confirm

On the success path — the commit in step 3 recorded the new milestone — print exactly one fixed terse status line and nothing else:

```
Milestone defined.
```

Do not add the created directory path, the title, the goal text, or a next-step pointer.

If instead the step-3 dirty-own-path guard fired (nothing under the milestone directory changed, so nothing was committed), do not print the terse line — print a single concise line stating that nothing changed and briefly why, e.g. `No change — the milestone directory holds no uncommitted files; nothing committed.`
