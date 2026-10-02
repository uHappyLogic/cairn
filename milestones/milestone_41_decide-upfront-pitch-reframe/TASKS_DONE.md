# TASKS DONE

## Replace Root README Tagline And One-Liner

In the root `README.md` title block, replace the bold tagline with "Mark the path first, then hand off the walk." and the line below it with the one-liner "Cairn brings all the important questions up to be decided upfront, so you can hand long-running execution to your agent confidently.", so the first screen states the decide-upfront identity as plain fact with no category noun and no tail. Verified when both new lines sit under `# Cairn` in the same two places, each exactly once, and neither "Mark the path from idea to shipped." nor the old milestone-driven one-liner remains in the file.

**Verified:**

- The bold tagline under `# Cairn` in the root `README.md` (line 28, the old tagline's place) reads exactly `**Mark the path first, then hand off the walk.**`.
- The line directly below it (line 29, the old one-liner's place) reads exactly "Cairn brings all the important questions up to be decided upfront, so you can hand long-running execution to your agent confidently.", with no category noun and no tail.
- `grep -c` finds each of the two new lines exactly once in `README.md`.
- `grep -c` finds neither "Mark the path from idea to shipped" nor "Milestone-driven development for your coding agent" in `README.md` (zero matches each).
- `git diff -- README.md` shows those two lines as the file's only change (2 insertions, 2 deletions).

---

