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

A Short Title names a block by its id and ALTERNATIVE_ID names an alternative by its id;
both are compared against the document's un-escaped values, case-folded.

Document format, the canonical form every write re-renders the whole document into:
  - a bare <open-questions> root with no XML declaration and no attributes; the empty
    document is that one root element, written self-closing
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
import stat
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Optional

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

    if not question_texts:
        raise ToolError(f"{context} has no <question> element")
    if len(question_texts) > 1:
        raise ToolError(f"{context} carries {len(question_texts)} <question> elements")
    if len(recommendations) > 1:
        raise ToolError(f"{context} carries {len(recommendations)} <recommendation> elements")
    question.question = question_texts[0]
    if recommendations:
        question.recommendation = recommendations[0]
    return question


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
