# Milestone 26: README landing page

## Goal

Turn the root `README.md` from a 6,500-word reference document into a landing page: drop the banner so the first screen is the release/CI/license badges and the adoption block, a generic host-neutral one-liner, a single simplified mermaid diagram of one milestone loop (define → review → recommend → answer → derive → complete, a stand-in until a later milestone records the demo GIF), and per-host installation, followed by a host-neutral "Why Cairn?" and a short "Design principles" block built from selected design claims. Move the phase narrative with its six mermaid diagrams, the skill reference, the commit conventions, and the answer-principle-learning loop into a new `docs/` directory, promote `temp/cairn-design-claims.md` into it as a committed page the principles block links to, and update every cross-reference in `CLAUDE.md` and `CONTRIBUTING.md` that named those README sections. Rework the two distribution README templates under `scripts/hosts/*/README.md` to the same shape — one-liner, that repository's adoption badges, installation, and the redirect to the root repository for contributors — and rebuild `hosts/` so `build_hosts.py --check` passes.

## Relevant starting state

## Decisions

## Out of Scope

