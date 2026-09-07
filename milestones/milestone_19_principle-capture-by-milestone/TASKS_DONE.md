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

## Walk All Three Answer Provenances With Diffs

Replace the `Manual-answer:`-only commit walk with a path-scoped `git log` over `<MILESTONE_DIR>/requirements.md` matching all three subjects (`Manual-answer:`, `Alternative-answer:`, `Recommendation-answer:`), reading for each commit its subject, body, and the diff's removed `<open-question>` block to reconstruct the `<recommendation option>`, the `<applied-principle>` citations, and the alternatives the user saw. Each commit is then classified by two tests in order — agreement of the recorded option against the removed recommendation, where a block with no recommendation counts as a non-override manual answer, then deliberated-vs-bare body by the existing bare-cold-answer test — producing the per-commit record the later steps consume. Verified when the walk step can be followed against this repo's milestone 11, 14, or 17 answer commits to yield the right provenance, agreement, and body classification for each.

**Verified:**

- Step 3 (`### 3. Walk the milestone's answer commits`) no longer describes a `Manual-answer:`-only walk; its collection command is the path-scoped `git log --format='%h %s' -E --grep='^(Manual-answer|Alternative-answer|Recommendation-answer): ' -- milestones/<milestone_id>/requirements.md`, with the path filter kept as the sole boundary and the empty-range exit to step 7 preserved.
- For each commit the step reads subject, body, and diff (`git show <hash> --format='%s%n%n%b' -- …`) and reconstructs from the removed lines the answered `<open-question>` block — keyed on the `id` matching the subject's Short Title so cascaded sibling removals are excluded — yielding the `<recommendation option>` and rationale, every `<applied-principle>` citation, and each `<alternative id>` with its what-it-is text and `<advantage>`/`<drawback>` children, entity-unescaped; a bare `<question>`-only block or a pre-block-form blockquote is the stated no-recommendation case.
- Classification is stated as two tests in order: agreement of the recorded option (derived per provenance — body-before-em-dash for lifted answers, named/matched alternative for manual ones) against the removed recommendation's `option`, with a no-`<recommendation>` block classed `non-override` before any comparison; then deliberated-vs-bare body by the existing bare-cold-answer test, trailers stripped, with every `Alternative-answer:`/`Recommendation-answer:` body `bare` by construction.
- A named per-commit record with explicit fields (`hash`, `provenance`, `short_title`, `body`, `recorded_decision`, `question`, `alternatives`, `applied_principles`, `recommendation`, `recorded_option`, `agreement`, `body_class`) is defined as what steps 4 and 5 consume.
- Dry-running the step's commands against milestones 11, 14, and 17 yielded the right classification for every commit: all 20 `Recommendation-answer:` commits `agrees`, all four `Alternative-answer:` commits `overrides` (4716cce, 325ca01, 514ff81, 7165d5d), every body `bare`, and `<applied-principle>` citations only on 7621a66, 135179f, and dc3fbc9.
- Frontmatter is unchanged and loads under `yaml.safe_load` (15-word description, no colon or semicolon); no `## Rules` section exists; step numbering 1–7 is unchanged so every intra-file cross-reference still resolves.
- `uv run scripts/migrate_skills_to_agy.py` regenerated `.agents/plugins/cairn/`; only the capture skill copy changed, differing from the source solely by the step-6 `${CLAUDE_PLUGIN_ROOT}` path rewrite and dropped `echo` hint.

---

## Override Rationale Prompts With Best Guesses

Add a prompting step that asks the user why the alternative was preferred only for override commits carrying no user rationale — every non-agreeing `Alternative-answer:` and a non-agreeing `Manual-answer:` whose body is the bare literal answer — showing the skill's best guess derived from the removed alternatives, recommendation, and recorded option, skippable per prompt, with the run opening on a one-shot choice to accept every guess or skip every prompt; deliberated manual bodies and agreeing answers are never prompted. Verified when the prompt step states exactly these eligibility rules, the best-guess display, and the one-shot opener.

**Verified:**

- A new top-level `### 4. Prompt for override rationales` step sits between `### 3. Walk the milestone's answer commits` and phase 1; the former steps 4–7 (and 5a) are renumbered 5–8 (and 6a), and every intra-file step cross-reference (usage note, step 1, guards, empty-range and no-candidate exits, body-test pointer, schema pointer, commit and report steps) resolves to the renumbered step.
- The step states the eligibility rule exactly: a commit is prompted only when its record has `agreement` = `overrides` and `body_class` = `bare` — every non-agreeing `Alternative-answer:` and a non-agreeing `Manual-answer:` whose body is the bare literal answer — and states that deliberated `Manual-answer:` bodies and agreeing answers (every `Recommendation-answer:`, plus any agreeing `Alternative-answer:`/`Manual-answer:`) are never prompted, with non-override manual answers likewise unprompted (no recommendation existed to prefer the answer over) while staying a principle source.
- Each prompt shows the Short Title and question, the recommended option with its rationale digest, the recorded option, and the skill's best guess at the override reason derived from the removed alternatives, the removed recommendation, and the recorded option (or the recorded decision for a fresh option), and is skippable individually (accept the guess / state own reason / skip).
- The prompting opens with a one-shot choice — accept every best guess, skip every prompt, or review one at a time — asked once and only when at least one commit is eligible; with none eligible the step prints nothing and asks nothing.
- The step's output is an `override_rationale` field added to the step-3 per-commit record (accepted guess or typed reason; `none` when unprompted or skipped), and phase 1's extraction reads it in place of the bare body for a prompted commit.
- Frontmatter is unchanged and loads under `yaml.safe_load` (15-word description, no colon or semicolon); no `## Rules` section exists anywhere under `skills/`, `agents/`, or `shared/`.
- `uv run scripts/migrate_skills_to_agy.py` regenerated `.agents/plugins/cairn/`; only the capture skill copy changed, and it differs from the source solely by the `${CLAUDE_PLUGIN_ROOT}` path rewrite and dropped `echo` hint.

---
