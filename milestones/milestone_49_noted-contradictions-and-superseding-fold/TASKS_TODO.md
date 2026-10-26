# TASKS TODO

## Note Writing And Rewrite In Answer Core

Extend `core/shared/answer-procedure.md` so its analyse step judges each contradiction its fourth question finds, with the fold rewriting the other entry's conflicting text in place in the same targeted edit pass and writing no note when the new answer plainly supersedes it, and the old entry staying as written with a note written when the answer does not plainly settle which entry should hold, doubt noting; and so its fold step, for a conflict question asking which of two entries stands, edits the losing entry in place and adds nothing. Add one numbered step after the fold and before the block's removal that writes each remaining note under `## Noted contradictions`, a section standing directly after `## Decisions` and before `## Out of Scope` whose heading is inserted together with the first note, each note holding the two `###` headings of the conflicting entries with enough of each entry's lead or opening words to tell them apart where they share a heading or sit among several bullets, plus one sentence in the skill's own words stating what each entry says and why both cannot hold, and no ready-made question text; the closing ban on otherwise rewriting `requirements.md` gains this one exception, the core gains no new input and no branch, and `hand-answer-procedure.md` and `answer-with-recommendation-procedure.md` stay unchanged so all three single-question skills reach the step. Verified by the rebuilt `hosts/` trees passing `uv run scripts/build_hosts.py --check` and by the sweep's references to the core's analyse step and fold step numbers still resolving to those steps.

---

## Conflict Phrase And Note Handling In Review

Extend `core/skills/review-milestone-requirements/SKILL.md` so its document-structure block keeps the four sections and adds `## Noted contradictions` as an optional fifth between `## Decisions` and `## Out of Scope`, present only while a note stands; so step 4 states once one fixed phrase, in a form that also names the two `###` headings of the pair, that opens every conflict question's text it authors; and so the pass handles each note under that section against recorded state only, deleting it with no block when a standing block already flags the pair or either named entry no longer stands as the note describes it (its heading gone, or rewritten so the two now hold together), otherwise authoring one block per note as noted without re-judging and then deleting the note, and deleting the heading too with the last note. Amend step 3's statement that the pass never edits `requirements.md` to allow this one edit, which rides in the existing `Requirements-review:` commit whose paths already include that file. Verified by the rebuilt `hosts/` trees passing `uv run scripts/build_hosts.py --check` and by the rendered skill reading consistently from its structure block through its report.

---

## Conflict Section In The Answer Sweep

Extend `core/skills/answer-all-open-questions-with-recommendation/SKILL.md` so step 3a recognizes a conflict question by an exact-prefix check of its question text, as the view's `list --with-question` printed it, against the review pass's fixed phrase (a block written before the convention gets the ordinary append section), composing for it the losing entry's `###` heading and the whole new body of that subsection, unchanged bullets included in a topical subsection, with no decision folded anywhere else. The batched call's conflict section carries exactly one `python3 {{PLUGIN_ROOT}}/tools/requirements.py replace <MILESTONE_DIR> --section "<Heading>"` call on a quoted heredoc standing where `fold` stands, chained ahead of `remove`, and is otherwise identical to an ordinary section so every section keeps a fixed number of tool calls; the winning entry and any knock-on clause elsewhere stay as written for the next review pass's consistency step, and the sweep still records every pick as given and forms no contradiction judgment. Verified by the rebuilt `hosts/` trees passing `uv run scripts/build_hosts.py --check` and by `tests/test_sweep_batched_call.py` and `tests/test_sweep_compact_view.py` still extracting their calls.

---

## Cover Conflict Section In Batched Call Test

Extend `tests/fixtures/sweep` with a recommendation-bearing conflict question whose text opens with the review pass's fixed phrase and whose losing entry sits in a `###` subsection of the fixture's `requirements.md`, and extend `tests/test_sweep_batched_call.py` to extract the conflict section from the rendered Claude Code tree at the boundaries the step states and run it under bash in the same clean run as the ordinary sections, asserting that its commit's `requirements.md` diff is exactly the rewritten subsection body with the heading line and every other byte unchanged, that the section holds one `replace` call and no `fold`, and that the ordinary sections, the silent skip, and the dirty-start stop behave as before. Verified by `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest` both passing.

---

## Add Tie-Break Rule To Derive-Tasks

Extend `core/skills/derive-tasks/SKILL.md` with the tie-break rule applied while building the briefs and the coverage matrix: where two `## Decisions` entries cannot both hold, the later-recorded entry governs the brief, found by the commit that added each entry's lines in `requirements.md` through blame or a pickaxe search path-scoped to that file, never by file position and never from the note; every pair listed under `## Noted contradictions` is taken as conflicting as noted without re-judging, any other pair the runner itself finds is resolved the same way, and nothing is flagged for either kind. The empty-`list` precondition stays as it is, so a noted contradiction never blocks the run. Verified by the rebuilt `hosts/` trees passing `uv run scripts/build_hosts.py --check`.

---

## Record Noted Contradictions In CLAUDE.md

Update `CLAUDE.md`'s milestone file structure to the four sections plus the optional `## Noted contradictions` fifth between `## Decisions` and `## Out of Scope`, present only while a note stands and created by no tool, and revise the invariants this milestone moves with rationale only: the fold tool's `replace` subcommand (a whole subsection, never creating, `fold` untouched, called by the sweep's conflict section alone with exactly one `replace` per section), tidy versus record (the answer core rewrites an entry the answer plainly supersedes and notes one it cannot settle, the review pass turns each note into one question opened by its fixed phrase and deletes it against recorded state only, the sweep recognizes a conflict question by that prefix and still judges nothing), `derive-tasks`' later-recorded tie-break by commit with nothing flagged, and `finish-current-milestone` and capture left unchanged. Verified by reading the revised passages against the milestone's `## Decisions` with no statement contradicting a shipped file and `uv run scripts/build_hosts.py --check` still passing.

---

## Describe Noted Contradictions In Docs

Update `docs/skill-reference.md` (the review pass, the answer sweep, the three single-question answer skills, and `derive-tasks` entries), the requirements-loop paragraph of `docs/workflow.md`, and the fold-tool mentions of `docs/design-claims.md` to describe the noted-contradictions section and when it exists, the note-versus-rewrite rule, the review pass's note handling and fixed phrase, the fold tool's `replace` subcommand and the sweep's conflict section, and the task-derivation tie-break. Verified by a grep showing no remaining claim that the fold tool has one subcommand, that the review pass never edits `requirements.md`, or that the sweep's every section folds through `fold`.

---
