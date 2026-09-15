# TASKS DONE


## Review Skill Authors Status-Free Blocks

Rewrite step 3 of `skills/review-milestone-requirements/SKILL.md` so every finding it surfaces is authored as one ordinary three-line block whose opening tag is exactly `<open-question id="Short Title">`, deleting the "it's fine to leave some decisions to settle while doing the work" sentence, the Blocking/Deferred categories, the "do not mark something blocking if a reasonable, low-risk-to-reverse choice exists" rule, and the deferred template with no reworded threshold or pointer in their place. The shape rules state the single-physical-line opening tag plainly, dropping the id-first ordering clause and `status` from the entity-escaping rule, because the sweep and answer skills match against exactly this shape. Verified by reading the step and finding one template, no triage, and no mention of `status`.

**Verified:**

- The opening paragraph of `skills/review-milestone-requirements/SKILL.md` no longer carries the "it's fine to leave some decisions to settle while doing the work if they're better solved there" sentence; it ends at "ready enough for the work to begin."
- Step 3 contains no **Blocking** or **Deferred** category, no "Categorise each new finding" instruction, no "do not mark something blocking if a reasonable, low-risk-to-reverse choice exists" rule, and no reworded don't-raise threshold or pointer sentence in their place.
- Step 3 renders exactly one three-line template, whose opening tag is exactly `<open-question id="Short Title">`; the deferred template is gone.
- The shape rules state the single-physical-line opening tag plainly as `<open-question id="…">` carrying the double-quoted `id` attribute, with no id-first ordering clause, and the entity-escaping rule names only the `id` attribute value.
- `grep -n status` over step 3 (from `### 3.` to `### 4.`) returns nothing; the file's remaining `status`/`deferred` hits sit only in step 1 and step 5, which the sibling task "Review Skill Convergence On Any Block" owns.
- Step 3's "only annotate gaps relative to what is already written" rule survives as the pass's altitude guard.

---

## Review Skill Convergence On Any Block

Update the step 1 inventory and the step 5 report of `skills/review-milestone-requirements/SKILL.md` so the still-open list names every remaining `<open-question>` block and the convergence verdict is "ready for `/derive-tasks` only when no `<open-question>` block remains", removing the deferred carry-forward clause. This is needed because the derive-tasks precondition it mirrors no longer passes any block through. Verified by grepping the file for `status=` and `deferred` and finding nothing.

**Verified:**

- Step 1's inventory bullet in `skills/review-milestone-requirements/SKILL.md` names the `<open-question>` blocks present under `## Open questions` with no `status="open"`/`status="deferred"` qualifier.
- Step 5's "What's still open" item lists every remaining `<open-question>` block by Short Title (`id`).
- Step 5's convergence rule reads that `/derive-tasks` requires no `<open-question>` block remains, its two sub-bullets branch on any block remaining vs. none, the deferred carry-forward clause and the "noting any deferred blocks" wording are gone, and no retirement note was added in their place.
- `grep -i -E 'status=|deferred'` over the file returns nothing; the only surviving `status` hit is the "terse status line" wording in step 5.
- The diff touches only step 1's bullet and step 5's four report lines; steps 0, 2, 3, 4, the no-op paragraph, and the frontmatter are unchanged.

---

## Derive Tasks Precondition Stops On Any Block

Change the precondition and step 2 of `skills/derive-tasks/SKILL.md` so derivation stops when any `<open-question` block remains in `requirements.md`, deleting the deferred pass-through sentence and its "may carry forward" wording. This is the only runtime control flow that read the attribute value, so with it gone nothing branches on `status`. Verified by grepping the file for `status=` and `deferred` and finding nothing.

**Verified:**

- The `## Preconditions` bullet in `skills/derive-tasks/SKILL.md` states that derivation requires no `<open-question` block remain in `requirements.md`, with no `status="open"`, `status="deferred"`, or "may carry forward" wording.
- Step 2 scans `requirements.md` for any `<open-question` block and stops when one exists; its scan instruction carries no `status="open"` qualifier.
- The deferred pass-through sentence ("A block with `status="deferred"` does **not** block derivation — deferred questions may carry forward past this point.") is deleted entirely, with no reworded replacement or retirement note.
- `grep -i -E 'status=|deferred'` over the file returns nothing; the only surviving `status` hit is the "terse status line" wording in step 8.
- The diff touches only the precondition bullet and step 2; the frontmatter and steps 0–1 and 3–9 are unchanged.

---

## Shared Procedures Drop Status Qualifiers

Sweep `shared/answer-procedure.md`, `shared/answer-with-recommendation-procedure.md`, and `shared/recommend-procedure.md` to remove every "open or deferred", `status="open"`/`status="deferred"`, and "status may precede or follow id" phrasing, stating the `id="([^"]*)"` extraction and single-physical-line locate plainly without the attribute-order justification, per the Attribute-order wording decision. The mechanisms are unchanged; only the qualifiers that described the retired distinction go. Verified by grepping `shared/` for `status` and `deferred` and finding only the `git status --porcelain` line in the commit procedure.

**Verified:**

- `grep -rn -i "status\|deferred" shared/` returns only `shared/commit-procedure.md:26` (the `git status --porcelain` line); `shared/answer-procedure.md`, `shared/answer-with-recommendation-procedure.md`, and `shared/recommend-procedure.md` carry no `status="open"`, `status="deferred"`, "open or deferred", "open and deferred", or "status may precede or follow id" phrasing.
- `shared/answer-procedure.md` step 2 states the locate plainly: each `<open-question …>` opening boundary line is the block's opening tag on one physical line and its `id` is pulled with the regex `id="([^"]*)"`, with the "independent of attribute order" justification and its parenthetical cut; the matched-block sentence ends at "one boundary-token pair per block".
- `shared/answer-with-recommendation-procedure.md` step 2 names the `id` extraction as "pulled by the regex `id="([^"]*)"`" and its SHORT TITLE input drops the status clause; `shared/recommend-procedure.md`'s QUESTION input and disclosure duty read "the resolved question" and "a sibling that is itself still unanswered".
- The `<depends-on>` `question` read in `shared/answer-procedure.md` step 6 keeps its "pulled by attribute-name-anchored regex, entity-unescaped, and case-folded exactly as step 2 matches `id`" wording, as the only line with two attributes.
- `git diff` over the three files shows only qualifier removals and the rephrased locate sentence: the boundary-line CLI, entity unescaping, case-folding, fold-before-remove order, cascade, and the two reconciliation outcomes are unchanged, and no other `shared/` file is modified.

---

## Recommend Sweep Drops Status Reads

Update `skills/recommend-all-open-questions/SKILL.md` so the gather extracts only each block's `id` and `<question>` text, the ranking judges over those alone, gate test 7 no longer states that it reads no `status` or that a deferred target is as valid as an open one, the worked example's opening tag is `<open-question id="Short Title">`, and every "open and deferred"/"open/deferred" phrasing including the frontmatter description is reworded, keeping that description at 25 words or fewer and unquoted. The attribute-order justification on the `id` regex is cut, while `<depends-on>` reads keep their two-attribute order-immaterial wording. Verified by grepping the file for `status` and `deferred` and finding only the "terse status line" and "never deferred to the end" wording.

**Verified:**

- The frontmatter `description` carries no "open and deferred" wording, is 15 words, stays an unquoted plain YAML scalar with no colon or semicolon, and loads under `yaml.safe_load`.
- Step 1's gather extracts only each block's `id` (by the regex `id="([^"]*)"` over the opening boundary line) and `<question>` text — no `status` extraction, no attribute-order justification on the `id` regex, and no open-vs-deferred sentence.
- Step 3's ranking judges over each block's `id` and `<question>` text alone.
- Gate test 7 no longer says it reads no `status` or that a deferred target is as valid as an open one, while its `<depends-on>` `question`/`option` read keeps its attribute-name-anchored wording.
- The worked example's opening tag is exactly `<open-question id="Short Title">`.
- Every "open and deferred" / "open/deferred" / `status="open"` / `status="deferred"` phrasing (intro, Usage, step 1, step 6) is reworded.
- `grep -n -i -E 'status|deferred'` on the file hits only line 312's "terse status line" and line 249's "never deferred until every dispatch has returned" wording.

---

## Answer Sweep Drops Status Qualifiers

Update `skills/answer-all-open-questions-with-recommendation/SKILL.md` so its frontmatter description, gather, block-shape note, and re-check no longer name `status="open"`/`status="deferred"` or "open and deferred", keeping the description at 25 words or fewer and unquoted, and cutting the attribute-order justification on the `id` regex while the `<depends-on>` `question` read keeps its order-immaterial wording. Verified by grepping the file for `status` and `deferred` and finding only the "terse status line" and DONE/FAILED status wording.

**Verified:**

- The frontmatter `description` no longer says "open and deferred", is a plain unquoted YAML scalar of 18 words (under the 25-word cap), and the frontmatter loads under `yaml.safe_load` with `name` and `description` keys.
- The Usage paragraph names no `status="open"`/`status="deferred"`.
- Step 1's `id` extraction is stated as a plain extraction — the `(and `status`)` read and the "so extraction is independent of attribute order" justification are cut.
- Step 1's `<depends-on>` `question` read keeps explicit attribute-name-anchored wording stating the read is independent of the order of `question` and `option` on that line.
- The block-shape note ("Open and deferred blocks share one … boundary-token pair distinguished only by `status`") is removed.
- Step 2's re-check and step 3's report name no `status="open"`/`status="deferred"`.
- `grep -in 'status\|deferred'` on the file returns only the "terse status line" hit and the DONE/FAILED "status" hit.
- `git diff` on the file touches only the description, Usage, the step-1 gather paragraph, and the step-3 report; the dependency walk, dispatch, and commit logic are unchanged.

---

## Single Question Skills Drop Status Qualifiers

Sweep `skills/discuss-open-question/SKILL.md`, `skills/answer-open-question/SKILL.md`, `skills/answer-open-question-with-recommendation/SKILL.md`, `skills/answer-open-question-with-alternative/SKILL.md`, and `skills/modify-milestone-goal/SKILL.md` to remove every `status="open|deferred"`, "open or deferred", "whether open or deferred", and "open or `Deferred` questions" qualifier plus the "independent of attribute order" justification on the `<open-question>` `id` regex, stating each locate as a plain extraction. Verified by grepping those five files for `status` and `deferred` and finding only "terse status line" hits.

**Verified:**

- `skills/discuss-open-question/SKILL.md`, `skills/answer-open-question/SKILL.md`, `skills/answer-open-question-with-recommendation/SKILL.md`, `skills/answer-open-question-with-alternative/SKILL.md`, and `skills/modify-milestone-goal/SKILL.md` carry no `status="open|deferred"`, "whether `status="open"` or `status="deferred"`", "open or deferred", "open or `Deferred` questions", or "shared by open and deferred blocks (they differ only in the `status` value)" wording.
- The "independent of attribute order (`status` may precede or follow `id`)" justification is cut from every `<open-question>` `id` locate in those files; each locate states the plain extraction — pull the `id` attribute with the regex `id="([^"]*)"` — matching the swept `shared/answer-procedure.md` wording, and the alternative skill's matched-block sentence ends at "one boundary-token pair per block".
- `grep -i -E 'status|deferred'` over the five files returns only the "terse status line" hits in the four committing skills' reporting steps (`discuss-open-question` is conversational and has none).
- No retirement note or replacement sentence is added; the diff touches only the qualifier phrases and the rewrapped locate paragraph — the boundary-line CLI, entity unescaping, case-folding, the `<alternative id>` lookup, and every other step are unchanged.
- Each file's frontmatter still loads under `yaml.safe_load` with `name` and `description`, the descriptions untouched and all at 21 words or fewer.

---

## Agents Drop Status Qualifiers

Update `agents/recommend-open-question.md` and `agents/answer-open-question-with-recommendation.md` so the dispatch framing says "once per question", the sibling-declaration rule no longer says "whatever its `status`", and the resolved block is described without `status="open|deferred"`, leaving the `<depends-on>` element rendering and the step 4 self-check untouched. Verified by grepping `agents/` for `status` and `deferred` and finding nothing besides DONE/FAILED wording.

**Verified:**

- `agents/recommend-open-question.md` line 9 reads "dispatches you once per question" with no "Open/Deferred" qualifier.
- The `<depends-on>` sibling-declaration bullet in step 3 of `agents/recommend-open-question.md` no longer carries "whatever its `status`"; the rest of that bullet, the rendered template (line 78's `<depends-on question="Sibling Short Title" option="Option X"/>`), and the child-order rule are unchanged.
- Step 4 (self-check) of `agents/recommend-open-question.md` is byte-for-byte unchanged — the file's only two diff hunks sit at lines 9 and 104.
- `agents/answer-open-question-with-recommendation.md` describes the resolved block as an `<open-question>` block, with no `status="open|deferred"`.
- `grep -rn -i -E 'status|deferred' agents/` returns nothing (no DONE/FAILED "status" wording exists in `agents/`, so nothing else survives).
- `git diff --stat` shows exactly three changed lines across the two agent files; both frontmatters load under `yaml.safe_load` with `name` and `description`, the descriptions untouched at 19 and 23 words.

---
