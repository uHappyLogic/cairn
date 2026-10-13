"""The only writer of a milestone's existing TASKS_TODO.md and TASKS_DONE.md, the task lists.

Usage: python3 <plugin root>/tools/task_list.py <subcommand> MILESTONE_DIR [...]

define_milestone.py creates both task files together with their milestone directory; from
then on this module is their only writer. Every subcommand takes the already-resolved
milestone directory as its first argument and acts on the task files inside it, which must
already exist: no subcommand creates one. The caller resolves the milestone; this module
never reads milestones/README.md, and it touches no git.

Subcommands:
  initialize MILESTONE_DIR
      replace TASKS_TODO.md with its heading followed by the whole ordered list read from
      standard input, written in the file's own form: each section a "## <Task Title>"
      heading line, its body, and a trailing "---" line. Every section is validated before
      anything is written, so the list lands whole and in the order given or the file is
      left byte-for-byte as it was; whatever the file held before is replaced, with no flag
      and no refusal for it
  insert MILESTONE_DIR TASK_TITLE (--end | --before TASK_TITLE | --after TASK_TITLE)
      put one new section into TASKS_TODO.md whose heading is TASK_TITLE (folded to one
      line) and whose body is read from standard input, at exactly the one position the
      required flag names: after the last section, ahead of the named section, or behind
      the named section. The tool composes the heading, the body, and the "---" itself, so
      a body line reading as a "---" separator or a "## " heading is written verbatim as
      body text by this call
  move MILESTONE_DIR TASK_TITLE
      move the TASKS_TODO.md section whose heading is TASK_TITLE to the end of
      TASKS_DONE.md, reading the acceptance bar it was verified against from standard
      input as opaque Markdown: the entry is the section's heading and body, the
      "**Verified:**" line, the bar verbatim with only its leading and trailing blank lines
      trimmed, and the "---". An empty bar is refused; the bar is neither split into
      criteria nor checked for bullets, and the title is never checked against the entries
      TASKS_DONE.md already holds. Both new contents are rendered before either file is
      touched; TASKS_DONE.md is replaced first and TASKS_TODO.md second, and when the second
      replace fails TASKS_DONE.md's original bytes are written back, so the call fails with
      both files as they were. Only when that restore fails too does the entry stand in both
      files, and the Error line then says so

A TASK_TITLE is matched against the "## " headings only by exact equality after
whitespace-folding and case-folding; a partial title, a title two sections share, or one
no section carries is refused. Both writers refuse an empty title or body, and a title
whose folded form equals one TASKS_TODO.md already holds (for initialize, one the list
itself repeats). No other rule of the task format is checked: titles and bodies are written
as given.

A free-text body (the list of initialize, the section body of insert, the bar of move) travels on standard
input, never as an argument: the tool reads sys.stdin.buffer to end of file exactly once
per call and decodes it as UTF-8 itself, and it refuses a terminal stdin so a call that
forgot to pipe its body (a quoted heredoc, a redirected file) fails instead of blocking.

Task file model, read whole on every write:
  - the preamble is everything before the first column-0 "## " line; it is never checked
    and never refused, and every write discards it and renders the file's fixed heading
    ("# TASKS TODO" or "# TASKS DONE") in its place
  - every column-0 "## " line is a section heading, with no code-fence exemption
  - a section ends at its "---" line when one comes first, and otherwise at the next
    heading or the end of the file; a "---" line is that separator only when the next
    non-blank line is a heading or the end of the file, and every other "---" line is body
    text of its section, so a separator is always the one standing directly before the
    next heading or the end of the file
  - in TASKS_DONE.md a section's last "**Verified:**" line splits its body from its
    acceptance bar
  - a section's body (and bar) is carried through as parsed, with only its leading and
    trailing blank lines trimmed

Canonical layout, the form every write renders the whole file into, every section the call
did not touch included: the heading line and one blank line; then for each section its
"## <Task Title>" line, a blank line, the body and a blank line, in TASKS_DONE.md the
"**Verified:**" line, a blank line, the bar and a blank line, then "---"; one blank line
between sections; UTF-8, LF line ends, the file ending in "---" plus one newline (or in the
heading's blank line when it holds no section).

Output and error contract:
  - a mutator prints nothing on success
  - every failure is exactly one line "Error: <reason>" on stderr with exit status 1, and
    a non-zero exit leaves both task files byte-for-byte unchanged (move restores
    TASKS_DONE.md itself when its second replace fails, and says so in the one line when
    that restore fails too); a malformed invocation
    gets argparse's own usage message and exit status 2; no traceback ever reaches the
    caller
  - each file is replaced through a temporary file in its own directory renamed over it,
    keeping its mode

Standard library only; runs on Python 3.9 and later.
"""

import argparse
import os
import stat
import sys
import tempfile
from dataclasses import dataclass
from typing import List, Optional

TODO_NAME = "TASKS_TODO.md"
TODO_HEADING = "# TASKS TODO"
DONE_NAME = "TASKS_DONE.md"
DONE_HEADING = "# TASKS DONE"
HEADING_PREFIX = "## "
SEPARATOR = "---"
VERIFIED_LABEL = "**Verified:**"


class ToolError(Exception):
    """A failure the caller is told about as one `Error: <reason>` line with exit status 1."""


@dataclass
class Section:
    title: str
    body: str
    bar: Optional[str] = None


@dataclass
class TaskFile:
    heading: str
    sections: List[Section]
    with_bar: bool


# --- text -----------------------------------------------------------------------------


def fold(text):
    """The text as one line: whitespace runs and newlines collapsed to a space, ends trimmed."""
    return " ".join((text or "").split())


def title_key(value):
    """The comparison form of a title: whitespace-folded and case-folded."""
    return fold(value).casefold()


def lines_of(text):
    """The text's lines, CRLF and LF alike ending a line."""
    return text.replace("\r\n", "\n").split("\n")


def is_blank(line):
    return not line.strip()


def is_heading(line):
    return line.startswith(HEADING_PREFIX)


def is_separator(lines, index):
    """Whether lines[index] is a section's separator: a "---" line whose next non-blank line
    is a heading or the end of the file."""
    if lines[index].rstrip() != SEPARATOR:
        return False
    following = index + 1
    while following < len(lines) and is_blank(lines[following]):
        following += 1
    return following == len(lines) or is_heading(lines[following])


def trimmed(lines):
    """The lines joined, with leading and trailing blank lines dropped."""
    start, end = 0, len(lines)
    while start < end and is_blank(lines[start]):
        start += 1
    while end > start and is_blank(lines[end - 1]):
        end -= 1
    return "\n".join(lines[start:end])


# --- model ----------------------------------------------------------------------------


def parse_sections(text, with_bar):
    """The text's preamble (the lines before its first heading) and its sections."""
    lines = lines_of(text)
    index = 0
    while index < len(lines) and not is_heading(lines[index]):
        index += 1
    preamble = lines[:index]
    sections = []
    while index < len(lines):
        title = lines[index][len(HEADING_PREFIX):].strip()
        index += 1
        content = []
        while index < len(lines) and not is_heading(lines[index]):
            if is_separator(lines, index):
                index += 1
                while index < len(lines) and not is_heading(lines[index]):
                    index += 1
                break
            content.append(lines[index])
            index += 1
        sections.append(make_section(title, content, with_bar))
    return preamble, sections


def make_section(title, content, with_bar):
    if with_bar:
        labels = [position for position, line in enumerate(content) if line.rstrip() == VERIFIED_LABEL]
        if labels:
            label = labels[-1]
            return Section(title, trimmed(content[:label]), trimmed(content[label + 1:]))
    return Section(title, trimmed(content))


def render_section(section):
    parts = [HEADING_PREFIX + section.title, ""]
    if section.body:
        parts += [section.body, ""]
    if section.bar is not None:
        parts += [VERIFIED_LABEL, ""]
        if section.bar:
            parts += [section.bar, ""]
    parts.append(SEPARATOR)
    return "\n".join(parts) + "\n"


def render_file(task_file):
    """The whole file in the canonical layout."""
    head = task_file.heading + "\n\n"
    return head + "\n".join(render_section(section) for section in task_file.sections)


# --- the files ------------------------------------------------------------------------


def todo_path(milestone_dir):
    return os.path.join(milestone_dir, TODO_NAME)


def done_path(milestone_dir):
    return os.path.join(milestone_dir, DONE_NAME)


def read_file_bytes(path):
    try:
        with open(path, "rb") as handle:
            return handle.read()
    except FileNotFoundError:
        raise ToolError(f"{path} does not exist")


def load_task_file(path, heading, with_bar):
    """The parsed task file at path, its preamble discarded."""
    return decode_task_file(path, read_file_bytes(path), heading, with_bar)


def decode_task_file(path, data, heading, with_bar):
    """The parsed task file whose bytes, read from path, are data, its preamble discarded."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise ToolError(f"{path} is not UTF-8 text")
    _, sections = parse_sections(text, with_bar)
    return TaskFile(heading, sections, with_bar)


def load_todo(milestone_dir):
    return load_task_file(todo_path(milestone_dir), TODO_HEADING, with_bar=False)


def load_done(milestone_dir):
    return load_task_file(done_path(milestone_dir), DONE_HEADING, with_bar=True)


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


def save_task_file(path, task_file):
    write_bytes(path, render_file(task_file).encode("utf-8"))


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


# --- lookups --------------------------------------------------------------------------


def _quoted(values):
    return ", ".join(f'"{value}"' for value in values)


def find_section(task_file, path, title):
    """The index of the one section whose heading equals the title, compared whitespace-
    folded and case-folded; none matching or more than one matching is a ToolError."""
    wanted = title_key(title)
    matches = [index for index, section in enumerate(task_file.sections) if title_key(section.title) == wanted]
    if len(matches) > 1:
        raise ToolError(f"{len(matches)} sections of {path} are titled \"{fold(title)}\"; the title names no single section")
    if not matches:
        titles = [section.title for section in task_file.sections]
        held = f"its sections are {_quoted(titles)}" if titles else "it holds no section"
        raise ToolError(f"no section of {path} is titled \"{fold(title)}\"; {held}")
    return matches[0]


def check_new_title(task_file, path, title):
    """Refuse a title whose folded form a section of the file already carries."""
    wanted = title_key(title)
    for section in task_file.sections:
        if title_key(section.title) == wanted:
            raise ToolError(f"{path} already holds a section titled \"{section.title}\"")


# --- subcommands ----------------------------------------------------------------------


def cmd_initialize(args):
    path = todo_path(args.milestone_dir)
    read_file_bytes(path)
    text = read_body("the task list")
    preamble, sections = parse_sections(text, with_bar=False)
    if any(not is_blank(line) for line in preamble):
        raise ToolError(
            "the task list on standard input holds text before its first \"## \" heading; "
            "pipe only the task sections"
        )
    if not sections:
        raise ToolError("the task list on standard input holds no \"## \" section")
    seen = {}
    for position, section in enumerate(sections, start=1):
        if not section.title:
            raise ToolError(f"section {position} of the task list on standard input has an empty title")
        if not section.body:
            raise ToolError(f"the section titled \"{section.title}\" on standard input has an empty body")
        key = title_key(section.title)
        if key in seen:
            raise ToolError(f"the task list on standard input titles two sections \"{seen[key]}\" and \"{section.title}\", which fold to the same title")
        seen[key] = section.title
    save_task_file(path, TaskFile(TODO_HEADING, sections, with_bar=False))
    return 0


def cmd_insert(args):
    title = fold(args.task_title)
    if not title:
        raise ToolError("the task title is empty")
    path = todo_path(args.milestone_dir)
    task_file = load_todo(args.milestone_dir)
    body = trimmed(lines_of(read_body("the task body")))
    if not body:
        raise ToolError("the task body on standard input is empty")
    check_new_title(task_file, path, title)
    if args.end:
        position = len(task_file.sections)
    elif args.before is not None:
        position = find_section(task_file, path, args.before)
    else:
        position = find_section(task_file, path, args.after) + 1
    task_file.sections.insert(position, Section(title, body))
    save_task_file(path, task_file)
    return 0


def cmd_move(args):
    todo = todo_path(args.milestone_dir)
    done = done_path(args.milestone_dir)
    todo_file = load_todo(args.milestone_dir)
    done_bytes = read_file_bytes(done)
    done_file = decode_task_file(done, done_bytes, DONE_HEADING, with_bar=True)
    position = find_section(todo_file, todo, args.task_title)
    bar = trimmed(lines_of(read_body("the acceptance bar")))
    if not bar:
        raise ToolError("the acceptance bar on standard input is empty")
    section = todo_file.sections.pop(position)
    done_file.sections.append(Section(section.title, section.body, bar))
    new_done = render_file(done_file).encode("utf-8")
    new_todo = render_file(todo_file).encode("utf-8")
    write_bytes(done, new_done)
    try:
        write_bytes(todo, new_todo)
    except Exception as error:
        try:
            write_bytes(done, done_bytes)
        except Exception as restore_error:
            raise ToolError(
                f"replacing {todo} failed ({describe(error)}) and restoring {done} failed too "
                f"({describe(restore_error)}); the section \"{section.title}\" now stands in both files"
            )
        raise
    return 0


# --- command line ---------------------------------------------------------------------


def build_parser():
    parser = argparse.ArgumentParser(
        prog="task_list.py",
        description="Write a milestone's existing TASKS_TODO.md and TASKS_DONE.md, the task lists this tool writes.",
    )
    subcommands = parser.add_subparsers(dest="subcommand", metavar="<subcommand>", required=True)

    def add_subcommand(name, func, help_text):
        subparser = subcommands.add_parser(name, help=help_text, description=help_text)
        subparser.add_argument(
            "milestone_dir",
            metavar="MILESTONE_DIR",
            help="the resolved milestone directory holding TASKS_TODO.md and TASKS_DONE.md",
        )
        subparser.set_defaults(func=func)
        return subparser

    add_subcommand(
        "initialize",
        cmd_initialize,
        "replace TASKS_TODO.md with its heading and the whole ordered list of sections read "
        "from standard input in the file's own form (a \"## <Task Title>\" heading, the body, "
        "a \"---\" line); every section is validated first, so the list lands whole or the file "
        "is left unchanged",
    )

    insert_parser = add_subcommand(
        "insert",
        cmd_insert,
        "put one new section into TASKS_TODO.md, its heading the given title and its body read "
        "from standard input, at the one position the required flag names",
    )
    insert_parser.add_argument(
        "task_title",
        metavar="TASK_TITLE",
        help="the new section's title, compared whitespace-folded and case-folded against the existing titles",
    )
    position = insert_parser.add_mutually_exclusive_group(required=True)
    position.add_argument(
        "--end",
        action="store_true",
        help="put the section after the last section",
    )
    position.add_argument(
        "--before",
        metavar="TASK_TITLE",
        help="put the section ahead of the section with this title, compared whitespace-folded and case-folded",
    )
    position.add_argument(
        "--after",
        metavar="TASK_TITLE",
        help="put the section behind the section with this title, compared whitespace-folded and case-folded",
    )

    move_parser = add_subcommand(
        "move",
        cmd_move,
        "move the TASKS_TODO.md section with the given title to the end of TASKS_DONE.md, "
        "followed by the \"**Verified:**\" line and the acceptance bar read from standard input",
    )
    move_parser.add_argument(
        "task_title",
        metavar="TASK_TITLE",
        help="the title of the section to move, compared whitespace-folded and case-folded against the TASKS_TODO.md titles",
    )
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
