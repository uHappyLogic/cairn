# TASKS TODO

## Add Tie-Break Rule To Derive-Tasks

Extend `core/skills/derive-tasks/SKILL.md` with the tie-break rule applied while building the briefs and the coverage matrix: where two `## Decisions` entries cannot both hold, the later-recorded entry governs the brief, found by the commit that added each entry's lines in `requirements.md` through blame or a pickaxe search path-scoped to that file, never by file position and never from the note; every pair listed under `## Noted contradictions` is taken as conflicting as noted without re-judging, any other pair the runner itself finds is resolved the same way, and nothing is flagged for either kind. The empty-`list` precondition stays as it is, so a noted contradiction never blocks the run. Verified by the rebuilt `hosts/` trees passing `uv run scripts/build_hosts.py --check`.

---

## Record Noted Contradictions In CLAUDE.md

Update `CLAUDE.md`'s milestone file structure to the four sections plus the optional `## Noted contradictions` fifth between `## Decisions` and `## Out of Scope`, present only while a note stands and created by no tool, and revise the invariants this milestone moves with rationale only: the fold tool's `replace` subcommand (a whole subsection, never creating, `fold` untouched, called by the sweep's conflict section alone with exactly one `replace` per section), tidy versus record (the answer core rewrites an entry the answer plainly supersedes and notes one it cannot settle, the review pass turns each note into one question opened by its fixed phrase and deletes it against recorded state only, the sweep recognizes a conflict question by that prefix and still judges nothing), `derive-tasks`' later-recorded tie-break by commit with nothing flagged, and `finish-current-milestone` and capture left unchanged. Verified by reading the revised passages against the milestone's `## Decisions` with no statement contradicting a shipped file and `uv run scripts/build_hosts.py --check` still passing.

---

## Describe Noted Contradictions In Docs

Update `docs/skill-reference.md` (the review pass, the answer sweep, the three single-question answer skills, and `derive-tasks` entries), the requirements-loop paragraph of `docs/workflow.md`, and the fold-tool mentions of `docs/design-claims.md` to describe the noted-contradictions section and when it exists, the note-versus-rewrite rule, the review pass's note handling and fixed phrase, the fold tool's `replace` subcommand and the sweep's conflict section, and the task-derivation tie-break. Verified by a grep showing no remaining claim that the fold tool has one subcommand, that the review pass never edits `requirements.md`, or that the sweep's every section folds through `fold`.

---
