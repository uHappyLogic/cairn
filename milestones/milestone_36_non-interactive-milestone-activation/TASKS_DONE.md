# TASKS DONE

## Define Candidates By Number And History Headings

Rewrite the candidate-collection half of step 2 in `core/skills/goto-next-milestone/SKILL.md` so a candidate is a directory matching `milestone_<digits>_<slug>` whose number is read by stripping leading zeros and compared as an integer, stated as a standalone sentence, with a `milestone_*` directory whose prefix is not all digits silently left out of the set, adding no third stop and no advisory. A directory counts as done when that number matches an integer N parsed from a `### Milestone N — Title` heading under `## Milestone History`, with the `## Completed Milestones` table never consulted. Verified by reading the step and by `uv run scripts/build_hosts.py --check` passing against the rebuilt host trees.

**Verified:**

- Step 2 of `core/skills/goto-next-milestone/SKILL.md` defines a candidate as a directory matching `milestone_<digits>_<slug>`, with the standalone sentence that its number is read by stripping leading zeros and compared as an integer.
- Step 2 states that a `milestone_*` directory whose prefix is not all digits is silently left out of the candidate set, and the step adds no third stop and no advisory (the remainder branches are still exactly zero, one, and multiple candidates).
- Step 2 counts a directory as done when its number matches an integer N parsed from a `### Milestone N — Title` heading under `## Milestone History`, and says the `## Completed Milestones` table is never consulted.
- `uv run scripts/build_hosts.py` rebuilt both host trees and `uv run scripts/build_hosts.py --check` passed against them.

---

## Activate Lowest Candidate Without Prompts

Replace the three-way branch on the remainder in step 2 of `core/skills/goto-next-milestone/SKILL.md` with activating the lowest-numbered candidate outright, removing the single-candidate confirmation and the multiple-candidate choice and adding no target argument. The skill stops only when step 1 finds the `Current milestone:` pointer not reading `none` (pointing at `/finish-current-milestone`) or when no candidate exists (pointing at `/define-milestone-goal`), while steps 3 to 5 keep the pointer overwrite, the `Milestone-activation:` commit, and the fixed `Milestone activated.` line. Verified by reading the file for no question to the user on any path and by `uv run scripts/build_hosts.py --check` passing against the rebuilt host trees.

**Verified:**

- Step 2 of `core/skills/goto-next-milestone/SKILL.md` no longer branches three ways on the remainder: with candidates it activates the lowest-numbered one outright, and the single-candidate confirmation and the multiple-candidate choice are gone.
- The Usage section still takes no arguments; no target argument was added.
- The skill stops only in step 1 when the `Current milestone:` pointer does not read `none` (pointing at `/finish-current-milestone`) and in step 2 when no candidate exists (pointing at `/define-milestone-goal`).
- Steps 3 to 5 still overwrite the pointer line, commit `milestones/README.md` under `Milestone-activation: milestone_<number>_<slug>`, and print the fixed `Milestone activated.` line.
- Reading the whole file finds no question to the user on any path.
- `uv run scripts/build_hosts.py` rebuilt both host trees and `uv run scripts/build_hosts.py --check` passed against them.

---

## Reword No-Change Branch Example Reason

In step 5 of `core/skills/goto-next-milestone/SKILL.md`, keep the no-change branch but rewrite its example reason to say only that the pointer line already matched the last commit, dropping the claim that the pointer already named that milestone, which step 1 has just contradicted. The branch still prints its one distinct no-op line, never `Milestone activated.`, and commits nothing. Verified by reading the step and by `uv run scripts/build_hosts.py --check` passing against the rebuilt host trees.

**Verified:**

- Step 5 of `core/skills/goto-next-milestone/SKILL.md` keeps the no-change branch for when the step-4 dirty-own-path guard fires.
- The branch's example reason reads `No change — the pointer line already matched the last commit; nothing committed.`, saying only that the pointer line matched the last commit, and no longer claims the pointer already named that milestone.
- The branch still prints its one distinct no-op line, never `Milestone activated.`, and commits nothing.
- `uv run scripts/build_hosts.py` rebuilt both host trees and `uv run scripts/build_hosts.py --check` passed against them.

---

## Delete Bootstrap README Template Note

Delete the blockquote under the README template in `core/skills/init-milestone-base-workflow/SKILL.md` that credits the `## Completed Milestones` table to `/goto-next-milestone`, without rewording it, so the template's two sections stay and no sentence names which skill writes or reads them. Verified by reading the template and by `uv run scripts/build_hosts.py --check` passing against the rebuilt host trees.

**Verified:**

- The blockquote under the README template in step 5 of `core/skills/init-milestone-base-workflow/SKILL.md` that credited `## Completed Milestones` to `/goto-next-milestone` is deleted outright, with no replacement sentence (the diff is two removed lines, the quote and its trailing blank).
- The README template still carries both the `## Milestone History` section and the `## Completed Milestones` table.
- No sentence in the file names which skill writes or reads either section; the only remaining mentions of them are the template's own headings.
- `uv run scripts/build_hosts.py` rebuilt both host trees and `uv run scripts/build_hosts.py --check` passed against them.

---
