# Milestone 22: Drop Open-Question Status

## Goal

Remove the `status` attribute from `<open-question>` blocks so the opening boundary tag is exactly `<open-question id="Short Title">`, and delete every rule that existed only to carry the open/deferred distinction: the review skill's Blocking/Deferred triage and deferred authoring template (findings it would have deferred are authored as ordinary questions), the deferred pass-through in the derive-tasks precondition and the review skill's convergence verdict (both become "no `<open-question>` block remains"), and every "open or deferred", "whatever its status", and "reads no status" qualifier across skills/, agents/, shared/, README.md, and the CLAUDE.md invariants, including milestone 21's accepted residual about deferred targets carrying forward. Regenerate the Antigravity tree so it carries no trace of the attribute. No migration is needed: no live requirements.md holds a block today.

## Relevant starting state

### The `<open-question>` block and its `status` attribute

Every question lives under the single `## Open questions` section of a milestone's `requirements.md` as a raw XML block whose opening boundary line is authored on one physical line, attributes id-first: `<open-question id="Short Title" status="open">`, with `status="deferred"` as the only other value. `skills/review-milestone-requirements/SKILL.md` is the sole author: its step 3 classifies each finding as **Blocking** (authored `status="open"`) or **Deferred** ("better decided while doing the work", authored `status="deferred"`), renders two three-line templates that differ only in the `status` value and the child text, and its shape rules name `status` in the id-first ordering rule and the entity-escaping rule. Its step 5 report lists the remaining `status="open"` blocks and states the convergence verdict as "no `status="open"` blocks remain; `status="deferred"` blocks may carry forward". No live `requirements.md` in `milestones/` holds any `<open-question` block today, so no file needs migrating; the `migrate-workspace` skill no longer exists in the tree.

### The one consumer that branches on the value

`skills/derive-tasks/SKILL.md` is the only runtime file whose control flow reads the value: its precondition (line 22) and its step 2 stop on any block carrying `status="open"` and let `status="deferred"` blocks pass ("deferred questions may carry forward past this point"). Nothing downstream of derive-tasks reads deferred blocks — `shared/complete-procedure.md`, `agents/complete-task.md`, `complete-task`, `complete-all-tasks`, and `finish-current-milestone` contain no mention — so a deferred block that carried forward would never be settled. Across the 21 finished milestones 47 deferred and 50 open blocks were authored; every deferred block was removed before its milestone's `Task-derivation:` commit (45 by answer commits, 2 by hand), so the pass-through never fired.

### Every other mention is a qualifier that ignores the value

The remaining runtime mentions all say the same thing — the mechanism treats both values identically — and would become meaningless once one value exists. By file: `skills/recommend-all-open-questions/SKILL.md` (lines 29–30, 46, 49, 90, 181, 269: the gather extracts `status` by regex alongside `id`, the ranking reads it, gate test 7 states it reads "no `status`", the worked example carries the attribute); `skills/answer-all-open-questions-with-recommendation/SKILL.md` (lines 29–30, 49, 56, 168); `shared/answer-procedure.md` (lines 15, 44, 52, 65, 99: the locate step, the "`status` may precede or follow `id`" attribute-order note, and three "open or deferred entry" phrasings in the cascade); `shared/answer-with-recommendation-procedure.md` (19); `shared/recommend-procedure.md` (14, 34: "open or deferred" in the QUESTION input and the disclosure duty); `skills/discuss-open-question/SKILL.md` (8, 16, 33); `skills/answer-open-question/SKILL.md` (16); `skills/answer-open-question-with-recommendation/SKILL.md` (22); `skills/answer-open-question-with-alternative/SKILL.md` (32, 63); `agents/recommend-open-question.md` (9, 104: "Open/Deferred question", "whatever its `status`"); `agents/answer-open-question-with-recommendation.md` (17); `skills/modify-milestone-goal/SKILL.md` (47: "open or `Deferred` questions"). The attribute-name-anchored `id="([^"]*)"` regex rule is justified in several of these files by "independent of attribute order (`status` may precede or follow `id`)"; the regex itself is used by every locate and gather and stays load-bearing regardless of the justification. Unrelated hits that must survive: "terse status line" in every reporting step, `git status --porcelain` in `shared/commit-procedure.md` and capture, "finish status" in capture, and the `DONE`/`FAILED` "status" wording in both orchestrators.

### Historical formats capture still reads

`skills/capture-milestone-principle-updates/SKILL.md` line 154 names the pre-XML `> **Deferred — …:**` / `> **Open — …:**` blockquote form when explaining that an answer recorded before the block form existed removes no `<open-question>` at all. That is a description of old commits it walks during backfill, not of the current format; the walked diffs of milestones 9–21 also contain `status="…"` on their removed `-<open-question id="…"` lines, which capture locates by the `id` attribute alone (line 138, "attribute order immaterial").

### Documentation and the generated tree

`README.md` mentions the distinction in five places: the workflow overview (line 104), the review skill's reference entry (235, the Blocking/Deferred triage and convergence rule), and the two sweeps' and the recommend agent's entries (265, 281, 285: "every open and deferred `<open-question>` block", "Open/Deferred"). `CLAUDE.md` carries it in the skill table (lines 42, 48) and four invariants (76: the review skill's `status="open"`/`status="deferred"` reconcile and convergence rule; 78: the recommend sweep gather, "a `status="deferred"` sibling the sweep annotated is a declarable target", and gate test 7 "no `status` read"; 83: "still-unanswered (open or deferred) sibling"; 102: the gate "reads no `status`" and "a deferred target is as valid as an open one"). Milestone 21's `requirements.md` records the accepted residual that a deferred `<depends-on>` target may carry forward unanswered past `/derive-tasks`; it is a finished milestone's historical record. The Antigravity tree `.agents/plugins/cairn/` is generated whole by `uv run scripts/migrate_skills_to_agy.py` from `skills/`, `agents/`, and `shared/` and currently mirrors the attribute in 12 files; the script itself contains no reference to `status`, and the last sync was committed under `Agy-regeneration: sync Antigravity plugin tree`.

## Decisions

## Out of Scope

## Open questions

<open-question id="Historical milestone records" status="open">
  <question>Does the repo-wide sweep also edit the finished milestones&apos; own files (their requirements.md, TASKS_DONE.md, and the completed-milestone summaries in milestones/README.md) wherever they mention the status attribute or the open/deferred distinction, or are those left untouched as historical records with only the runtime layer, README.md, CLAUDE.md, and the generated tree in scope?</question>
</open-question>

<open-question id="Capture legacy format note" status="open">
  <question>Should capture-milestone-principle-updates keep its description of the pre-XML `&gt; **Deferred — …:**` / `&gt; **Open — …:**` blockquote form (and gain a note that walked diffs from milestones 9–21 carry `status=&quot;…&quot;` on their removed opening lines), since it reads those historical commits during backfill, or is that description dropped along with every other deferred mention?</question>
</open-question>

<open-question id="Attribute-order wording" status="deferred">
  <question>With `id` as the only attribute, is the &quot;attribute-name-anchored regex, independent of attribute order&quot; phrasing and the review skill&apos;s &quot;id first&quot; ordering rule kept as-is (future-proofing for later attributes), reworded to a plain `id=&quot;([^&quot;]*)&quot;` extraction rule, or dropped?</question>
</open-question>
