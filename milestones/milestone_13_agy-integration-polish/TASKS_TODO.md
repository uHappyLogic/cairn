# TASKS TODO


## Update GitHub Project Description

Update the GitHub repository description programmatically using the GitHub CLI to reflect the project's dual-platform support. This is needed to provide a clear, direct signal of dual-support for users searching for either Claude Code or Google Antigravity.

**Notes:**
- The GitHub CLI (`gh`) is already configured locally, so no authentication setup is required before running the edit command.

**Success:**
- Running `gh repo edit --description "Milestone-driven development workflow for Claude Code and Google Antigravity."` executes successfully.
- Running `gh repo view` confirms the description matches the new text.

---
