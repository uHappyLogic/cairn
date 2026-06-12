# TASKS TODO

## Replace Pipeline Diagram with Mermaid Flowchart

Replace the plain-text fenced block in README.md's "Workflow pipeline" section (currently lines ~40–68) with an equivalent `mermaid` fenced flowchart. The diagram must cover the full skill sequence from `init-milestone-base-workflow` through `goto-next-milestone`, and must represent the open-questions trio (`highlight-milestone-requirements-open-questions` → `discuss-open-question` → `answer-open-question`) as an actual cycle with a back-edge, not a static box.

**Notes:**
- The current block opens with a bare ` ``` ` fence (no language tag) at approximately line 42. Replacing it requires changing the opening fence to ` ```mermaid ` and rewriting the contents as a valid Mermaid flowchart.
- `discuss-open-question` is labeled "(optional)" in the ASCII art; preserve that intent in the Mermaid graph (e.g. via a label on the edge or a note in the node label).
- The back-edge must point from the end of the loop (`answer-open-question`) back to `highlight-milestone-requirements-open-questions` so the cycle is explicit rather than implied by a surrounding box.
- The prose paragraph immediately after the closing fence (line ~70: "Run `highlight-milestone-requirements-open-questions` as many times…") stays unchanged.

**Success:**
- README.md's "Workflow pipeline" section contains a ` ```mermaid ` fenced block (not a bare ` ``` ` fence).
- The Mermaid block includes all twelve steps: `init-milestone-base-workflow`, `/init`, `discuss-milestone-goal`, `define-milestone-goal`, `specify-milestone-starting-implementation-state`, `highlight-milestone-requirements-open-questions`, `discuss-open-question`, `answer-open-question`, `populate-backlog`, `implement-backlog-tasks`, `finish-current-milestone`, `goto-next-milestone`.
- The block contains a back-edge from `answer-open-question` (or equivalent loop-end node) pointing back to `highlight-milestone-requirements-open-questions`.
- No other section of README.md is modified.

---








