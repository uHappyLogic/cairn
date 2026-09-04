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
