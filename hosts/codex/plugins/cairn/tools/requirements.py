"""The fold and replace commands for a milestone's requirements.md: fold splices one decision
under ## Decisions, and replace rewrites the body of one existing subsection of it.

Usage: python3 <plugin root>/tools/requirements.py fold MILESTONE_DIR --section HEADING
       (the decision on standard input)
       python3 <plugin root>/tools/requirements.py replace MILESTONE_DIR --section HEADING
       (the subsection's new body on standard input)

define_milestone.py creates requirements.md with its milestone directory, and the file keeps
being written by hand and by other writers afterwards: this module is not its only writer and
writes one place of it only, so a call changes no byte it did not write. Each subcommand takes
the already-resolved milestone directory as its first argument and acts on the requirements.md
inside it, which must already exist: the call never creates it. The caller resolves the
milestone; this module never reads milestones/README.md, and it touches no git.

Subcommands:
  fold MILESTONE_DIR --section HEADING
      read one decision from standard input and splice it into the "## Decisions" section of
      requirements.md: at the end of the "### " subsection whose heading is HEADING, or, when
      no subsection carries that heading, under a new "### HEADING" line (HEADING folded to
      one line) added at the end of the section, just before the next "## " heading. The
      --section flag is required on every call, so there is no form of the call that lands a
      decision under no subsection
  replace MILESTONE_DIR --section HEADING
      read a subsection's new body from standard input and write it in place of the body of
      the "### " subsection of "## Decisions" whose heading is HEADING, keeping that heading
      line and every byte outside the subsection's body. It never creates a subsection: when
      none carries HEADING the call is refused. The --section flag is required on every call

The body either subcommand reads is opaque Markdown: it is written verbatim with only its
leading and trailing blank lines trimmed, adding no bullet, bold lead, or wrapping of its own;
a heading line in it is written as given, nothing of its prose is checked, and a decision the
section already holds is folded again.

The free-text body travels on standard input, never as an argument: the tool reads
sys.stdin.buffer to end of file exactly once per call and decodes it as UTF-8 itself, and it
refuses a terminal stdin so a call that forgot to pipe its body (a quoted heredoc, a
redirected file) fails instead of blocking.

Requirements file model, read whole on every call only to find the landing point:
  - the section is the one column-0 line reading "## Decisions" (compared whitespace-folded
    and case-folded) and runs to the next column-0 "## " line or the end of the file; every
    column-0 "## " line ends it, with no code-fence exemption
  - inside it every column-0 "### " line is a subsection heading, and a subsection runs to
    the next one or the end of the section
  - HEADING is matched against the subsection headings by exact equality after
    whitespace-folding and case-folding; when two subsections carry it, the first is used
  - a line holding only whitespace is blank

The fold's splice: the block (when a subsection is created, its "### HEADING" line and a blank
line, then the decision) is inserted directly after the last non-blank line of the matched
subsection, or of the section when a subsection is created. One blank line is added before
the block, the line it follows never being blank, and one after it only where the line that
follows is not already blank; at the end of the file nothing follows, so nothing is added
after the block, and a file whose last line had no line ending keeps ending without one.

The replace's rewrite: the matched subsection's body runs from its first non-blank line after
the heading line to its last non-blank line, and those lines, every blank line between them
included, are replaced by the new body; the heading line and the blank lines standing between
it and the body, and between the body and the subsection's end, are kept as they are. When the
subsection holds no non-blank line after its heading, the new body is placed after the heading
line exactly as the fold's splice places a block after its anchor. A body whose last line had
no line ending at the end of the file keeps ending without one.

Inserted lines end as the file's lines do (CRLF when its first line ending is CRLF, LF
otherwise), and every other byte of the file is written back unchanged: nothing the call did
not write is normalized, so the file's diff is exactly the folded decision or the rewritten
body.

Refusals, each leaving requirements.md byte-for-byte unchanged: an empty HEADING, an empty
body, a requirements.md that is missing or not UTF-8 text, and a file holding no column-0
"## Decisions" heading or more than one; replace also refuses a HEADING no subsection of
"## Decisions" carries, naming the heading. Nothing else is checked.

Output and error contract:
  - a mutator prints nothing on success
  - every failure is exactly one line "Error: <reason>" on stderr with exit status 1, and a
    non-zero exit leaves requirements.md byte-for-byte unchanged; a malformed invocation gets
    argparse's own usage message and exit status 2; no traceback ever reaches the caller
  - the file is replaced through a temporary file in its own directory renamed over it,
    keeping its mode

Standard library only; runs on Python 3.9 and later.
"""

import argparse
import os
import stat
import sys
import tempfile

REQUIREMENTS_NAME = "requirements.md"
SECTION_PREFIX = "## "
SECTION_TITLE = "Decisions"
SUBSECTION_PREFIX = "### "


class ToolError(Exception):
    """A failure the caller is told about as one `Error: <reason>` line with exit status 1."""


# --- text -----------------------------------------------------------------------------


def fold(text):
    """The text as one line: whitespace runs and newlines collapsed to a space, ends trimmed."""
    return " ".join((text or "").split())


def title_key(value):
    """The comparison form of a heading: whitespace-folded and case-folded."""
    return fold(value).casefold()


def split_lines(text):
    """The text's lines, each keeping its LF or CRLF ending; only the last may lack one."""
    lines = []
    start = 0
    while start < len(text):
        end = text.find("\n", start)
        if end < 0:
            lines.append(text[start:])
            break
        lines.append(text[start:end + 1])
        start = end + 1
    return lines


def is_blank(line):
    return not line.strip()


def heading_text(line, prefix):
    """The text of a column-0 heading line opened by prefix, or None for any other line."""
    if not line.startswith(prefix):
        return None
    return line[len(prefix):]


def line_ending(lines):
    """The line ending inserted lines take: CRLF when the file's first line ending is CRLF,
    LF otherwise."""
    for line in lines:
        if line.endswith("\n"):
            return "\r\n" if line.endswith("\r\n") else "\n"
    return "\n"


def decision_lines(text):
    """The body's lines (a decision, or a subsection's new body), with its leading and
    trailing blank lines dropped."""
    lines = text.replace("\r\n", "\n").split("\n")
    start, end = 0, len(lines)
    while start < end and is_blank(lines[start]):
        start += 1
    while end > start and is_blank(lines[end - 1]):
        end -= 1
    return lines[start:end]


# --- the file -------------------------------------------------------------------------


def requirements_path(milestone_dir):
    return os.path.join(milestone_dir, REQUIREMENTS_NAME)


def read_text(path):
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except FileNotFoundError:
        raise ToolError(f"{path} does not exist")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        raise ToolError(f"{path} is not UTF-8 text")


def write_bytes(path, data):
    """Write data to path through a temporary file in the same directory renamed over the
    target, so a failure part-way leaves the existing file byte-for-byte unchanged; the file
    keeps the target's mode, or takes the default mode when it is new."""
    directory = os.path.dirname(path) or os.curdir
    name = os.path.basename(path)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{name}.", suffix=".tmp", dir=directory)
    try:
        try:
            mode = stat.S_IMODE(os.stat(path).st_mode)
        except FileNotFoundError:
            umask = os.umask(0)
            os.umask(umask)
            mode = 0o666 & ~umask
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def read_body(what):
    """The one free-text body a call carries on standard input, read to end of file once
    and decoded as UTF-8; a terminal, closed, or non-UTF-8 stdin is a ToolError, so a call
    that forgot to pipe its body fails instead of blocking."""
    stream = sys.stdin
    if stream is None or getattr(stream, "closed", False):
        raise ToolError(f"{what} must be supplied on standard input, which is closed")
    if stream.isatty():
        raise ToolError(f"{what} must be piped on standard input (as a quoted heredoc or a redirected file), not typed at a terminal")
    data = stream.buffer.read()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        raise ToolError(f"{what} on standard input is not UTF-8 text")


# --- locating -------------------------------------------------------------------------


def find_decisions(lines, path):
    """The index of the one column-0 "## Decisions" line; none or more than one is a
    ToolError."""
    wanted = title_key(SECTION_TITLE)
    matches = [
        index
        for index, line in enumerate(lines)
        if heading_text(line, SECTION_PREFIX) is not None
        and title_key(heading_text(line, SECTION_PREFIX)) == wanted
    ]
    if not matches:
        raise ToolError(f"{path} holds no column-0 \"{SECTION_PREFIX}{SECTION_TITLE}\" heading")
    if len(matches) > 1:
        numbers = ", ".join(str(index + 1) for index in matches)
        raise ToolError(
            f"{path} holds {len(matches)} column-0 \"{SECTION_PREFIX}{SECTION_TITLE}\" headings "
            f"(lines {numbers}); the decision has no single section to land in"
        )
    return matches[0]


def section_end(lines, start):
    """The index of the first column-0 "## " line after start, or the end of the file."""
    index = start + 1
    while index < len(lines) and heading_text(lines[index], SECTION_PREFIX) is None:
        index += 1
    return index


def find_subsection(lines, start, end, heading):
    """The (heading index, end index) of the first subsection in lines[start:end] whose
    heading equals heading after folding, or None when none carries it."""
    wanted = title_key(heading)
    headings = [index for index in range(start, end) if heading_text(lines[index], SUBSECTION_PREFIX) is not None]
    for position, index in enumerate(headings):
        if title_key(heading_text(lines[index], SUBSECTION_PREFIX)) == wanted:
            following = headings[position + 1] if position + 1 < len(headings) else end
            return index, following
    return None


def last_content_line(lines, start, end):
    """The index of the last non-blank line in lines[start:end]; lines[start] is a heading,
    so there always is one."""
    index = end - 1
    while index > start and is_blank(lines[index]):
        index -= 1
    return index


# --- the splice -----------------------------------------------------------------------


def splice(lines, decisions, heading, decision):
    """The file's new text, its lines given and its "## Decisions" line at index decisions:
    the decision folded under the named subsection, every byte outside the inserted block
    unchanged."""
    end = section_end(lines, decisions)
    subsection = find_subsection(lines, decisions + 1, end, heading)
    if subsection is None:
        anchor = last_content_line(lines, decisions, end)
        block = [SUBSECTION_PREFIX + heading, ""] + decision
    else:
        anchor = last_content_line(lines, *subsection)
        block = decision
    return insert_after(lines, anchor, block)


def insert_after(lines, anchor, block):
    """The file's new text with block inserted directly after the non-blank line at index
    anchor: one blank line before it, one after it only where the following line is not
    already blank, nothing after it at the end of the file."""
    newline = line_ending(lines)
    block_text = newline.join(block)
    after = anchor + 1
    if lines[anchor].endswith("\n"):
        inserted = newline + block_text + newline
        if after < len(lines) and not is_blank(lines[after]):
            inserted += newline
    else:
        inserted = newline + newline + block_text
    return "".join(lines[:after]) + inserted + "".join(lines[after:])


# --- the rewrite ----------------------------------------------------------------------


def rewrite(lines, decisions, heading, body, path):
    """The file's new text, its lines given and its "## Decisions" line at index decisions:
    the body of the named subsection replaced by body, its heading line, the blank lines
    around its body, and every byte outside it unchanged. A heading no subsection of the
    section carries is a ToolError: the rewrite never creates a subsection."""
    end = section_end(lines, decisions)
    subsection = find_subsection(lines, decisions + 1, end, heading)
    if subsection is None:
        raise ToolError(
            f"{path} holds no \"{SUBSECTION_PREFIX}{heading}\" subsection under "
            f"\"{SECTION_PREFIX}{SECTION_TITLE}\"; replace rewrites an existing subsection only "
            f"and never creates one"
        )
    start, stop = subsection
    last = last_content_line(lines, start, stop)
    if last == start:
        return insert_after(lines, start, body)
    first = start + 1
    while is_blank(lines[first]):
        first += 1
    newline = line_ending(lines)
    replacement = newline.join(body)
    if lines[last].endswith("\n"):
        replacement += newline
    return "".join(lines[:first]) + replacement + "".join(lines[last + 1:])


# --- subcommands ----------------------------------------------------------------------


def cmd_fold(args):
    heading = fold(args.section)
    if not heading:
        raise ToolError("the subsection heading given as --section is empty")
    path = requirements_path(args.milestone_dir)
    lines = split_lines(read_text(path))
    decisions = find_decisions(lines, path)
    decision = decision_lines(read_body("the decision"))
    if not decision:
        raise ToolError("the decision on standard input is empty")
    write_bytes(path, splice(lines, decisions, heading, decision).encode("utf-8"))
    return 0


def cmd_replace(args):
    heading = fold(args.section)
    if not heading:
        raise ToolError("the subsection heading given as --section is empty")
    path = requirements_path(args.milestone_dir)
    lines = split_lines(read_text(path))
    decisions = find_decisions(lines, path)
    body = decision_lines(read_body("the new subsection body"))
    if not body:
        raise ToolError("the new subsection body on standard input is empty")
    write_bytes(path, rewrite(lines, decisions, heading, body, path).encode("utf-8"))
    return 0


# --- command line ---------------------------------------------------------------------


def build_parser():
    parser = argparse.ArgumentParser(
        prog="requirements.py",
        description=(
            "Fold a decision into the ## Decisions section of a milestone's existing "
            "requirements.md, or replace the body of one of its existing subsections."
        ),
    )
    subcommands = parser.add_subparsers(dest="subcommand", metavar="<subcommand>", required=True)

    fold_help = (
        "splice the decision read from standard input, verbatim, at the end of the ## Decisions "
        "subsection with the given heading, creating that subsection at the end of the section "
        "when none carries it; every other byte of requirements.md is left unchanged"
    )
    fold_parser = subcommands.add_parser("fold", help=fold_help, description=fold_help)
    fold_parser.add_argument(
        "milestone_dir",
        metavar="MILESTONE_DIR",
        help="the resolved milestone directory holding requirements.md",
    )
    fold_parser.add_argument(
        "--section",
        required=True,
        metavar="HEADING",
        help="the heading of the ### subsection the decision lands in, compared whitespace-folded and case-folded",
    )
    fold_parser.set_defaults(func=cmd_fold)

    replace_help = (
        "replace the body of the ## Decisions subsection with the given heading by the text read "
        "from standard input, verbatim, keeping the heading line and every byte outside the "
        "subsection's body; a heading no subsection carries is refused, never created"
    )
    replace_parser = subcommands.add_parser("replace", help=replace_help, description=replace_help)
    replace_parser.add_argument(
        "milestone_dir",
        metavar="MILESTONE_DIR",
        help="the resolved milestone directory holding requirements.md",
    )
    replace_parser.add_argument(
        "--section",
        required=True,
        metavar="HEADING",
        help="the heading of the existing ### subsection whose body is replaced, compared whitespace-folded and case-folded",
    )
    replace_parser.set_defaults(func=cmd_replace)
    return parser


def describe(error):
    """The reason a failure reports, as the one Error line gives it."""
    if isinstance(error, ToolError):
        return str(error)
    if isinstance(error, OSError):
        if error.strerror and error.filename is not None:
            return f"{error.strerror}: {error.filename}"
        return str(error)
    return f"{type(error).__name__}: {error}"


def _fail(reason):
    print("Error: " + fold(reason), file=sys.stderr)
    return 1


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except Exception as error:  # the contract: no traceback ever reaches the caller
        return _fail(describe(error))


if __name__ == "__main__":
    sys.exit(main())
