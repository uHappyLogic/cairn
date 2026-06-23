# TASKS DONE

## Split Workflow Pipeline Into Per-Phase Diagrams

Replace the single monolithic `flowchart TD` Mermaid block under `## Workflow pipeline` in `README.md` (currently lines ~56–148) with six smaller per-phase `flowchart TD` diagrams, one per existing subgraph `S0`–`S5`, each in its own `###` subsection preceded by a short paragraph of flow prose and chained via the shared parallelogram state seam nodes `D0`–`D5` (each diagram ends with the seam node the next one begins with). Apply every design decision settled in this milestone's `requirements.md` `## Decisions` section — node-label trimming, per-diagram styling, node shapes, flow direction, and the cross-phase loop are all specified there. This task touches **only** the `## Workflow pipeline` section.

The six `###` subsections, in this top-to-bottom order, carry the nodes from the current subgraphs:
1. **One-time setup** — `/init`, `/init-milestone-base-workflow` (was `S0`); ends at `D0`.
2. **Initializing a milestone** — `/discuss-milestone-goal`, `/define-milestone-goal`, `/goto-next-milestone` (was `S1`); enters from `D0` and also from `D5` labeled "next milestone"; ends at `D1`.
3. **Iterating milestone requirements** — `/specify-milestone-starting-state`, `/review-milestone-requirements`, `/discuss-open-question`, `/answer-open-question`, `/try-capture-answer-principle`, `/try-answer-all-questions-by-principle`, `/reject-auto-answer` (was `S2`, the largest at 7 nodes); enters from `D1`; ends at `D2`.
4. **Automated one-shot task derivation and completion** — `/derive-tasks`, `/complete-all-tasks` (was `S3`); enters from `D2`; ends at `D3`.
5. **Semi-manual follow-up and adjustments** — `/ask-in-milestone-context`, `/discuss-new-task`, `/submit-task`, `/complete-task` (was `S4`); enters from `D3`; ends at `D4`.
6. **Ending a milestone** — `/finish-current-milestone` (was `S5`); enters from `D4`; terminates at `D5`.

**Notes:**
- Full skill descriptions stay only in the `## Skill reference` section — do not duplicate them in the trimmed nodes.
- Do not edit `## Skill reference`, `## Self-dogfooding`, or any other README section; this task is scoped to `## Workflow pipeline` only.
- The following are **deferred to the human visual pass — NOT part of this task's completion bar** (this repo has no render/build step, so legibility cannot be machine-verified). The completer produces the primary structure (uniform `flowchart TD`, loop on the receiving end, no regrouping) and a human does visual tuning afterward:
  - (a) the Deferred legibility-target width / nodes-per-row bar — settled visually while rendering.
  - (b) if the requirements-iteration (phase 3) diagram renders uncomfortably tall at GitHub's content width, the fix is to regroup or split its nodes — **not** to switch it to `LR`.
  - (c) the ghost-node fallback for the cross-phase loop (a sending-end "Initializing a milestone" ghost node in the Ending diagram) if a dashed loop from an otherwise-orphan `D5` renders confusingly.
  - (d) optional inter-subsection markdown anchor links between the chained phases.

**Success:**
- `## Workflow pipeline` contains exactly six `### ` subsections in the order above, each with a short prose paragraph and exactly one fenced ```mermaid``` block opened by `flowchart TD`.
- Every skill node label is a bare skill name — no `<br/>` description text and no `(optional)`/`(auto)` qualifier appears in any node label.
- State nodes `D0`–`D5` keep the parallelogram `[/ /]` shape and the amber `state` class; each internal seam node (`D0`–`D4`) appears in its two adjacent diagrams.
- The Initializing-a-milestone diagram contains a "next milestone" entry arrow from `D5` into `/discuss-milestone-goal`; the Ending-a-milestone diagram terminates at `D5` with no outgoing cross-phase edge.
- The two former hexagon nodes (`/answer-open-question`, `/complete-task`) are plain boxes (`[ ]`, not `{{ }}`); a dashed `optional` `classDef` is still present and applied.
- No `linkStyle 11,15,24,28` line referencing the old monolith's edge indices remains.
- No README section other than `## Workflow pipeline` is modified.

---

