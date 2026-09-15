# TASKS TODO

## CLAUDE Invariants Drop Status Mentions

Sweep `CLAUDE.md` so the skill-table rows for the two sweeps and the invariants on the review skill, the answer-recording mechanism, the recommend sweep, the recommend procedure, and the dispatched-agent return contracts no longer mention `status="open"`/`status="deferred"`, "open/deferred", "a deferred sibling is a declarable target", "no `status` read", "a deferred target is as valid as an open one", or the milestone-21 residual about deferred targets carrying forward, and the review invariant's convergence rule reads "no `<open-question>` block remains". Per the Retirement invariant decision this is delete-only: the attribute-order clause on the `<open-question>` locate is cut, `<depends-on>` and capture keep theirs, and no retirement invariant or "do not reintroduce" sentence is added. Verified by grepping `CLAUDE.md` for `status=` and `deferred` and finding nothing.

---

## Regenerate Antigravity Tree Status Free

Run `uv run scripts/migrate_skills_to_agy.py` to regenerate `.agents/plugins/cairn/` from the swept `skills/`, `agents/`, and `shared/` so the generated tree carries no trace of the attribute, and use the same pass to confirm the whole sweep is grep-clean. Verified by grepping `skills/`, `agents/`, `shared/`, `README.md`, `CLAUDE.md`, and `.agents/plugins/cairn/` for `status=`, `deferred`, and `Blocking` and finding only the capture skill's legacy blockquote note (and its generated copy), while "terse status line", `git status --porcelain`, "finish status", and the DONE/FAILED status wording survive untouched.

---
