# Milestone workflow guidance (shared)

This is the single source of truth for the `## Milestone Workflow` section of
`CLAUDE.md`, the guidance that tells anyone working in the project where milestones live
and how each is named and finished. `init-milestone-base-workflow` writes it into a project
whose `CLAUDE.md` lacks it, and `migrate-milestones` rewrites an older section to it; each
states which of the cases below it writes, and this file states what the section is and how
each case writes it.

## The section

The section is this heading and paragraph, exactly:

```markdown
## Milestone Workflow

This project uses the milestone-driven workflow. Each milestone lives at
`<scope>/milestones/<slug>/`, under the `milestones/` container of the directory holding the
core of its work, with `requirements.md`, `open_questions.xml`, and `TASKS_TODO.md`. No
milestone is current: every skill working inside one is given its path as
`--milestone <path>`, exactly as `/define-milestone-goal` printed it, trailing slash included.
A milestone directory is removed only by `/finish-milestone`, whose `Milestone-finish: <path>`
commit carries the milestone's record, so the directories standing are the live milestones and
the git log holds the finished ones.
```

Never write a milestone path into it, and never document the project's environment context in
it.

## Writing it

- **`CLAUDE.md` does not exist** — create it with this minimal content, the section
  last:

  ```markdown
  # CLAUDE.md

  This file provides guidance to the coding agent working in this repository.

  <the section>
  ```

- **`CLAUDE.md` exists and holds no `## Milestone Workflow` section** — append the
  section to the end of the file, leaving every existing line untouched.
- **`CLAUDE.md` holds a `## Milestone Workflow` section** — replace that section whole,
  from its heading line down to the line before the next `# ` or `## ` heading, or to the end of
  the file when none follows, with the section, leaving every line outside it untouched.
