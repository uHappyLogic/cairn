# TASKS TODO

## Center Adoption Table On First Screen

The three-repository adoption pipe table under the centered badge paragraph on the root `README.md` first screen renders left-aligned; wrap it so GitHub renders it horizontally centered at any viewport width, matching the badge row above it — keep it a Markdown pipe table if GitHub honors a centering HTML wrapper around it, and only if it does not convert it to an HTML `<table align="center">`, updating the `CLAUDE.md` repository-layout wording that calls it a "pipe table" in the same commit. The first screen is this milestone's landing-page deliverable, and the table is its one element left out of the centered header. Verify by rendering the README the way GitHub does (a pushed view or GitHub's markdown rendering) and confirming the table sits centered with its links and badge images intact, with `uv run scripts/build_hosts.py --check` still passing since the root README is not a build input.

---
