"""Sole writer of a milestone's open_questions.xml, the open-question document.

Usage: python3 <plugin root>/tools/open_questions.py <subcommand> MILESTONE_DIR [...]

Every subcommand takes the already-resolved milestone directory as its first argument and
acts on the one file this module owns inside it, MILESTONE_DIR/open_questions.xml. The
caller resolves the milestone; this module never reads milestones/README.md.

Subcommands:
  create MILESTONE_DIR
      write the empty document, creating the directory when it is missing, and refuse to
      touch an existing document
  list MILESTONE_DIR [--unannotated]
      print the id of every <open-question> block, one per line in document order;
      --unannotated keeps only the blocks carrying no <recommendation> element
  locate MILESTONE_DIR SHORT_TITLE...
      print each named block verbatim, as the document holds it, in the order named
  lift MILESTONE_DIR SHORT_TITLE [--alternative ALTERNATIVE_ID]
      print the block's answer text on one line: "<option> — <rationale>" from its
      <recommendation option="…">, or with --alternative "<id> — <what-it-is>" from the
      named <alternative id="…"> with its <advantage>/<drawback> children excluded
  add MILESTONE_DIR SHORT_TITLE
      append a bare block — the wrapper and its one <question> child — whose id is the
      Short Title and whose question text is the body read from standard input; an id an
      existing block already carries is refused
  strip MILESTONE_DIR SHORT_TITLE...
      delete every child but <question> from each named block — its <alternative>,
      <applied-principle>, <depends-on>, and <recommendation> elements — leaving the
      wrapper and <question> intact; no other block is touched, so a <depends-on> tag that
      names a stripped block stays where it is, and a block already bare is left as it is
  embed MILESTONE_DIR SHORT_TITLE
      put the recommend agent's returned children into the named block, which must carry no
      <recommendation> yet: the agent's whole final message is the body read from standard
      input, the fragment is sliced from its first line holding "<alternative" through its
      last line holding "</recommendation>" (the identity on a clean return, discarding a
      grounding summary or closing remark otherwise), parsed, and validated — no
      <open-question> or <question> line, no text outside its elements, at least one
      <alternative>, exactly one <recommendation> whose option names one of the fragment's
      own alternatives, every <depends-on question="…" option="…"/> resolving one hop to a
      block of the document that carries a <recommendation> and to one of that block's
      <alternative> ids, no element of a kind the format does not define, and never the
      order of its children — then written as the block's children grouped by kind in the
      canonical order; every miss, the two extraction misses included, is one Error line
  remove MILESTONE_DIR SHORT_TITLE [--option RECORDED_OPTION]
      delete the named block and, before the one write, reconcile the blocks that depend on
      it: with --option (the option recorded as the answer, which must be one of the removed
      block's own <alternative> ids or the call is refused with the document unchanged) a
      surviving block whose <depends-on> names the removed id with that same option loses
      only that tag, and every other block whose <depends-on> names the removed id is
      stripped as by strip; without --option every such block is stripped; either way the
      strip runs transitively over the blocks that depend on a stripped block, so no
      <depends-on> tag is left naming a block removed or stripped by the call
  walk MILESTONE_DIR
      print the id of every block carrying a <recommendation>, one per line in the order the
      answer sweep dispatches them: those blocks are gathered in document order, each one's
      <depends-on question="…"> values are edges to the gathered block that id names (an edge
      naming a block that is absent or carries no <recommendation> is dropped, so a block left
      with no edge is an origin), and the blocks are placed origins first, then every block
      whose every edge names a block already placed, same-depth ties in document order, a
      stranded remainder (a cycle) broken by promoting its document-order-first block to an
      origin; a document with no such block prints nothing
  sort MILESTONE_DIR
      rewrite the document with the blocks carrying a <recommendation> first, in exactly the
      order walk prints them, and every block carrying none last, in its prior document
      order — so on a sorted document walk prints exactly the annotated prefix of list; a
      document already in that order is left as it is, and no other subcommand reorders
      blocks

A Short Title names a block by its id, ALTERNATIVE_ID names an alternative by its id, and
RECORDED_OPTION names an alternative by its id too; all are compared against the document's
un-escaped values, case-folded.

A free-text body (the question text of add, the recommend agent's message of embed) travels
on standard input, never as an argument: the tool reads sys.stdin.buffer to end of file
exactly once per call and decodes it as UTF-8 itself, and it refuses a terminal stdin so a
call that forgot to pipe its body (a quoted heredoc, a redirected file) fails instead of
blocking.

Document format, the canonical form every write re-renders the whole document into:
  - a bare <open-questions> root with no XML declaration and no attributes; the empty
    document is that one root element, written self-closing
  - the <open-question> blocks in the order the document already holds them: add appends,
    and only sort reorders
  - one element per line, indented two spaces per depth: the root at column 0, each
    <open-question id="Short Title"> at 2, its children at 4, and inside an alternative
    the what-it-is text, <advantage>, and <drawback> at 6
  - each block's children grouped by kind in the fixed order <question>, the
    <alternative> elements (in their relative order), <applied-principle>, <depends-on>,
    <recommendation>; inside an alternative the what-it-is text, then every <advantage>,
    then every <drawback>
  - every text and attribute value folded to one line: whitespace runs collapsed to one
    space, ends trimmed
  - an element with neither text nor children written self-closing as <tag/>
  - the five predefined entities (&amp; &lt; &gt; &quot; &apos;) substituted in element
    text and attribute values alike
  - UTF-8, LF line ends, one trailing newline

Output and error contract:
  - a read prints only the bare, un-escaped values the caller needs, one per line; an
    empty result set is empty stdout with exit status 0
  - a mutator prints nothing on success
  - every failure is exactly one line "Error: <reason>" on stderr with exit status 1, and
    a non-zero exit leaves the document byte-for-byte unchanged; a malformed invocation
    gets argparse's own usage message and exit status 2; no traceback ever reaches the
    caller

Standard library only; runs on Python 3.9 and later.
"""

import argparse
import os
import re
import stat
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Optional
from xml.parsers import expat

DOCUMENT_NAME = "open_questions.xml"
ROOT_TAG = "open-questions"
BLOCK_TAG = "open-question"
INDENT = "  "


class ToolError(Exception):
    """A failure the caller is told about as one `Error: <reason>` line with exit status 1."""


# --- model ----------------------------------------------------------------------------


@dataclass
class Alternative:
    id: str
    text: str = ""
    advantages: List[str] = field(default_factory=list)
    drawbacks: List[str] = field(default_factory=list)


@dataclass
class Dependency:
    question: str
    option: str


@dataclass
class Recommendation:
    option: str
    rationale: str = ""


@dataclass
class Question:
    id: str
    question: str = ""
    alternatives: List[Alternative] = field(default_factory=list)
    principles: List[str] = field(default_factory=list)
    depends_on: List[Dependency] = field(default_factory=list)
    recommendation: Optional[Recommendation] = None


@dataclass
class Document:
    questions: List[Question] = field(default_factory=list)


# --- text -----------------------------------------------------------------------------


def fold(text):
    """The text as one line: whitespace runs and newlines collapsed to a space, ends trimmed."""
    return " ".join((text or "").split())


def escape(value):
    """The value with the five predefined entities substituted, for text and attributes alike."""
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


# --- parsing --------------------------------------------------------------------------


def parse_document(text):
    """The Document a well-formed open_questions.xml text describes; any shape the model
    does not define is a ToolError naming the offending element."""
    try:
        root = ET.fromstring(text)
    except ET.ParseError as error:
        raise ToolError(f"{DOCUMENT_NAME} is not well-formed XML: {error}")
    if root.tag != ROOT_TAG:
        raise ToolError(f"{DOCUMENT_NAME} has a <{root.tag}> root, not <{ROOT_TAG}>")
    _attributes(root, (), f"<{ROOT_TAG}>")
    _no_text(root.text, f"<{ROOT_TAG}>")

    document = Document()
    seen = set()
    for child in root:
        if child.tag != BLOCK_TAG:
            raise ToolError(f"<{ROOT_TAG}> carries an unexpected <{child.tag}> element")
        question = _parse_question(child)
        key = question.id.casefold()
        if key in seen:
            raise ToolError(f'two <{BLOCK_TAG}> blocks carry the id "{question.id}"')
        seen.add(key)
        document.questions.append(question)
        _no_text(child.tail, f"<{ROOT_TAG}>")
    return document


def _parse_question(elem):
    (block_id,) = _attributes(elem, ("id",), f"an <{BLOCK_TAG}> element")
    context = f'<{BLOCK_TAG} id="{block_id}">'
    _no_text(elem.text, context)

    question = Question(id=block_id)
    question_texts = _parse_children(elem, context, question)
    if not question_texts:
        raise ToolError(f"{context} has no <question> element")
    if len(question_texts) > 1:
        raise ToolError(f"{context} carries {len(question_texts)} <question> elements")
    question.question = question_texts[0]
    return question


def _parse_children(elem, context, question):
    """Fill the block's alternatives, applied principles, depends-on tags, and recommendation
    from the element's children in document order — the walk a block of the document and the
    recommend agent's fragment share — and return the texts of its <question> children for the
    caller to judge; a child the format does not define, text between the children, a repeated
    alternative id, or a second <recommendation> is a ToolError."""
    question_texts = []
    recommendations = []
    alternative_ids = set()
    for child in elem:
        if child.tag == "question":
            _attributes(child, (), f"the <question> element of {context}")
            question_texts.append(_leaf_text(child, f"the <question> element of {context}"))
        elif child.tag == "alternative":
            alternative = _parse_alternative(child, context)
            key = alternative.id.casefold()
            if key in alternative_ids:
                raise ToolError(f'{context} carries two <alternative> elements with the id "{alternative.id}"')
            alternative_ids.add(key)
            question.alternatives.append(alternative)
        elif child.tag == "applied-principle":
            _attributes(child, (), f"an <applied-principle> element of {context}")
            question.principles.append(_leaf_text(child, f"an <applied-principle> element of {context}"))
        elif child.tag == "depends-on":
            target, option = _attributes(child, ("question", "option"), f"a <depends-on> element of {context}")
            if _leaf_text(child, f"a <depends-on> element of {context}"):
                raise ToolError(f"a <depends-on> element of {context} carries text")
            question.depends_on.append(Dependency(question=target, option=option))
        elif child.tag == "recommendation":
            (option,) = _attributes(child, ("option",), f"the <recommendation> element of {context}")
            rationale = _leaf_text(child, f"the <recommendation> element of {context}")
            recommendations.append(Recommendation(option=option, rationale=rationale))
        else:
            raise ToolError(f"{context} carries an unexpected <{child.tag}> element")
        _no_text(child.tail, context)

    if len(recommendations) > 1:
        raise ToolError(f"{context} carries {len(recommendations)} <recommendation> elements")
    if recommendations:
        question.recommendation = recommendations[0]
    return question_texts


def _parse_alternative(elem, block_context):
    (alternative_id,) = _attributes(elem, ("id",), f"an <alternative> element of {block_context}")
    context = f'<alternative id="{alternative_id}"> of {block_context}'
    alternative = Alternative(id=alternative_id)
    # The what-it-is text is every run of text directly inside the alternative, wherever it
    # sits among the children, folded and joined; grouping by kind puts it first on write.
    pieces = [fold(elem.text)]
    for child in elem:
        if child.tag == "advantage":
            _attributes(child, (), f"an <advantage> element of {context}")
            alternative.advantages.append(_leaf_text(child, f"an <advantage> element of {context}"))
        elif child.tag == "drawback":
            _attributes(child, (), f"a <drawback> element of {context}")
            alternative.drawbacks.append(_leaf_text(child, f"a <drawback> element of {context}"))
        else:
            raise ToolError(f"{context} carries an unexpected <{child.tag}> element")
        pieces.append(fold(child.tail))
    alternative.text = " ".join(piece for piece in pieces if piece)
    return alternative


def _attributes(elem, names, context):
    """The folded values of exactly the named attributes, in that order; an attribute the
    model does not define, a missing one, or an empty one is a ToolError."""
    unknown = sorted(set(elem.attrib) - set(names))
    if unknown:
        raise ToolError(f'{context} carries an unknown attribute "{unknown[0]}"')
    values = []
    for name in names:
        if name not in elem.attrib:
            raise ToolError(f"{context} has no {name} attribute")
        value = fold(elem.attrib[name])
        if not value:
            raise ToolError(f"{context} has an empty {name} attribute")
        values.append(value)
    return values


def _leaf_text(elem, context):
    """The folded text of an element that holds text only."""
    for child in elem:
        raise ToolError(f"{context} carries an unexpected <{child.tag}> element")
    return fold(elem.text)


def _no_text(text, context):
    if fold(text):
        raise ToolError(f"{context} carries text outside its child elements")


# --- rendering ------------------------------------------------------------------------


def render_document(document):
    """The canonical text of the document: the same Document always renders the same bytes."""
    children = []
    for question in document.questions:
        children.extend(_question_lines(question, 1))
    return "\n".join(_element_lines(0, ROOT_TAG, (), "", children)) + "\n"


def _question_lines(question, depth):
    children = _element_lines(depth + 1, "question", (), question.question, ())
    for alternative in question.alternatives:
        body = []
        for advantage in alternative.advantages:
            body.extend(_element_lines(depth + 2, "advantage", (), advantage, ()))
        for drawback in alternative.drawbacks:
            body.extend(_element_lines(depth + 2, "drawback", (), drawback, ()))
        children.extend(
            _element_lines(depth + 1, "alternative", (("id", alternative.id),), alternative.text, body, text_inline=False)
        )
    for principle in question.principles:
        children.extend(_element_lines(depth + 1, "applied-principle", (), principle, ()))
    for dependency in question.depends_on:
        attributes = (("question", dependency.question), ("option", dependency.option))
        children.extend(_element_lines(depth + 1, "depends-on", attributes, "", ()))
    if question.recommendation is not None:
        attributes = (("option", question.recommendation.option),)
        children.extend(_element_lines(depth + 1, "recommendation", attributes, question.recommendation.rationale, ()))
    return _element_lines(depth, BLOCK_TAG, (("id", question.id),), "", children)


def _element_lines(depth, tag, attributes, text, children, text_inline=True):
    """The lines of one element at the given depth: self-closing when it holds nothing, one
    line when it holds inline text only, otherwise its start tag, its text on a line of its
    own, its already-rendered children, and its end tag."""
    indent = INDENT * depth
    start = " ".join([tag] + [f'{name}="{escape(value)}"' for name, value in attributes])
    if not text and not children:
        return [f"{indent}<{start}/>"]
    if text_inline and not children:
        return [f"{indent}<{start}>{escape(text)}</{tag}>"]
    lines = [f"{indent}<{start}>"]
    if text:
        lines.append(f"{INDENT * (depth + 1)}{escape(text)}")
    lines.extend(children)
    lines.append(f"{indent}</{tag}>")
    return lines


# --- the file -------------------------------------------------------------------------


def document_path(milestone_dir):
    return os.path.join(milestone_dir, DOCUMENT_NAME)


def load_document(milestone_dir):
    """The parsed document of a milestone directory."""
    path = document_path(milestone_dir)
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except FileNotFoundError:
        raise ToolError(f"{path} does not exist")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise ToolError(f"{path} is not UTF-8 text")
    return parse_document(text)


def save_document(milestone_dir, document):
    """Write the document's canonical form as the milestone's one file, replacing it whole."""
    _write_bytes(document_path(milestone_dir), render_document(document).encode("utf-8"))


def _write_bytes(path, data):
    """Write data to path through a temporary file in the same directory renamed over the
    target, so a failure part-way leaves any existing document byte-for-byte unchanged; the
    file keeps the target's mode, or takes the default mode when it is new."""
    directory = os.path.dirname(path) or os.curdir
    descriptor, temporary = tempfile.mkstemp(prefix=f".{DOCUMENT_NAME}.", suffix=".tmp", dir=directory)
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


# --- lookups --------------------------------------------------------------------------


def id_key(value):
    """The comparison form of an id: the un-escaped value, whitespace-folded and case-folded."""
    return fold(value).casefold()


def _quoted(values):
    return ", ".join(f'"{value}"' for value in values)


def find_question(document, short_title):
    """The block whose id matches the Short Title; none matching is a ToolError that names
    the ids the document does hold."""
    wanted = id_key(short_title)
    for question in document.questions:
        if id_key(question.id) == wanted:
            return question
    held = _quoted(question.id for question in document.questions) or "no blocks"
    raise ToolError(f'no <{BLOCK_TAG}> block has the id "{short_title}"; the document holds {held}')


def find_questions(document, short_titles):
    """The blocks the Short Titles name, once each in the order first named; every title is
    resolved before anything is returned, so one unknown title fails the whole lookup."""
    questions = []
    seen = set()
    for short_title in short_titles:
        question = find_question(document, short_title)
        if id_key(question.id) not in seen:
            seen.add(id_key(question.id))
            questions.append(question)
    return questions


def find_alternative(question, alternative_id):
    """The block's alternative whose id matches; none matching is a ToolError that names the
    ids the block does carry."""
    wanted = id_key(alternative_id)
    for alternative in question.alternatives:
        if id_key(alternative.id) == wanted:
            return alternative
    context = f'<{BLOCK_TAG} id="{question.id}">'
    if not question.alternatives:
        raise ToolError(f"{context} carries no <alternative> elements")
    held = _quoted(alternative.id for alternative in question.alternatives)
    raise ToolError(f'{context} has no <alternative> with the id "{alternative_id}"; its alternatives are {held}')


# --- per-block edits ------------------------------------------------------------------


def is_bare(question):
    """Whether the block holds nothing but its <question>."""
    return not (
        question.alternatives or question.principles or question.depends_on or question.recommendation is not None
    )


def strip_question(question):
    """Delete every child of the block but its <question> — the <alternative>,
    <applied-principle>, <depends-on>, and <recommendation> elements — leaving the wrapper
    and <question> intact and touching no other block. The one per-block primitive behind
    the strip subcommand and the transitive strip of dependent reconciliation; returns
    whether anything was deleted, so a block already bare reports no change."""
    if is_bare(question):
        return False
    question.alternatives = []
    question.principles = []
    question.depends_on = []
    question.recommendation = None
    return True


# --- removal and dependent reconciliation ---------------------------------------------


def dependents_of(document, block_id):
    """The blocks carrying a <depends-on> tag whose question names the given id (compared
    un-escaped and case-folded), in document order."""
    wanted = id_key(block_id)
    return [
        question
        for question in document.questions
        if any(id_key(dependency.question) == wanted for dependency in question.depends_on)
    ]


def check_recorded_option(question, recorded_option):
    """A ToolError unless the recorded option is one of the block's own <alternative> ids,
    compared un-escaped and case-folded: a mistyped option must fail loudly with the
    document unchanged rather than strip every dependent silently."""
    context = f'<{BLOCK_TAG} id="{question.id}">'
    if not question.alternatives:
        raise ToolError(f'--option "{recorded_option}" was given, but {context} carries no <alternative> elements')
    wanted = id_key(recorded_option)
    if not any(id_key(alternative.id) == wanted for alternative in question.alternatives):
        held = _quoted(alternative.id for alternative in question.alternatives)
        raise ToolError(f'--option "{recorded_option}" names none of the <alternative> ids of {context}, which are {held}')


def remove_question(document, question, recorded_option=None):
    """Delete the block from the document and reconcile every block that depends on it, all
    on the parsed tree so the caller writes once. With a recorded option — one of the removed
    block's own alternative ids, as check_recorded_option has confirmed — a dependent whose
    every <depends-on> tag naming the removed block carries that same option (compared
    un-escaped and case-folded) loses just those tags and keeps its other children, and every
    other dependent is stripped as strip_question strips; without one every dependent is
    stripped. The strip is transitive: a block whose <depends-on> names a block stripped here
    is stripped in turn, until no tag names a block removed or stripped by this call. A tag
    naming any other block is left as it is. Returns the ids of the blocks stripped, in the
    order they were stripped."""
    document.questions = [other for other in document.questions if other is not question]
    removed = id_key(question.id)
    recorded = None if recorded_option is None else id_key(recorded_option)

    pending = []
    for dependent in dependents_of(document, question.id):
        tags = [dependency for dependency in dependent.depends_on if id_key(dependency.question) == removed]
        if recorded is not None and all(id_key(tag.option) == recorded for tag in tags):
            dependent.depends_on = [dependency for dependency in dependent.depends_on if id_key(dependency.question) != removed]
        else:
            pending.append(dependent)

    stripped = []
    seen = set()
    while pending:
        block = pending.pop(0)
        if id_key(block.id) in seen:
            continue
        seen.add(id_key(block.id))
        strip_question(block)
        stripped.append(block.id)
        pending.extend(dependents_of(document, block.id))
    return stripped


# --- the answer sweep's dispatch order ------------------------------------------------


def walk_order(document):
    """The blocks carrying a <recommendation>, in the order the answer sweep dispatches them.
    Gathered in document order, each block's <depends-on question="…"> values are edges to the
    gathered block that id names (compared un-escaped and case-folded; the option is not read),
    and an edge naming a block that is absent or carries no <recommendation> is dropped — this
    sweep never answers that block, so a block left with no edge is an ordinary origin. The
    walk places the origins first in document order, then, repeatedly, every unplaced block
    whose every edge names a placed block, in document order among themselves, so a target
    always precedes its dependents; when blocks remain but each waits on another of them (a
    <depends-on> cycle), the document-order-first remaining block is promoted to an origin and
    the walk goes on. Deterministic and total: every gathered block is placed exactly once."""
    gathered = [question for question in document.questions if question.recommendation is not None]
    annotated = {id_key(question.id) for question in gathered}
    edges = {
        id_key(question.id): {id_key(dependency.question) for dependency in question.depends_on} & annotated
        for question in gathered
    }
    placed = set()
    order = []
    remaining = gathered
    while remaining:
        ready = [question for question in remaining if edges[id_key(question.id)] <= placed]
        if not ready:
            ready = remaining[:1]
        for question in ready:
            order.append(question)
            placed.add(id_key(question.id))
        remaining = [question for question in remaining if id_key(question.id) not in placed]
    return order


# --- the sorted document ---------------------------------------------------------------


def sort_order(document):
    """Every block of the document in the order sort writes them: the blocks carrying a
    <recommendation> first, in exactly the order walk_order places them, then every block
    carrying none, in its document order. A permutation of document.questions, so on a
    document already in this order walk prints exactly the annotated prefix of list."""
    return walk_order(document) + [question for question in document.questions if question.recommendation is None]


# --- the recommend agent's fragment ---------------------------------------------------

FRAGMENT = "the fragment"
FRAGMENT_TAG = "fragment"
# A start or end tag of the wrapper or of <question>, by name and a boundary after it.
_BLOCK_TAG_LINE = re.compile(rf"</?({BLOCK_TAG}|question)(?=[\s/>])")


def extract_fragment(message):
    """The fragment inside the recommend agent's whole final message: its lines from the first
    line holding "<alternative" through the last line holding "</recommendation>", joined —
    the identity on a clean return, the discarding of a grounding summary above or a closing
    remark below otherwise. A message missing either anchor line is a ToolError naming it."""
    lines = message.splitlines()
    starts = [index for index, line in enumerate(lines) if "<alternative" in line]
    ends = [index for index, line in enumerate(lines) if "</recommendation>" in line]
    if not starts:
        raise ToolError("no <alternative> line to extract from")
    if not ends:
        raise ToolError("no </recommendation> line to extract to")
    start, end = starts[0], ends[-1]
    if end < start:
        raise ToolError("the last </recommendation> line precedes the first <alternative> line")
    return "\n".join(lines[start : end + 1])


def parse_fragment(region):
    """The children an extracted fragment describes, as a Question with no id and no question
    text, once the fragment is well-formed and valid: no <open-question> or <question> line,
    no text outside its elements, at least one <alternative>, exactly one <recommendation>
    whose option names one of the fragment's own alternatives, and no element of a kind the
    format does not define. The order of the children is not checked — the writer groups them
    by kind — and a <depends-on> tag is checked against the document by check_dependencies."""
    for line in region.splitlines():
        found = _BLOCK_TAG_LINE.search(line)
        if found:
            tag = found.group(0) + ">"
            article = "an" if tag.startswith("<o") else "a"
            raise ToolError(
                f"{FRAGMENT} contains {article} {tag} line; the <{BLOCK_TAG}> wrapper and its "
                f"<question> element belong to the document, not to the fragment"
            )
    try:
        root = ET.fromstring(f"<{FRAGMENT_TAG}>\n{region}\n</{FRAGMENT_TAG}>")
    except ET.ParseError as error:
        raise ToolError(f"{FRAGMENT} is not well-formed XML: {_parse_error_text(error)}")

    children = list(root)
    if fold(root.text):
        raise ToolError(f"text precedes <alternative> on {FRAGMENT}'s opening line")
    if children and fold(children[-1].tail):
        raise ToolError(f"text trails </recommendation> on {FRAGMENT}'s closing line")
    if any(fold(child.tail) for child in children[:-1]):
        raise ToolError(f"{FRAGMENT} carries text between its elements")

    fragment = Question(id="")
    if _parse_children(root, FRAGMENT, fragment):
        raise ToolError(f"{FRAGMENT} contains a <question> element")
    if not fragment.alternatives:
        raise ToolError(f"{FRAGMENT} contains no <alternative> element")
    if fragment.recommendation is None:
        raise ToolError(f"{FRAGMENT} contains no <recommendation> element")
    wanted = id_key(fragment.recommendation.option)
    if not any(id_key(alternative.id) == wanted for alternative in fragment.alternatives):
        held = _quoted(alternative.id for alternative in fragment.alternatives)
        raise ToolError(
            f'the <recommendation> option "{fragment.recommendation.option}" names none of '
            f"{FRAGMENT}'s <alternative> ids, which are {held}"
        )
    return fragment


def _parse_error_text(error):
    """The parser's reason with its line counted from the fragment's own first line (the parse
    wraps the fragment in a root element on the line above it)."""
    line, column = error.position
    reason = expat.errors.messages.get(getattr(error, "code", None), "syntax error")
    return f"{reason} at line {line - 1}, column {column}"


def check_dependencies(document, question, fragment):
    """A ToolError unless every <depends-on> tag of the fragment resolves one hop: its question
    names a block of the document other than the one being embedded that carries a
    <recommendation>, and its option is one of that block's own <alternative> ids — both
    compared un-escaped and case-folded. The target's own tags are not followed and no cycle
    is looked for."""
    annotated = [other for other in document.questions if other is not question and other.recommendation is not None]
    for dependency in fragment.depends_on:
        wanted = id_key(dependency.question)
        target = next((other for other in annotated if id_key(other.id) == wanted), None)
        if target is None:
            held = _quoted(other.id for other in annotated)
            held = f"the annotated blocks are {held}" if held else "no other block carries one"
            raise ToolError(
                f'the <depends-on question="{dependency.question}"/> names no block that carries a '
                f"<recommendation>; {held}"
            )
        option = id_key(dependency.option)
        if not any(id_key(alternative.id) == option for alternative in target.alternatives):
            held = _quoted(alternative.id for alternative in target.alternatives)
            raise ToolError(
                f'the <depends-on question="{dependency.question}" option="{dependency.option}"/> names '
                f"none of that block's <alternative> ids, which are {held}"
            )


def embed_fragment(document, question, fragment):
    """Make the fragment's children the block's children — its alternatives in their returned
    order, applied principles, depends-on tags, and recommendation — once every <depends-on>
    tag resolves against the document; the caller writes, and the writer groups them by kind."""
    check_dependencies(document, question, fragment)
    question.alternatives = list(fragment.alternatives)
    question.principles = list(fragment.principles)
    question.depends_on = list(fragment.depends_on)
    question.recommendation = fragment.recommendation


# --- subcommands ----------------------------------------------------------------------


def cmd_create(args):
    path = document_path(args.milestone_dir)
    if os.path.lexists(path):
        raise ToolError(f"{path} already exists")
    os.makedirs(args.milestone_dir, exist_ok=True)
    save_document(args.milestone_dir, Document())
    return 0


def cmd_list(args):
    document = load_document(args.milestone_dir)
    for question in document.questions:
        if args.unannotated and question.recommendation is not None:
            continue
        print(question.id)
    return 0


def cmd_locate(args):
    document = load_document(args.milestone_dir)
    for question in find_questions(document, args.short_titles):
        # The document is always the serializer's own output, so the block's canonical
        # lines at its depth inside the root are the very lines the file holds.
        for line in _question_lines(question, 1):
            print(line)
    return 0


def cmd_lift(args):
    document = load_document(args.milestone_dir)
    question = find_question(document, args.short_title)
    if args.alternative is None:
        if question.recommendation is None:
            raise ToolError(f'<{BLOCK_TAG} id="{question.id}"> carries no <recommendation> element')
        head, body = question.recommendation.option, question.recommendation.rationale
    else:
        alternative = find_alternative(question, args.alternative)
        head, body = alternative.id, alternative.text
    print(" — ".join(part for part in (head, body) if part))
    return 0


def cmd_add(args):
    short_title = fold(args.short_title)
    if not short_title:
        raise ToolError("the Short Title is empty")
    document = load_document(args.milestone_dir)
    wanted = id_key(short_title)
    for question in document.questions:
        if id_key(question.id) == wanted:
            raise ToolError(f'an <{BLOCK_TAG}> block with the id "{question.id}" already exists')
    text = fold(read_body("the question text"))
    if not text:
        raise ToolError("the question text on standard input is empty")
    document.questions.append(Question(id=short_title, question=text))
    save_document(args.milestone_dir, document)
    return 0


def cmd_strip(args):
    document = load_document(args.milestone_dir)
    changed = False
    for question in find_questions(document, args.short_titles):
        changed = strip_question(question) or changed
    if changed:
        save_document(args.milestone_dir, document)
    return 0


def cmd_embed(args):
    document = load_document(args.milestone_dir)
    question = find_question(document, args.short_title)
    if question.recommendation is not None:
        raise ToolError(
            f'<{BLOCK_TAG} id="{question.id}"> already carries a <recommendation> element; strip it first to embed a new one'
        )
    fragment = parse_fragment(extract_fragment(read_body("the recommend agent's message")))
    embed_fragment(document, question, fragment)
    save_document(args.milestone_dir, document)
    return 0


def cmd_remove(args):
    document = load_document(args.milestone_dir)
    question = find_question(document, args.short_title)
    if args.option is not None:
        check_recorded_option(question, args.option)
    remove_question(document, question, args.option)
    save_document(args.milestone_dir, document)
    return 0


def cmd_walk(args):
    document = load_document(args.milestone_dir)
    for question in walk_order(document):
        print(question.id)
    return 0


def cmd_sort(args):
    document = load_document(args.milestone_dir)
    ordered = sort_order(document)
    if any(placed is not held for placed, held in zip(ordered, document.questions)):
        document.questions = ordered
        save_document(args.milestone_dir, document)
    return 0


# --- command line ---------------------------------------------------------------------


def build_parser():
    parser = argparse.ArgumentParser(
        prog="open_questions.py",
        description="Read and write a milestone's open_questions.xml, the one file this tool owns.",
    )
    subcommands = parser.add_subparsers(dest="subcommand", metavar="<subcommand>", required=True)

    def add_subcommand(name, func, help_text):
        subparser = subcommands.add_parser(name, help=help_text, description=help_text)
        subparser.add_argument(
            "milestone_dir",
            metavar="MILESTONE_DIR",
            help="the resolved milestone directory holding (or to hold) open_questions.xml",
        )
        subparser.set_defaults(func=func)
        return subparser

    add_subcommand(
        "create",
        cmd_create,
        "write the empty document into MILESTONE_DIR, creating the directory when it is "
        "missing; an existing document is refused and left untouched",
    )

    list_parser = add_subcommand(
        "list",
        cmd_list,
        "print the id of every <open-question> block, one per line in document order; an "
        "empty document prints nothing",
    )
    list_parser.add_argument(
        "--unannotated",
        action="store_true",
        help="print only the blocks carrying no <recommendation> element",
    )

    locate_parser = add_subcommand(
        "locate",
        cmd_locate,
        "print each named block verbatim, as the document holds it, in the order named",
    )
    locate_parser.add_argument(
        "short_titles",
        metavar="SHORT_TITLE",
        nargs="+",
        help="the id of a block, compared un-escaped and case-folded",
    )

    lift_parser = add_subcommand(
        "lift",
        cmd_lift,
        "print the block's answer text on one line: \"<option> — <rationale>\" from its "
        "<recommendation>, or with --alternative \"<id> — <what-it-is>\" from the named "
        "<alternative>, its <advantage> and <drawback> children excluded",
    )
    lift_parser.add_argument(
        "short_title",
        metavar="SHORT_TITLE",
        help="the id of the block, compared un-escaped and case-folded",
    )
    lift_parser.add_argument(
        "--alternative",
        metavar="ALTERNATIVE_ID",
        help="lift the named <alternative> of the block instead of its <recommendation>",
    )

    add_parser = add_subcommand(
        "add",
        cmd_add,
        "append a bare block whose id is SHORT_TITLE and whose <question> text is the body "
        "read from standard input as UTF-8 (pipe it as a quoted heredoc; a terminal stdin "
        "is refused); an id an existing block already carries is refused",
    )
    add_parser.add_argument(
        "short_title",
        metavar="SHORT_TITLE",
        help="the id of the new block, compared un-escaped and case-folded against the existing ids",
    )

    strip_parser = add_subcommand(
        "strip",
        cmd_strip,
        "delete every child but <question> from each named block, leaving the wrapper and "
        "<question> intact and every other block, <depends-on> tags naming it included, "
        "untouched; a block already bare is left as it is",
    )
    strip_parser.add_argument(
        "short_titles",
        metavar="SHORT_TITLE",
        nargs="+",
        help="the id of a block, compared un-escaped and case-folded",
    )

    embed_parser = add_subcommand(
        "embed",
        cmd_embed,
        "put the recommend agent's returned children into the named block, which must carry no "
        "<recommendation> yet: the agent's whole final message is read from standard input "
        "(pipe it as a quoted heredoc; a terminal stdin is refused), the fragment is sliced from "
        "its first <alternative line through its last </recommendation> line, parsed, validated "
        "(no <open-question> or <question> line, no text outside the elements, at least one "
        "<alternative>, exactly one <recommendation> naming one of them, every <depends-on> "
        "resolving to an annotated block and one of its <alternative> ids, no unknown element; "
        "child order is not checked), and written grouped by kind; every miss is one Error line",
    )
    embed_parser.add_argument(
        "short_title",
        metavar="SHORT_TITLE",
        help="the id of the block, compared un-escaped and case-folded",
    )

    remove_parser = add_subcommand(
        "remove",
        cmd_remove,
        "delete the named block and, in the same write, reconcile the blocks that depend on "
        "it: with --option, a dependent whose <depends-on> names the block with that same "
        "option loses only that tag and every other dependent is stripped as by strip; "
        "without it every dependent is stripped; both transitively over the dependents of a "
        "stripped block, so no <depends-on> tag is left naming a removed or stripped block",
    )
    remove_parser.add_argument(
        "short_title",
        metavar="SHORT_TITLE",
        help="the id of the block, compared un-escaped and case-folded",
    )
    remove_parser.add_argument(
        "--option",
        metavar="RECORDED_OPTION",
        help="the option recorded as the block's answer, one of its own <alternative> ids "
        "(compared un-escaped and case-folded); any other value is refused with the document "
        "unchanged",
    )

    add_subcommand(
        "walk",
        cmd_walk,
        "print the id of every block carrying a <recommendation>, one per line in the answer "
        "sweep's dispatch order: the blocks a block's <depends-on> tags name among them precede "
        "it (a tag naming an absent or recommendation-less block is ignored), same-depth ties "
        "fall in document order, and a cycle is broken by promoting its document-order-first "
        "block to an origin; a document with no such block prints nothing",
    )

    add_subcommand(
        "sort",
        cmd_sort,
        "rewrite the document with the blocks carrying a <recommendation> first, in exactly "
        "the order walk prints them, and every block carrying none last, in its prior document "
        "order, so that walk then prints the annotated prefix of list; a document already in "
        "that order is left as it is",
    )
    return parser


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
