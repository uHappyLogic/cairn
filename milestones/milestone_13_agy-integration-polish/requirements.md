# Milestone 13: agy-integration-polish

## Goal

Polish the Google Antigravity (agy) integration by manually verifying and fixing the scripts/migrate_skills_to_agy.py script so it correctly transpiles both skills and agents. Document this local build step in the project documentation and update the GitHub project description to reflect dual-support.

## Relevant starting state

### Migration Script
`scripts/migrate_skills_to_agy.py` exists and handles the basic transpilation of `.mcp.json`, skills, and agents into `.agents/plugins/cairn/`. It performs a direct copy of the `agents/` directory without any agy-specific formatting adjustments, and injects YAML frontmatter into `SKILL.md` files if missing.

### Project Documentation
The project's main documentation (`README.md` and `CLAUDE.md`) focuses exclusively on Claude Code. There are currently no instructions documented for running the local transpilation step.

### GitHub Integration
The project's GitHub description currently reflects single-platform support and is known to be missing the Google Antigravity dual-support update.

## Decisions

## Out of Scope

## Open questions

<open-question id="Agent format compatibility" status="open">
  <question>Do the copied agent `.md` files require any Google Antigravity-specific formatting (e.g. YAML frontmatter, different extension, or structural changes) to function correctly as subagents in the transpiled plugin?</question>
</open-question>

<open-question id="Skill frontmatter requirements" status="open">
  <question>What specific YAML frontmatter fields does Google Antigravity require for skills, and does the current script inject all of them?</question>
</open-question>

<open-question id="Transpilation docs placement" status="open">
  <question>Where should the local transpilation step instructions be documented (e.g., a new section in README.md, added to CLAUDE.md, or elsewhere)?</question>
</open-question>

<open-question id="GitHub description update method" status="open">
  <question>How should the GitHub project description update be delivered? (e.g. Should we just draft the new text for manual update, or is there an API/scripted way we should use?)</question>
</open-question>
