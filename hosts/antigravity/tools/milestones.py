"""The read-only milestones tool: a project's live milestones, read from its working tree, and
its record of finished work, read from its git log.

Usage: python3 <plugin root>/tools/milestones.py live [MILESTONE_PATH]
       python3 <plugin root>/tools/milestones.py gate MILESTONE_PATH
       python3 <plugin root>/tools/milestones.py tasks PATH [--with-body]
       python3 <plugin root>/tools/milestones.py milestones (PATH | --milestone MILESTONE_PATH) [--last N]
       python3 <plugin root>/tools/milestones.py summary MILESTONE_PATH
       python3 <plugin root>/tools/milestones.py record PATH
       python3 <plugin root>/tools/milestones.py since MILESTONE_PATH [--milestones]
       python3 <plugin root>/tools/milestones.py show MILESTONE_PATH

Run from the workspace root. Every git read is a read-only git command (git log, git ls-files,
the gate and since queries' git rev-parse, and the show query's git show) run in the working
directory the tool is started from, so git reads PATH relative to that directory, literally
rather than as a pattern; the one file read is each live milestone's requirements.md, read from
the working tree for its title and its goal and by the show query whole, and the one file
content read from a commit is a finished milestone's requirements.md at its finish commit's
parent, read by the show query. The tool writes no file, commits nothing, reads no file of its
own, and never reads milestones/README.md.

A live milestone is a directory holding a tracked file that matches the discovery pattern
**/milestones/*/requirements.md and is present in the working tree: "**/" stands for any run
of leading directories, none included, and "*" for exactly one directory name. The pattern is
matched against the repository paths git ls-files lists, so a milestones/ container may stand
at the root or at any depth beneath it. The tasks query joins a commit to its milestone by the
same pattern, read with TASKS_TODO.md in place of requirements.md.

A finished milestone is a milestone path that is not live and that the subject of a commit
other than a merge names after the "Milestone-finish:" marker, its surrounding spaces trimmed:
a milestone path being a path with its trailing slash that the discovery pattern matches read
with requirements.md appended, with no empty, "." or ".." component. When several such
commits name one path, the first the log lists, the latest, is that milestone's finish commit,
and its body is the milestone's record: its title line, a blank line, and its summary bullets.
Presence wins over the log, so a milestone whose finish was reverted, its directory present
again, is live. A milestone's scope is the directory holding its milestones/ container, the
repository root for milestones/<slug>/ and pkg/ for pkg/milestones/<slug>/.

Every commit body the tool prints (the task bars under tasks --with-body, the finish bodies
summary and record print) has its outer blank lines trimmed and then drops a trailing
paragraph whose every line is a trailer, "Token: value" with a token of letters, digits, and
hyphens (Co-Authored-By: for instance), so a body that is only an attribution trailer prints
as no body.

Subcommands:
  live [MILESTONE_PATH]
      print one line for every live milestone, ordered by path. Each line is three fields
      separated by single tab characters: the milestone path, the directory holding the
      matched requirements.md with its trailing slash, as the definition tool prints it; its
      state, the fixed word "started" when a commit other than a merge modified the
      milestone's TASKS_TODO.md after the commit that added it (the path-scoped
      "git log -1 --diff-filter=M" test, one log read per live milestone) and the fixed word
      "defined" otherwise; and its title, the text of the first "# " heading of its
      requirements.md with any legacy "Milestone <N>: " prefix stripped and whitespace runs
      folded to one space, or the fixed placeholder "-" when the file holds no such heading.
      When no milestone is live the tool prints nothing and exits 0.
      With MILESTONE_PATH, read and refused as the gate query reads and refuses it, the query
      prints, in the same line and order, only every live milestone other than the one
      MILESTONE_PATH names, started or defined, whose scope equals MILESTONE_PATH's scope,
      contains it, or lies under it; the milestone it names need not be live. Without it the
      query prints every live milestone.
  gate MILESTONE_PATH
      print the milestones holding MILESTONE_PATH's scope, one bare path per line, the
      milestone path as the live query prints it, ordered by path: every live milestone other
      than the one MILESTONE_PATH names that is started, by the live query's started test, and
      whose scope equals MILESTONE_PATH's scope, contains it, or lies under it. MILESTONE_PATH
      is read lexically relative to the workspace root, as the milestones query reads PATH
      ("." components and a trailing slash folded away), and must name a directory directly
      inside a milestones/ container, whose own directory is its scope; the milestone it names
      need not be live. A defined milestone holds nothing, and a finished one, its directory
      gone, is not live. The query prints nothing when no milestone holds the scope and exits
      0 whether or not it prints. It first runs "git rev-parse --is-shallow-repository" and
      refuses when that prints "true", since a shallow clone's truncated log can read a
      started milestone as defined: the remedy is "git fetch --unshallow". A MILESTONE_PATH
      with no milestones/ container (an absolute one or one leading out of the workspace
      included) is refused.
  tasks PATH [--with-body]
      print one line for every commit that changed PATH and whose subject opens with
      "Task-completion:", the completion of one task. Each line is four fields separated
      by single tab characters: the commit's abbreviated hash as git's %h prints it, its
      author date as YYYY-MM-DD, the milestone the task belongs to, and the task title,
      which is the subject after the "Task-completion:" marker with its surrounding spaces
      trimmed. The milestone is the directory, with its trailing slash, of the one file in
      the commit's whole file list that matches the discovery pattern read with TASKS_TODO.md
      as its last component, **/milestones/*/TASKS_TODO.md (the task list the completion
      removed the task from), so a milestones/ container at any depth joins; when no file of
      the list matches, or more than one does, the field holds the fixed placeholder "-" and
      the line is printed all the same. The lines are ordered newest first by author
      timestamp, sorted after the log is read, commits sharing a timestamp keeping git's
      order. A commit changed PATH when PATH, a file or a directory, differs between it and
      its parent; merge commits are never listed. PATH may be a milestone directory, which
      lists that milestone's completed tasks.
      With --with-body each task line is followed by the commit's body, the verified bar
      the task was completed against, every body line printed beneath it indented by four
      spaces (a blank line inside the body included) with the body's outer blank lines
      trimmed and a trailing trailer paragraph dropped, nothing else changed; a commit with
      no body is its task line alone. Every task line stays at column 0, so the next column-0
      line is the next task.
      When no task commit changed PATH the tool prints nothing and exits 0 if PATH is
      present in the working tree or was changed by any commit at all, and refuses
      otherwise, a path that is neither being most likely mistyped.
  milestones (PATH | --milestone MILESTONE_PATH) [--last N]
      print one line for every milestone, live or finished, that changed PATH through a task
      commit (a commit the tasks query lists for PATH and joins to that milestone) or whose
      scope overlaps PATH: the scope contains PATH or lies under it, read lexically from
      PATH taken relative to the workspace root, so every milestone's scope overlaps "." and
      a PATH that is absolute or leads out of the workspace overlaps no scope. Each line is
      four fields separated by single tab characters: the state, the fixed word "live" or
      "finished"; the date, the finish commit's author date as YYYY-MM-DD for a finished
      milestone and the fixed placeholder "-" for a live one; the milestone path with its
      trailing slash; and the title, for a live milestone as the live query reads it and for
      a finished one the first line of its finish commit's body with whitespace runs folded
      to one space, or "-" when the body is empty. Every live line stands above every
      finished one: the live lines ordered by path, then the finished lines newest first by
      the finish commit's author timestamp, those sharing a timestamp keeping git's order.
      A PATH neither present in the working tree nor changed by any commit is refused; one
      that is, with no milestone to list, prints nothing and exits 0.
      With --milestone MILESTONE_PATH in place of PATH, read and refused as the gate query
      reads and refuses it, the query prints the overview of that milestone's scope: exactly
      what it prints with that scope as PATH ("." for the repository root), the named
      milestone included when it is listed there; the milestone it names need not be live.
      With --last N, N a whole number, every live line is printed and only the N newest
      finished lines, by the finish commit's author timestamp, the order they are printed in;
      without it every finished line is printed. Exactly one of PATH and --milestone is given.
  summary MILESTONE_PATH
      print one milestone's summary, MILESTONE_PATH being its path exactly as the milestones
      query prints it, trailing slash included. The first line is a single field: the
      finish commit's author date as YYYY-MM-DD for a finished milestone, the fixed word
      "live" for a live one. For a finished milestone the finish commit's body follows (its
      title line, a blank line, and its bullets); for a live one its title as the live
      query reads it, then, when the section holds anything, a blank line and the body of
      the requirements.md "## Goal" section, read from the working tree, from the line after
      that heading to the next "# " or "## " heading or the end of the file, verbatim with
      its outer blank lines trimmed. A MILESTONE_PATH that names neither a live nor a
      finished milestone is refused.
  record PATH
      print, for every milestone the milestones query lists for PATH and in its order, that
      query's line verbatim at column 0, then beneath it, every line indented by four spaces
      (a blank line included): first the summary's last part, the bullets of a finished
      milestone and the goal body of a live one, the summary's first line, title line, and
      the blank line after the title dropped, since the column-0 line names them; then one
      line, verbatim as the tasks query prints it and in its order, for every task commit
      that changed PATH and joins that milestone, with no bar. No blank line or separator
      stands between milestones, so the next column-0 line is the next milestone. A
      milestone listed only because its scope overlaps PATH prints its line and its summary
      alone, and "record ." prints the whole record. PATH is refused as the milestones
      query refuses it.
  since MILESTONE_PATH [--milestones]
      print what changed around a milestone since its starting state was written, one line
      per commit, each three fields separated by single tab characters: the commit's
      abbreviated hash as git's %h prints it, its author date as YYYY-MM-DD, and its subject.
      MILESTONE_PATH is read and refused as the gate query reads and refuses it. The first
      line is the anchor: the latest commit, the first the log lists, other than a merge,
      that changed MILESTONE_PATH's requirements.md and whose subject opens with
      "Starting-state:", whatever follows the marker. When no such commit exists the query
      prints nothing at all and exits 0. Beneath the anchor stands one line for every later
      commit, a commit other than a merge reachable from HEAD and not from the anchor, that
      changed a path inside the milestone's scope but outside the milestone's own directory,
      ordered newest first by author timestamp, commits sharing a timestamp keeping git's
      order; the milestone's own task commits, those whose subject opens with
      "Task-completion:" and which the tasks query's join joins to the milestone, are never
      listed. Without --milestones such a commit is left out when every path it changed lies
      inside the directory of another live milestone that reads "defined" now, by the live
      query's started test, unless it is another milestone's task or finish commit, and the
      milestone's own commits whose subject opens with "Goal-revision:" and which changed
      its requirements.md are listed too. With --milestones only other milestones' task and
      finish commits are listed: those whose subject opens with "Task-completion:" and which
      the join does not join to the milestone, and those whose subject opens with
      "Milestone-finish:". The broad form therefore lists every line --milestones lists. The
      query first runs "git rev-parse --is-shallow-repository" and refuses when that prints
      "true", in both forms and before any log read: the remedy is "git fetch --unshallow".
  show MILESTONE_PATH
      print one milestone's requirements.md whole, verbatim, MILESTONE_PATH being its path
      exactly as the milestones query prints it, trailing slash included: for a live milestone
      the file as it stands in the working tree, and for a finished one the file as it stood at
      its finish commit's parent, read with "git show". The query takes no FILE argument: the
      question document and the task list are served by no query. A MILESTONE_PATH that names
      neither a live nor a finished milestone is refused, as the summary query refuses it.

Limits:
  - the record is the git log: in a shallow clone the truncated history omits older task
    and finish commits without any sign, and no check is made for it, so a milestone whose
    finish commit is cut off is neither listed by the milestones and record queries nor
    summarized; live's started test reads the same log, so there a started milestone whose
    task list was modified only in the omitted history reads "defined", with no check made
    for it either; two queries check, gate and since, each refusing a shallow repository
    rather than reading its truncated log
  - only subjects opening with "Task-completion:" are read as task commits, so the record
    starts at that marker's first use (2026-09-02, in the plugin's own milestone_15); a task
    completed earlier, under the retired "Tasklist-completion:" marker that carried the task
    title in the commit body, is not listed
  - only "Milestone-finish:" subjects naming a milestone path are read as finish commits,
    so a milestone whose finish subject names it by its id instead (the form used before
    milestones were addressed by path) is not finished to the tool

Output and error contract:
  - a query prints its lines on stdout and exits 0, printing nothing for an empty result
  - every failure is exactly one line "Error: <reason>" on stderr with exit status 1 and
    nothing on stdout: a PATH or MILESTONE_PATH that is empty, a PATH neither present in the
    working tree nor changed by any commit and a summary or show MILESTONE_PATH naming neither
    a live nor a finished milestone (the reason naming the value as given), a shallow
    repository, which the gate and since queries refuse naming "git fetch --unshallow", and a
    live, gate, or since MILESTONE_PATH or a milestones --milestone value with no milestones/
    container (the reason naming the value as given), a git command that could not be run or failed (outside a git repository, for
    instance), the reason naming the command and its exit status and carrying git's own
    message folded to one line, and a live milestone's requirements.md that could not be read;
    a malformed invocation gets
    argparse's own usage message and exit status 2; no traceback ever reaches the caller

Standard library only; runs on Python 3.9 and later.
"""

import argparse
import os
import posixpath
import re
import subprocess
import sys
from dataclasses import dataclass

TASK_MARKER = "Task-completion:"
FINISH_MARKER = "Milestone-finish:"
STARTING_STATE_MARKER = "Starting-state:"
GOAL_REVISION_MARKER = "Goal-revision:"
NO_MILESTONE = "-"
BODY_INDENT = "    "
TASK_LIST_NAME = "TASKS_TODO.md"

# The discovery pattern, defined here once: every tracked file matching it, present in the
# working tree, is one live milestone, the directory holding the file, and the tasks join reads
# it with the task list's name in place of its last component. "**" stands for any run of whole
# leading path components, none included, "*" for exactly one non-empty component, and every
# other component is matched literally.
DISCOVERY_PATTERN = "**/milestones/*/requirements.md"
# The container's name, read from the discovery pattern: the component the milestone's own
# directory stands directly inside.
CONTAINER = DISCOVERY_PATTERN.split("/")[-3]

STARTED = "started"
DEFINED = "defined"
NO_TITLE = "-"
TITLE_HEADING = re.compile(r"# (.*)")
LEGACY_TITLE_PREFIX = re.compile(r"Milestone [0-9]+: ")

LIVE = "live"
FINISHED = "finished"
NO_DATE = "-"
GOAL_HEADING = "## Goal"
# A line ending the goal section: the next top-level or second-level heading.
SECTION_HEADING = re.compile(r"##? ")
# One trailer line: a token of letters, digits, and hyphens, a colon, a space, and a value.
TRAILER = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]*: .*\S.*")

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
Read the project's live milestones from its working tree and its record of
finished work from its git log, writing nothing. Run from the workspace root:
git reads every PATH relative to the working directory."""

LIVE_DESCRIPTION = """\
Print one line per live milestone, ordered by path: every tracked file matching
the discovery pattern **/milestones/*/requirements.md that is present in the
working tree is one live milestone, the directory holding it. Each line is three
fields separated by tabs: the milestone path with its trailing slash; "started"
when a commit other than a merge modified the milestone's TASKS_TODO.md after
the one adding it (git log -1 --diff-filter=M on that path), "defined"
otherwise; and the title, the first "# " heading of its requirements.md with any
legacy "Milestone <N>: " prefix stripped ("-" when it has none). Nothing is
printed when no milestone is live.
With MILESTONE_PATH, read lexically relative to the workspace root and refused
when it names no directory directly inside a milestones/ container, as for the
gate query, only the other live milestones, started or defined, whose scope, the
directory holding their milestones/ container, equals MILESTONE_PATH's scope,
contains it, or lies under it are printed, in the same line and order; the
milestone it names is left out and need not be live."""

TASKS_DESCRIPTION = """\
Print one line per commit that changed PATH and whose subject opens with
Task-completion:, newest first by author timestamp. Each line is four fields
separated by tabs: the abbreviated hash, the author date as YYYY-MM-DD, the
milestone directory, with its trailing slash, joined from the one task list in
the commit's file list matching the discovery pattern read with TASKS_TODO.md
as its last component, **/milestones/*/TASKS_TODO.md ("-" when none or several
match), and the task title.
A milestone directory as PATH lists that milestone's completed tasks. When no
task commit changed PATH, nothing is printed if PATH is present in the working
tree or was changed by any commit, and one Error line is printed otherwise.
With --with-body, each body has its outer blank lines trimmed and drops a
trailing paragraph whose every line is a trailer, Token: value (Co-Authored-By:,
for instance)."""

TASKS_LIMITS = """\
Limits:
  - the record is the git log: in a shallow clone the truncated history omits
    older task commits without any sign, and no check is made for it
  - only subjects opening with Task-completion: are read, so the record starts at
    that marker's first use (2026-09-02, in the plugin's own milestone_15); a task
    completed earlier, under the retired Tasklist-completion: marker that carried
    the task title in the commit body, is not listed"""

GATE_DESCRIPTION = """\
Print the milestones holding MILESTONE_PATH's scope, one bare path per line, as
the live query prints it, ordered by path: every other live milestone that is
started, by the live query's started test, and whose scope, the directory
holding its milestones/ container, equals MILESTONE_PATH's scope, contains it,
or lies under it. MILESTONE_PATH is read lexically relative to the workspace
root and must name a directory directly inside a milestones/ container; the
milestone it names need not be live. A defined milestone holds nothing. Nothing
is printed when no milestone holds the scope, and the query exits 0 whether or
not it prints.
A shallow repository (git rev-parse --is-shallow-repository printing true) is
refused, since its truncated log can read a started milestone as defined: run
git fetch --unshallow first. A MILESTONE_PATH with no milestones/ container is
refused."""

LIVE_LIMITS = """\
Limits:
  - the started test reads the git log: in a shallow clone the truncated history
    may omit the commit that modified a milestone's task list, which then reads
    "defined" without any sign, and no check is made for it"""

FINISHED_DEFINITION = """\
A finished milestone is a milestone path, with its trailing slash, that is not
live and that a Milestone-finish: <path> subject names; the latest such commit
is its finish commit, whose body is its summary (title line, blank line,
bullets). A reverted finish, its directory present again, reads live."""

TRAILER_RULE = """\
Every body printed has its outer blank lines trimmed and drops a trailing
paragraph whose every line is a trailer, Token: value (Co-Authored-By:, for
instance)."""

MILESTONES_DESCRIPTION = (
    """\
Print one line per milestone, live or finished, that changed PATH through a task
commit (one the tasks query lists for PATH and joins to it) or whose scope
overlaps PATH: the scope, the directory holding the milestone's milestones/
container (the root for milestones/<slug>/), contains PATH or lies under it,
read lexically, so every scope overlaps ".". Each line is four fields separated
by tabs: "live" or "finished"; the finish commit's author date as YYYY-MM-DD,
"-" for a live milestone; the milestone path with its trailing slash; and the
title, read as the live query reads it for a live milestone and from the first
line of the finish commit's body for a finished one ("-" when empty). Every live
line stands above every finished one, the live lines by path, the finished ones
newest first by the finish commit's author timestamp. A PATH neither present in
the working tree nor changed by any commit is refused.
With --milestone MILESTONE_PATH in place of PATH, read lexically relative to the
workspace root and refused when it names no directory directly inside a
milestones/ container, as for the gate query, the query prints the overview of
that milestone's scope, exactly what it prints with the scope as PATH ("." for
the root); the milestone it names need not be live. With --last N every live
line is printed and only the N newest finished lines; without it, every one."""
    + "\n\n"
    + FINISHED_DEFINITION
)

SUMMARY_DESCRIPTION = (
    """\
Print one milestone's summary, MILESTONE_PATH being its path exactly as the
milestones query prints it, trailing slash included. The first line is the
finish commit's author date as YYYY-MM-DD for a finished milestone and the word
"live" for a live one. Then follows the finish commit's body for a finished
milestone (title line, blank line, bullets), and for a live one its title from
the requirements.md heading, a blank line, and the body of its ## Goal section,
read from the working tree, verbatim with its outer blank lines trimmed. A
MILESTONE_PATH naming neither a live nor a finished milestone is refused."""
    + "\n\n"
    + FINISHED_DEFINITION
    + "\n\n"
    + TRAILER_RULE
)

RECORD_DESCRIPTION = (
    """\
Print, for each milestone the milestones query lists for PATH and in its order,
that query's line at column 0, then beneath it, indented by four spaces: the
summary's bullets for a finished milestone or its goal body for a live one (the
date or "live" line, the title line, and the blank line after it dropped, since
the column-0 line names them), then the tasks line of every task commit that
changed PATH and joins that milestone, newest first, with no bar. No blank line
or separator stands between milestones: the next column-0 line is the next
milestone. A milestone listed only because its scope overlaps PATH prints its
line and summary alone; record . prints the whole record. PATH is refused as the
milestones query refuses it."""
    + "\n\n"
    + TRAILER_RULE
)

SINCE_DESCRIPTION = """\
Print what changed around a milestone since its starting state was written, one
line per commit, three fields separated by tabs: the abbreviated hash, the
author date as YYYY-MM-DD, and the subject. MILESTONE_PATH is read lexically
relative to the workspace root and must name a directory directly inside a
milestones/ container, as for the gate query.
The first line is the anchor: the latest commit other than a merge that changed
MILESTONE_PATH's requirements.md and whose subject opens with Starting-state:,
whatever follows the marker. With no anchor nothing is printed at all. Beneath
it, newest first by author timestamp, stands every later commit (reachable from
HEAD and not from the anchor, merges left out) that changed a path inside the
milestone's scope, the directory holding its milestones/ container, but outside
its own directory; the milestone's own Task-completion: commits, joined to it as
the tasks query joins them, are never listed. Without --milestones a commit is
left out when every path it changed lies inside the directory of another live
milestone that reads "defined" now, unless it is another milestone's task or
finish commit, and the milestone's own Goal-revision: commits that changed its
requirements.md are listed too. With --milestones only other milestones' task
and finish commits are listed (Task-completion: subjects the join does not tie
to this milestone, and Milestone-finish: subjects), so the broad form lists
every line --milestones lists.
A shallow repository (git rev-parse --is-shallow-repository printing true) is
refused in both forms before any log read, since its truncated log can omit the
anchor or the commits after it: run git fetch --unshallow first. A
MILESTONE_PATH with no milestones/ container is refused."""

SHOW_DESCRIPTION = (
    """\
Print one milestone's requirements.md whole, verbatim, MILESTONE_PATH being its
path exactly as the milestones query prints it, trailing slash included: for a
live milestone the file as it stands in the working tree, for a finished one the
file as it stood at its finish commit's parent, read with git show. The query
takes no FILE argument: the question document and the task list are served by no
query. A MILESTONE_PATH naming neither a live nor a finished milestone is
refused, as the summary query refuses it."""
    + "\n\n"
    + FINISHED_DEFINITION
)

SINCE_LIMITS = """\
Limits:
  - two queries check for a shallow clone, gate and since, each refusing one;
    every other query reads whatever the truncated log yields"""

HISTORY_LIMITS = """\
Limits:
  - the record is the git log: in a shallow clone the truncated history omits
    older finish and task commits without any sign, and no check is made for it,
    so a milestone whose finish commit is cut off is neither listed nor
    summarized
  - only Milestone-finish: subjects naming a milestone path are read, so a
    milestone whose finish subject names its id instead is not finished to the
    tool
  - only subjects opening with Task-completion: are read as task commits, so task
    lines start at that marker's first use (2026-09-02, in the plugin's own
    milestone_15); a task completed under the retired Tasklist-completion: marker
    is not listed"""

LIMITS = """\
Limits:
  - the record is the git log: in a shallow clone the truncated history omits
    older task and finish commits without any sign, and no check is made for it;
    live's started test reads the same log, so there a started milestone whose
    task list was modified only in the omitted history reads "defined"; two
    queries check, gate and since, each refusing a shallow repository
  - only subjects opening with Task-completion: are read, so the record starts at
    that marker's first use (2026-09-02, in the plugin's own milestone_15); a task
    completed earlier, under the retired Tasklist-completion: marker that carried
    the task title in the commit body, is not listed
  - only Milestone-finish: subjects naming a milestone path are read, so a
    milestone whose finish subject names its id instead is not finished to the
    tool"""


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


@dataclass
class FinishCommit:
    full_hash: str
    timestamp: int
    date: str
    body: str


@dataclass
class Milestone:
    """One milestone as the history queries print it: its state, date, path, and title, and
    its summary's lines, the first line and the title line included."""

    state: str
    date: str
    path: str
    title: str
    summary: list


# --- text -----------------------------------------------------------------------------


def fold(text):
    """The text as one line: whitespace runs and newlines collapsed to a space, ends trimmed."""
    return " ".join((text or "").split())


def decoded(data):
    return data.decode("utf-8", "replace")


def trimmed(lines):
    """The lines with the leading and trailing ones holding only whitespace dropped."""
    start, end = 0, len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return lines[start:end]


def body_lines(body):
    """A commit body's lines as the tool prints them: its outer blank lines trimmed, then a
    trailing paragraph whose every line is a trailer dropped, and the rest trimmed again."""
    lines = trimmed(body.split("\n"))
    start = len(lines)
    while start > 0 and lines[start - 1].strip():
        start -= 1
    if start < len(lines) and all(TRAILER.fullmatch(line) for line in lines[start:]):
        lines = trimmed(lines[:start])
    return lines


def text_lines(text):
    return re.split(r"\r?\n", text.lstrip("\ufeff"))


def goal_lines(text):
    """The body of a requirements.md text's "## Goal" section, from the line after its heading
    to the next "# " or "## " heading or the end of the text, its outer blank lines trimmed;
    no line when the text holds no such section."""
    lines = text_lines(text)
    for index, line in enumerate(lines):
        if line.rstrip() != GOAL_HEADING:
            continue
        body = []
        for following in lines[index + 1 :]:
            if SECTION_HEADING.match(following):
                break
            body.append(following)
        return trimmed(body)
    return []


def title_of(text):
    """A milestone's title: the text of the first "# " heading of its requirements.md, any
    legacy "Milestone <N>: " prefix stripped and whitespace folded, or the fixed placeholder
    when the text holds no such heading or the heading holds nothing else."""
    for line in text.lstrip("﻿").splitlines():
        heading = TITLE_HEADING.fullmatch(line)
        if heading is None:
            continue
        title = fold(heading.group(1))
        prefix = LEGACY_TITLE_PREFIX.match(title)
        if prefix is not None:
            title = title[prefix.end() :].strip()
        return title or NO_TITLE
    return NO_TITLE


# --- discovery ------------------------------------------------------------------------


def matches_components(pattern, components):
    """Whether a path's components match a pattern's, "**" taking any run of whole leading
    components (none included), "*" exactly one non-empty component, any other literally."""
    if not pattern:
        return not components
    head, rest = pattern[0], pattern[1:]
    if head == "**":
        return any(matches_components(rest, components[start:]) for start in range(len(components) + 1))
    if not components:
        return False
    if head == "*":
        if components[0] == "":
            return False
    elif components[0] != head:
        return False
    return matches_components(rest, components[1:])


def milestone_holding(name, file_name):
    """The milestone directory, with its trailing slash, holding a repository path as its file
    named file_name, when the path matches the discovery pattern read with file_name as its last
    component, and None otherwise."""
    components = name.split("/")
    pattern = DISCOVERY_PATTERN.split("/")[:-1] + [file_name]
    if not matches_components(pattern, components):
        return None
    return "/".join(components[:-1]) + "/"


def discovered_milestone(name):
    """The milestone directory a repository path names, with its trailing slash, when the path
    matches the discovery pattern, and None otherwise."""
    return milestone_holding(name, DISCOVERY_PATTERN.split("/")[-1])


def is_milestone_path(text):
    """Whether a text is a milestone path: a path with its trailing slash, no empty, "." or ".."
    component, that the discovery pattern matches read with requirements.md appended."""
    if not text.endswith("/"):
        return False
    if any(part in ("", ".", "..") for part in text[:-1].split("/")):
        return False
    return discovered_milestone(text + DISCOVERY_PATTERN.split("/")[-1]) == text


def scope_of(directory):
    """A milestone's scope as path components: the directory holding its milestones/ container,
    no component for the repository root."""
    return directory[:-1].split("/")[:-2]


def path_scope(path):
    """PATH as components relative to the workspace root, read lexically ("." and a trailing
    slash folded away), or None when PATH is absolute or leads out of the workspace."""
    normal = posixpath.normpath(path)
    if normal == ".":
        return []
    if normal.startswith("/") or normal == ".." or normal.startswith("../"):
        return None
    return normal.split("/")


def named_milestone(path):
    """A gate MILESTONE_PATH as components relative to the workspace root, read lexically as
    path_scope reads PATH, its last two the milestones/ container and the milestone's own
    directory, or None when it names no directory directly inside such a container."""
    components = path_scope(path)
    if components is None or len(components) < 2 or components[-2] != CONTAINER:
        return None
    return components


def overlaps(scope, components):
    """Whether a scope contains PATH's components or lies under them."""
    if components is None:
        return False
    shorter = min(len(scope), len(components))
    return scope[:shorter] == components[:shorter]


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


def milestone_of(names):
    """The milestone directory, with its trailing slash, a commit's file list joins it to: the
    directory of the one file of the list that is a milestone's task list by the discovery
    pattern, or the fixed placeholder when no file of the list, or more than one, is one."""
    directories = (milestone_holding(name, TASK_LIST_NAME) for name in names)
    matches = sorted({directory for directory in directories if directory is not None})
    if len(matches) != 1:
        return NO_MILESTONE
    return matches[0]


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


def finish_commits():
    """Every milestone path a finish commit names, mapped to the latest such commit, the first
    the log lists: the commits other than merges whose subject opens with the finish marker
    and names a milestone path."""
    data = git(
        [
            "log",
            "--no-merges",
            "-z",
            "--fixed-strings",
            "--grep=" + FINISH_MARKER,
            "--date=short",
            "--format=" + LOG_FORMAT,
        ]
    )
    found = {}
    for fields, _ in parse_log(data):
        full_hash, _, timestamp, date, subject, body = (decoded(field) for field in fields)
        if not subject.startswith(FINISH_MARKER):
            continue
        path = subject[len(FINISH_MARKER) :].strip()
        if not is_milestone_path(path) or path in found:
            continue
        try:
            seconds = int(timestamp)
        except ValueError:
            raise ToolError(f"git log printed an author timestamp this tool cannot read: {timestamp}")
        found[path] = FinishCommit(full_hash=full_hash, timestamp=seconds, date=date, body=body)
    return found


def changed_by_any_commit(path):
    return bool(git(["log", "-1", "--full-history", "--format=%h", "--", path]).strip())


def present_in_working_tree(path):
    return bool(git(["ls-files", "--cached", "--others", "--directory", "-z", "--", path]).strip(b"\0"))


def live_milestones():
    """Every live milestone as (directory, requirements.md path), ordered by directory: each
    tracked file matching the discovery pattern that is present in the working tree."""
    found = {}
    for token in git(["ls-files", "--cached", "-z"]).split(b"\0"):
        name = decoded(token)
        if not name:
            continue
        directory = discovered_milestone(name)
        if directory is not None and os.path.isfile(name):
            found[directory] = name
    return sorted(found.items())


def is_started(directory):
    """Whether a commit other than a merge modified the milestone's task list after the commit
    adding it: the path-scoped git log -1 --diff-filter=M test."""
    log = git(
        [
            "log",
            "-1",
            "--full-history",
            "--no-merges",
            "--diff-filter=M",
            "--format=%h",
            "--",
            directory + TASK_LIST_NAME,
        ]
    )
    return bool(log.strip())


def is_shallow():
    """Whether the repository is a shallow clone, by git rev-parse --is-shallow-repository."""
    return git(["rev-parse", "--is-shallow-repository"]).strip() == b"true"


def read_bytes(requirements):
    with open(requirements, "rb") as handle:
        return handle.read()


def read_text(requirements):
    return decoded(read_bytes(requirements))


def read_title(requirements):
    return title_of(read_text(requirements))


def live_milestone(directory, requirements):
    text = read_text(requirements)
    title = title_of(text)
    goal = goal_lines(text)
    return Milestone(LIVE, NO_DATE, directory, title, [LIVE, title] + ([""] + goal if goal else []))


def finished_milestone(path, finish):
    body = body_lines(finish.body)
    title = fold(body[0]) if body else ""
    return Milestone(FINISHED, finish.date, path, title or NO_TITLE, [finish.date] + body)


def require_existing(path):
    if not changed_by_any_commit(path) and not present_in_working_tree(path):
        raise ToolError(f"the path {path} is neither present in the working tree nor changed by any commit")


def listed_milestones(path):
    """The milestones the milestones query lists for PATH, in its order, with the task commits
    that changed PATH, newest first: every live milestone, by path, then every finished one,
    newest first by the finish commit's author timestamp, that a task commit which changed PATH
    joins or whose scope overlaps PATH."""
    if not path:
        raise ToolError("the PATH given is empty")
    commits = task_commits(path)
    if not commits:
        require_existing(path)
    joined = {commit.milestone for commit in commits}
    components = path_scope(path)

    def wanted(directory):
        return directory in joined or overlaps(scope_of(directory), components)

    live = live_milestones()
    live_directories = {directory for directory, _ in live}
    listed = [live_milestone(directory, requirements) for directory, requirements in live if wanted(directory)]
    finished = [
        (finish.timestamp, finished_milestone(directory, finish))
        for directory, finish in finish_commits().items()
        if directory not in live_directories and wanted(directory)
    ]
    finished.sort(key=lambda pair: pair[0], reverse=True)
    listed.extend(milestone for _, milestone in finished)
    return listed, commits


def anchor_commit(own):
    """The milestone's anchor: the latest commit other than a merge, the first the log lists,
    that changed its requirements.md and whose subject opens with the starting-state marker,
    as (full hash, its line), or None when there is none."""
    data = git(
        [
            "log",
            "--full-history",
            "--no-merges",
            "-z",
            "--fixed-strings",
            "--grep=" + STARTING_STATE_MARKER,
            "--date=short",
            "--format=" + LOG_FORMAT,
            "--",
            own + DISCOVERY_PATTERN.split("/")[-1],
        ]
    )
    for fields, _ in parse_log(data):
        full_hash, short_hash, _, date, subject, _ = (decoded(field) for field in fields)
        if subject.startswith(STARTING_STATE_MARKER):
            return full_hash, f"{short_hash}\t{date}\t{subject}\n"
    return None


def inside(name, directory):
    """Whether a repository path lies inside a directory given with its trailing slash."""
    return name.startswith(directory)


def under_scope(name, scope):
    """Whether a repository path lies inside a scope given as path components."""
    components = name.split("/")
    return len(components) > len(scope) and components[: len(scope)] == scope


def since_lines(own, scope, anchor, milestones_only):
    """The lines beneath the anchor, newest first by author timestamp: every later commit other
    than a merge that changed a path inside the scope and outside the milestone's own directory,
    filtered as the since query's form asks."""
    data = git(
        [
            "log",
            "--no-merges",
            "--name-only",
            "--no-renames",
            "-z",
            "--date=short",
            "--format=" + LOG_FORMAT,
            anchor + "..HEAD",
            "--",
        ]
    )
    own_requirements = own + DISCOVERY_PATTERN.split("/")[-1]
    defined = None
    found = []
    for fields, raw_names in parse_log(data):
        _, short_hash, timestamp, date, subject, _ = (decoded(field) for field in fields)
        names = [decoded(name) for name in raw_names]
        is_task = subject.startswith(TASK_MARKER)
        if is_task and milestone_of(names) == own:
            continue
        other_milestone = is_task or subject.startswith(FINISH_MARKER)
        touches_scope = any(under_scope(name, scope) and not inside(name, own) for name in names)
        if milestones_only:
            wanted = other_milestone and touches_scope
        elif subject.startswith(GOAL_REVISION_MARKER) and own_requirements in names:
            wanted = True
        elif not touches_scope:
            wanted = False
        elif other_milestone:
            wanted = True
        else:
            if defined is None:
                defined = [
                    directory
                    for directory, _ in live_milestones()
                    if directory != own and not is_started(directory)
                ]
            wanted = not all(any(inside(name, directory) for directory in defined) for name in names)
        if not wanted:
            continue
        try:
            seconds = int(timestamp)
        except ValueError:
            raise ToolError(f"git log printed an author timestamp this tool cannot read: {timestamp}")
        found.append((seconds, f"{short_hash}\t{date}\t{subject}\n"))
    found.sort(key=lambda pair: pair[0], reverse=True)
    return [line for _, line in found]


def milestone_line(milestone):
    return f"{milestone.state}\t{milestone.date}\t{milestone.path}\t{milestone.title}\n"


def task_line(commit):
    return f"{commit.short_hash}\t{commit.date}\t{commit.milestone}\t{commit.title}\n"


# --- the queries ----------------------------------------------------------------------


def required_milestone(path):
    """A live, gate, or since MILESTONE_PATH, or a milestones --milestone value, as components,
    as named_milestone reads it, an empty one or one with no milestones/ container refused."""
    if not path:
        raise ToolError("the MILESTONE_PATH given is empty")
    components = named_milestone(path)
    if components is None:
        raise ToolError(
            f"the path {path} has no milestones/ container: a milestone path names a directory "
            "directly inside one, read relative to the workspace root"
        )
    return components


def cmd_live(args):
    listed = live_milestones()
    if args.milestone_path is not None:
        components = required_milestone(args.milestone_path)
        own = "/".join(components) + "/"
        scope = components[:-2]
        listed = [
            (directory, requirements)
            for directory, requirements in listed
            if directory != own and overlaps(scope_of(directory), scope)
        ]
    lines = []
    for directory, requirements in listed:
        state = STARTED if is_started(directory) else DEFINED
        lines.append(f"{directory}\t{state}\t{read_title(requirements)}\n")
    sys.stdout.write("".join(lines))
    return 0


def cmd_gate(args):
    path = args.milestone_path
    if is_shallow():
        raise ToolError(
            "the repository is a shallow clone, whose truncated log can read a started milestone "
            "as defined; run git fetch --unshallow and query again"
        )
    components = required_milestone(path)
    own = "/".join(components) + "/"
    scope = components[:-2]
    holders = [
        directory
        for directory, _ in live_milestones()
        if directory != own and overlaps(scope_of(directory), scope) and is_started(directory)
    ]
    sys.stdout.write("".join(directory + "\n" for directory in holders))
    return 0


def cmd_tasks(args):
    path = args.path
    if not path:
        raise ToolError("the PATH given is empty")
    commits = task_commits(path)
    if not commits:
        require_existing(path)
        return 0
    lines = []
    for commit in commits:
        lines.append(task_line(commit))
        if args.with_body:
            lines.extend(BODY_INDENT + line + "\n" for line in body_lines(commit.body))
    sys.stdout.write("".join(lines))
    return 0


def bounded(listed, last):
    """The listed milestones with every live one kept and, when a bound is given, only that many
    of the finished ones, which stand after the live ones newest first."""
    if last is None:
        return listed
    live = [milestone for milestone in listed if milestone.state == LIVE]
    finished = [milestone for milestone in listed if milestone.state != LIVE]
    return live + finished[:last]


def cmd_milestones(args):
    path = args.path
    if args.milestone is not None:
        scope = required_milestone(args.milestone)[:-2]
        path = "/".join(scope) or "."
    listed, _ = listed_milestones(path)
    sys.stdout.write("".join(milestone_line(milestone) for milestone in bounded(listed, args.last)))
    return 0


def whole_number(text):
    """A --last value: a whole number, zero included; anything else is argparse's refusal."""
    if not re.fullmatch(r"[0-9]+", text):
        raise argparse.ArgumentTypeError(f"invalid whole number: {text!r}")
    return int(text)


def resolved_milestone(path):
    """A summary or show MILESTONE_PATH as (live requirements.md path, None) for a live
    milestone or (None, its finish commit) for a finished one; a path naming neither is refused."""
    if not path:
        raise ToolError("the MILESTONE_PATH given is empty")
    live = dict(live_milestones())
    if path in live:
        return live[path], None
    finish = finish_commits().get(path)
    if finish is None:
        raise ToolError(
            f"the path {path} names neither a live milestone nor a finished one "
            "(a milestone path ends in /, as the milestones query prints it)"
        )
    return None, finish


def cmd_summary(args):
    path = args.milestone_path
    requirements, finish = resolved_milestone(path)
    if finish is None:
        milestone = live_milestone(path, requirements)
    else:
        milestone = finished_milestone(path, finish)
    sys.stdout.write("".join(line + "\n" for line in milestone.summary))
    return 0


def cmd_record(args):
    listed, commits = listed_milestones(args.path)
    by_milestone = {}
    for commit in commits:
        by_milestone.setdefault(commit.milestone, []).append(commit)
    lines = []
    for milestone in listed:
        lines.append(milestone_line(milestone))
        lines.extend(BODY_INDENT + line + "\n" for line in trimmed(milestone.summary[2:]))
        lines.extend(BODY_INDENT + task_line(commit) for commit in by_milestone.get(milestone.path, ()))
    sys.stdout.write("".join(lines))
    return 0


def cmd_since(args):
    path = args.milestone_path
    if is_shallow():
        raise ToolError(
            "the repository is a shallow clone, whose truncated log can omit a milestone's "
            "starting state or the commits after it; run git fetch --unshallow and query again"
        )
    components = required_milestone(path)
    own = "/".join(components) + "/"
    anchor = anchor_commit(own)
    if anchor is None:
        return 0
    full_hash, anchor_line = anchor
    lines = [anchor_line] + since_lines(own, components[:-2], full_hash, args.milestones)
    sys.stdout.write("".join(lines))
    return 0


def cmd_show(args):
    path = args.milestone_path
    requirements, finish = resolved_milestone(path)
    if finish is None:
        data = read_bytes(requirements)
    else:
        name = path + DISCOVERY_PATTERN.split("/")[-1]
        data = git(["show", "--no-textconv", finish.full_hash + "^:" + name])
    sys.stdout.flush()
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()
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

    live_parser = subcommands.add_parser(
        "live",
        help="list the live milestones, each with its state and title",
        description=LIVE_DESCRIPTION,
        epilog=LIVE_LIMITS,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    live_parser.add_argument(
        "milestone_path",
        metavar="MILESTONE_PATH",
        nargs="?",
        help=(
            "a milestone directory directly inside a milestones/ container, read relative to the "
            "workspace root, whose overlapping scope's other live milestones alone are listed"
        ),
    )
    live_parser.set_defaults(func=cmd_live)

    gate_parser = subcommands.add_parser(
        "gate",
        help="list the started milestones holding a milestone's scope",
        description=GATE_DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    gate_parser.add_argument(
        "milestone_path",
        metavar="MILESTONE_PATH",
        help=(
            "a milestone directory directly inside a milestones/ container, read relative to the "
            "workspace root"
        ),
    )
    gate_parser.set_defaults(func=cmd_gate)

    tasks_parser = subcommands.add_parser(
        "tasks",
        help="list the task commits that changed PATH",
        description=TASKS_DESCRIPTION,
        epilog=TASKS_LIMITS,
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

    milestones_parser = subcommands.add_parser(
        "milestones",
        help="list the milestones, live and finished, that changed PATH or whose scope overlaps it",
        description=MILESTONES_DESCRIPTION,
        epilog=HISTORY_LIMITS,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    milestones_target = milestones_parser.add_mutually_exclusive_group(required=True)
    milestones_target.add_argument(
        "path",
        metavar="PATH",
        nargs="?",
        help="a file or directory, read by git relative to the working directory",
    )
    milestones_target.add_argument(
        "--milestone",
        metavar="MILESTONE_PATH",
        help=(
            "in place of PATH, a milestone directory directly inside a milestones/ container, read "
            "relative to the workspace root, whose scope's overview is printed"
        ),
    )
    milestones_parser.add_argument(
        "--last",
        metavar="N",
        type=whole_number,
        help="print every live line and only the N newest finished lines",
    )
    milestones_parser.set_defaults(func=cmd_milestones)

    summary_parser = subcommands.add_parser(
        "summary",
        help="print one milestone's summary, its finish date and body or its goal",
        description=SUMMARY_DESCRIPTION,
        epilog=HISTORY_LIMITS,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    summary_parser.add_argument(
        "milestone_path",
        metavar="MILESTONE_PATH",
        help="a milestone path, trailing slash included, as the milestones query prints it",
    )
    summary_parser.set_defaults(func=cmd_summary)

    record_parser = subcommands.add_parser(
        "record",
        help="print the composed record of the work that changed PATH",
        description=RECORD_DESCRIPTION,
        epilog=HISTORY_LIMITS,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    record_parser.add_argument(
        "path",
        metavar="PATH",
        help="a file or directory, read by git relative to the working directory",
    )
    record_parser.set_defaults(func=cmd_record)

    since_parser = subcommands.add_parser(
        "since",
        help="print a milestone's starting-state anchor and the commits around it since",
        description=SINCE_DESCRIPTION,
        epilog=SINCE_LIMITS,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    since_parser.add_argument(
        "milestone_path",
        metavar="MILESTONE_PATH",
        help=(
            "a milestone directory directly inside a milestones/ container, read relative to the "
            "workspace root"
        ),
    )
    since_parser.add_argument(
        "--milestones",
        action="store_true",
        help="list only other milestones' task and finish commits beneath the anchor",
    )
    since_parser.set_defaults(func=cmd_since)

    show_parser = subcommands.add_parser(
        "show",
        help="print one milestone's requirements.md, live or as it stood at its finish",
        description=SHOW_DESCRIPTION,
        epilog=HISTORY_LIMITS,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    show_parser.add_argument(
        "milestone_path",
        metavar="MILESTONE_PATH",
        help="a milestone path, trailing slash included, as the milestones query prints it",
    )
    show_parser.set_defaults(func=cmd_show)
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
