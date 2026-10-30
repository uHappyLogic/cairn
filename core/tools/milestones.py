"""The read-only milestones tool: a project's record of finished work, read from its git log.

Usage: python3 <plugin root>/tools/milestones.py tasks PATH [--with-body]

Run from the workspace root. Every read is a read-only git command (git log and git ls-files)
run in the working directory the tool is started from, so git reads PATH relative to that
directory, literally rather than as a pattern. The tool writes no file, commits nothing,
reads no file of its own, and never reads milestones/README.md.

Subcommands:
  tasks PATH [--with-body]
      print one line for every commit that changed PATH and whose subject opens with
      "Task-completion:", the completion of one task. Each line is four fields separated
      by single tab characters: the commit's abbreviated hash as git's %h prints it, its
      author date as YYYY-MM-DD, the milestone the task belongs to, and the task title,
      which is the subject after the "Task-completion:" marker with its surrounding spaces
      trimmed. The milestone is the "milestones/<name>/" directory of the one file in the
      commit's whole file list that matches the root-anchored pattern
      milestones/*/TASKS_TODO.md (the task list the completion removed the task from);
      when no file of the list matches, or more than one does, the field holds the fixed
      placeholder "-" and the line is printed all the same. The lines are ordered newest
      first by author timestamp, sorted after the log is read, commits sharing a timestamp
      keeping git's order. A commit changed PATH when PATH, a file or a directory, differs
      between it and its parent; merge commits are never listed. PATH may be a milestone
      directory, which lists that milestone's completed tasks.
      With --with-body each task line is followed by the commit's body, the verified bar
      the task was completed against, every body line printed beneath it indented by four
      spaces (a blank line inside the body included) with the body's outer blank lines
      trimmed and nothing else changed; a commit with no body is its task line alone. Every
      task line stays at column 0, so the next column-0 line is the next task.
      When no task commit changed PATH the tool prints nothing and exits 0 if PATH is
      present in the working tree or was changed by any commit at all, and refuses
      otherwise, a path that is neither being most likely mistyped.

Limits:
  - the record is the git log: in a shallow clone the truncated history omits older task
    commits without any sign, and no check is made for it
  - only subjects opening with "Task-completion:" are read, so the record starts at that
    marker's first use (2026-09-02, in the plugin's own milestone_15); a task completed
    earlier, under the retired "Tasklist-completion:" marker that carried the task title in
    the commit body, is not listed

Output and error contract:
  - a query prints its lines on stdout and exits 0, printing nothing for an empty result
  - every failure is exactly one line "Error: <reason>" on stderr with exit status 1 and
    nothing on stdout: a PATH that is empty, or neither present in the working tree nor
    changed by any commit (the reason naming PATH as given), and a git command that could
    not be run or failed (outside a git repository, for instance), the reason naming the
    command and its exit status and carrying git's own message folded to one line; a
    malformed invocation gets argparse's own usage message and exit status 2; no traceback
    ever reaches the caller

Standard library only; runs on Python 3.9 and later.
"""

import argparse
import subprocess
import sys
from dataclasses import dataclass

TASK_MARKER = "Task-completion:"
NO_MILESTONE = "-"
BODY_INDENT = "    "
TASK_LIST_NAME = "TASKS_TODO.md"
MILESTONES_ROOT = "milestones"

# The fields of one commit in the log read, each preceded by a NUL: the full hash, %h, the
# author timestamp, the author date, the subject, and the body. git makes no commit message
# and no path holding a NUL, so every NUL in the read is structure.
LOG_FORMAT = "%x00%H%x00%h%x00%at%x00%ad%x00%s%x00%b"
FIELD_COUNT = 6

# Settings a repository or user configuration could otherwise change in the reads: no
# rename-following, no signature output, the root commit's files listed, and every path in
# a file list given from the repository root.
GIT_SETTINGS = (
    "-c",
    "log.follow=false",
    "-c",
    "log.showSignature=false",
    "-c",
    "log.showRoot=true",
    "-c",
    "diff.relative=false",
)

DESCRIPTION = """\
Read the project's record of finished work from its git log, writing nothing.
Run from the workspace root: git reads every PATH relative to the working directory."""

TASKS_DESCRIPTION = """\
Print one line per commit that changed PATH and whose subject opens with
Task-completion:, newest first by author timestamp. Each line is four fields
separated by tabs: the abbreviated hash, the author date as YYYY-MM-DD, the
milestone directory joined from the one milestones/*/TASKS_TODO.md in the
commit's file list ("-" when none or several match), and the task title.
A milestone directory as PATH lists that milestone's completed tasks. When no
task commit changed PATH, nothing is printed if PATH is present in the working
tree or was changed by any commit, and one Error line is printed otherwise."""

LIMITS = """\
Limits:
  - the record is the git log: in a shallow clone the truncated history omits
    older task commits without any sign, and no check is made for it
  - only subjects opening with Task-completion: are read, so the record starts at
    that marker's first use (2026-09-02, in the plugin's own milestone_15); a task
    completed earlier, under the retired Tasklist-completion: marker that carried
    the task title in the commit body, is not listed"""


class ToolError(Exception):
    """A failure the caller is told about as one `Error: <reason>` line with exit status 1."""


@dataclass
class TaskCommit:
    short_hash: str
    timestamp: int
    date: str
    milestone: str
    title: str
    body: str


# --- text -----------------------------------------------------------------------------


def fold(text):
    """The text as one line: whitespace runs and newlines collapsed to a space, ends trimmed."""
    return " ".join((text or "").split())


def decoded(data):
    return data.decode("utf-8", "replace")


def body_lines(body):
    """The body's lines with its leading and trailing blank lines trimmed."""
    lines = body.split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


# --- git ------------------------------------------------------------------------------


def git(arguments):
    """Run one read-only git command reading its pathspecs literally, with no standard input,
    and return its stdout; a command that cannot be run or exits non-zero is a ToolError."""
    command = arguments[0]
    try:
        result = subprocess.run(
            ["git", "--literal-pathspecs", *GIT_SETTINGS, *arguments],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            check=False,
        )
    except OSError as error:
        raise ToolError(f"git {command} could not be run: {error.strerror or error}")
    if result.returncode != 0:
        message = decoded(result.stderr)
        if not message.strip():
            message = decoded(result.stdout)
        reason = f"git {command} exited {result.returncode}"
        if message.strip():
            reason += ": " + message
        raise ToolError(reason)
    return result.stdout


def parse_log(data):
    """The commits of a log read made with LOG_FORMAT, -z, and --name-only: a list of
    (fields, file names) pairs, the six fields and the names as bytes, in git's order.

    Each commit is a NUL, its six NUL-separated fields, the NUL ending the commit's message,
    then its file names, each ending in a NUL and the first preceded by the newline git puts
    between a message and its file list. A file name is never empty, so an empty token among
    the names is the NUL opening the next commit."""
    tokens = data.split(b"\0")
    commits = []
    index = 0
    while index < len(tokens) - 1:
        if tokens[index] != b"":
            raise ToolError("git log printed output this tool cannot read")
        fields = tokens[index + 1 : index + 1 + FIELD_COUNT]
        if len(fields) != FIELD_COUNT:
            raise ToolError("git log printed output this tool cannot read")
        index += 1 + FIELD_COUNT
        names = []
        while index < len(tokens) and tokens[index] != b"":
            name = tokens[index]
            if not names and name.startswith(b"\n"):
                name = name[1:]
            if name:
                names.append(name)
            index += 1
        commits.append((fields, names))
    return commits


def is_task_list(name):
    """Whether a repository-root path matches milestones/*/TASKS_TODO.md."""
    parts = name.split("/")
    return len(parts) == 3 and parts[0] == MILESTONES_ROOT and parts[1] != "" and parts[2] == TASK_LIST_NAME


def milestone_of(names):
    """The milestone directory a commit's file list joins it to, or the fixed placeholder when
    no file of the list, or more than one, is a milestone's task list."""
    matches = sorted({name for name in names if is_task_list(name)})
    if len(matches) != 1:
        return NO_MILESTONE
    return matches[0][: -len(TASK_LIST_NAME)]


def task_commits(path):
    """Every commit that changed PATH and whose subject opens with the task marker, newest
    first by author timestamp."""
    data = git(
        [
            "log",
            "--full-history",
            "--no-merges",
            "--full-diff",
            "--name-only",
            "--no-renames",
            "-z",
            "--date=short",
            "--format=" + LOG_FORMAT,
            "--",
            path,
        ]
    )
    found = []
    for fields, names in parse_log(data):
        _, short_hash, timestamp, date, subject, body = (decoded(field) for field in fields)
        if not subject.startswith(TASK_MARKER):
            continue
        try:
            seconds = int(timestamp)
        except ValueError:
            raise ToolError(f"git log printed an author timestamp this tool cannot read: {timestamp}")
        found.append(
            TaskCommit(
                short_hash=short_hash,
                timestamp=seconds,
                date=date,
                milestone=milestone_of([decoded(name) for name in names]),
                title=subject[len(TASK_MARKER) :].strip(),
                body=body,
            )
        )
    return sorted(found, key=lambda commit: commit.timestamp, reverse=True)


def changed_by_any_commit(path):
    return bool(git(["log", "-1", "--full-history", "--format=%h", "--", path]).strip())


def present_in_working_tree(path):
    return bool(git(["ls-files", "--cached", "--others", "--directory", "-z", "--", path]).strip(b"\0"))


# --- the query ------------------------------------------------------------------------


def cmd_tasks(args):
    path = args.path
    if not path:
        raise ToolError("the PATH given is empty")
    commits = task_commits(path)
    if not commits:
        if not changed_by_any_commit(path) and not present_in_working_tree(path):
            raise ToolError(f"the path {path} is neither present in the working tree nor changed by any commit")
        return 0
    lines = []
    for commit in commits:
        lines.append(f"{commit.short_hash}\t{commit.date}\t{commit.milestone}\t{commit.title}\n")
        if args.with_body:
            lines.extend(BODY_INDENT + line + "\n" for line in body_lines(commit.body))
    sys.stdout.write("".join(lines))
    return 0


# --- command line ---------------------------------------------------------------------


def build_parser():
    parser = argparse.ArgumentParser(
        prog="milestones.py",
        description=DESCRIPTION,
        epilog=LIMITS,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subcommands = parser.add_subparsers(dest="subcommand", metavar="<subcommand>", required=True)

    tasks_parser = subcommands.add_parser(
        "tasks",
        help="list the task commits that changed PATH",
        description=TASKS_DESCRIPTION,
        epilog=LIMITS,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    tasks_parser.add_argument(
        "path",
        metavar="PATH",
        help="a file or directory, read by git relative to the working directory",
    )
    tasks_parser.add_argument(
        "--with-body",
        action="store_true",
        help=(
            "print each commit's body, the task's verified bar, beneath its line: every body line "
            "indented by four spaces, the body's outer blank lines trimmed, nothing beneath a "
            "commit with no body"
        ),
    )
    tasks_parser.set_defaults(func=cmd_tasks)
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
