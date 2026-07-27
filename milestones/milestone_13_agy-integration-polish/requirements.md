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

<open-question id="Transpilation docs placement" status="open">
  <question>Where should the local transpilation step instructions be documented (e.g., a new section in README.md, added to CLAUDE.md, or elsewhere)?</question>
  <alternative id="Add to CLAUDE.md">
    Document the transpilation step in a new section within CLAUDE.md alongside the existing skill-editing invariants.
    <advantage>Consolidates all contributor-facing architectural constraints and build steps in one place, keeping the public README focused on adoption.</advantage>
    <drawback>Human contributors might overlook CLAUDE.md, assuming it contains only AI-specific prompts rather than manual build steps.</drawback>
  </alternative>
  <alternative id="Add to README.md">
    Add a &quot;Development&quot; or &quot;Contributing&quot; section to the bottom of the project&apos;s README.md to house the instructions.
    <advantage>Places the instructions in the most universally expected location for open-source human contributors.</advantage>
    <drawback>Clutters an otherwise clean, adoption-focused user manual with contributor-specific build commands.</drawback>
  </alternative>
  <alternative id="Create CONTRIBUTING.md">
    Create a new root-level CONTRIBUTING.md file dedicated to local development and transpilation instructions.
    <advantage>Cleanly separates contributor documentation from both the user manual (README.md) and AI guidance (CLAUDE.md).</advantage>
    <drawback>Introduces a new root document just to host the instructions for a single script.</drawback>
  </alternative>
  <recommendation option="Add to CLAUDE.md">CLAUDE.md already serves as the de facto contributor guide by hosting the extensive skill-editing invariants, making it the natural home for the post-edit transpilation step without polluting the public README.</recommendation>
</open-question>

<open-question id="GitHub description update method" status="open">
  <question>How should the GitHub project description update be delivered? (e.g. Should we just draft the new text for manual update, or is there an API/scripted way we should use?)</question>
  <alternative id="Draft text for manual update">
    Draft the new description text and provide it in a task or requirements file for the user to manually copy and paste into the GitHub web UI.
    <advantage>Simplest approach that avoids the overhead of managing GitHub CLI authentication for a single string change.</advantage>
    <drawback>Requires the user to remember to apply the change manually outside of the local task workflow.</drawback>
  </alternative>
  <alternative id="Scripted update via GitHub CLI">
    Author a task to run `gh repo edit --description &quot;...&quot;` to apply the update programmatically using the GitHub CLI.
    <advantage>Automates the update entirely within the project&apos;s task execution flow without manual web UI interaction.</advantage>
    <drawback>Requires the user to have the GitHub CLI installed, authenticated, and configured with adequate permissions for a one-off settings change.</drawback>
  </alternative>
  <recommendation option="Draft text for manual update">Drafting text is better because automating a one-off metadata change via the GitHub CLI introduces unnecessary authentication and dependency overhead that outweighs the effort of a manual copy-paste.</recommendation>
</open-question>
