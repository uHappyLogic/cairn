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
- The transpilation script will enforce source frontmatter (requiring `name` and `description` to be present in legacy source skills) rather than injecting dummy fallbacks, ensuring Antigravity's semantic intent matching works.


## Out of Scope

## Open questions

<open-question id="Missing frontmatter behavior" status="open">
  <question>When the transpilation script encounters a legacy source skill missing its required frontmatter, should it abort with a hard error or skip the file with a warning?</question>
  <alternative id="Abort with a hard error">
    The script immediately fails and halts transpilation if any SKILL.md lacks frontmatter.
    <advantage>It guarantees the resulting plugin is never deployed with silently missing skills, forcing the developer to supply the required semantic intent data.</advantage>
    <drawback>It interrupts the migration process on the first failure, potentially requiring multiple runs to discover all non-compliant skills.</drawback>
  </alternative>
  <alternative id="Skip the file with a warning">
    The script logs a warning for the non-compliant skill and skips transpiling it, continuing with the rest of the directory.
    <advantage>It allows the developer to see all missing-frontmatter warnings across the whole codebase in a single run.</advantage>
    <drawback>It produces an incomplete, seemingly successful plugin build that will fail at runtime if a user tries to invoke the silently skipped skill.</drawback>
  </alternative>
  <recommendation option="Abort with a hard error">A silently missing skill in the transpiled plugin creates confusing runtime failures in Antigravity, so failing fast at build time safely enforces the new frontmatter requirement.</recommendation>
</open-question>

<open-question id="GitHub description wording" status="deferred">
  <question>What exact text should be used for the new GitHub project description to reflect dual-support for both Claude Code and Google Antigravity?</question>
  <alternative id="Direct replacement">
    Replace the single-platform mention with both names: &quot;Milestone-driven development workflow for Claude Code and Google Antigravity.&quot;
    <advantage>Directly and concisely answers the dual-support requirement by naming both platforms upfront for maximum discoverability.</advantage>
    <drawback>Couples the high-level project summary entirely to third-party product names rather than what the tool actually does.</drawback>
  </alternative>
  <alternative id="Appended to tagline">
    Append the platforms to the established tagline: &quot;Mark the path from idea to shipped. Supported on Claude Code and Google Antigravity.&quot;
    <advantage>Preserves the project&apos;s established brand identity while still explicitly fulfilling the requirement to surface both platforms.</advantage>
    <drawback>The longer text pushes the critical platform keywords toward the end where they might be truncated in some UI views.</drawback>
  </alternative>
  <alternative id="Category with specific tools">
    Use a broad category with explicit examples: &quot;Milestone-driven development workflow for AI agents (Claude Code, Google Antigravity).&quot;
    <advantage>Frames the tool generically for any future platforms while retaining the required specific keywords for search visibility.</advantage>
    <drawback>The parenthetical list adds visual clutter to a field meant for a punchy, high-level summary.</drawback>
  </alternative>
  <recommendation option="Direct replacement">It provides the clearest, most direct signal of dual-support for users searching for either specific platform without unnecessary padding.</recommendation>
</open-question>
