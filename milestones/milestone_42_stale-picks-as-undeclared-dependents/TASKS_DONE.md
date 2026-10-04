# TASKS DONE

## Build Local Replay Case Manifest

Assemble, under the git-ignored `temp/`, the case manifest for the replay: the eight windows (fourteen pick-versus-decision pairs) the uncommitted sweep-contradiction analysis there identified, in this repository and in other local projects, with no other windows added, each hand answer of a window (and each goal revision in it, as a case of its own, since a revision now clears picks too) resolved to its commit and that commit's parent, and for each case the decision it folded laid beside every standing pick's option and recommendation text at that parent, every label left blank for the maintainer. This is the fixed case set the change is measured on, and all of it is per-case material that stays local. Verified when the manifest accounts for all eight windows and fourteen pairs, every case resolves read-only in its own repository, and `git status` shows no change outside `temp/`.

**Verified:**

- The manifest `temp/stale-pick-replay/manifest.json` exists under the git-ignored `temp/` (`git check-ignore` matches it), beside the script that built it and a rendered reading view, and holds exactly the eight windows of the analysis's stale-pick class, in this repository and in other local projects, with no other window.
- All fourteen pick-versus-decision pairs are accounted for: each is recorded in its window as a candidate pointer (never a label) to one case, and its pick stands among that case's standing picks at the parent.
- Every hand answer and every goal revision inside each window is a case of its own, 31 in all (24 hand answers, 7 goal revisions), each recorded with its commit and that commit's single parent.
- Each case lays the decision it folded (its `requirements.md` change, with the commit body) beside every pick standing at the parent, 449 pick entries in all, each with its recommended option's what-it-is text and its recommendation text, none empty.
- Every label is blank (0 of 449 labelled), and the bar's two thresholds and round count are empty slots left for the maintainer.
- `python3 temp/stale-pick-replay/build_manifest.py verify` re-resolves every case in its own repository with read-only git commands, finds commit, parent, folded text, and standing picks equal to the manifest, finds each source repository's `HEAD`, refs, and status unchanged across the run, and exits 0.
- `git status` in this repository showed no change outside `temp/` before the task-list move.

---

## Let Remove Reconcile Named Undermined Dependents

Extend `remove` in `core/tools/open_questions.py` with an optional argument naming further Short Titles to reconcile as undermined dependents of the removed block: every title is resolved before anything changes (a title matching no block, and equally the answered block's own title, stops the call on one `Error:` line naming that title and, for an unknown one, the ids the document holds, with exit status 1 and the document byte-for-byte unchanged), and each named block then goes through the same per-block strip primitive as the `<depends-on>`-tagged dependents in the same one write, transitively and keeping its `<alternative>` children, except that a named block carrying no `<recommendation>` is left exactly as it stands and seeds no transitive strip. The hand-answer path needs this to clear picks no tag declares; the tool still prints nothing on success, and its docstring and `--help` state the new contract. Verified by new cases in `tests/test_remove.py` for each of those behaviours passing under both `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest`, with `hosts/` rebuilt and `uv run scripts/build_hosts.py --check` passing.

**Verified:**

- `remove` in `core/tools/open_questions.py` takes the optional `--undermined SHORT_TITLE...` (one or more Short Titles after the block's own, the flag repeatable, compared un-escaped and case-folded, a title named twice counted once), and a call without it behaves as before: the 48 earlier tests of `tests/test_remove.py` pass unchanged.
- Every named title is resolved before anything changes: a title matching no block stops the call on the one line `Error: no <open-question> block has the id "<title>"; the document holds <ids>`, and the removed block's own title on the one line `Error: --undermined names "<title>", the block being removed, which cannot be reconciled as its own dependent`, each with exit status 1, empty stdout, no write reached, and the document byte-for-byte unchanged even when valid titles and tagged dependents accompany the bad one.
- Each named block goes through `strip_recommendation`, the same primitive as the `<depends-on>`-tagged dependents, in the same single write (one `save_document` call covering the removal, the tagged dependents, and the named ones), keeping its `<alternative>` children; a named block is stripped even when its own tag agrees with `--option`, while an un-named agreeing dependent still loses only its tag.
- The strip is transitive from a named block: blocks whose `<depends-on>` names a stripped named block are stripped in turn, alternatives kept, with no tag left naming a stripped block and unrelated blocks byte-identical.
- A named block carrying no `<recommendation>` (alternatives only, or bare) is left exactly as it stands, the call still succeeds and makes its write, and a block whose `<depends-on>` names it keeps its pick and its tag; `remove_question` returns no id for it.
- The tool prints nothing on success with `--undermined` (exit status 0, empty stdout and stderr).
- The module docstring's `remove` entry and `remove --help` state the new contract (the flag, resolution before any change, the two refusals, the same strip in the same write, the no-recommendation exception), checked by a test.
- 17 new cases in `tests/test_remove.py` cover those behaviours; `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest` each pass all 544 tests.
- `hosts/` was rebuilt with `uv run scripts/build_hosts.py` (the tool rendered into all three host trees) and `uv run scripts/build_hosts.py --check` passes.

---

