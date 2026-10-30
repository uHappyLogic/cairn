"""The commit command of the skill layer: one git commit of exactly the named paths, made with
those paths as its pathspec, each git write repeated while another process holds git's lock,
with an optional removal of named paths made inside the same commit and an optional author
date given to it.

Usage: python3 <plugin root>/tools/commit.py --subject SUBJECT [--body BODY] [--date DATE] [--remove PATH ...] [--] PATH [PATH ...]
       python3 <plugin root>/tools/commit.py --subject SUBJECT [--body BODY] [--date DATE] [--remove PATH ...] --path-file FILE
       python3 <plugin root>/tools/commit.py --subject SUBJECT [--body BODY] [--date DATE] --remove PATH [--remove PATH ...]

Unlike the document writers beside it, which touch no git, this module exists to run git: it
reads or writes no milestone file and takes no milestone directory. It runs git in the
working directory it is started from, so git reads every PATH relative to that directory, as
a path of the repository holding it.

Steps, each run only when the one before it succeeded:
  1. the dirty-own-path guard, "git status --porcelain -- PATH... REMOVED...", over the named
     paths and the paths to remove only, and, for each path given as --remove,
     "git ls-files -- REMOVED", which tells whether the index still holds a file under it.
     When the status prints nothing and no path to remove is still in the index, none of the
     paths changed: the call removes nothing, stages nothing, commits nothing, prints its
     fixed no-op line on standard output, and exits 0. The guard is a read: it runs with
     git's optional locks off, so it never takes the index lock another process's write may
     be waiting for, and it is never repeated
  2. the removal, "git rm -r -q -- REMOVED", once for each path given as --remove that the
     index still holds, in the order given and before any path is staged: it takes the
     path's tracked files out of the index and the working tree, and leaves every untracked
     file under it in place. A path whose files have already left the index (the staged
     removal a failed earlier run of the same call left behind) is not removed again; its
     staged removal is recorded by the commit as it stands. Git refuses to remove a tracked
     file holding a change of its own, so a removal never discards uncommitted work
  3. the path-scoped stage, "git add -- PATH...", staging exactly the named paths, run only
     when a PATH is given
  4. the commit, "git commit -m SUBJECT [-m BODY] [--date DATE] -- PATH... REMOVED...", with
     the named paths and the paths to remove together as its pathspec, so the one commit
     records the removals and those paths and nothing else whatever else the index holds, and
     every other staged change stays staged and uncommitted

The paths are given either as arguments (behind "--" when one may begin with "-") or, with
--path-file, in a file holding one path per line, never both. A path file is read
line-exact: it is split at its newlines only, each line taken whole as one path with no word
splitting, quoting, or trimming of its own, a line holding nothing is skipped (it names no
path), and its last line needs no newline. The paths to remove are given as --remove, one
path per option, repeated for each, beside either form or alone. However they are given, the
paths reach every git command as separate arguments, read literally rather than as
patterns, so a path holding a glob character names that one file only. No path is checked
beyond that: git reports a path it cannot use. A call without --remove runs exactly steps 1,
3, and 4 over its named paths, the guard's status alone and no ls-files.

SUBJECT is the commit's one-line subject, passed to git as given. BODY, when given and holding
anything but whitespace, is the commit's body, passed to git as given, line breaks included;
an empty or whitespace-only BODY makes the same subject-only commit as no BODY.

DATE, when given, is the commit's author date, passed to git unchanged as "git commit --date
DATE" and parsed by git, which accepts among its forms the ISO 8601 date "git log
--format=%aI" prints. It sets the author date only: the committer date stays the time the
commit is actually made. A call without --date runs exactly the commands it ran before the
option existed, both dates the time of the commit. A DATE git cannot parse fails the commit
with git's own message; since git exits 128 for it, that failure is reported after the last
attempt of the retry below.

The retry: each git write (steps 2, 3, and 4) is repeated when git exits with status 128,
its fatal-error status and the one a held .git/index.lock produces, up to ATTEMPTS attempts
in all with a fixed pause of PAUSE seconds between two. The schedule is one constant applied
at every write, with no option or variable to change it. Every other non-zero status (1: a
hook's refusal, nothing to commit, a removal git refuses, a commit pathspec matching no
file) is passed on at once. Only the exit status is tested; no message text is read.

Refusals, made before any git command runs: an empty or multi-line SUBJECT, an empty or
whitespace-only DATE, an empty path argument, an empty --remove value, no path and no
--remove given at all, and a path file that is missing, unreadable, not UTF-8 text, or
naming no path. Nothing else is checked.

Output and error contract:
  - a commit that lands prints nothing; a call whose guard found none of the paths changed
    prints exactly the one line "Nothing committed — none of the paths changed." on stdout
    and exits 0
  - every failure is exactly one line "Error: <reason>" on stderr with exit status 1: a
    refusal, or a git command that failed, the reason naming the command and its exit status
    and carrying git's own message folded to one line, after the last attempt for a write
    that kept exiting 128; a malformed invocation (no --subject, or paths given both as
    arguments and through --path-file) gets argparse's own usage message and exit status 2;
    no traceback ever reaches the caller
  - a failing call commits nothing and discards or unstages nothing; a failure after the
    removal leaves each removal staged as step 2 made it, and a failure at the commit leaves
    the paths staged as step 3 left them, so a later run of the same call records them

Standard library only; runs on Python 3.9 and later.
"""

import argparse
import os
import subprocess
import sys
import time

NO_OP_LINE = "Nothing committed — none of the paths changed."

LOCK_EXIT = 128
ATTEMPTS = 16
PAUSE = 0.25


class ToolError(Exception):
    """A failure the caller is told about as one `Error: <reason>` line with exit status 1."""


# --- text -----------------------------------------------------------------------------


def fold(text):
    """The text as one line: whitespace runs and newlines collapsed to a space, ends trimmed."""
    return " ".join((text or "").split())


def decoded(data):
    return data.decode("utf-8", "replace")


# --- the inputs -----------------------------------------------------------------------


def check_subject(subject):
    if not subject.strip():
        raise ToolError("the subject given as --subject is empty")
    if "\n" in subject or "\r" in subject:
        raise ToolError("the subject given as --subject holds a line break; a subject is one line")
    return subject


def commit_body(body):
    """The body git is given, or None for a subject-only commit."""
    if body is None or not body.strip():
        return None
    return body


def check_date(date):
    """The author date git is given unchanged, or None when --date is absent."""
    if date is not None and not date.strip():
        raise ToolError("the date given as --date is empty")
    return date


def read_path_file(path):
    """The paths a path file names: one per line, each line taken whole, empty lines skipped."""
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except FileNotFoundError:
        raise ToolError(f"the path file {path} does not exist")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise ToolError(f"the path file {path} is not UTF-8 text")
    paths = [line for line in text.split("\n") if line]
    if not paths:
        raise ToolError(f"the path file {path} names no path")
    return paths


def gather_removals(removals):
    """The paths given as --remove, in the order given; none when the option is absent."""
    removals = list(removals or ())
    if any(not path for path in removals):
        raise ToolError("a path given as --remove is empty")
    return removals


def gather_paths(paths, path_file, removals):
    if path_file is not None:
        return read_path_file(path_file)
    if any(not path for path in paths):
        raise ToolError("a path given as an argument is empty")
    if not paths and not removals:
        raise ToolError(
            "no path is given: name the paths to commit as arguments or in a file given as "
            "--path-file, or the paths to remove as --remove"
        )
    return list(paths)


# --- git ------------------------------------------------------------------------------


def git(arguments, environment=None):
    """Run one git command reading its pathspecs literally, with no standard input."""
    return subprocess.run(
        ["git", "--literal-pathspecs", *arguments],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        check=False,
        env=environment,
    )


def write(arguments):
    """Run one git write, repeating it after a fixed pause while git exits with LOCK_EXIT and
    attempts remain: -> (the last attempt's result, the number of attempts made)."""
    attempt = 1
    while True:
        result = git(arguments)
        if result.returncode != LOCK_EXIT or attempt == ATTEMPTS:
            return result, attempt
        time.sleep(PAUSE)
        attempt += 1


def failure(command, result, attempts=1):
    """The ToolError reporting a failed git command, carrying git's own message."""
    message = decoded(result.stderr)
    if not message.strip():
        message = decoded(result.stdout)
    reason = f"git {command} exited {result.returncode}"
    if attempts > 1:
        reason += f" on all {attempts} attempts"
    if message.strip():
        reason += ": " + message
    return ToolError(reason)


# --- the commit -----------------------------------------------------------------------


def commit(args):
    subject = check_subject(args.subject)
    body = commit_body(args.body)
    date = check_date(args.date)
    removals = gather_removals(args.remove)
    paths = gather_paths(args.paths, args.path_file, removals)

    guard_environment = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    status = git(["status", "--porcelain", "--", *paths, *removals], guard_environment)
    if status.returncode != 0:
        raise failure("status", status)
    indexed = []
    for removal in removals:
        listing = git(["ls-files", "--", removal], guard_environment)
        if listing.returncode != 0:
            raise failure("ls-files", listing)
        if listing.stdout.strip():
            indexed.append(removal)
    if not status.stdout.strip() and not indexed:
        print(NO_OP_LINE)
        return 0

    for removal in indexed:
        result, attempts = write(["rm", "-r", "-q", "--", removal])
        if result.returncode != 0:
            raise failure("rm", result, attempts)

    if paths:
        result, attempts = write(["add", "--", *paths])
        if result.returncode != 0:
            raise failure("add", result, attempts)

    message = ["-m", subject] if body is None else ["-m", subject, "-m", body]
    if date is not None:
        message += ["--date", date]
    result, attempts = write(["commit", *message, "--", *paths, *removals])
    if result.returncode != 0:
        raise failure("commit", result, attempts)
    return 0


# --- command line ---------------------------------------------------------------------


def build_parser():
    parser = argparse.ArgumentParser(
        prog="commit.py",
        description=(
            "Commit exactly the named paths, with those paths as the commit's pathspec: a "
            "status guard over them, git rm -r -q of each path given as --remove, a "
            "path-scoped git add of the other paths, and one git commit over the removals and "
            "those paths together, given --date as its author date when one is named, each git "
            "write repeated on a fixed schedule while git exits 128. Prints nothing when the "
            "commit lands and one fixed line when none of the paths changed."
        ),
    )
    parser.add_argument(
        "--subject",
        required=True,
        metavar="SUBJECT",
        help="the commit's one-line subject",
    )
    parser.add_argument(
        "--body",
        metavar="BODY",
        help="the commit's body, passed to git as given; empty or absent makes a subject-only commit",
    )
    parser.add_argument(
        "--date",
        metavar="DATE",
        help=(
            "the commit's author date, passed to git unchanged as git commit --date DATE, such as "
            "the ISO 8601 date git log --format=%%aI prints; it sets the author date only, the "
            "committer date staying the time the commit is made; absent, both dates are that time"
        ),
    )
    parser.add_argument(
        "--path-file",
        metavar="FILE",
        help="a file naming the paths to commit, one per line, each line taken whole; instead of PATH arguments",
    )
    parser.add_argument(
        "--remove",
        action="append",
        metavar="PATH",
        help=(
            "a path to remove, run as git rm -r -q -- PATH inside the retry schedule before the "
            "other paths are staged, its removal recorded by the same commit as those paths; "
            "repeatable, one path per option, beside PATH arguments, --path-file, or alone"
        ),
    )
    parser.add_argument(
        "paths",
        nargs="*",
        metavar="PATH",
        help="a path to commit, read literally by git relative to the working directory",
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
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.path_file is not None and args.paths:
        parser.error("the paths are given either as PATH arguments or through --path-file, not both")
    try:
        return commit(args)
    except Exception as error:  # the contract: no traceback ever reaches the caller
        return _fail(describe(error))


if __name__ == "__main__":
    sys.exit(main())
