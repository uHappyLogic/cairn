# Milestone 25: Traffic Adoption Badges

## Goal

Publish adoption evidence in README.md as a table of albertoarena/github-traffic-badge badges — one row per repository (uHappyLogic/cairn, cairn-claude, cairn-antigravity), two columns (unique views, unique clones), and a caption stating the counts are cumulative from the workflows' first run and that the monorepo's clones include CI checkouts. Each repository runs a daily scheduled workflow (the action pinned to a full commit SHA, one step per metric writing a distinct SVG to the traffic-data branch): the monorepo's under .github/workflows/, each distribution repository's rendered from a scripts/hosts/<host>/ template into its hosts/<host>/ tree so releases publish it. The milestone stores the fine-grained PAT at temp/PAT as the TRAFFIC_TOKEN secret on all three repositories with gh secret set, seeds every traffic-data branch once via workflow_dispatch before the README references its badges, and verifies that the action's daily push keeps the distribution repositories' cron workflows from GitHub's 60-day inactivity disable.

## Relevant starting state

## Decisions

## Out of Scope

