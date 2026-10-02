"""Creator of a new milestone: its directory and the four files it starts with.

Usage: python3 <plugin root>/tools/define_milestone.py --title TITLE  (goal text on stdin)

Run from the workspace root. The milestones root is always `milestones` relative to the
working directory; the tool never creates it, and when it is missing the call is refused
with a pointer at /init-milestone-base-workflow and nothing is written.

The title comes as --title and is folded to one line (whitespace runs and newlines
collapsed to one space, ends trimmed); it is refused only when empty after that fold, and
is otherwise written into the requirements.md heading with its words, case, and
punctuation unchanged. The goal text travels on standard input, never as an argument: the
tool reads sys.stdin.buffer to end of file exactly once and decodes it as UTF-8 itself,
refusing a terminal, closed, or non-UTF-8 stdin, and refusing text that is empty or only
whitespace. The goal is written under `## Goal` exactly as received with only its leading
and trailing whitespace trimmed.

Number: every directory directly under the milestones root whose whole name matches
milestone_<ASCII digits>_<non-empty slug> counts, any other entry is skipped without a
message; its digits are read as an integer with leading zeros stripped, the new number is
the maximum plus one (1 on a root holding none), formatted with at least two digits.

Slug: the first five whitespace-separated words of the folded title that survive
cleaning, joined by hyphens. Each word is folded to its ASCII base with NFKD and its
combining marks dropped, lowercased, stripped of apostrophes, and every remaining run of
characters outside [a-z0-9] turned into one hyphen with edge hyphens trimmed, so a
hyphenated compound stays one word; a word that cleans down to nothing is skipped and the
five are filled from the words that follow. A title no word of which survives is refused.

Conflict: the milestone directory milestones/milestone_<NN>_<slug> is created
exclusively, so anything already at that path (a directory, a file, or a symlink) refuses
the call before anything is written. That is the only conflict check.

Files, written in this order into the new directory, each through a temporary file in the
same directory renamed over the target:
  - open_questions.xml, the empty open-question document: <open-questions/> and a newline
  - requirements.md, headed "# Milestone <N>: <title>" with the integer number, the goal
    under "## Goal", then empty "## Relevant starting state", "## Decisions", and
    "## Out of Scope" sections
  - TASKS_TODO.md, headed "# TASKS TODO"
  - TASKS_DONE.md, headed "# TASKS DONE"

Output and error contract:
  - on success exactly two unlabeled lines on stdout: the commit subject
    "Milestone-definition: milestone_<NN>_<slug>", then the milestone directory path
    "milestones/milestone_<NN>_<slug>/", relative to the working directory
  - every failure is exactly one line "Error: <reason>" on stderr with exit status 1 and
    empty stdout; a malformed invocation gets argparse's own usage message and exit status
    2; no traceback ever reaches the caller
  - a failure after the milestone directory was created removes what the call created, in
    reverse creation order, with a plain unlink for each file and a non-recursive rmdir for
    the directory, so nothing the call did not create is ever removed; a removal that fails
    stops the cleanup, and the one Error line then gives the original reason followed by
    the paths left in place

Standard library only; runs on Python 3.9 and later.
"""

import argparse
import os
import re
import sys
import tempfile
import unicodedata

MILESTONES_ROOT = "milestones"
SUBJECT_MARKER = "Milestone-definition"
SLUG_WORDS = 5
MILESTONE_NAME = re.compile(r"milestone_([0-9]+)_(.+)", re.DOTALL)
APOSTROPHES = ("'", "‘", "’", "ʼ")
NOT_SLUG_CHARACTERS = re.compile(r"[^a-z0-9]+")

OPEN_QUESTIONS_NAME = "open_questions.xml"
OPEN_QUESTIONS_TEMPLATE = "<open-questions/>\n"

REQUIREMENTS_NAME = "requirements.md"
REQUIREMENTS_TEMPLATE = """\
# Milestone {number}: {title}

## Goal

{goal}

## Relevant starting state

## Decisions

## Out of Scope

"""

TASKS_TODO_NAME = "TASKS_TODO.md"
TASKS_TODO_TEMPLATE = """\
# TASKS TODO

"""

TASKS_DONE_NAME = "TASKS_DONE.md"
TASKS_DONE_TEMPLATE = """\
# TASKS DONE

"""


class ToolError(Exception):
    """A failure the caller is told about as one `Error: <reason>` line with exit status 1."""


# --- inputs ---------------------------------------------------------------------------


def fold(text):
    """The text as one line: whitespace runs and newlines collapsed to a space, ends trimmed."""
    return " ".join((text or "").split())


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


def read_title(value):
    title = fold(value)
    if not title:
        raise ToolError("the title given as --title is empty")
    return title


def read_goal():
    goal = read_body("the goal text").strip()
    if not goal:
        raise ToolError("the goal text on standard input is empty")
    return goal


# --- naming ---------------------------------------------------------------------------


def slug_word(word):
    """One title word as a slug word: ASCII-folded, lowercased, apostrophes deleted, every
    other run outside [a-z0-9] one hyphen, edge hyphens trimmed; empty when nothing survives."""
    decomposed = unicodedata.normalize("NFKD", word)
    base = "".join(character for character in decomposed if not unicodedata.combining(character))
    lowered = base.lower()
    for apostrophe in APOSTROPHES:
        lowered = lowered.replace(apostrophe, "")
    return NOT_SLUG_CHARACTERS.sub("-", lowered).strip("-")


def derive_slug(title):
    words = []
    for word in title.split():
        cleaned = slug_word(word)
        if cleaned:
            words.append(cleaned)
            if len(words) == SLUG_WORDS:
                break
    if not words:
        raise ToolError(f"no word of the title {title!r} leaves any letter or digit to build the milestone slug from")
    return "-".join(words)


def root_label(root):
    return root.rstrip("/") + "/"


def next_number(root):
    """The maximum number among the milestone directories directly under root, plus one."""
    highest = 0
    with os.scandir(root) as entries:
        for entry in entries:
            match = MILESTONE_NAME.fullmatch(entry.name)
            if match is None:
                continue
            try:
                is_directory = entry.is_dir()
            except OSError:
                continue
            if is_directory:
                highest = max(highest, int(match.group(1)))
    return highest + 1


# --- writing --------------------------------------------------------------------------


def write_new_file(path, text):
    """Write text as UTF-8 through a temporary file in the same directory renamed over the
    target; the file takes the default mode."""
    directory = os.path.dirname(path) or os.curdir
    name = os.path.basename(path)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{name}.", suffix=".tmp", dir=directory)
    try:
        umask = os.umask(0)
        os.umask(umask)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(text.encode("utf-8"))
        os.chmod(temporary, 0o666 & ~umask)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def milestone_files(number, title, goal):
    """The four files of a new milestone, in creation order, as (name, text) pairs."""
    return [
        (OPEN_QUESTIONS_NAME, OPEN_QUESTIONS_TEMPLATE),
        (REQUIREMENTS_NAME, REQUIREMENTS_TEMPLATE.format(number=number, title=title, goal=goal)),
        (TASKS_TODO_NAME, TASKS_TODO_TEMPLATE),
        (TASKS_DONE_NAME, TASKS_DONE_TEMPLATE),
    ]


def create_directory(directory):
    try:
        os.mkdir(directory)
    except FileExistsError:
        raise ToolError(f"{directory} already exists; nothing was written")


def remove_created(created):
    """Remove the created paths in reverse creation order, stopping at the first that cannot
    be removed; the paths left in place, in creation order."""
    remaining = list(created)
    while remaining:
        path = remaining[-1]
        try:
            if os.path.isdir(path) and not os.path.islink(path):
                os.rmdir(path)
            else:
                os.unlink(path)
        except FileNotFoundError:
            pass
        except OSError:
            return remaining
        remaining.pop()
    return []


def create_milestone(directory, files):
    """Create the milestone directory exclusively and write its files into it; on any
    failure remove what was created and raise one ToolError carrying the reason."""
    create_directory(directory)
    created = [directory]
    try:
        for name, text in files:
            path = os.path.join(directory, name)
            write_new_file(path, text)
            created.append(path)
    except BaseException as error:
        left = remove_created(created)
        if not isinstance(error, Exception):
            raise
        reason = describe(error)
        if left:
            reason += "; the cleanup could not remove " + ", ".join(left)
        raise ToolError(reason) from error


# --- command --------------------------------------------------------------------------


def define(args):
    title = read_title(args.title)
    slug = derive_slug(title)
    goal = read_goal()
    root = MILESTONES_ROOT
    if not os.path.isdir(root):
        raise ToolError(
            f"the milestones root {root_label(root)} does not exist in the working directory; "
            "run /init-milestone-base-workflow first"
        )
    number = next_number(root)
    name = f"milestone_{number:02d}_{slug}"
    directory = os.path.join(root, name)
    create_milestone(directory, milestone_files(number, title, goal))
    sys.stdout.write(f"{SUBJECT_MARKER}: {name}\n{root_label(directory)}\n")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="define_milestone.py",
        description=(
            "Create the next milestone directory under milestones/ with its open_questions.xml, "
            "requirements.md, TASKS_TODO.md, and TASKS_DONE.md; the goal text is read from "
            "standard input"
        ),
    )
    parser.add_argument(
        "--title",
        required=True,
        help="the milestone title, written into the requirements.md heading and the source of the slug",
    )
    parser.set_defaults(func=define)
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
    except ToolError as error:
        return _fail(str(error))
    except OSError as error:
        if error.strerror and error.filename is not None:
            return _fail(f"{error.strerror}: {error.filename}")
        return _fail(str(error))
    except Exception as error:  # the contract: no traceback ever reaches the caller
        return _fail(f"{type(error).__name__}: {error}")


if __name__ == "__main__":
    sys.exit(main())
