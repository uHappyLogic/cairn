# TASKS DONE

## Add Replace Subcommand To Fold Tool

Give `core/tools/requirements.py` a second subcommand, `replace <MILESTONE_DIR> --section "<Heading>"` with the new text on standard input, that has its own argparse parser, help text, and refusal set, reuses the file's internal readers, `## Decisions` locator, and atomic writer, and replaces everything between the matched `###` heading line (found by the same whitespace- and case-folded exact equality `fold` uses, the subsection running to the next `###` line or the end of `## Decisions`) and the subsection's end with the stdin text written verbatim with its outer blank lines trimmed, the heading line and every byte outside the subsection staying as they are. When no subsection matches it prints one `Error:` line on stderr naming the heading, exits 1, and leaves `requirements.md` byte-for-byte unchanged, never creating a subsection; `fold` stays exactly as it is, append-only, with its contract and call shape untouched, and the module docstring documents the new subcommand. Verified by both pytest runs passing and by `uv run scripts/build_hosts.py` rebuilding the host trees so `uv run scripts/build_hosts.py --check` passes with the tool byte-identical in each.

**Verified:**

- `core/tools/requirements.py` has a second subcommand, `replace MILESTONE_DIR --section HEADING`, with its own argparse subparser (required `--section`, its own help text naming the existing `###` subsection) and its own refusal set, and `requirements.py --help` lists both `fold` and `replace`.
- `replace` reuses the file's internal readers (`read_text`, `split_lines`, `read_body`), the `## Decisions` locator (`find_decisions`, `section_end`, `find_subsection`), and the atomic writer `write_bytes`.
- `replace` matches `--section` against the `###` headings under `## Decisions` by the same whitespace- and case-folded exact equality as `fold`, the first of two matches winning and a same-named subsection outside `## Decisions` never matched; the subsection runs to the next `###` line or the end of `## Decisions`.
- On the golden fixture, `replace` on the prose subsection and on the topical-bullets subsection rewrites only the subsection body with the stdin text verbatim, outer blank lines trimmed, keeping the heading line, the blank lines around the body, and every byte outside the subsection unchanged; CRLF files, a file with no final line ending, and an empty subsection were checked by hand.
- A heading no subsection of `## Decisions` carries prints one `Error:` line on stderr naming the heading, exits 1, and leaves `requirements.md` byte-for-byte unchanged with no subsection created; an empty heading or body is refused the same way, and a missing `--section` gets argparse's exit 2.
- `fold` is unchanged in contract and call shape: its six test files pass untouched, and its output from the old and new versions is byte-identical across fixture, CRLF, missing-final-line-ending, and empty-subsection inputs.
- The module docstring documents the `replace` subcommand, its rewrite rule, and its extra refusal.
- `uv run pytest` (790 passed) and `uv run --no-project --python 3.9 --with pytest pytest` (786 passed, 1 skipped) both pass.
- `uv run scripts/build_hosts.py` rebuilt the host trees, `uv run scripts/build_hosts.py --check` passes, and `hosts/claude/tools/requirements.py`, `hosts/antigravity/tools/requirements.py`, and `hosts/codex/plugins/cairn/tools/requirements.py` are byte-identical to `core/tools/requirements.py`.

---

## Add Replace Mode Test Files

Add new flat `tests/test_requirements_replace_<concern>.py` files over the golden fixture `tests/fixtures/requirements.md` pinning the `replace` contract: the whole-subsection rewrite for both recorded decision shapes with the heading line and every other byte unchanged, the folded heading match with the first of two matches winning and a same-named subsection outside `## Decisions` never matched, the verbatim body with its outer blank lines trimmed, the missing-subsection refusal naming the heading with no subsection created, the shared refusals (an empty heading or body, a missing or non-UTF-8 file, zero or more than one `## Decisions` heading), argparse's exit 2 on a missing `--section`, and `--help` listing both subcommands, leaving the six existing fold test files untouched. Also pin, in a new file, that a `fold`-created subsection lands immediately above a `## Noted contradictions` heading standing between `## Decisions` and `## Out of Scope`. Verified by `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest` both passing with the new tests collected.

**Verified:**

- Five new flat files `tests/test_requirements_replace_{rewrite,matching,body,refusals,contract}.py` pin the `replace` contract over the golden fixture `tests/fixtures/requirements.md`, which is unchanged.
- `test_requirements_replace_rewrite.py` pins the whole-subsection rewrite for both recorded decision shapes (the prose subsection and the topical-bullets subsection with its unchanged bullets carried in the body), plus the last subsection, with the heading line, the blank lines around the body, and every other byte unchanged, including the blank-line, file-end, empty-subsection, and CRLF seams.
- `test_requirements_replace_matching.py` pins the whitespace- and case-folded heading match (non-ASCII included), the first of two matches winning, the subsection's extent to the next `###` or the end of `## Decisions`, and a same-named subsection outside `## Decisions` never matched, a heading only it carries being refused with the file unchanged.
- `test_requirements_replace_body.py` pins the body written verbatim with only its outer blank lines trimmed: inner blank lines, indentation, bold-lead bullets, heading lines, markup, and non-ASCII text kept, no bullet or wrapping added, CRLF body lines taking the file's ending.
- `test_requirements_replace_refusals.py` pins the missing-subsection refusal as one `Error:` line naming the folded heading, the file byte-for-byte unchanged and no subsection created, and the shared refusals: an empty heading, an empty body, a missing file (nothing created), a non-UTF-8 file, and zero or more than one column-0 `## Decisions` heading.
- `test_requirements_replace_contract.py` pins argparse's exit 2 on a missing `--section` with the file unchanged, `--help` listing both `fold` and `replace`, `replace --help` naming `--section HEADING`, the silent success, one-line errors, and the terminal-stdin refusal.
- The new file `tests/test_requirements_noted_contradictions.py` pins that a `fold`-created subsection lands immediately above a `## Noted contradictions` heading standing between `## Decisions` and `## Out of Scope`, on the golden fixture and on the fresh template, with the noted section's bytes unchanged.
- The six existing fold test files (`test_requirements_{body,contract,landing,parity,refusals,splice}.py`) show no diff.
- `uv run pytest` passes with 889 tests (790 before, the 99 new tests collected) and `uv run --no-project --python 3.9 --with pytest pytest` passes with 885 and 1 skipped (786 before, the 99 new tests collected).

---
