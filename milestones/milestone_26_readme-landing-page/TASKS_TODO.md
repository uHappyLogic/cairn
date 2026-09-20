# TASKS TODO

## Promote Design Claims Into Docs Page

Commit `temp/cairn-design-claims.md` as `docs/design-claims.md` with its 19 claims, six-group order, **Design** paragraphs, and **Metric** lines kept word for word in Simplified Technical English, changing only the frame: the intro becomes one orienting paragraph for a repository reader (what the list is, why it uses a controlled register, that each Metric names the test that would check the claim, and that no test suite in the repository runs them yet), the closing note keeps only the half saying claims 17–19 concern the plugin's own code, and claim 12's sentence "the work tree is clean after each skill" is corrected in the same register to match the non-committing bootstrap skill and the partial-work-stays rule. Verified when the committed page diffs from the source only in those three places and each claim line still heads its own entry so the README block can link to it.

---

## Rebuild README First Screen Header

Rework the top of `README.md` so the first screen opens with the three shields.io badges followed by the adoption block — the existing three-row pipe table with its `## Adoption` heading dropped, its caption cut to one sentence of about two lines that keeps the four facts (cumulative since 2026-09-04, unique counts summed per day, the badge workflow's own fetch adds one unique clone per repository per day, the monorepo's clones include CI checkouts) — placed above `# Cairn`, then the title with its bold "Mark the path from idea to shipped." lead and the subtitle replaced verbatim by "Milestone-driven development for your coding agent — any kind of work, one milestone at a time." Delete the `<p align="center">` banner paragraph together with `.github/assets/readme/cairn-banner.png` and the then-empty `.github/assets/` directory in the same commit, and remove the old `## Adoption` section from its place near the foot of the file. Verified when the rendered page opens on badges, table, and title with no banner, the file has one adoption table and no `## Adoption` heading, and nothing in the repository references the deleted image.

---

## Add Simplified Milestone Loop Diagram

Insert one mermaid `flowchart` directly under the title block of `README.md`, before `## Installation`, drawing the six verbs define, review, recommend, answer, derive, complete chained by plain arrows plus one dashed return edge from answer back to review labelled with the convergence condition (until no open questions remain), with no finish step and no milestone-return edge, under the same `%%{init: …}%%` theme block the six phase diagrams in `docs/workflow.md` carry so the wrappingWidth keeps the return label on one line. Verified when the diagram renders on GitHub with exactly those six nodes and seven edges, its theme block is byte-identical to the phase diagrams', and the file gains no `{{` sequence.

---

## Demote Migration Note And Reorder Tail Sections

Move the "Already installed from `uHappyLogic/cairn`?" marketplace-migration paragraph and its second command block out of `## Installation` into a short `##` section of its own placed between `## Contributing` and `## License`, leaving one bold pointer line to it in the `### Claude Code` subsection, so Installation keeps only the two per-host subsections and `### Bootstrap your project`; order the remaining tail as `## How it works`, `## Self-dogfooding`, `## Contributing`, the migration section, `## License`, and add one closing sentence to `## How it works` linking `docs/workflow.md` and `docs/skill-reference.md`, changing no other section text. Verified when the section order reads Installation, Why Cairn, How it works, Self-dogfooding, Contributing, migration, License, the Claude Code subsection matches the root's install commands plus the pointer line, and the migration commands appear once, below the fold.

---

## Neutralize Why Cairn And Add Design Principles

Change the one host sentence in `## Why Cairn?` from "Cairn gives Claude Code a structured, repeatable process" to "Cairn gives your coding agent a structured, repeatable process", keeping its heading and three paragraphs otherwise intact, and add a short `## Design principles` section directly beneath it presenting three entries — claim 11 (records are machine-readable), claim 2 carrying claim 12's provenance subject (each decision has a record in git), and claim 5 (advice gets better with each milestone) — each the claim line verbatim as it heads `docs/design-claims.md` followed by one sentence of the design behind it in the README's voice, closing with one link to that page for all nineteen. Verified when the block is about a hundred words, each verbatim claim line matches a heading on the claims page, and `README.md` no longer names Claude Code as the host outside the Installation section.

---

## Rework Distribution README Templates And Rebuild Hosts

Rework `scripts/hosts/claude/README.md` and `scripts/hosts/antigravity/README.md` to the same shape: a centred two-badge strip of that repository's `traffic-data` unique-views and unique-clones badges above `# Cairn for <Host>` with no caption and no heading, the one-liner "Milestone-driven development for your coding agent — any kind of work, one milestone at a time." verbatim under the title, the generated-do-not-edit note with its `traffic-data` sentence reworded to say the SVGs now serve this page too and gaining one clause that the workflow's own daily fetch counts as one unique clone a day in the clones badge, the host's installation section (the Claude one split exactly as the root's, its install subsection word for word identical and the migration note in its own section reached by the same pointer line), over the existing `## Source` and `## License` tail, with no loop diagram, no "Why Cairn?" text, and no design-principles block; then run `uv run scripts/build_hosts.py` and commit the rebuilt `hosts/` trees with the templates. Verified when `uv run scripts/build_hosts.py --check` exits zero and both rendered `hosts/<host>/README.md` files carry exactly those items with no `{{` left outside a `${{` expression.

---

## Update CLAUDE.md Cross-References For Docs Move

Update every place `CLAUDE.md` describes the README or its sections to the finished layout: the `README.md` repository-layout entry (now a landing page with the first-screen adoption table and no `## Adoption` heading, the loop diagram, and the design-principles block), new layout entries for `docs/workflow.md`, `docs/skill-reference.md`, and `docs/design-claims.md`, the **Skill Frontmatter** invariant's statement of where cut material lives (now `docs/skill-reference.md`), and the `## Development` sentences that name the README's `## Adoption` table, and confirm `CONTRIBUTING.md` retains no link to a moved README section. Verified when a grep of `CLAUDE.md` and `CONTRIBUTING.md` for `Skill reference`, `Workflow pipeline`, `How skills commit`, and `## Adoption` finds only references that name their new homes and every relative link in both files resolves to an existing file and heading.

---
