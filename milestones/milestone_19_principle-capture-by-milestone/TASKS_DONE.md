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

## Override Candidates And Acceptance Evidence

Rework phase 1 so new principle candidates are distilled only from override commits — a deliberated or prompted override rationale, plus non-override and deliberated agreeing `Manual-answer:` bodies — keeping the non-generalizable filter and the cross-candidate dedup, while accepted recommendations and agreeing answers supply evidence only: each removed `<applied-principle>` reinforces its store entry and shields it from prune or narrowing in this pass, and an accepted rationale contradicting an existing entry flags that entry for the salvage path. Verified when the skill states that an accepted `Recommendation-answer:` never yields a candidate, that an agreeing `Alternative-answer:` yields none while a deliberated agreeing `Manual-answer:` still does, and that both evidence signals fall out of the diff read.

**Verified:**

- Phase 1 (step 5) step 1 states candidate sources exactly: an override commit's reasoning — its step-4 `override_rationale` when filled, otherwise its `body` when `body_class` = `deliberated` — plus every `non-override` `Manual-answer:` body and every deliberated agreeing `Manual-answer:` body; a skipped bare override yields none, and nothing else yields a candidate.
- The skill states that an accepted `Recommendation-answer:` never yields a candidate (its body is the recommender's own lifted reasoning, so it cannot supply the guideline the recommender lacked).
- The skill states that an agreeing `Alternative-answer:` yields no candidate (its body is only the chosen alternative's text) while a deliberated agreeing `Manual-answer:` still does through its body, with source eligibility governed by the reasoning a commit carries, never its subject alone.
- The non-generalizable filter (restatement / bare cold answer drop, many-to-many mapping, with its drop/keep examples) and the cross-candidate dedup (cluster survivors, rank strongest-first) remain in phase 1 as steps 2 and 3.
- Phase 1 step 4 states both evidence signals from the agreeing commits (every accepted `Recommendation-answer:`, plus any agreeing `Alternative-answer:`/`Manual-answer:`): each removed `<applied-principle>` reinforces the store entry it names and shields it from being pruned or narrowed in this pass (an agreeing manual/alternative answer reinforcing exactly as an accepted recommendation does), and an accepted rationale contradicting an existing entry flags that entry for the salvage path, with a reinforced-and-flagged entry keeping its shield.
- The skill states that both signals fall out of the diff read: they are read from the `applied_principles` and `recommendation` fields the step-3 diff read already filled, with no further read of git or the store.
- Phase 1's output names both the ranked candidate set and the evidence set (reinforced entries with their citing commits, flagged entries with the contradicting commit); phase 2 reads the evidence set — a revision never prunes or narrows a reinforced entry, and each unresolved flagged entry is walked after the candidates for a salvage decision — and the nothing-captured exit fires only with no surviving candidate and no flagged entry.
- Frontmatter is unchanged and loads under `yaml.safe_load` (15-word description, no colon or semicolon); no `## Rules` section exists anywhere under `skills/`, `agents/`, or `shared/`.
- `uv run scripts/migrate_skills_to_agy.py` regenerated `.agents/plugins/cairn/`; only the capture skill copy changed, and it differs from the source solely by the `${CLAUDE_PLUGIN_ROOT}` path rewrite and dropped `echo` hint.

---

## Compose Whole-Store Rewrite In Place

Replace the per-candidate confirm-and-write loop with a single composition of the entire proposed store — adds, revisions, prunes, merges, generalizations, and shortenings applied together over the baseline — written directly to `milestones/answer_decision_principles.md` after taking a snapshot of the store immediately before the first write, printing no diff and no store content to the conversation. Substantive change to an entry requires the harvested milestone's own evidence, while form-only hygiene may reach any entry: directives target roughly 40-80 words and are flagged for shortening past about 100 with the "as short as it can be while still reading as an intuitive rule" test deciding, plainly duplicate entries merge, there is no ceiling on entry count, and the optional `*Origin:*` line survives as a single-line pointer. Verified when the write step describes one in-place rewrite under these rules and the `### <Short Title>` entry schema is preserved.

**Verified:**

- Step 6 (`### 6. Phase 2 — compose the whole-store rewrite and write it in place`) no longer describes a per-candidate confirm-and-write loop — no "one candidate at a time", no per-candidate confirmation, no re-scan between writes — and instead describes one composition of the entire proposed store (adds, revisions, prunes, merges, generalizations, shortenings applied together over the step-2 working-tree baseline) landing in a single in-place write of `milestones/answer_decision_principles.md`, with the write stated as not the confirmation (the user reviews the working-tree change with `git diff`; the confirmation gates step 7's commit).
- The step takes a snapshot of the store immediately before the first write (`SNAPSHOT="$(mktemp)" && cp milestones/answer_decision_principles.md "$SNAPSHOT"`, recorded as *absent* when the store does not exist), names it — not `HEAD` — as the restore point, and states twice that no diff and no store content is printed to the conversation.
- The evidence gate is stated: a substantive change (adding, or pruning/narrowing/generalizing/replacing what an entry decides) requires the harvested milestone's own evidence (an overlapping candidate or a flag), while form-only hygiene (shortening past the ~100-word flag, merging plain duplicates) may reach any entry with the applied test unchanged; an unevidenced, in-bar, non-duplicate entry passes through verbatim.
- The compactness bar reads roughly 40–80 words, flagged for shortening past about 100, with "as short as it can be while still reading as an intuitive rule" as the deciding standard (soft target, not a hard cap); there is no ceiling on entry count (prune and merge are the only count control); the `*Origin:*` line survives as a single-line pointer; reinforced entries are shielded from prune or narrowing; a composed store identical to the baseline writes nothing and exits to step 8.
- Step 6a preserves the `### <Short Title>` entry schema (heading handle, prose directive now noting the compactness bar, optional single-line `*Origin:*`, no status field), and steps 7 and 8 reference the new "composed store identical to its baseline (step 6)" no-op case in place of the retired "declined every candidate" one; every intra-file step reference (1–8, 6a) resolves.
- Frontmatter is unchanged and loads under `yaml.safe_load` (15-word description, no colon or semicolon); no `## Rules` section exists under `skills/`, `agents/`, or `shared/`.
- `uv run scripts/migrate_skills_to_agy.py` regenerated `.agents/plugins/cairn/`; only the capture skill copy changed, and it differs from the source solely by the `${CLAUDE_PLUGIN_ROOT}` path rewrite and dropped `echo` hint.

---

## Contradicted Entry Salvage Ladder

State in the rewrite composition how an entry contradicted by current reasoning is salvaged, attempted in this fixed order: narrow its scope clause, generalize it so the prior accepted citations and the override both fit, replace it with a fresh directive when its premise is wrong, and delete it only when nothing survives, breaking a tie between forms by whichever yields the shortest entry that still predicts both. Entries reinforced by a citation in the same pass stay shielded from prune or narrowing. Verified when the skill lists the four forms in this order with the tie-break and the shield, and notes the chosen form is visible in the working-tree change.

**Verified:**

- Step 6's rewrite composition (the "Resolve each flagged entry" move) lists the four salvage forms for an entry contradicted by current reasoning as a ladder tried in this fixed order, taking the first that fits: narrow its scope clause (every entry opens with one); generalize it so the prior accepted citations and the override both fit; replace it with a fresh directive when its premise is wrong; delete it only when nothing survives.
- The step states the tie-break: when two forms fit equally, whichever yields the shortest entry that still predicts both the prior accepted citations and the override.
- The step states the shield: an entry reinforced by a citation in the same pass is never pruned or narrowed, by a revision or a flagged-entry salvage, so for a reinforced-and-flagged entry the ladder's first and last rungs are unavailable and the salvage must find a generalizing or replacing form that fits both.
- The step notes the chosen form is visible in the working-tree change the user reviews with `git diff` before step 7's confirmation (a narrowed clause, a generalized or replaced directive, or a removed entry), with no separate account of the choice printed.
- Frontmatter is unchanged and loads under `yaml.safe_load` (15-word description, no colon or semicolon); no `## Rules` section exists under `skills/`, `agents/`, or `shared/`; step headings run 1–8 (with 6a) and every intra-file step reference resolves.
- `uv run scripts/migrate_skills_to_agy.py` regenerated `.agents/plugins/cairn/`; only the capture skill copy changed, and it differs from the source solely by the step-7 `${CLAUDE_PLUGIN_ROOT}` path rewrite and dropped `echo` hint.

---

## Single Rewrite Confirmation Gates The Commit

Add the review loop after the in-place write: the user reviews the working-tree change with `git diff` and requests changes in conversation, the skill re-edits the file in place each round, and one confirmation gates the commit — on acceptance the store is committed path-scoped under `Principle-capture: <milestone_id>`, and on explicit rejection the skill restores the pre-write snapshot and exits without invoking `shared/commit-procedure.md`, reporting the no-op line. The report step keeps `Principles captured.` for a committed rewrite and one distinct line for every nothing-captured case (empty range, no candidates, composed store identical to the baseline, rejection). Verified when the confirmation, rejection, and report steps read exactly so.

**Verified:**

- Step 7 (`### 7. Review, confirm, and commit the principle-store update`) states the review loop after step 6's in-place write: the user reviews the working-tree change with `git diff -- milestones/answer_decision_principles.md` and requests changes in conversation; each round the skill re-edits the store in place under step 6's rules, takes no new snapshot (the step-6 snapshot stays the restore point), prints no diff or store content, and asks the same single confirmation again — exactly one confirmation gates the commit, not the write, with no per-entry or per-change confirmation.
- On acceptance step 7 runs `shared/commit-procedure.md` with PATHS = the fixed-path store `milestones/answer_decision_principles.md` and SUBJECT = `Principle-capture: <milestone_id>` (the step-1 argument verbatim), committing the rewrite as it stands after the last review round over the working-tree baseline, then discards the snapshot.
- On explicit rejection step 7 restores the store from the step-6 snapshot, not from `HEAD` (`cp "$SNAPSHOT" milestones/answer_decision_principles.md`; removes the created file when the snapshot was recorded as *absent*), so the store stands exactly as before the first write in the clean and dirty cases alike, then exits explicitly without invoking `shared/commit-procedure.md` — stating that its dirty-own-path guard would otherwise commit the user's surviving edits under `Principle-capture:` — with no empty commit, and goes to step 8's nothing-captured report.
- Step 7 states it runs only after a write: the empty range (step 3), no candidates (step 5), and identical-to-baseline (step 6) cases go straight to step 8 and never reach the shared procedure.
- Step 8 keeps `Principles captured.` solely for a committed rewrite (a written-but-uncommitted rewrite never earns it) and prints one distinct single no-op line — never a collapse into the success line — for every nothing-captured case, naming all four: empty commit range (step 3), no candidates (step 5), composed store identical to its baseline (step 6), rejection (step 7).
- Surrounding prose is consistent: the usage note says the rewrite is committed once the user confirms it after reviewing `git diff` and that a rejected rewrite leaves the store as it stood; the repeat-capture guard names "a rejected rewrite" among undetectable no-op runs; step 6's references to "step 7's confirmation" resolve; step headings run 1–8 (with 6a) and every intra-file step reference resolves.
- Frontmatter is unchanged and loads under `yaml.safe_load` (15-word description, no colon or semicolon); no `## Rules` section exists under `skills/`, `agents/`, or `shared/`.
- `uv run scripts/migrate_skills_to_agy.py` regenerated `.agents/plugins/cairn/`; only the capture skill copy changed, and it differs from the source solely by the step-7 `${CLAUDE_PLUGIN_ROOT}` path rewrite and dropped `echo` hint.

---
