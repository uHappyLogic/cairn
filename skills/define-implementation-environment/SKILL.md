---
name: define-implementation-environment
description: Analyze the workspace and write IMPLEMENTATION_ENVIRONMENT.md with project root, tech stack, MCP tools, build/test commands, file organization, and key conventions. Run once per project before the first milestone.
---

# define-implementation-environment

Analyzes the current workspace and writes `IMPLEMENTATION_ENVIRONMENT.md` — the authoritative descriptor of the project's tech stack, tooling, and file layout. Skills that explore or implement code read this file instead of making environment assumptions.

## Usage

```
/define-implementation-environment [<intro>]
```

`<intro>` is optional free-form context for things that cannot be auto-discovered — most importantly, which MCP servers are connected and any non-obvious conventions. If omitted, the skill proceeds with file-based discovery only and leaves MCP Tools as a placeholder.

**Examples:**
```
/define-implementation-environment
/define-implementation-environment We use MCP for Unity (mcp__UnityMCP__*) for all Editor automation. Scripts live under Assets/Scripts.
/define-implementation-environment Playwright MCP (mcp__playwright__*) is connected for browser automation.
```

## Workflow

### 1. Guard — check for existing file

Check whether `IMPLEMENTATION_ENVIRONMENT.md` exists in the workspace root.

If it does exist, stop and tell the user:
```
IMPLEMENTATION_ENVIRONMENT.md already exists. To overwrite it, delete it first or run /update-implementation-environment to update specific sections.
```

### 2. Note the intro

If `<intro>` was provided, hold it in context for use in the MCP Tools and Key Conventions sections. Otherwise note that MCP Tools will be written as a placeholder.

### 3. Discover Project Root

The project root is the directory where `CLAUDE.md` lives. Write its absolute path.

### 4. Discover Tech Stack

Probe for indicator files in this order. Read whichever are found and extract language, runtime version where available, framework, and key dependencies:

- `package.json` → Node.js project. Read `name`, `engines`, `dependencies`, `devDependencies` to identify:
  - Framework (Next.js, React, Express, NestJS, Fastify, Vue, Svelte, etc.)
  - Test runner (Jest, Vitest, Mocha, etc.)
  - Language (TypeScript if `typescript` in dependencies; otherwise JavaScript)
- `pyproject.toml` or `setup.py` or `requirements.txt` → Python project. Read for framework (FastAPI, Django, Flask, etc.) and Python version
- `Cargo.toml` → Rust. Read `[package]` for name and edition
- `go.mod` → Go. Read module name and Go version
- `*.csproj` or `*.sln` → C#/.NET. Read to identify target framework version
- `pom.xml` or `build.gradle` or `build.gradle.kts` → Java/Kotlin. Read for artifact ID and dependencies
- `Assets/` directory alongside `ProjectSettings/ProjectVersion.txt` → Unity. Read `ProjectVersion.txt` for Unity version
- `pubspec.yaml` → Dart/Flutter

If multiple indicator files exist, list all relevant stacks. If none are found, write: `Not detected — fill in manually`.

### 5. Discover Build & Test Commands

Derive from the tech stack found above:

- **Node.js (`package.json`)**: read the `scripts` key. Extract the following entries verbatim (only include entries that exist): `build`, `test`, `lint`, `typecheck` (or `type-check`), `dev`, `start`. Format as `- Build: npm run build` etc.
- **Python**: check for `pytest` (write `pytest`), `ruff` or `flake8` (write lint command), `mypy` (write `mypy .`)
- **Rust**: `cargo build`, `cargo test`, `cargo clippy`
- **Go**: `go build ./...`, `go test ./...`, `go vet ./...`
- **C#/.NET**: `dotnet build`, `dotnet test`
- **Java/Maven**: `mvn compile`, `mvn test`
- **Java/Gradle**: `./gradlew build`, `./gradlew test`
- **Unity**: Note that builds are triggered via the Editor; write `- Verify: check Unity Console for errors after each script change`
- **Makefile present**: read it and list targets named `build`, `test`, `lint`, `run` verbatim

If nothing is discoverable, write: `- Build: [not detected — fill in manually]`

### 6. Discover File Organization

Run `find . -maxdepth 2 -type d` excluding hidden directories and build artifacts (`.git`, `node_modules`, `.next`, `__pycache__`, `target`, `build`, `dist`, `.nuxt`, `.output`, `vendor`).

For each top-level and second-level directory found, annotate its role based on name and tech stack. Common patterns:
- `src/` or `lib/` → main source code
- `src/app/` or `app/` → app router pages / top-level app structure
- `src/components/` or `components/` → UI components
- `src/lib/` or `src/utils/` → utilities and shared logic
- `tests/` or `__tests__/` or `spec/` → test files
- `docs/` → documentation
- `public/` or `static/` → static assets
- `Assets/` (Unity) → Unity assets (Scripts, Prefabs, Scenes, etc.)
- `migrations/` → database migrations
- `prisma/` → Prisma schema and migrations

Omit directories with no meaningful content to describe (e.g. empty scaffold dirs).

### 7. Derive Key Conventions

Generate post-edit verification rules from the tech stack and build commands:

- **TypeScript project**: `After editing any .ts or .tsx file, run the typecheck command from ## Build & Test Commands and fix all errors before continuing.`
- **Python with mypy**: `After editing any .py file, run mypy and fix all type errors before continuing.`
- **Python with ruff/flake8**: `After editing any .py file, run the lint command and fix all issues.`
- **Rust**: `After editing any .rs file, run cargo clippy and fix all warnings before continuing.`
- **Go**: `After editing any .go file, run go vet ./... and fix all issues before continuing.`
- **C#/.NET**: `After editing any .cs file, run dotnet build and fix all errors before continuing.`
- **Unity**: `After editing any .cs file: poll mcpforunity://editor/state until isCompiling == false, then call read_console with types=["error"] and fix all errors before attaching components or creating prefabs.`

If `<intro>` mentioned specific conventions, append them verbatim.

If no stack is detected, write: `[Not detected — fill in manually]`

### 8. Handle MCP Tools

If `<intro>` mentions MCP tools, servers, or prefixes, extract them as a bullet list:
```
- `mcp__<prefix>__*` — <purpose>
```

If `<intro>` does not mention MCP tools (or no intro was provided), write:
```
None — run /update-implementation-environment to add MCP tools if any are available.
```

### 9. Write the file

Write `IMPLEMENTATION_ENVIRONMENT.md` to the workspace root using this exact structure:

```markdown
# Implementation Environment

## Project Root

<absolute path>

## Tech Stack

<discovered content>

## MCP Tools

<discovered content>

## Build & Test Commands

<discovered content>

## File Organization

<discovered content>

## Key Conventions

<discovered content>
```

### 10. Confirm

Report:
- Which sections were auto-discovered vs. left as placeholders
- Any sections that need manual review
- Suggested next steps: run `/update-implementation-environment` for any placeholder sections, then `/define-milestone-goal` to start the first milestone

## Rules

- Never overwrite `IMPLEMENTATION_ENVIRONMENT.md` if it already exists — stop and report instead.
- Never invent conventions not derivable from discovered files.
- Prefer exact values from source files (e.g. the literal script name from `package.json`) over paraphrases.
- If a section has nothing to auto-discover, write a clearly-marked placeholder rather than omitting it.
- Do not commit — leave staging to the user.
