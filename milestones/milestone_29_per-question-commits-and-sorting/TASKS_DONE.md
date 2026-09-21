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

## Tool Sort Subcommand With Tests

Add a `sort MILESTONE_DIR` subcommand to `core/tools/open_questions.py` — registered through `add_subcommand` and listed in the module docstring's `Subcommands:` — that rewrites the document with the `<recommendation>`-bearing blocks first in exactly `walk_order`'s order (origins, then dependents by depth, same-depth ties in prior document order) and every `<recommendation>`-less block last in stable prior document order, reusing `walk_order` rather than reimplementing it, printing nothing on success and one `Error:` line with the document unchanged on failure; `render_document` and every other subcommand keep writing blocks in their existing order. Needed so `walk` is by construction the annotated prefix of `list` on a sorted document. Verified by a new `tests/test_sort.py` (annotated prefix equals `walk`'s print, un-annotated blocks last in prior order, `sort` idempotent and the identity on an already-sorted document such as the `annotated` fixture, silent success, `Error:` on a missing document) passing under both `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest`, and by a rebuild with `uv run scripts/build_hosts.py --check` passing with the tool rendered byte-identical.

**Verified:**

- `core/tools/open_questions.py` registers `sort` through `add_subcommand` in `build_parser`, taking `MILESTONE_DIR` alone — an extra argument or a missing directory is argparse's usage error with exit 2, and `--help` lists it beside the other nine subcommands.
- The module docstring's `Subcommands:` list carries a `sort MILESTONE_DIR` entry, and its format list states that blocks stay in the order the document holds them, `add` appending and only `sort` reordering.
- The written order is `sort_order(document)` = `walk_order(document)` followed by every `<recommendation>`-less block in its prior document order — the walk reused by call, never reimplemented (a monkeypatched `walk_order` changes what `sort` writes) — so after a sort `list` prints exactly `walk`'s ids then `list --unannotated`'s.
- `sort` prints nothing on success; a missing or malformed document is one `Error: <reason>` line on stderr with exit 1, the document byte-for-byte unchanged and nothing created; a document already in sorted order is left untouched (same inode and mtime), the `annotated`, `bare`, `entities`, and `empty` fixtures included, and a second sort after a first writes nothing.
- The diff to the tool is purely additive (0 removed lines): `render_document`, `save_document`, and every other `cmd_*` keep writing blocks in `document.questions` order, pinned by a test running `add`, `strip`, and `remove` on an unsorted document and by `render_document` on an unsorted `Document`.
- `tests/test_sort.py` (28 tests) pins the annotated prefix equalling `walk`'s print, un-annotated blocks last in prior order, same-depth ties and cycle promotion matching `walk`, blocks moved verbatim with the document kept canonical, idempotence, the identity on every golden fixture, silent success, and the `Error:` on a missing document; `tests/test_contract.py`'s help enumeration gained `sort`.
- `uv run pytest` passes (347 passed) and `uv run --no-project --python 3.9 --with pytest pytest` passes (347 passed under Python 3.9.25).
- `uv run scripts/build_hosts.py` rebuilt both host trees and `uv run scripts/build_hosts.py --check` passes ("Check passed: hosts/antigravity/ and hosts/claude/ match a fresh build of core/ at version 1.6.0."); `cmp` confirms `hosts/claude/tools/open_questions.py` and `hosts/antigravity/tools/open_questions.py` byte-identical to `core/tools/open_questions.py`.

---

## Recommend Sweep Per-Question Commits

Change `core/skills/recommend-all-open-questions/SKILL.md` so that after each silent `embed` in step 3 the orchestrator runs the tool's `lift <MILESTONE_DIR> "<Short Title>"` and commits through `{{PLUGIN_ROOT}}/shared/commit-procedure.md` with PATHS `<MILESTONE_DIR>/open_questions.xml`, SUBJECT `Recommendation-annotation: <Short Title>`, and BODY the lifted "`<option>` — `<rationale>`" line, before the next dispatch, while a skipped question commits nothing and the once-per-run `Recommendation-annotation: <milestone_id>` commit of step 4 and its "never inside the dispatch loop" wording are removed. Needed so the sweep's granularity mirrors the answer sweep's one commit per question. Verified by reading the skill against `answer-all-open-questions-with-recommendation`'s step 2 for the same lift-then-commit shape, and by a rebuild with `uv run scripts/build_hosts.py --check` passing.

**Verified:**

- In step 3 of `core/skills/recommend-all-open-questions/SKILL.md`, every silent `embed` — a first return's or a repaired return's — is followed by a new sub-step **d** that runs `python3 {{PLUGIN_ROOT}}/tools/open_questions.py lift <MILESTONE_DIR> "<Short Title>"` and holds its printed "`<option>` — `<rationale>`" line as the commit body, before the next dispatch (sub-step **b**'s silent branch and the repaired-return sentence both route to it).
- Sub-step **d** commits through `{{PLUGIN_ROOT}}/shared/commit-procedure.md` with the three inputs named exactly as PATHS `<MILESTONE_DIR>/open_questions.xml`, SUBJECT `Recommendation-annotation: <Short Title>`, and BODY the lifted line — the same "Supply it these three inputs" shape the body-supplying callers use.
- The skill states that a skipped question commits nothing, both in sub-step **d** and in the second-failure skip sentence of sub-step **c**, and that the sweep needs no clean working tree.
- The once-per-run commit is gone: `grep` for `Recommendation-annotation: <milestone_id>`, `never inside the dispatch loop`, `once at the end of the run`, and `these two inputs` returns nothing in the skill; the old step 4 heading is removed and the report step is renumbered to `### 4. Report`.
- Every cross-reference is consistent with the new structure: step 1b and the two advisory notes point at step 4, the report step's nothing-committed condition names "no `embed` call wrote, so step 3 reached its sub-step **d** for no question" instead of a removed step-4 guard, and the opening paragraph names `lift` among the tool calls and states one `Recommendation-annotation: <Short Title>` commit per annotated question.
- Read against `answer-all-open-questions-with-recommendation`'s step 2, the shape is the same: one `lift` per question whose print is the body, one commit per question under a `<Marker>: <Short Title>` subject before the next dispatch, and "the per-question granularity is the point"; the one difference — the shared commit procedure's path-scoped stage rather than an agent-staged index — is the writer-is-the-orchestrator arrangement `requirements.md`'s starting state names.
- `uv run scripts/build_hosts.py` rebuilt both host trees and `uv run scripts/build_hosts.py --check` passes ("Check passed: hosts/antigravity/ and hosts/claude/ match a fresh build of core/ at version 1.6.0."); `uv run pytest` still passes (347 passed).
- `hosts/claude/skills/recommend-all-open-questions/SKILL.md` and `hosts/antigravity/skills/recommend-all-open-questions/SKILL.md` carry the change, each differing from `core/` only by its plugin-root literal.

---
