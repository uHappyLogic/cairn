# TASKS TODO

## Draft Comparison Set And Input Versioning

Rewrite the draft's comparison-set, input, and trend text: a set is five versions (the seed tag, one prompt version per phase, the operator definition, the rater definition, and one pinned host CLI version the pre-flight refuses a run against when the installed one differs, a new rater version re-rating existing runs into a new set without re-running); it declares before its first scored run a roster holding at least the stated minimum scenarios and three phase-1 runs per scenario each with its own phase-2 child and no stopping rule; the checklist and hidden-requirement entries are frozen by blob hash before that run with a changed statement starting a new set and a changed check line a new rating version; a superseded set carries an authored one-line reason without which regeneration refuses; the trend restarts as a labeled segment on every input change with nothing re-run; and everything stays public with a canary, a dated contamination flag read from published training cutoffs, and a rotation rule. Verify by reading the text against the seven decisions and gaps 11, 12, 15, and 16.

---

## Draft README Table And Radar Rework

Rewrite the draft's README page section and the rank paragraph: the table's and the radar's openings recast as refutable expectations naming the table and the curves as what would refute them, each score cell carrying its minimum and maximum beside the mean as `82 (76–88)` with cost, time, invocations, and sessions staying means, ranks shared within a tie margin derived from the set's own per-run noise with cost playing no part, the hidden axis keeping its equal third with the stated reason, one declared reference scenario per family drawn on the radar whatever the ranking, five curves with the clarify family's rows and curve added, the voided-run count and causes beside the runs column, the repeat-rating agreement line and the lost column's noise floor, and the generated list of superseded sets with versions, input diff, reason, and link. Verify by reading the section against the nine decisions it carries and gaps 11, 16, and 18.

---

## Separate Draft Examples From Cairn Claims

Pass over the whole draft so every concrete example value (scenario ids, the manifest's plugin and host versions, model ids) is kept but stated once as a hypothetical example tracking no real version, while every statement about the current content of a Cairn document or tool, the tested-claim count in `docs/design-claims.md` first, points at that document without restating a value that moves. Verify by searching the draft for version numbers, model ids, and Cairn document references and confirming each is a marked example or a pointer.

---

## Audit Gap Coverage And Remove Report

Read `ideas/benchmark_design_gaps.md` gap by gap against the finished draft, confirm each of the eighteen ends as a decision written into the draft, adopted, adapted, or rejected with its reason stated in the text, write in any reason still missing, then remove the report as the milestone's last change so the draft is the single document under `ideas/` handed to the benchmark repository. Verify that the file is gone from the working tree and reachable only in git history from `aeb280a`, and that the draft refers to the report nowhere.

---
