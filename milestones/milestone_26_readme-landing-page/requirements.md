# Milestone 26: README landing page

## Goal

Turn the root `README.md` from a 6,500-word reference document into a landing page: drop the banner so the first screen is the release/CI/license badges and the adoption block, a generic host-neutral one-liner, a single simplified mermaid diagram of one milestone loop (define → review → recommend → answer → derive → complete, a stand-in until a later milestone records the demo GIF), and per-host installation, followed by a host-neutral "Why Cairn?" and a short "Design principles" block built from selected design claims. Move the phase narrative with its six mermaid diagrams, the skill reference, the commit conventions, and the answer-principle-learning loop into a new `docs/` directory, promote `temp/cairn-design-claims.md` into it as a committed page the principles block links to, and update every cross-reference in `CLAUDE.md` and `CONTRIBUTING.md` that named those README sections. Rework the two distribution README templates under `scripts/hosts/*/README.md` to the same shape — one-liner, that repository's adoption badges, installation, and the redirect to the root repository for contributors — and rebuild `hosts/` so `build_hosts.py --check` passes.

## Relevant starting state

### Root `README.md`

`README.md` is 6,498 words in ten `##` sections, weighted toward reference: `## Skill reference` is 4,312 words (25 `###` entries — 23 skills plus the two agents), `## Workflow pipeline` 1,107 (six mermaid `flowchart TD` diagrams, one per phase, chained by shared amber state nodes `D0`–`D5`, each under an identical `%%{init: …}%%` theme block that contains no `{{`), `## How skills commit` 329, `## Installation` 210, `## Why Cairn?` 147, `## Adoption` 110, `## How it works` 96, `## Contributing` 72, `## Self-dogfooding` 58, `## License` 6. The file opens with a `<p align="center">` banner (`.github/assets/readme/cairn-banner.png`, 4.7 MB, `width="100%"`) above a second centered paragraph of three shields.io badges (latest release, drift-gate CI on `main`, MIT), then `# Cairn`, the tagline "Mark the path from idea to shipped. / Milestone-driven development for any kind of work.", and `## Why Cairn?`, whose second paragraph reads "Cairn gives Claude Code a structured, repeatable process…". The one internal anchor is `[Skill reference](#skill-reference)` in the pipeline intro. The pipeline's "Iterating milestone requirements" paragraph already carries the boundary-line-CLI / query-where-it-pays rationale, and a `### The answer-principle-learning loop` subsection (three bullets: teaching flow, recommendation advisory, correction loop) sits inside the skill reference between `review-milestone-requirements` and `discuss-open-question`. Two skill-reference entries are known stale, recorded as follow-ups by milestone 15: `goto-next-milestone <number> <title>` (the skill is argument-free and creates nothing) and `finish-current-milestone`'s trailing "run `/goto-next-milestone` after".

### Cross-references to README sections

No `docs/` directory exists and nothing links to one. `CLAUDE.md` names the README in its repository-layout entry (line 41: "authoritative workflow documentation and skill reference, with a `## Adoption` section…"), in the **Skill Frontmatter** invariant (material cut from frontmatter descriptions has "`README.md`'s `## Skill reference` and this file" as its homes), and in the `## Development` prose ("the README's `ci` badge reports `main`'s pushed HEAD"; the `traffic-data` branch holds what "the README's `## Adoption` table reads"). `CONTRIBUTING.md` line 38 links `[Installation](README.md#installation)`; its `## Development` section is the build-loop text milestone 24 moved out of the README. `.github/PULL_REQUEST_TEMPLATE.md`, the three issue forms, and the release skill reference `milestones/README.md` and the rendered distribution README templates only, never a root-README section.

### Distribution README templates and the host build

`scripts/hosts/claude/README.md` (402 words) and `scripts/hosts/antigravity/README.md` (381 words) share one shape: `# Cairn for <Host>`, an opening paragraph (the Claude one says the plugin "gives Claude Code a milestone-driven development workflow", the Antigravity one "gives your coding agent…"), a **Generated — do not edit** blockquote that names the `traffic-data` branch, says issues are disabled, and redirects problems and proposals to `uHappyLogic/cairn`, then `## Installation` (that host's install steps plus `### Bootstrap your project`), `## Source` (the only `{{VERSION}}` slot, twice on one line), and `## License`. Each definition directory also carries a slot-free `CONTRIBUTING.md` pointer that already routes bug reports, pull requests, vulnerabilities, and questions to the root repository. `scripts/build_hosts.py` renders every non-`settings.toml` file in a definition directory to the same relative path in `hosts/<host>/`, and its `unfilled-placeholder` check (`(?<!\$)\{\{`) runs over every rendered file, README included, so any `{{` a template gains outside a `${{` expression fails the build; the committed `hosts/<host>/README.md` files are pure renders and `--check` diffs them byte-for-byte. Both distribution repositories carry their own `traffic-data` branch with `views-unique.svg` and `clones-unique.svg`, already linked from the root README's `## Adoption` table, so per-repository badges exist for each template. A template change reaches `hosts/` on rebuild but reaches the distribution repositories only through `/release-plugin`.

### Design-claims source

`temp/cairn-design-claims.md` is 1,288 words and untracked — `temp/` is in `.gitignore`. It lists 19 claims in six groups (Decisions 1–6, Work 7–9, Records 10–12, Efficiency 13–14, Robustness 15–16, Engineering 17–19), each a one-line claim with a **Design** paragraph and a **Metric** line, written in ASD-STE100 Simplified Technical English, closing with a note that claims 17–19 concern the plugin code rather than a user project. The three novelties the goal names map to claim 11 (machine-readable records, boundary-line CLI), claims 2 and 12 (one answer = one commit with a provenance subject; path-scoped staging), and claim 5 (advice improves per milestone via the principle store).

### Hosts and assets

Exactly two hosts exist — `scripts/hosts/claude/` and `scripts/hosts/antigravity/` — and the bug issue form's host dropdown mirrors that directory; the string "Codex" appears nowhere in the repository. `.github/assets/readme/` holds only `cairn-banner.png`, referenced solely by `README.md` line 2. The repository contains no terminal-recording tooling, tape script, sample project, or GIF — the demo the goal defers has no existing footing.

## Decisions

## Out of Scope

## Open questions

<open-question id="Adoption block form">
  <question>How compact should the adoption block be on the first screen, given that today it is a three-repository table of six badges under a three-sentence caption?</question>
</open-question>
<open-question id="One-liner wording">
  <question>What does the generic host-neutral one-liner say, and does it replace the existing two-line tagline or sit beside it?</question>
</open-question>
<open-question id="Loop diagram shape">
  <question>What does the simplified first-screen mermaid diagram show beyond the six named loop steps — the review-and-answer iteration, the milestone close, neither — and does it keep the theme block the six phase diagrams share?</question>
</open-question>
<open-question id="Docs page layout">
  <question>How are the moved sections — the phase narrative with its six diagrams, the skill reference, the commit conventions, and the answer-principle-learning loop — split across files under docs/, and what are those pages named?</question>
</open-question>
<open-question id="Design-claims page fidelity">
  <question>Is the design-claims file promoted into docs/ verbatim, keeping its Simplified Technical English style, its Metric lines, and its closing note on the plugin-code claims, or edited for a reader of the repository?</question>
</open-question>
<open-question id="Design principles selection">
  <question>Which design claims does the README design-principles block present, how many, and in what form — the claim line alone, or the claim with one sentence of the design behind it?</question>
</open-question>
<open-question id="Why Cairn rewrite depth">
  <question>Does the &quot;Why Cairn?&quot; section change only its host-naming sentence, or is it rewritten around the design-claims narrative, and does it stay a section separate from the design-principles block?</question>
</open-question>
<open-question id="Install section scope">
  <question>Does the first-screen installation section keep the bootstrap steps and the marketplace-migration paragraph, or do those move below the fold so only the per-host install commands remain on the first screen?</question>
</open-question>
<open-question id="Below-the-fold sections">
  <question>Which existing root README sections stay below the fold — how it works, contributing, self-dogfooding, license — and in what order after the design-principles block?</question>
</open-question>
<open-question id="Distribution README depth">
  <question>Beyond the one-liner, adoption badges, installation, and contributor redirect, do the distribution README templates also carry the loop diagram, the &quot;Why Cairn?&quot; text, or the design-principles block?</question>
</open-question>
<open-question id="Distribution badge form">
  <question>Where do a distribution repository&apos;s own unique-views and unique-clones badges sit in its README — in the top badge row or in an adoption section — and do they carry the caption about the workflow&apos;s own daily clone?</question>
</open-question>
<open-question id="Stale skill entries">
  <question>Are the two known stale skill-reference entries — the goto-next-milestone arguments and the finish-current-milestone next-step sentence — corrected as the reference moves into docs/, or left for a later milestone?</question>
</open-question>
<open-question id="Banner file disposal">
  <question>Is the banner image file deleted from the repository once the README no longer references it, or kept for another use?</question>
</open-question>
