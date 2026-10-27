# TASKS TODO

## Separate Draft Examples From Cairn Claims

Pass over the whole draft so every concrete example value (scenario ids, the manifest's plugin and host versions, model ids) is kept but stated once as a hypothetical example tracking no real version, while every statement about the current content of a Cairn document or tool, the tested-claim count in `docs/design-claims.md` first, points at that document without restating a value that moves. Verify by searching the draft for version numbers, model ids, and Cairn document references and confirming each is a marked example or a pointer.

---

## Audit Gap Coverage And Remove Report

Read `ideas/benchmark_design_gaps.md` gap by gap against the finished draft, confirm each of the eighteen ends as a decision written into the draft, adopted, adapted, or rejected with its reason stated in the text, write in any reason still missing, then remove the report as the milestone's last change so the draft is the single document under `ideas/` handed to the benchmark repository. Verify that the file is gone from the working tree and reachable only in git history from `aeb280a`, and that the draft refers to the report nowhere.

---
