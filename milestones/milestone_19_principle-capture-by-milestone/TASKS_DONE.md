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
