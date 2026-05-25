---
name: update-implementation-environment
description: Update one or more sections of IMPLEMENTATION_ENVIRONMENT.md based on a free-form description. Use when a new MCP server is added, the build system changes, conventions evolve, or the file organization is restructured.
---

# update-implementation-environment

Reads the current `IMPLEMENTATION_ENVIRONMENT.md` and updates the relevant section(s) based on the provided description. Edits the minimum necessary — sections not mentioned are left exactly as-is.

## Usage

```
/update-implementation-environment <description>
```

`<description>` is free-form text describing what changed or needs to be updated.

**Examples:**
```
/update-implementation-environment Added a Playwright MCP server: mcp__playwright__* for browser automation
/update-implementation-environment Switched from Jest to Vitest. Test command is now: npx vitest run
/update-implementation-environment After editing any TypeScript file also run npm run lint -- --fix
/update-implementation-environment Moved all shared utilities to src/shared/. Removed src/utils/.
/update-implementation-environment Added Prisma ORM. Database schema is at prisma/schema.prisma.
```

## Workflow

### 1. Guard

Read `IMPLEMENTATION_ENVIRONMENT.md` at the workspace root. If it does not exist, stop and tell the user:
```
IMPLEMENTATION_ENVIRONMENT.md not found. Run /define-implementation-environment first to create it.
```

### 2. Parse the description

Read the full current file. Then analyze `<description>` to determine which section(s) need to change:

| Description mentions | Update section |
|---|---|
| MCP tool, MCP server, `mcp__*` prefix | `## MCP Tools` |
| build, test, lint, typecheck, run command | `## Build & Test Commands` |
| language, framework, library, package, dependency | `## Tech Stack` |
| directory, folder, path, moved, renamed (code structure) | `## File Organization` |
| convention, rule, after editing, always run, pattern | `## Key Conventions` |
| project root, workspace path | `## Project Root` |

If the description spans multiple sections, update all affected ones.

### 3. Apply targeted edits

For each affected section:
- Additions: append the new item to the section's bullet list (or replace the placeholder if the section currently reads "None" or "[not detected]")
- Updates: find the existing item and replace it
- Removals: remove the item if the description says something was removed or replaced

Do not reformat, reorder, or rewrite items in sections that are not being updated.

### 4. Confirm

Report which sections were changed and summarize what was added, updated, or removed.

## Rules

- Edit only the sections that the description explicitly affects — do not touch other sections.
- Do not reformat untouched sections.
- If the description is ambiguous about which section to update, make the most reasonable choice and state it in the confirmation.
- Do not commit — leave staging to the user.
