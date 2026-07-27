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

- The GitHub project description will be updated programmatically via a task running `gh repo edit --description "..."` since the GitHub CLI is already configured locally.
- The local transpilation step instructions will be documented in both `CLAUDE.md` and a new development section in `README.md`.
- No changes are required for agent format compatibility: the existing flat `.md` files parse correctly for internal dispatch in Google Antigravity while naturally staying hidden from the public registry, preserving their encapsulated design.


## Out of Scope

## Open questions

<open-question id="Skill frontmatter requirements" status="open">
  <question>What specific YAML frontmatter fields does Google Antigravity require for skills, and does the current script inject all of them?</question>
  <alternative id="Accept current injection">
    Conclude that Antigravity requires `name` and `description` and the script successfully injects these fields as fallback values when missing.
    <advantage>Requires zero modifications to the current transpilation script.</advantage>
    <drawback>The fallback &quot;Transpiled from...&quot; description destroys Antigravity&apos;s semantic intent matching, leaving those skills undiscoverable by the agent.</drawback>
  </alternative>
  <alternative id="Enforce source frontmatter">
    Conclude that Antigravity requires `name` and `description` for discovery, and the script should be updated to fail on missing frontmatter rather than injecting dummy fallbacks.
    <advantage>Guarantees all transpiled skills have accurate descriptions, ensuring they are discoverable and usable by the Antigravity agent.</advantage>
    <drawback>Requires a manual pass to author frontmatter for any legacy source skills before the transpilation will succeed.</drawback>
  </alternative>
  <recommendation option="Enforce source frontmatter">Because Antigravity relies entirely on the description field to trigger skills, a dummy fallback description defeats the purpose of the integration, so strict source enforcement is necessary.</recommendation>
</open-question>


