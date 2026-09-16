# TASKS TODO

## Release Skill Revises Notes At Pause

Extend step 7 of `.claude/skills/release-plugin/SKILL.md` with a third answer beside publish and stop: while the `Release: <VERSION>` commit is still unpushed (after a fetch, `git merge-base --is-ancestor HEAD origin/main` fails), a revision applies the maintainer's stated change to the `<VERSION>` entry in the working `CHANGELOG.md` (a hand edit already made there counts the same), stages it with `git add -- CHANGELOG.md`, amends with `git commit --amend --no-edit` so the subject is untouched, re-extracts the entry from `HEAD:CHANGELOG.md`, shows it in full, and asks again; once `origin/main` carries the commit a revision request is a stop naming that reason, and step 6d's one-commit sentence names this as the run's only amend. Verify by reading step 7 and 6d together: the amend is path-scoped, subject-preserving, and gated on the unpushed check.

---

## Replace README Development With Contributing Section

Remove the README's `## Development` section (its body now lives in `CONTRIBUTING.md`) and put a `## Contributing` section in its place, between the skill reference and `## Self-dogfooding`, in the one-line shape of `## License`: one sentence naming the `core/`-once-rebuild model with a link to `CONTRIBUTING.md` for the full contributor path, then one line each routing bug reports and proposals to the issue forms, questions to the Discussions tab, vulnerability reports to `SECURITY.md`, and release notes to `CHANGELOG.md` — five or six lines, with `CODE_OF_CONDUCT.md` left to GitHub's About sidebar and the badge row untouched. Verify no `## Development` heading remains, every linked file exists in the tree, and nothing in the repository links to the README's `#development` anchor.

---
