# TASKS TODO

## Run Independent Zero-Findings Re-Audit

Run the milestone's final independent re-audit of the whole plugin — the success proof. Dispatch a single fresh-context subagent given only (a) the decided finding criteria and (b) the full file set to audit, with no access to this sweep's reasoning, and collect its structured output. This is the milestone's success-proof mechanism per the "Re-audit execution form" and "Re-audit task success wording" decisions; it audits, it does not fix.

**Notes:**
- The subagent must be given only two inputs and nothing about how the sweep was done (independence is the whole point). Input (a) — the finding criteria, taken verbatim from the "SE-specific finding boundary" decision: a finding is any text assuming the user's own deliverable or domain is software engineering (personas, "the code/codebase," insertion points, build/test verification, code examples, and the like), applied as the generalizable "does this assume the user's deliverable is software?" test to cases the initial audit did not foresee; with Cairn's own operating mechanics exempt as domain-uniform plugin infrastructure — git commits and git-log greps, path-scoped staging, the `CLAUDE.md`/`README.md`/`milestones/README.md` file names, and the consuming project being a git repository. Input (b) — the full file set: everything under `skills/`, `agents/`, `shared/`, plus root `README.md` and `CLAUDE.md`.
- The subagent returns a structured per-finding list — each finding giving the file path, the location, the offending phrase, and which criterion/layer it violates — or an explicit zero-findings verdict when it finds nothing. Report that structured output.
- Success is that the audit ran and its structured output was delivered — the per-finding list or the explicit zero-findings verdict — **not** that the verdict is clean. Do not fix findings within this task and do not author the next round here: on findings, follow-up fix tasks plus a fresh re-audit task are appended after this one (that queuing is separate work), iterating until a run comes back clean; that final clean verdict is the milestone's zero-findings proof.

**Success:**
- A single fresh-context subagent was dispatched with only the two inputs — the decided finding criteria (the "SE-specific finding boundary" test and its exemptions) and the full file set (`skills/`, `agents/`, `shared/`, `README.md`, `CLAUDE.md`) — and no access to the sweep's reasoning.
- The subagent's structured output was produced and reported: either a per-finding list (each entry carrying file path, location, offending phrase, and the criterion/layer violated) or an explicit zero-findings verdict.
- No findings were fixed and no follow-up tasks were authored within this task — its deliverable is solely the delivered audit output, whatever the verdict.

---
