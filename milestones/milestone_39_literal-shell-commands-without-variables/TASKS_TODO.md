# TASKS TODO

## Record Literal-Command Invariant in CLAUDE.md

Add one new standalone bullet under `## Invariants to preserve when editing skills` in `CLAUDE.md` recording the shell-splitting failure, the literal-path rule at `commit-procedure.md` and the `complete-task` agent's staging, the full-command rule for every runner that calls the open-question tool more than once (the five sites and the alternatives agent), and why the fix is a prose rule rather than a structural one such as a commit tool; it scopes the invariant to those sites by naming the `capture-milestone-principle-updates` snapshot (`SNAPSHOT="$(mktemp)"`, used quoted) as outside the rule, and leaves the open-question-tool bullet and the committing bullet unchanged with no pointer added. Verified by reading the bullet against the "CLAUDE.md rationale" decisions and, as the milestone's closing check, by `uv run scripts/build_hosts.py --check`, `uv run pytest`, and `uv run --no-project --python 3.9 --with pytest pytest` all passing with no file under `docs/` and no line of the capture skill changed.

---
