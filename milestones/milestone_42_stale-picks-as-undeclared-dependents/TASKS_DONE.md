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

