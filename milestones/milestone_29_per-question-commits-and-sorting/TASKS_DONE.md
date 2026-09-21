# TASKS DONE

## Commit Procedure Optional BODY Input

Give `core/shared/commit-procedure.md` a third, optional input, BODY — zero or more body lines the caller supplies already resolved, never a policy the procedure decides — and make its commit step run `git commit -m "<SUBJECT>" -m "<BODY>"` when a body is given and subject-only otherwise, then have the four body-supplying callers (`answer-open-question`, `answer-open-question-with-alternative`, `answer-open-question-with-recommendation`, `capture-milestone-principle-updates`) hand their body over as BODY exactly as they hand over PATHS and SUBJECT, with every body-less caller unchanged. Needed because the recommend sweep's per-question commits carry a lifted body and the procedure is the single source of truth for how a body reaches git. Verified by reading the procedure and each caller for the three-input contract, by a rebuild of both host trees with `uv run scripts/build_hosts.py --check` passing, and by `uv run pytest` still passing.

**Verified:**

- `core/shared/commit-procedure.md` declares three inputs — PATHS, SUBJECT, and an optional BODY defined as zero or more caller-resolved body lines, with what a body holds and whether a pass carries one stated as the caller's decision and never the procedure's.
- Its step 3 commits with `git commit -m "<SUBJECT>" -m "<BODY>"` when the caller supplied a body and with `git commit -m "<SUBJECT>"` otherwise.
- Each of the four body-supplying callers (`answer-open-question`, `answer-open-question-with-alternative`, `answer-open-question-with-recommendation`, `capture-milestone-principle-updates`) says "Supply it these three inputs" and names its body input **BODY**, exactly as it names PATHS and SUBJECT; the one restated `git commit` command in the capture skill was replaced by a reference to the procedure.
- The eleven body-less callers are unchanged: `git diff --name-only -- core/` lists only the procedure and those four skills.
- Both host trees rebuilt with `uv run scripts/build_hosts.py` and `uv run scripts/build_hosts.py --check` passes ("Check passed: hosts/antigravity/ and hosts/claude/ match a fresh build of core/ at version 1.6.0.").
- `uv run pytest` passes (319 passed).

---
