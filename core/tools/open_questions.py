"""Sole writer of a milestone's open_questions.xml, the open-question document.

Usage: python3 <plugin root>/tools/open_questions.py <subcommand> MILESTONE_DIR [...]

Every subcommand takes the already-resolved milestone directory as its first argument and
acts on the one file this module owns inside it, MILESTONE_DIR/open_questions.xml. The
caller resolves the milestone; this module never reads milestones/README.md.

Subcommands:
  create MILESTONE_DIR
      write the empty document, creating the directory when it is missing, and refuse to
      touch an existing document
  list MILESTONE_DIR [--without-alternatives] [--without-recommendation]
      print the id of every <open-question> block, one per line in document order;
      --without-alternatives keeps only the blocks carrying no <alternative> element and
      --without-recommendation only the blocks carrying no <recommendation> element, a
      block printed under both flags only when it carries neither
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
  strip MILESTONE_DIR [--recommendation] SHORT_TITLE...
      delete every child but <question> from each named block — its <alternative>,
      <applied-principle>, <depends-on>, and <recommendation> elements — leaving the
      wrapper and <question> intact; with --recommendation delete only the <recommendation>,
      <depends-on>, and <applied-principle> elements and leave the <alternative> elements
      standing; either way no other block is touched, so a <depends-on> tag that names a
      stripped block stays where it is, and a block holding nothing the call would delete is
      left as it is
  embed MILESTONE_DIR SHORT_TITLE (--alternatives | --recommendation)
      put one half of a block's children into the named block, the half the required flag
      names: the whole message carrying them is the body read from standard input, the
      fragment is sliced out of it (the identity on a clean message, discarding a grounding
      summary or closing remark otherwise), parsed, validated — no <open-question> or
      <question> line, no text outside its elements, no element of a kind the format does
      not define, no element of the other half, and never the order of its children — and
      written as that half of the block's children, the other half's elements left exactly
      as the block holds them and the whole block placed in the canonical child order the
      document format below states; every miss, the two extraction misses included, is one
      Error line. With --alternatives the block must carry no
      <alternative> yet (bare strip is the hatch), the slice runs from the first line
      holding "<alternative" through the last line holding "</alternative>", and the
      fragment must hold at least one <alternative>. With --recommendation the block must
      already carry at least one <alternative> and no <recommendation> yet (strip
      --recommendation is the hatch), the slice runs from the first line holding
      "<applied-principle", "<depends-on", or "<recommendation" through the last line
      holding "</recommendation>", the fragment must hold exactly one <recommendation> whose
      option names one of the block's own <alternative> ids, and every
      <depends-on question="…" option="…"/> must resolve one hop to another block of the
      document that carries <alternative> elements and to one of that block's <alternative>
      ids — so the alternative set the first shape embedded stays frozen under the second
  remove MILESTONE_DIR SHORT_TITLE [--option RECORDED_OPTION]
      delete the named block and, before the one write, reconcile the blocks that depend on
      it: with --option (the option recorded as the answer, which must be one of the removed
      block's own <alternative> ids or the call is refused with the document unchanged) a
      surviving block whose <depends-on> names the removed id with that same option loses
      only that tag, and every other block whose <depends-on> names the removed id is
      stripped as by strip --recommendation, keeping its <alternative> elements; without
      --option every such block is so stripped; either way the strip runs transitively over
      the blocks that depend on a stripped block, so no <depends-on> tag is left naming a
      block removed or stripped by the call
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

A free-text body (the question text of add, the message embed slices its fragment from) travels
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
  - each block's children grouped by kind: a block carrying a <recommendation> in the
    order <question>, <applied-principle>, <depends-on>, <recommendation>, the one
    <alternative> whose id the recommendation's option names, then the other <alternative>
    elements in their relative order — an option naming none of them promotes nothing, the
    alternatives keeping their relative order after the recommendation; a block carrying
    none in the order <question>, the <alternative> elements (in their relative order),
    <applied-principle>, <depends-on>; the order written is the alternatives' relative order
    from then on, so a later strip --recommendation keeps it; inside an alternative the
    what-it-is text, then every <advantage>, then every <drawback>
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
    from the element's children in document order — the walk a block of the document and an
    embed fragment share — and return the texts of its <question> children for the
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
    """The lines of one block. A block carrying a <recommendation> renders its recommendation
    half first, then the alternative its option names, then the rest in their relative order;
    a block without one renders its alternatives before the other three kinds."""
    children = _element_lines(depth + 1, "question", (), question.question, ())
    if question.recommendation is None:
        children.extend(_alternatives_lines(question.alternatives, depth + 1))
        children.extend(_recommendation_half_lines(question, depth + 1))
    else:
        children.extend(_recommendation_half_lines(question, depth + 1))
        children.extend(_alternatives_lines(_promoted(question.alternatives, question.recommendation.option), depth + 1))
    return _element_lines(depth, BLOCK_TAG, (("id", question.id),), "", children)


def _promoted(alternatives, option):
    """The alternatives with the one whose id the option names moved to the front and the
    rest in their relative order; an option naming none of them moves nothing."""
    wanted = id_key(option)
    named = [alternative for alternative in alternatives if id_key(alternative.id) == wanted]
    return named + [alternative for alternative in alternatives if id_key(alternative.id) != wanted]


def _alternatives_lines(alternatives, depth):
    lines = []
    for alternative in alternatives:
        body = []
        for advantage in alternative.advantages:
            body.extend(_element_lines(depth + 1, "advantage", (), advantage, ()))
        for drawback in alternative.drawbacks:
            body.extend(_element_lines(depth + 1, "drawback", (), drawback, ()))
        lines.extend(_element_lines(depth, "alternative", (("id", alternative.id),), alternative.text, body, text_inline=False))
    return lines


def _recommendation_half_lines(question, depth):
    """The block's <applied-principle>, <depends-on>, and <recommendation> lines, in that order."""
    lines = []
    for principle in question.principles:
        lines.extend(_element_lines(depth, "applied-principle", (), principle, ()))
    for dependency in question.depends_on:
        attributes = (("question", dependency.question), ("option", dependency.option))
        lines.extend(_element_lines(depth, "depends-on", attributes, "", ()))
    if question.recommendation is not None:
        attributes = (("option", question.recommendation.option),)
        lines.extend(_element_lines(depth, "recommendation", attributes, question.recommendation.rationale, ()))
    return lines


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


def strip_recommendation(question):
    """Delete the block's <recommendation>, <depends-on>, and <applied-principle> elements —
    the recommendation half — leaving its <alternative> elements, wrapper, and <question>
    intact and touching no other block. The one per-block primitive behind strip
    --recommendation and the partial strip of dependent reconciliation; returns whether
    anything was deleted, so a block carrying none of the three reports no change."""
    if not (question.principles or question.depends_on or question.recommendation is not None):
        return False
    question.principles = []
    question.depends_on = []
    question.recommendation = None
    return True


def strip_question(question):
    """Delete every child of the block but its <question> — the <alternative> elements on top
    of everything strip_recommendation deletes — leaving the wrapper and <question> intact
    and touching no other block. The per-block primitive behind bare strip; returns whether
    anything was deleted, so a block already bare reports no change."""
    changed = strip_recommendation(question)
    if question.alternatives:
        question.alternatives = []
        changed = True
    return changed


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
    other dependent is stripped as strip_recommendation strips — its <recommendation>,
    <depends-on>, and <applied-principle> children deleted, its <alternative> children kept
    for the recommendation pass to re-pick over; without one every dependent is so stripped.
    The strip is transitive: a block whose <depends-on> names a block stripped here is
    stripped in turn, until no tag names a block removed or stripped by this call. A tag
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
        strip_recommendation(block)
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


# --- the two embed shapes and their fragment ------------------------------------------

FRAGMENT = "the fragment"
FRAGMENT_TAG = "fragment"
# A start or end tag of the wrapper or of <question>, by name and a boundary after it.
_BLOCK_TAG_LINE = re.compile(rf"</?({BLOCK_TAG}|question)(?=[\s/>])")
# Every child kind a block's fragment half may carry, across both shapes.
CHILD_KINDS = ("alternative", "applied-principle", "depends-on", "recommendation")


@dataclass(frozen=True)
class Shape:
    """One of the two halves embed puts into a block, named by the flag that selects it: the
    child kinds the half holds, and the one kind among them the fragment must hold — whose
    end tag also closes the slice extract_fragment takes out of the message."""

    flag: str
    kinds: tuple
    required: str

    @property
    def name(self):
        return self.flag.lstrip("-")

    @property
    def openings(self):
        """The start-tag markers a slice may open on, one per kind of the half."""
        return tuple(f"<{kind}" for kind in self.kinds)

    @property
    def opening_tags(self):
        return _listed(f"<{kind}>" for kind in self.kinds)

    @property
    def closing(self):
        """The end-tag marker the slice closes on."""
        return f"</{self.required}>"


ALTERNATIVES_SHAPE = Shape(flag="--alternatives", kinds=("alternative",), required="alternative")
RECOMMENDATION_SHAPE = Shape(
    flag="--recommendation", kinds=("applied-principle", "depends-on", "recommendation"), required="recommendation"
)


def _listed(items):
    """The items as prose: "a", "a or b", "a, b, or c"."""
    items = list(items)
    if len(items) <= 1:
        return "".join(items)
    if len(items) == 2:
        return f"{items[0]} or {items[1]}"
    return ", ".join(items[:-1]) + f", or {items[-1]}"


def _article(tag):
    """The article before a tag or tag name read aloud: "an <alternative>", "a </question>"."""
    return "an" if tag.lstrip("<").startswith(("a", "o")) else "a"


def check_block_state(question, shape):
    """A ToolError unless the block is in the state the shape writes into: for --alternatives
    a block carrying no <alternative> yet (bare strip is the hatch); for --recommendation a
    block already carrying at least one <alternative> — the frozen set the recommendation's
    option is checked against — and no <recommendation> yet (strip --recommendation is the
    hatch)."""
    context = f'<{BLOCK_TAG} id="{question.id}">'
    if shape == ALTERNATIVES_SHAPE:
        if question.alternatives:
            raise ToolError(f"{context} already carries <alternative> elements; strip it first to embed a new set")
    else:
        if not question.alternatives:
            raise ToolError(f"{context} carries no <alternative> elements; embed --alternatives first")
        if question.recommendation is not None:
            raise ToolError(
                f"{context} already carries a <recommendation> element; strip --recommendation first to embed a new one"
            )


def extract_fragment(message, shape):
    """The shape's fragment inside a whole message: its lines from the first line holding one
    of the shape's start-tag markers through the last line holding its end-tag marker, joined
    — the identity on a clean message, the discarding of a grounding summary above or a
    closing remark below otherwise. A message missing either anchor line is a ToolError
    naming it."""
    lines = message.splitlines()
    starts = [index for index, line in enumerate(lines) if any(opening in line for opening in shape.openings)]
    ends = [index for index, line in enumerate(lines) if shape.closing in line]
    if not starts:
        raise ToolError(f"no {shape.opening_tags} line to extract from")
    if not ends:
        raise ToolError(f"no {shape.closing} line to extract to")
    start, end = starts[0], ends[-1]
    if end < start:
        raise ToolError(f"the last {shape.closing} line precedes the first {shape.opening_tags} line")
    return "\n".join(lines[start : end + 1])


def parse_fragment(region, shape):
    """The children an extracted fragment describes, as a Question with no id and no question
    text, once the fragment is well-formed and valid under the shape: no <open-question> or
    <question> line, no text outside its elements, no element of a kind the format does not
    define, no element of the other half, and the shape's required kind present — at least one
    <alternative> for --alternatives, exactly one <recommendation> for --recommendation. The
    order of the children is not checked (the writer groups them by kind), and what the
    fragment must agree with in the document — the recommendation's option, every
    <depends-on> tag — is checked by embed_fragment against the block."""
    for line in region.splitlines():
        found = _BLOCK_TAG_LINE.search(line)
        if found:
            tag = found.group(0) + ">"
            raise ToolError(
                f"{FRAGMENT} contains {_article(tag)} {tag} line; the <{BLOCK_TAG}> wrapper and its "
                f"<question> element belong to the document, not to the fragment"
            )
    try:
        root = ET.fromstring(f"<{FRAGMENT_TAG}>\n{region}\n</{FRAGMENT_TAG}>")
    except ET.ParseError as error:
        raise ToolError(f"{FRAGMENT} is not well-formed XML: {_parse_error_text(error)}")

    children = list(root)
    if not children:
        raise ToolError(f"{FRAGMENT} contains no <{shape.required}> element")
    if fold(root.text):
        raise ToolError(f"text precedes <{children[0].tag}> on {FRAGMENT}'s opening line")
    if fold(children[-1].tail):
        raise ToolError(f"text trails </{children[-1].tag}> on {FRAGMENT}'s closing line")
    if any(fold(child.tail) for child in children[:-1]):
        raise ToolError(f"{FRAGMENT} carries text between its elements")
    for child in children:
        if child.tag in CHILD_KINDS and child.tag not in shape.kinds:
            raise ToolError(f"{FRAGMENT} carries {_article(child.tag)} <{child.tag}> element, which {shape.flag} does not take")

    fragment = Question(id="")
    if _parse_children(root, FRAGMENT, fragment):
        raise ToolError(f"{FRAGMENT} contains a <question> element")
    if shape == ALTERNATIVES_SHAPE and not fragment.alternatives:
        raise ToolError(f"{FRAGMENT} contains no <alternative> element")
    if shape == RECOMMENDATION_SHAPE and fragment.recommendation is None:
        raise ToolError(f"{FRAGMENT} contains no <recommendation> element")
    return fragment


def _parse_error_text(error):
    """The parser's reason with its line counted from the fragment's own first line (the parse
    wraps the fragment in a root element on the line above it)."""
    line, column = error.position
    reason = expat.errors.messages.get(getattr(error, "code", None), "syntax error")
    return f"{reason} at line {line - 1}, column {column}"


def check_recommendation_option(question, fragment):
    """A ToolError unless the fragment's <recommendation> option is one of the block's own
    <alternative> ids, compared un-escaped and case-folded: the recommendation half carries
    no alternatives of its own, so the block's frozen set is what it is checked against."""
    wanted = id_key(fragment.recommendation.option)
    if not any(id_key(alternative.id) == wanted for alternative in question.alternatives):
        context = f'<{BLOCK_TAG} id="{question.id}">'
        held = _quoted(alternative.id for alternative in question.alternatives)
        raise ToolError(
            f'the <recommendation> option "{fragment.recommendation.option}" names none of the '
            f"<alternative> ids of {context}, which are {held}"
        )


def check_dependencies(document, question, fragment):
    """A ToolError unless every <depends-on> tag of the fragment resolves one hop: its question
    names a block of the document other than the one being embedded that carries
    <alternative> elements, and its option is one of that block's own <alternative> ids —
    both compared un-escaped and case-folded. Whether the target carries a <recommendation>
    is not asked, so the recommendation pass may write its blocks in any order; the target's
    own tags are not followed and no cycle is looked for."""
    targets = [other for other in document.questions if other is not question and other.alternatives]
    for dependency in fragment.depends_on:
        wanted = id_key(dependency.question)
        target = next((other for other in targets if id_key(other.id) == wanted), None)
        if target is None:
            held = _quoted(other.id for other in targets)
            held = f"the blocks carrying them are {held}" if held else "no other block carries any"
            raise ToolError(
                f'the <depends-on question="{dependency.question}"/> names no block that carries '
                f"<alternative> elements; {held}"
            )
        option = id_key(dependency.option)
        if not any(id_key(alternative.id) == option for alternative in target.alternatives):
            held = _quoted(alternative.id for alternative in target.alternatives)
            raise ToolError(
                f'the <depends-on question="{dependency.question}" option="{dependency.option}"/> names '
                f"none of that block's <alternative> ids, which are {held}"
            )


def embed_fragment(document, question, fragment, shape):
    """Make the fragment's children the shape's half of the block's children, leaving the
    other half as the block holds it: under --alternatives the block takes the fragment's
    alternatives in their returned order and nothing else changes; under --recommendation,
    once the recommendation's option names one of the block's own alternatives and every
    <depends-on> tag resolves against the document, the block takes the fragment's applied
    principles, depends-on tags, and recommendation and its alternatives stay frozen. The
    caller writes, and the writer groups the children by kind."""
    if shape == ALTERNATIVES_SHAPE:
        question.alternatives = list(fragment.alternatives)
        return
    check_recommendation_option(question, fragment)
    check_dependencies(document, question, fragment)
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
        if args.without_alternatives and question.alternatives:
            continue
        if args.without_recommendation and question.recommendation is not None:
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
    strip = strip_recommendation if args.recommendation else strip_question
    changed = False
    for question in find_questions(document, args.short_titles):
        changed = strip(question) or changed
    if changed:
        save_document(args.milestone_dir, document)
    return 0


def cmd_embed(args):
    shape = args.shape
    document = load_document(args.milestone_dir)
    question = find_question(document, args.short_title)
    check_block_state(question, shape)
    fragment = parse_fragment(extract_fragment(read_body(f"the {shape.name} message"), shape), shape)
    embed_fragment(document, question, fragment, shape)
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
        "--without-alternatives",
        action="store_true",
        help="print only the blocks carrying no <alternative> element",
    )
    list_parser.add_argument(
        "--without-recommendation",
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
        "untouched; with --recommendation delete only the <recommendation>, <depends-on>, and "
        "<applied-principle> children and leave the <alternative> children standing; a block "
        "holding nothing the call would delete is left as it is",
    )
    strip_parser.add_argument(
        "short_titles",
        metavar="SHORT_TITLE",
        nargs="+",
        help="the id of a block, compared un-escaped and case-folded",
    )
    strip_parser.add_argument(
        "--recommendation",
        action="store_true",
        help="delete only the <recommendation>, <depends-on>, and <applied-principle> children, "
        "keeping the <alternative> children",
    )

    embed_parser = add_subcommand(
        "embed",
        cmd_embed,
        "put one half of a block's children into the named block, the half the required flag "
        "names, leaving the other half's elements as the block holds them: the whole message "
        "carrying them is read from standard input (pipe it as a quoted heredoc; a terminal stdin "
        "is refused), "
        "the fragment is sliced out of it — with --alternatives from the first <alternative line "
        "through the last </alternative> line, with --recommendation from the first "
        "<applied-principle, <depends-on, or <recommendation line through the last "
        "</recommendation> line — parsed, validated (no <open-question> or <question> line, no "
        "text outside the elements, no unknown element and none of the other half; with "
        "--alternatives at least one <alternative> into a block carrying none yet; with "
        "--recommendation exactly one <recommendation> naming one of the block's own "
        "<alternative> ids, into a block carrying alternatives and no <recommendation> yet, "
        "every <depends-on> resolving to another block carrying <alternative> elements and one "
        "of its ids; child order is not checked), and written with the whole block in the "
        "canonical child order the module docstring's document format states; every miss is one "
        "Error line",
    )
    embed_parser.add_argument(
        "short_title",
        metavar="SHORT_TITLE",
        help="the id of the block, compared un-escaped and case-folded",
    )
    embed_shape = embed_parser.add_mutually_exclusive_group(required=True)
    embed_shape.add_argument(
        "--alternatives",
        dest="shape",
        action="store_const",
        const=ALTERNATIVES_SHAPE,
        help="embed the <alternative> elements into a block carrying none yet",
    )
    embed_shape.add_argument(
        "--recommendation",
        dest="shape",
        action="store_const",
        const=RECOMMENDATION_SHAPE,
        help="embed the <recommendation>, <depends-on>, and <applied-principle> elements into a "
        "block carrying <alternative> elements and no <recommendation> yet",
    )

    remove_parser = add_subcommand(
        "remove",
        cmd_remove,
        "delete the named block and, in the same write, reconcile the blocks that depend on "
        "it: with --option, a dependent whose <depends-on> names the block with that same "
        "option loses only that tag and every other dependent is stripped as by strip "
        "--recommendation, keeping its <alternative> elements; without it every dependent is "
        "so stripped; both transitively over the dependents of a stripped block, so no "
        "<depends-on> tag is left naming a removed or stripped block",
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
