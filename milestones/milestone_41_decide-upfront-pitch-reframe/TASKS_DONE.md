# TASKS DONE

## Replace Root README Tagline And One-Liner

In the root `README.md` title block, replace the bold tagline with "Mark the path first, then hand off the walk." and the line below it with the one-liner "Cairn brings all the important questions up to be decided upfront, so you can hand long-running execution to your agent confidently.", so the first screen states the decide-upfront identity as plain fact with no category noun and no tail. Verified when both new lines sit under `# Cairn` in the same two places, each exactly once, and neither "Mark the path from idea to shipped." nor the old milestone-driven one-liner remains in the file.

**Verified:**

- The bold tagline under `# Cairn` in the root `README.md` (line 28, the old tagline's place) reads exactly `**Mark the path first, then hand off the walk.**`.
- The line directly below it (line 29, the old one-liner's place) reads exactly "Cairn brings all the important questions up to be decided upfront, so you can hand long-running execution to your agent confidently.", with no category noun and no tail.
- `grep -c` finds each of the two new lines exactly once in `README.md`.
- `grep -c` finds neither "Mark the path from idea to shipped" nor "Milestone-driven development for your coding agent" in `README.md` (zero matches each).
- `git diff -- README.md` shows those two lines as the file's only change (2 insertions, 2 deletions).

---

## Regroup First-Screen Diagram Into Two Subgraphs

Rework the root `README.md` mermaid diagram so define, review, provide alternatives, recommend, and answer sit inside a subgraph titled for deciding upfront and derive and complete sit inside a second subgraph titled for handing execution to agents, with the answer-to-derive edge crossing between them labelled as the handoff and the three colour classes (`init`, `req`, `auto`) reduced to two, one per group. All seven skill-named nodes, the left-to-right layout, and the dashed "until no open questions remain" return edge from answer to review are kept, so the picture shows the new identity instead of giving the question loop and execution equal weight. Verified when the block parses as valid mermaid and shows exactly that structure.

**Verified:**

- The root `README.md` mermaid block, extracted and passed to the mermaid library's `mermaid.parse`, parses without error as a `flowchart-v2` diagram, while a deliberately broken copy of it is rejected with a parse error.
- The parsed diagram's direction is `LR`, and its seven skill-named nodes are `define`, `review`, `provide alternatives`, `recommend`, `answer`, `derive`, and `complete`, with labels unchanged.
- The parsed diagram holds exactly two subgraphs: `upfront`, titled "Decide upfront", containing define, review, alternatives, recommend, and answer; and `agents`, titled "Hand execution to agents", containing derive and complete.
- The `answer -> derive` edge is a solid edge labelled "handoff" and is the only edge between the two subgraphs.
- The `answer -> review` return edge is dotted and labelled "until no open questions remain".
- The remaining edges are the solid chain `define -> review -> alternatives -> recommend -> answer` and `derive -> complete`, seven edges in all.
- The block defines exactly two colour classes, `decide` (the five nodes of the first subgraph) and `execute` (the two nodes of the second); `grep` finds no `classDef init`, `classDef req`, or `classDef auto` in `README.md`.
- `git diff -- README.md` shows changes only inside the mermaid block (lines 34 to 56); the `%%{init}%%` line, `flowchart LR`, and everything outside the block are unchanged.

---

