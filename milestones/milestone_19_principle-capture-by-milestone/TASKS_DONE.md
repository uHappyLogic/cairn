# TASKS DONE

## Capture Takes Required Milestone Id Argument

Rework `skills/capture-milestone-principle-updates/SKILL.md` so it requires a `<milestone_id>` argument — the directory name under `milestones/` exactly as `specify-milestone-starting-state` takes it — resolved as `milestones/<milestone_id>/` with a clean stop when that directory has no `requirements.md`, replacing the last-row-of-Completed-Milestones resolution and the pointer-none framing, and consuming the id verbatim in the path-scoped git-log prefix and the `Principle-capture: <milestone_id>` subject. The skill's usage and opening prose describe it as on-demand for any milestone id whose `requirements.md` exists (current, unfinished, or already finished, with finish the natural but never required moment), and its frontmatter description is reworded within 25 words to drop the "just-finished" framing. Verified when the skill mentions no Completed Milestones table or current-milestone pointer, the description loads under `yaml.safe_load`, and the regenerated `.agents/plugins/cairn/` tree matches the source.

**Verified:**

- `skills/capture-milestone-principle-updates/SKILL.md` `## Usage` shows `/capture-milestone-principle-updates <milestone_id>` with `<milestone_id>` required and described as the milestone directory name under `milestones/` (e.g. `milestone_12_user-guide`), exactly as `/specify-milestone-starting-state` takes it, with no bare-number form and no number-to-directory resolution.
- Step 1 resolves `milestones/<milestone_id>/` and stops cleanly, changing nothing, when `milestones/<milestone_id>/requirements.md` does not exist (listing the present `milestone_*` directories); the last-row-of-Completed-Milestones resolution and the pointer-`none` framing are gone.
- The id is consumed verbatim in the path-scoped git-log prefix (`-- milestones/<milestone_id>/requirements.md`, step 2) and in the `Principle-capture: <milestone_id>` commit subject (step 5).
- The opening prose and usage describe the skill as on-demand for any milestone id whose `requirements.md` exists (current, unfinished, or already finished), with running after `/finish-current-milestone` stated as the natural moment and never a precondition.
- `grep -i` over the skill for `Completed Milestones`, `current-milestone`, `get-current-milestone`, `just-finished`, `finish-time`, and `last row` finds no mention of the Completed Milestones table or the current-milestone pointer.
- The frontmatter `description` is reworded within 25 words (15), drops the "just-finished" framing, contains no colon or semicolon, and loads unquoted under `yaml.safe_load`.
- `uv run scripts/migrate_skills_to_agy.py` regenerated `.agents/plugins/cairn/`; only the capture skill copy changed, and it differs from the source solely by the expected `${CLAUDE_PLUGIN_ROOT}` path rewrite and dropped `echo` hint.

---

## Repeat Capture And Dirty Store Guards

Add two start-of-run guards to the capture skill, each a one-line notice plus a single proceed confirmation and never a stop: before the commit walk, grep the history for the exact both-ends-anchored subject `Principle-capture: <milestone_id>` and on a hit name the prior commit; and when `milestones/answer_decision_principles.md` already carries uncommitted changes, notice-and-confirm, then use the working-tree file rather than `HEAD` as the baseline the rewrite composes over. Verified when the skill states both guards with their exact anchoring, runs unchanged on no hit, and writes no empty commit to record a no-op run.

**Verified:**

- A new `### 2. Start-of-run guards` step sits between `### 1. Locate the milestone` and the commit walk (now step 3), and both guards are stated as a one-line notice plus a single proceed confirmation, never a stop (declining is the user's clean stop, reported in one line with nothing changed or committed).
- The repeat-capture guard greps history for the exact both-ends-anchored subject `git log --grep='^Principle-capture: <milestone_id>$'` with the id verbatim from step 1, and on a hit its notice names the prior commit (short hash, date, subject).
- The dirty-store guard checks `git status --porcelain -- milestones/answer_decision_principles.md` and, on proceed, names the working-tree file (not `HEAD`) as the baseline every later step reads and the store rewrite composes over; step 5's whole-store read now says it reads that working-tree baseline.
- With no hit a guard prints nothing and asks nothing, and the run continues unchanged; both guard commands were dry-run against this repo (zero `Principle-capture:` hits, clean store) as the no-hit case.
- The skill states that no empty commit records a no-op run (so a prior nothing-changed run is not detected, accepted as harmless), and the commit step sends a nothing-written pass straight to the report without invoking `shared/commit-procedure.md`, whose dirty-own-path guard would otherwise commit the user's admitted store edits under `Principle-capture:`.
- Headings run 1–7 (with 5a) and every intra-file step cross-reference (usage note, step 1, empty-range and no-candidate exits, schema pointer, report cases) resolves to the renumbered step; no `## Rules` section exists.
- Frontmatter is unchanged and loads under `yaml.safe_load` (15-word description, no colon or semicolon); `uv run scripts/migrate_skills_to_agy.py` regenerated `.agents/plugins/cairn/`, changing only the capture skill copy, which differs from the source solely by the `${CLAUDE_PLUGIN_ROOT}` path rewrite and dropped `echo` hint.

---
