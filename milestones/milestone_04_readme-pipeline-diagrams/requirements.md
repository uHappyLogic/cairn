# Milestone 4: README Pipeline Diagrams

## Goal

Replace the oversized Workflow pipeline Mermaid diagram in README.md with a sequence of smaller per-phase diagrams (setup, milestone init, requirements loop, automated derivation/completion, follow-up, ending), each in its own subsection with short flow prose, chained by shared linked start/end nodes, with nodes trimmed to skill names so the Skill reference section remains the single home for full descriptions — optimized for legibility at GitHub's content width on desktop, with general README polish as a secondary goal.

## Relevant starting state

### Monolithic workflow pipeline diagram (the replacement target)

`README.md` lines 56–148 hold a single `mermaid` fenced block under the `## Workflow pipeline` heading — this is what the milestone replaces. It is one `flowchart TD` opened by an `%%{init: ...}%%` theme block (base theme, custom `fontFamily`/`lineColor`/`primaryBorderColor`, `flowchart.wrappingWidth:9999`, `curve:basis`). Structure: six `subgraph`s `S0`–`S5` (One-time setup, Initializing a milestone, Iterating requirements, Automated derivation/completion, Semi-manual follow-up, Ending a milestone), each holding 1–7 skill nodes (`S2` is the largest at 7: `ITM0`–`ITM6`), interleaved with six parallelogram "state" nodes `D0`–`D5` that mark the hand-off between phases. Edges are declared in one block after the subgraphs, including dashed optional/repeat edges and the single cross-phase loop `D5 -.->|next milestone| IM1`.

### Node label convention and styling

Each skill node embeds both its name and a full description: `["<b>/skill-name</b><br/>long description"]`. The goal trims these to bare skill names. Node *shape* currently encodes role (`([...])` stadium for setup, `[...]` box, `{{...}}` hexagon for `/answer-open-question` and `/complete-task`, `[/.../]` parallelogram for state nodes). Styling lives in eight `classDef`s (`setup`, `init`, `req`, `auto`, `manual`, `finish`, `optional` dashed-stroke, `state`) plus per-node `class` assignments and a `linkStyle 11,15,24,28` line that recolours specific edges by index — note edge indices are positional, so splitting the diagram invalidates them.

### Skill reference section (the intended single home for descriptions)

`README.md` lines 150–234 (`## Skill reference`) document every skill as `### \`skill-name <args>\`` headings with full prose. The goal explicitly relies on this section remaining the authoritative description home once diagram nodes are trimmed to names. One subsection (`### The answer-principle-learning loop`, ~line 172) groups several skills under a narrative rather than one-per-heading. There is no per-skill anchor convention in use today beyond the auto-generated GitHub heading anchors.

### README structure and known polish targets

The file is a single linear document: centered banner image + release/license badges, `# Cairn`, `## Why Cairn?`, `## Installation`, `## How it works`, `## Workflow pipeline` (the diagram), `## Skill reference`, `## Self-dogfooding`, `## License`. The `## Self-dogfooding` section (lines 236–238) names the active milestone as `milestones/milestone_01_public-release-prep/`, which is stale — the current milestone is `milestone_04` and three milestones have since completed. This is the concrete polish example cited in the Polish-scope open question. The repo is plain Markdown with no build or render step, so diagram legibility is verified only by viewing the rendered README on GitHub.

## Decisions

### Polish scope

General README polish is strictly opportunistic: no discretionary polish edits are required, and polish is folded in only where the diagram rewrite already has the file open. The single exception — the only mandated polish edit — is fixing the stale `## Self-dogfooding` reference from `milestone_01_public-release-prep` to the current `milestone_04`, since it is a known factual error in a section the diagram work will not otherwise touch. This gives `/derive-tasks` a crisp boundary: zero discretionary polish required, exactly one mandated polish fix.

### Diagram chaining and the cross-phase loop

The per-phase diagrams are chained by reusing the existing parallelogram state nodes (`D0`–`D5`, the `[/ /]` blocks) as shared seams: each per-phase diagram ends with the state node that the next diagram begins with, so every internal state node (`D0`–`D4`) appears at exactly two adjacent seams. Visual repetition of the shared node at each seam is the load-bearing chaining mechanism; prose markdown anchor links between subsections are optional polish, added only if the legibility pass shows the chain is hard to follow. Clickable in-diagram Mermaid node links are not used.

The single cross-phase "next milestone" loop (formerly `D5 -.->|next milestone| IM1`) is hosted on the receiving end: the *Initializing a milestone* diagram shows `D5` as a second entry arrow into `/discuss-milestone-goal` labeled "next milestone," alongside the normal `D0` entry — so the loop reads as just another repeated state node entering a diagram, keeping one uniform rule. The *Ending a milestone* diagram stays clean and simply terminates at `D5`. Fallback, if a dashed loop from an otherwise-orphan `D5` renders confusingly: a sending-end ghost "Initializing a milestone" node in the Ending diagram instead — to be settled visually during the legibility pass.

### Node labels

Skill nodes are trimmed to bare skill names with no inline qualifiers — no `(optional)` / `(auto)` tags in the label text. All nuance is pushed out of the labels into its single natural home: optionality is carried by the dashed `optional` styling, triggers like "auto after answering" / "repeat until satisfied" / "next milestone" by edge labels, and any residual nuance by the per-subsection flow prose. This keeps each fact in exactly one place and maximizes legibility. The no-qualifier rule is conditional on the dashed optional styling being retained: if the per-diagram styling pass drops that styling, optionality loses its visual home and a minimal `(optional)` text tag may be reintroduced as the cheapest way to keep it visible.

### Per-diagram styling

The styling is kept rather than simplified. Each per-phase diagram retains its phase colour `classDef`, so the palette gives cross-diagram phase identity and continuity across the stacked sequence; within a single-phase diagram all skill nodes share one hue, which is expected — colour's job becomes cross-diagram identity rather than intra-diagram distinction. The shared seam state nodes (`D0`–`D5`) keep their amber `state` styling across every diagram so the chaining reads consistently. The dashed `optional` `classDef` is retained — this satisfies the condition the Node labels decision depends on, so the no-qualifier label rule stands and optionality keeps its visual home. On node shapes: the parallelogram shape is kept for the state seam nodes (it reinforces the hand-off markers), but the hexagons (`/answer-open-question`, `/complete-task`) are flattened to plain boxes — the hexagon's "manual node" signal only mattered when all phases shared one diagram; per-phase, colour carries phase identity and the parallelogram marks the seams, so the hexagon is redundant.

### Flow direction

All per-phase diagrams use `flowchart TD` uniformly — one flow axis for the whole stacked sequence, with the shared seam state nodes (`D0`–`D5`) forming a single top-to-bottom spine that matches the page's scroll direction. No diagram switches to `LR`. The one large diagram (the requirements-iteration phase, `ITM0`–`ITM6`) is the one to watch during the visual legibility pass: if TD makes it uncomfortably tall at GitHub's content width, the fix is to split or regroup that diagram's nodes rather than switch it to `LR` — keeping the TD axis uniform across all diagrams outweighs saving vertical space on a single diagram.

## Open questions

> **Deferred — Legibility target:** the concrete width / nodes-per-row bar for "legible at GitHub's content width on desktop" — settled visually while rendering.

## Out of Scope

