"""The commit command of the skill layer: one git commit of exactly the named paths, made with
those paths as its pathspec, each git write repeated while another process holds git's lock.

Usage: python3 <plugin root>/tools/commit.py --subject SUBJECT [--body BODY] [--] PATH [PATH ...]
       python3 <plugin root>/tools/commit.py --subject SUBJECT [--body BODY] --path-file FILE

Unlike the document writers beside it, which touch no git, this module exists to run git: it
reads or writes no milestone file and takes no milestone directory. It runs git in the
working directory it is started from, so git reads every PATH relative to that directory, as
a path of the repository holding it.

Steps, each run only when the one before it succeeded:
  1. the dirty-own-path guard, "git status --porcelain -- PATH...", over the named paths
     only. When it prints nothing, none of the paths changed: the call stages nothing,
     commits nothing, prints its fixed no-op line on standard output, and exits 0. The
     guard is a read: it runs with git's optional locks off, so it never takes the index
     lock another process's write may be waiting for, and it is never repeated
  2. the path-scoped stage, "git add -- PATH...", staging exactly the named paths
  3. the commit, "git commit -m SUBJECT [-m BODY] -- PATH...", with the named paths as its
     pathspec, so the commit records exactly those paths whatever else the index holds, and
     every other staged change stays staged and uncommitted

The paths are given either as arguments (behind "--" when one may begin with "-") or, with
--path-file, in a file holding one path per line, never both. A path file is read
line-exact: it is split at its newlines only, each line taken whole as one path with no word
splitting, quoting, or trimming of its own, a line holding nothing is skipped (it names no
path), and its last line needs no newline. However they are given, the paths reach every git
command as separate arguments, read literally rather than as patterns, so a path holding a
glob character names that one file only. No path is checked beyond that: git reports a path
it cannot use.

SUBJECT is the commit's one-line subject, passed to git as given. BODY, when given and holding
anything but whitespace, is the commit's body, passed to git as given, line breaks included;
an empty or whitespace-only BODY makes the same subject-only commit as no BODY.

The retry: each git write (steps 2 and 3) is repeated when git exits with status 128, its
fatal-error status and the one a held .git/index.lock produces, up to ATTEMPTS attempts in
all with a fixed pause of PAUSE seconds between two. The schedule is one constant applied at
every write, with no option or variable to change it. Every other non-zero status (1: a
hook's refusal, nothing to commit, a commit pathspec matching no file) is passed on at once.
Only the exit status is tested; no message text is read.

Refusals, made before any git command runs: an empty or multi-line SUBJECT, an empty path
argument, no path given at all, and a path file that is missing, unreadable, not UTF-8 text,
or naming no path. Nothing else is checked.

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
  - a failing call commits nothing and discards or unstages nothing; a failure at the commit
    leaves the paths staged as step 2 left them

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


def gather_paths(paths, path_file):
    if path_file is not None:
        return read_path_file(path_file)
    if not paths:
        raise ToolError("no path is given: name the paths to commit as arguments or in a file given as --path-file")
    if any(not path for path in paths):
        raise ToolError("a path given as an argument is empty")
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
    paths = gather_paths(args.paths, args.path_file)

    guard_environment = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    status = git(["status", "--porcelain", "--", *paths], guard_environment)
    if status.returncode != 0:
        raise failure("status", status)
    if not status.stdout.strip():
        print(NO_OP_LINE)
        return 0

    result, attempts = write(["add", "--", *paths])
    if result.returncode != 0:
        raise failure("add", result, attempts)

    message = ["-m", subject] if body is None else ["-m", subject, "-m", body]
    result, attempts = write(["commit", *message, "--", *paths])
    if result.returncode != 0:
        raise failure("commit", result, attempts)
    return 0


# --- command line ---------------------------------------------------------------------


def build_parser():
    parser = argparse.ArgumentParser(
        prog="commit.py",
        description=(
            "Commit exactly the named paths, with those paths as the commit's pathspec: a "
            "status guard over them, a path-scoped git add, and git commit, each git write "
            "repeated on a fixed schedule while git exits 128. Prints nothing when the commit "
            "lands and one fixed line when none of the paths changed."
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
        "--path-file",
        metavar="FILE",
        help="a file naming the paths to commit, one per line, each line taken whole; instead of PATH arguments",
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
