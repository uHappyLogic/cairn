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


## Out of Scope

## Open questions

<open-question id="Agent format compatibility" status="open">
  <question>Do the copied agent `.md` files require any Google Antigravity-specific formatting (e.g. YAML frontmatter, different extension, or structural changes) to function correctly as subagents in the transpiled plugin?</question>
  <alternative id="No changes required">
    Keep the migration script's direct copy of the flat `.md` files without adding Antigravity-specific directory structures or frontmatter flags.
    <advantage>The flat files already parse perfectly for internal orchestrator dispatch, and their non-canonical structure naturally keeps these internal subagents hidden from the user-facing public registry.</advantage>
    <drawback>Relies on undocumented platform behavior (parsing flat `.md` files) rather than explicitly adhering to the canonical `agent.md` format.</drawback>
  </alternative>
  <alternative id="Restructure to canonical agent.md">
    Modify the migration script to convert flat `agents/&lt;name&gt;.md` files into the documented `agents/&lt;name&gt;/agent.md` structure.
    <advantage>Aligns strictly with Antigravity's documented agent format, ensuring future-proof compatibility with the platform's parser.</advantage>
    <drawback>May inadvertently expose internal subagents to the platform's public plugin registry, encouraging direct invocation that violates their design.</drawback>
  </alternative>
  <alternative id="Inject explicit visibility flags">
    Modify the migration script to parse the YAML frontmatter and inject `subagent: true` or `visibility: private` flags.
    <advantage>Uses explicit metadata to control platform routing and visibility rather than relying on directory structure quirks.</advantage>
    <drawback>Adds YAML-parsing complexity to the migration script for agents when the flat files already achieve the desired behavior out-of-the-box.</drawback>
  </alternative>
  <recommendation option="No changes required">The existing flat files parse correctly for internal dispatch while naturally staying hidden from the public registry, preserving their encapsulated design with zero migration effort.</recommendation>
</open-question>

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


