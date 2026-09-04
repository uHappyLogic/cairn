# TASKS TODO

## Restructure Six Heaviest Skill Descriptions

Rewrite the frontmatter `description` of the six heaviest skills — `review-milestone-requirements`, `discuss-new-task`, `capture-milestone-principle-updates`, `recommend-all-open-questions`, `answer-all-open-questions-with-recommendation`, `modify-milestone-goal` — from scratch into a single independent clause of 25 words or fewer naming only what the skill does, deleting their trigger-phrase lists, mechanics, sequencing, design provenance, cross-skill references, and "Use when…" framing without preserving that content anywhere. These six carry the majority of the always-on description words and must be restructured rather than trimmed, and the `review-milestone-requirements` rewrite must also stop tripping the transpiler's re-quoting fallback. Verified when each of the six descriptions is 25 words or fewer, contains no semicolon or colon, keeps the `name` key and any `model` key untouched, and its raw frontmatter loads under `yaml.safe_load` with the `description:` line left unquoted.

---

## Shorten Nine Mid-Weight Skill Descriptions

Rewrite the frontmatter `description` of the nine skills currently over the cap — `answer-open-question-with-alternative`, `answer-open-question-with-recommendation`, `submit-task`, `init-milestone-base-workflow`, `derive-tasks`, `goto-next-milestone`, `complete-task`, `finish-current-milestone`, `discuss-open-question` — into a single independent clause of 25 words or fewer naming only what the skill does, deleting mechanics, commit subjects, sequencing, cross-skill references, and provenance outright. Verified when each of the nine descriptions is 25 words or fewer, contains no semicolon or colon, keeps the `name` key and any `model` key untouched, and its raw frontmatter loads under `yaml.safe_load` with the `description:` line left unquoted.

---

## Audit Six Short Skill Descriptions

Bring the six skill descriptions already at or under the cap — `answer-open-question`, `specify-milestone-starting-state`, `discuss-milestone-goal`, `define-milestone-goal`, `ask-in-milestone-context`, `complete-all-tasks` — up to the same bar, rewording only where a description still carries mechanics, sequencing, cross-skill references, or a semicolon or colon, and leaving descriptions already written with em-dash or parenthetical apposition alone on punctuation grounds. Verified when each of the six descriptions is a single independent clause of 25 words or fewer, contains no semicolon or colon, names only what the skill does, and its raw frontmatter loads under `yaml.safe_load` with the `description:` line left unquoted.

---

## Compress Three Agent Descriptions

Rewrite the frontmatter `description` of the three agents — `agents/complete-task.md`, `agents/recommend-open-question.md`, `agents/answer-open-question-with-recommendation.md` — into a single independent clause of 25 words or fewer that names what the agent does and folds its invocation contract in as a short clause naming what the prompt carries (the task's heading text, or the question's Short Title), deleting the separate "dispatched by X; not called directly by the user" note and all mechanics and provenance. Verified when each of the three descriptions is 25 words or fewer, contains no semicolon or colon, still names the prompt payload, keeps the `name`, `model`, and `color` keys untouched, and its raw frontmatter loads under `yaml.safe_load` with the `description:` line left unquoted.

---

## Amend Skill Frontmatter Invariant In CLAUDE.md

Extend the existing **Skill Frontmatter** bullet under `## Invariants to preserve when editing skills` in `CLAUDE.md` to carry the one-short-sentence description rule — a single clause of 25 words or fewer naming only what the skill or agent does, with provenance, mechanics, sequencing, cross-skill references, and trigger lists deleted, semicolon and colon banned, plain-YAML-scalar parsing required, and descriptions treated as routing labels rather than a record — and revise the milestone-15 "runtime files carry no editor-facing prose" bullet's sentence exempting frontmatter descriptions as "the triggering surface, edited only to correct a claim the body has falsified" so it instead points at the Skill Frontmatter bullet as the home of the frontmatter rule. Verified when every rule about the `description` key lives in the Skill Frontmatter bullet, the old exemption claim no longer appears, and no new standalone invariant bullet was added.

---

## Falsification Pass Over Parallel Doc Surfaces

Run one bounded pass over `README.md`'s `## Skill reference` entries and `CLAUDE.md`'s per-skill workflow map, editing an entry only where a shortened description has made an existing claim demonstrably false, adding no new prose and doing no general tidying, since both surfaces are the intended homes for the mechanics and provenance deleted from descriptions. Verified by a recorded per-entry check of both surfaces against the rewritten descriptions that either lists each falsified claim and its correction or reports a no-op with nothing edited.

---

## Regenerate Antigravity Tree After Rewrites

Run `uv run scripts/migrate_skills_to_agy.py` exactly once, after every description rewrite has landed, to regenerate the checked-in Antigravity tree at `.agents/plugins/cairn/` so the description savings reach that surface, touching no transpiler source. Verified when the transpiler exits cleanly without exercising its re-quoting fallback, a whole-set check confirms all 24 descriptions are 25 words or fewer with no semicolon or colon and every raw frontmatter loads under `yaml.safe_load` unquoted, and the regenerated tree's descriptions match the source files.

---
