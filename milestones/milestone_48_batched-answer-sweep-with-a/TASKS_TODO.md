# TASKS TODO

## Describe Batched Sweep And Fold Tool In Docs

Update the documentation surfaces: `docs/skill-reference.md`'s `answer-all-open-questions-with-recommendation` entry (the compact view and same-turn read, the one batched call with its guard, skip, stop, markers, and in-call walk, no cascade and no contradiction advisory, the fold tool) and `review-milestone-requirements` entry (the `## Decisions` consistency step authoring one block per conflicting pair), `docs/workflow.md`'s requirements-phase narrative (the fold tool beside the open-question tool, the sweep's recording sentence) and its committing paragraph (the sweep's per-section commit inside its one call), and `docs/design-claims.md` wherever a claim counts the tools or the `tests/` coverage, with `README.md`, `CONTRIBUTING.md`, `milestones/README.md`'s file list, `docs/ways-of-using-cairn.md`, and the host README templates confirmed to need no edit, naming no host in any rendered file. Verified by `grep` showing no doc still describing the sweep's whole XML read, per-answer `locate`, contradiction pairs, or cascade, by each touched claim matching the landed files and tests, and by `uv run scripts/build_hosts.py --check` passing.

---

## Hands-On Check Of Sweep In Claude Code

Run the rewritten sweep hands-on in Claude Code from the checkout's own `hosts/claude` marketplace install, headless as `docs/ways-of-using-cairn.md` invokes it, against a throwaway project whose current milestone holds recommendation-bearing blocks, a recommendation-less one, and a stale `<depends-on>` that makes one lift fail, covering the compact view and the requirements read sent in one turn, the batched call composed and run as shown, one commit per answer, the silent skip, the report's status line, and the stop path after a fold (provoked by hand on the shown call), and rewrite the dated block in the header of `scripts/hosts/claude/settings.toml` as that check, naming the installed `claude` version and the points covered while carrying forward its earlier points; read the rendered `hosts/antigravity/` and `hosts/codex/` sweep files through against the Claude Code one with no run, confirming they differ only by plugin root, and record nothing in those hosts' blocks. Verified when the block names every point checked, no other host's block and no `CLAUDE.md` invariant changes, and `uv run scripts/build_hosts.py --check` passes.

---
