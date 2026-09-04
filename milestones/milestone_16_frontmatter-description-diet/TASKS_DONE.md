# TASKS DONE

## Restructure Six Heaviest Skill Descriptions

Rewrite the frontmatter `description` of the six heaviest skills — `review-milestone-requirements`, `discuss-new-task`, `capture-milestone-principle-updates`, `recommend-all-open-questions`, `answer-all-open-questions-with-recommendation`, `modify-milestone-goal` — from scratch into a single independent clause of 25 words or fewer naming only what the skill does, deleting their trigger-phrase lists, mechanics, sequencing, design provenance, cross-skill references, and "Use when…" framing without preserving that content anywhere. These six carry the majority of the always-on description words and must be restructured rather than trimmed, and the `review-milestone-requirements` rewrite must also stop tripping the transpiler's re-quoting fallback. Verified when each of the six descriptions is 25 words or fewer, contains no semicolon or colon, keeps the `name` key and any `model` key untouched, and its raw frontmatter loads under `yaml.safe_load` with the `description:` line left unquoted.

**Verified:**

- Each of the six rewritten descriptions (`review-milestone-requirements`, `discuss-new-task`, `capture-milestone-principle-updates`, `recommend-all-open-questions`, `answer-all-open-questions-with-recommendation`, `modify-milestone-goal`) is 25 words or fewer — 22, 22, 15, 18, 21, 21 respectively.
- Each of the six descriptions contains no semicolon and no colon.
- Each of the six is a single independent clause naming only what the skill does, with its trigger-phrase list, mechanics, sequencing, design provenance, cross-skill references, and "Use when…" framing deleted and preserved nowhere.
- Each file's `name` key is unchanged and none of the six carries a `model` key, so no `model` key was added or altered — the diff touches exactly one `description:` line per file.
- Each of the six files' raw frontmatter loads under `yaml.safe_load` with the `description:` line left unquoted (plain scalar, no leading quote).
- `skills/review-milestone-requirements/SKILL.md` no longer trips the transpiler's re-quoting fallback — its raw frontmatter now parses under `yaml.safe_load` without the colon-space that previously raised.

---

## Shorten Nine Mid-Weight Skill Descriptions

Rewrite the frontmatter `description` of the nine skills currently over the cap — `answer-open-question-with-alternative`, `answer-open-question-with-recommendation`, `submit-task`, `init-milestone-base-workflow`, `derive-tasks`, `goto-next-milestone`, `complete-task`, `finish-current-milestone`, `discuss-open-question` — into a single independent clause of 25 words or fewer naming only what the skill does, deleting mechanics, commit subjects, sequencing, cross-skill references, and provenance outright. Verified when each of the nine descriptions is 25 words or fewer, contains no semicolon or colon, keeps the `name` key and any `model` key untouched, and its raw frontmatter loads under `yaml.safe_load` with the `description:` line left unquoted.

**Verified:**

- Each of the nine rewritten descriptions (`answer-open-question-with-alternative`, `answer-open-question-with-recommendation`, `submit-task`, `init-milestone-base-workflow`, `derive-tasks`, `goto-next-milestone`, `complete-task`, `finish-current-milestone`, `discuss-open-question`) is 25 words or fewer — 19, 15, 15, 21, 14, 13, 19, 21, 21 respectively.
- Each of the nine descriptions contains no semicolon and no colon.
- Each of the nine is a single independent clause naming only what the skill does, with its mechanics (commit subjects, staging, triage/insertion steps, "never overwrites existing files"), sequencing (`goto-next-milestone`'s finish-first precondition), cross-skill references, "Use when…" framing, and provenance deleted and preserved nowhere.
- Each file's `name` key is unchanged, and the `model: opus` key on `answer-open-question-with-alternative` and `answer-open-question-with-recommendation` is unchanged — the diff touches exactly one `description:` line per file, nine files, nine insertions and nine deletions.
- Each of the nine files' raw frontmatter loads under `yaml.safe_load` with the `description:` line left unquoted (plain scalar, no leading quote).

---

## Audit Six Short Skill Descriptions

Bring the six skill descriptions already at or under the cap — `answer-open-question`, `specify-milestone-starting-state`, `discuss-milestone-goal`, `define-milestone-goal`, `ask-in-milestone-context`, `complete-all-tasks` — up to the same bar, rewording only where a description still carries mechanics, sequencing, cross-skill references, or a semicolon or colon, and leaving descriptions already written with em-dash or parenthetical apposition alone on punctuation grounds. Verified when each of the six descriptions is a single independent clause of 25 words or fewer, contains no semicolon or colon, names only what the skill does, and its raw frontmatter loads under `yaml.safe_load` with the `description:` line left unquoted.

**Verified:**

- Each of the six descriptions (`answer-open-question`, `specify-milestone-starting-state`, `discuss-milestone-goal`, `define-milestone-goal`, `ask-in-milestone-context`, `complete-all-tasks`) is a single independent clause of 25 words or fewer — 18, 22, 21, 18, 20, 15 respectively.
- None of the six descriptions contains a semicolon or a colon.
- Each of the six names only what the skill does, with the remaining mechanics reworded away — `answer-open-question` lost "committing the manual-answer edit", `complete-all-tasks` lost "committing after each completed task", and `ask-in-milestone-context`'s "Use when…" framing was replaced with a statement of what the skill does.
- The three descriptions carrying no mechanics, sequencing, cross-skill reference, semicolon, or colon (`specify-milestone-starting-state`, `discuss-milestone-goal`, `define-milestone-goal`) were left byte-for-byte unchanged, including `define-milestone-goal`'s parenthetical apposition, which is not grounds for a rewrite.
- Each of the six files' raw frontmatter loads under `yaml.safe_load` with the `description:` line left unquoted (plain scalar, no leading quote indicator).
- Each file's `name` key is unchanged and none of the six carries a `model` key — the diff is three files, one `description:` line each, three insertions and three deletions.

---

## Compress Three Agent Descriptions

Rewrite the frontmatter `description` of the three agents — `agents/complete-task.md`, `agents/recommend-open-question.md`, `agents/answer-open-question-with-recommendation.md` — into a single independent clause of 25 words or fewer that names what the agent does and folds its invocation contract in as a short clause naming what the prompt carries (the task's heading text, or the question's Short Title), deleting the separate "dispatched by X; not called directly by the user" note and all mechanics and provenance. Verified when each of the three descriptions is 25 words or fewer, contains no semicolon or colon, still names the prompt payload, keeps the `name`, `model`, and `color` keys untouched, and its raw frontmatter loads under `yaml.safe_load` with the `description:` line left unquoted.

**Verified:**

- Each of the three rewritten agent descriptions (`agents/complete-task.md`, `agents/recommend-open-question.md`, `agents/answer-open-question-with-recommendation.md`) is 25 words or fewer — 19, 19, 23 respectively.
- None of the three descriptions contains a semicolon or a colon.
- Each is a single independent clause naming what the agent does, with the separate "dispatched by X / not called directly by the user" note, the mechanics (verification/task-list update, uncommitted-edit hand-back, read-only grounding, XML sub-element rendering), and the provenance ("non-interactive twin of discuss-open-question", "Mutates nothing") deleted and preserved nowhere.
- Each still names its prompt payload, folded into the same clause — "invoked with that task's heading text as the prompt" and, for both question agents, "invoked with that question's Short Title as the prompt".
- Each file's `name`, `model`, and `color` keys are unchanged — the diff touches exactly one `description:` line per file, three files, three insertions and three deletions.
- Each of the three files' raw frontmatter loads under `yaml.safe_load` with the `description:` line left unquoted (plain scalar, no leading quote indicator), and the parsed value round-trips byte-for-byte to the text after `description:` — including `agents/complete-task.md`, whose old ` ##` would have been swallowed as a YAML comment.

---

## Amend Skill Frontmatter Invariant In CLAUDE.md

Extend the existing **Skill Frontmatter** bullet under `## Invariants to preserve when editing skills` in `CLAUDE.md` to carry the one-short-sentence description rule — a single clause of 25 words or fewer naming only what the skill or agent does, with provenance, mechanics, sequencing, cross-skill references, and trigger lists deleted, semicolon and colon banned, plain-YAML-scalar parsing required, and descriptions treated as routing labels rather than a record — and revise the milestone-15 "runtime files carry no editor-facing prose" bullet's sentence exempting frontmatter descriptions as "the triggering surface, edited only to correct a claim the body has falsified" so it instead points at the Skill Frontmatter bullet as the home of the frontmatter rule. Verified when every rule about the `description` key lives in the Skill Frontmatter bullet, the old exemption claim no longer appears, and no new standalone invariant bullet was added.

**Verified:**

- The **Skill Frontmatter** bullet under `## Invariants to preserve when editing skills` in `CLAUDE.md` now carries the one-short-sentence rule: a description is one short sentence of 25 words or fewer naming only what that skill or agent does, across all `skills/*/SKILL.md` and all `agents/*.md`.
- That bullet states the shape rule (a single independent clause, comma/em-dash/parenthetical riders allowed) and bans the semicolon and the colon outright, with the reason they are banned.
- That bullet states the plain-YAML-scalar parsing bar (raw frontmatter loads under `yaml.safe_load` with the `description:` line left unquoted) and that the transpiler's re-quoting fallback stays as an unexercised net.
- That bullet states that design provenance, mechanics, sequencing, cross-skill references, "Use when…" framing, and trigger-phrase lists are deleted outright rather than relocated, that a description is a routing label and never a record, and that the 25-word cap is a hard pass/fail bar with no exceptions.
- That bullet states the agent-description invocation contract compressed into the same sentence, and that the "dispatched by X, not called directly by the user" note is deleted.
- The milestone-15 **Runtime files carry no editor-facing prose** bullet's closing sentence no longer claims descriptions are "the triggering surface, edited only to correct a claim the body has falsified" and instead points at the **Skill Frontmatter** invariant above as the home of every rule governing them; `grep -c "triggering surface" CLAUDE.md` returns 0.
- Every rule about the frontmatter `description` key lives in the Skill Frontmatter bullet — `grep -n '`description`' CLAUDE.md` inside the invariants section returns only that bullet plus the runtime bullet's pointer sentence.
- No new standalone invariant bullet was added — the `^- ` bullet count under `## Invariants to preserve when editing skills` is 27 both before and after the edit.

---

## Falsification Pass Over Parallel Doc Surfaces

Run one bounded pass over `README.md`'s `## Skill reference` entries and `CLAUDE.md`'s per-skill workflow map, editing an entry only where a shortened description has made an existing claim demonstrably false, adding no new prose and doing no general tidying, since both surfaces are the intended homes for the mechanics and provenance deleted from descriptions. Verified by a recorded per-entry check of both surfaces against the rewritten descriptions that either lists each falsified claim and its correction or reports a no-op with nothing edited.

**Verified:**

- Both surfaces were enumerated in full before checking: `README.md`'s `## Skill reference` holds 21 skill entries, 2 agent entries (`answer-open-question-with-recommendation` (agent), `recommend-open-question` (subagent)) and the non-skill `### The answer-principle-learning loop` section; `CLAUDE.md`'s per-skill workflow map holds 24 lines (21 skills + 3 agents). Every one was checked against its rewritten frontmatter description.
- The before/after description set was established from git rather than memory — `git show 4ca5a4b:<file>` for each of the 21 `skills/*/SKILL.md` and 3 `agents/*.md` versus the working tree — so each entry was checked against exactly what was cut.
- `git diff 4ca5a4b..HEAD -- skills agents` changes 21 files by exactly one line each, and filtering that diff to non-`description:` lines returns nothing: the rewrites altered no skill or agent body, so no behavioral claim on either surface could have changed truth value. (`define-milestone-goal`, `discuss-milestone-goal`, `specify-milestone-starting-state` were already under the cap and their descriptions are untouched.)
- Neither surface makes any claim *about* description text: `grep -i 'description\|frontmatter\|trigger\|says things like\|trigger it\|auto-discover\|routing label'` over `README.md` and `CLAUDE.md` returns, inside the two in-scope surfaces, only the argument placeholders `<overall_goal_description>` / `<issue description>` and task-section-description prose — no entry asserts what a frontmatter description contains, lists, or triggers on.
- `answer-all-open-questions-with-recommendation` — cut: 5 trigger phrases, "Use this after a recommend sweep…", strict-sequencing/dispatch mechanics, orchestrator-commits clause, recommendation-less-questions note. README (`### answer-all-open-questions-with-recommendation`) and map line 17 assert those mechanics as behavior, unchanged in the body. No falsified claim; not edited.
- `answer-open-question-with-alternative` — cut: "inline in this conversation, then commit that answer on its own", "Use when…" framing, override-the-recommendation note. README entry and map line 18 restate the inline run, the `Alternative-answer:` commit and the override purpose as behavior. No falsified claim; not edited.
- `answer-open-question-with-recommendation` (skill) — cut: inline-plus-commit clause and "Use when…" framing. README entry and map line 15 assert the inline run and the `Recommendation-answer:` commit. No falsified claim; not edited.
- `answer-open-question` — cut: "committing the manual-answer edit" and "downstream implications". README entry (the `Manual-answer:` commit, the literal-only rule, the redirect guard) and map line 14 all describe body behavior. No falsified claim; not edited.
- `ask-in-milestone-context` — cut: the whole "Use when the user is asking…" framing, replaced by a what-it-does clause. README entry and map line 26 describe the read-only Q&A behavior and the handoff offer. No falsified claim; not edited.
- `capture-milestone-principle-updates` — cut: 5 trigger phrases, finish-time sequencing, commit-walk mechanics, "It is the new sole writer of milestones/answer_decision_principles.md". README entry and map line 28 still call it the sole writer and the finish-time follow-up, which the body and the invariants confirm. No falsified claim; not edited.
- `complete-all-tasks` — cut: "committing after each completed task" (replaced by the TODO→DONE move). README entry's per-task path-scoped `Tasklist-completion:` commit and map line 23's "commits after each" are body behavior. No falsified claim; not edited.
- `complete-task` (skill) — cut: "Use for one ad-hoc task you want to stay available to discuss and tweak afterwards"; the inline clause is retained. README entry and map line 24 assert the inline run and the `Task-completion:` commit. No falsified claim; not edited.
- `define-milestone-goal` — description unchanged by the diet, so nothing on either surface could be falsified; README entry and map line 8 checked and left as is.
- `derive-tasks` — cut: the decomposition/coverage/writes-briefs second sentence. README entry (traceability matrix, single writer, no second pass, open-questions precondition) and map line 20 are body behavior. No falsified claim; not edited.
- `discuss-milestone-goal` — description unchanged; README entry and map line 7 checked and left as is.
- `discuss-new-task` — cut: the `/submit-task` handoff cross-reference, "Use this whenever…" framing, and the oversized-issue guidance. README entry still states the handoff to `/submit-task` and the near-1:1 brief mapping, both true of the body; map line 22 likewise. No falsified claim; not edited.
- `discuss-open-question` — reworded only (same alternatives/trade-offs/recommendation content). README entry and map line 13 unaffected. No falsified claim; not edited.
- `finish-current-milestone` — cut: the `to "none"` detail and the "lasting changes to the project's environment context" qualifier. README entry and map line 27 describe the summary write, the pointer clear and the CLAUDE.md update. No falsified claim; not edited.
- `goto-next-milestone` — cut: the milestones/ scan and the finish-first precondition. README's entry heading `### goto-next-milestone <number> <title>` and its "Creates the next milestone directory with empty starter files" claim are false, but were already false before this milestone — the pre-rewrite description and map line 29 both said "activates an already-defined milestone", and milestone 15's completion summary records this exact claim as a pre-existing follow-up. Not made false by a shortened description, so out of this falsification-only pass; not edited.
- `init-milestone-base-workflow` — cut: "Safe to run on an existing project; never overwrites existing files." README entry still claims additive-and-idempotent/never-overwrites, which the body and the first invariant confirm. No falsified claim; not edited.
- `modify-milestone-goal` — cut: "This is the only skill that mutates an existing milestone's Goal", the surfaces-never-cascades mechanic, the `/discuss-open-question` cross-reference, and the "Use when…" examples. README entry and map line 19 assert the same as behavior, backed by the invariant. No falsified claim; not edited.
- `recommend-all-open-questions` — cut: 5 trigger phrases, the batch-form framing, the subagent dispatch, "requires no clean working tree", and the commits-once-at-the-end clause. README entry and map line 11 carry all of it as behavior. No falsified claim; not edited.
- `review-milestone-requirements` — cut: 5 trigger phrases, the loop-engine framing, when-to-run sequencing, and "It never answers questions or records decisions itself" (also removing the `loop: ` colon-space). README entry and map line 10 restate the three jobs and the never-answers boundary. No falsified claim; not edited.
- `specify-milestone-starting-state` — description unchanged; README entry and map line 9 checked and left as is.
- `submit-task` — cut: "Use when the user reports a concrete bug, gap…" framing plus the triage/position/inline mechanics. README entry and map line 21 assert the triage, the position decision, the inline authoring and the `Task-submission:` commit. No falsified claim; not edited.
- `agents/answer-open-question-with-recommendation` — cut: "leaving the edit uncommitted for the orchestrator to commit" and the "Dispatched per-question by … not called directly by the user" note; the Short-Title invocation clause is retained. README's agent entry still says not-user-invocable, dispatched-per-question, mutates-but-never-commits — body behavior, backed by the orchestrator invariant; map line 16 likewise. No falsified claim; not edited.
- `agents/complete-task` — cut: "verifies success criteria, and updates the task list"; the heading-text invocation clause is retained. Map line 25 (isolated run of `shared/complete-procedure.md`, `DONE`/`FAILED`) is unaffected. `README.md` has no entry for this agent — a pre-existing absence, and adding one would be new prose this pass forbids. No falsified claim; not edited.
- `agents/recommend-open-question` — cut: the twin-of-`discuss-open-question` framing, the XML sub-element enumeration, "not user-triggered", and "Mutates nothing"; the Short-Title invocation clause is retained. README's subagent entry and map line 12 carry the same as behavior. No falsified claim; not edited.
- `README.md`'s `### The answer-principle-learning loop` section makes no claim about any frontmatter description (it covers the principle store, the recommendation advisory and the correction loop). No falsified claim; not edited.
- Outcome is a no-op with nothing edited: `git status --porcelain` and `git diff --stat README.md CLAUDE.md` are both empty after the pass, so no entry was corrected, no new prose was added, and no general tidying was done.
- The per-entry check is recorded in this `**Verified:**` ledger, one bullet per checked entry, with no separate checklist artifact added under the milestone directory.

---
