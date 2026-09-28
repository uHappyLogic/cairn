# TASKS DONE

## Define Candidates By Number And History Headings

Rewrite the candidate-collection half of step 2 in `core/skills/goto-next-milestone/SKILL.md` so a candidate is a directory matching `milestone_<digits>_<slug>` whose number is read by stripping leading zeros and compared as an integer, stated as a standalone sentence, with a `milestone_*` directory whose prefix is not all digits silently left out of the set, adding no third stop and no advisory. A directory counts as done when that number matches an integer N parsed from a `### Milestone N — Title` heading under `## Milestone History`, with the `## Completed Milestones` table never consulted. Verified by reading the step and by `uv run scripts/build_hosts.py --check` passing against the rebuilt host trees.

**Verified:**

- Step 2 of `core/skills/goto-next-milestone/SKILL.md` defines a candidate as a directory matching `milestone_<digits>_<slug>`, with the standalone sentence that its number is read by stripping leading zeros and compared as an integer.
- Step 2 states that a `milestone_*` directory whose prefix is not all digits is silently left out of the candidate set, and the step adds no third stop and no advisory (the remainder branches are still exactly zero, one, and multiple candidates).
- Step 2 counts a directory as done when its number matches an integer N parsed from a `### Milestone N — Title` heading under `## Milestone History`, and says the `## Completed Milestones` table is never consulted.
- `uv run scripts/build_hosts.py` rebuilt both host trees and `uv run scripts/build_hosts.py --check` passed against them.

---
