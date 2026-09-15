# TASKS TODO

## Agents Drop Status Qualifiers

Update `agents/recommend-open-question.md` and `agents/answer-open-question-with-recommendation.md` so the dispatch framing says "once per question", the sibling-declaration rule no longer says "whatever its `status`", and the resolved block is described without `status="open|deferred"`, leaving the `<depends-on>` element rendering and the step 4 self-check untouched. Verified by grepping `agents/` for `status` and `deferred` and finding nothing besides DONE/FAILED wording.

---

## Capture Legacy Note Marker Correction

In `skills/capture-milestone-principle-updates/SKILL.md` keep the parenthetical describing the pre-XML blockquote form as the no-recommendation case, correcting its second marker from `> **Open — …:**` to `> **Open question — …:**` (what those milestone 6–9 commits actually contain), and add no sentence about `status="…"` on historical removed lines, since the id-anchored, attribute-order-immaterial locate already absorbs it and that wording stays. Verified by reading the note and confirming its surviving "Deferred" is the single known exception a grep of `skills/` carries.

---

## README Drops Open Deferred Distinction

Rewrite the five `README.md` passages — the workflow overview, the review skill's reference entry with its Blocking/Deferred triage and convergence rule, and the two sweeps' and the recommend agent's entries — so they describe the review skill authoring every finding as an ordinary block, convergence as no `<open-question>` block remaining, and the sweeps gathering every `<open-question>` block, with no open/deferred wording and no retirement note. Verified by grepping `README.md` for `status=`, `deferred`, and `Blocking` and finding nothing.

---

## CLAUDE Invariants Drop Status Mentions

Sweep `CLAUDE.md` so the skill-table rows for the two sweeps and the invariants on the review skill, the answer-recording mechanism, the recommend sweep, the recommend procedure, and the dispatched-agent return contracts no longer mention `status="open"`/`status="deferred"`, "open/deferred", "a deferred sibling is a declarable target", "no `status` read", "a deferred target is as valid as an open one", or the milestone-21 residual about deferred targets carrying forward, and the review invariant's convergence rule reads "no `<open-question>` block remains". Per the Retirement invariant decision this is delete-only: the attribute-order clause on the `<open-question>` locate is cut, `<depends-on>` and capture keep theirs, and no retirement invariant or "do not reintroduce" sentence is added. Verified by grepping `CLAUDE.md` for `status=` and `deferred` and finding nothing.

---

## Regenerate Antigravity Tree Status Free

Run `uv run scripts/migrate_skills_to_agy.py` to regenerate `.agents/plugins/cairn/` from the swept `skills/`, `agents/`, and `shared/` so the generated tree carries no trace of the attribute, and use the same pass to confirm the whole sweep is grep-clean. Verified by grepping `skills/`, `agents/`, `shared/`, `README.md`, `CLAUDE.md`, and `.agents/plugins/cairn/` for `status=`, `deferred`, and `Blocking` and finding only the capture skill's legacy blockquote note (and its generated copy), while "terse status line", `git status --porcelain`, "finish status", and the DONE/FAILED status wording survive untouched.

---
