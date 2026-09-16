#!/usr/bin/env python3
"""Validate the literature registry and regenerate its cross-reference.

The registry answers three questions the bibliography alone cannot. What does
a source establish, which project claim does it bear on, and what does it not
establish. It has four layers.

`paper/references.bib` holds bibliographic fields and nothing else. It is the
only place an author, year, title, DOI, or URL is recorded. The annotated
literature review asks for a `literature/bibliography/` copy; this project
keeps the single file at `paper/references.bib` instead, because pandoc and
the manuscript header already read it and two copies is the drift this
registry exists to prevent. Once Better BibTeX drives the file from Zotero it
becomes generated, so this script never writes it. A missing entry is fixed
upstream, in Zotero.

`literature/claims/<claim-id>.md` holds one file per project claim. Claims are
shared across sources, so "which sources bear on this claim" is a lookup.

`literature/sources/<key>.md` holds one note per bib entry. The filename stem
is the citation key, which joins the whole registry. Every machine-read field
lives in the YAML frontmatter, so a schema validates it rather than a regex.
The markdown body holds the summary prose, which keeps it under the Vale and
proselint hooks like the rest of the project's writing.

`outputs/` holds the generated cross-reference: an index to read, an
evidence matrix as CSV, and three parquet tables to query with DuckDB.

Two rules from the annotated review's maintenance list drive the checks.
Every quantitative claim needs a page, section, figure, or table. "Does not
establish" is mandatory, never optional. A claim link that asserts more than
context and cites no located evidence fails, unless the note records a
`follow_up`, which turns the failure into tracked debt.

Run `--write` to regenerate the generated layer, and no flag to check it. The
check is what `prek` runs. Regenerating is separate because a commit hook must
not silently rewrite tracked files.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import pyarrow as pa
import pyarrow.parquet as pq
import yaml
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

ROOT = Path(__file__).resolve().parent
PAPER_DIR = ROOT / "paper"
DOCS_DIR = ROOT / "docs"
LIT_DIR = ROOT / "literature"
SOURCES_DIR = LIT_DIR / "sources"
CLAIMS_DIR = LIT_DIR / "claims"
BIB_PATH = PAPER_DIR / "references.bib"
SCHEMA_PATH = LIT_DIR / "schema.json"
ALLOWLIST_PATH = LIT_DIR / "url-allowlist.txt"
PENDING_PATH = LIT_DIR / "pending.txt"
OUTPUT_DIR = ROOT / "outputs"
INDEX_PATH = LIT_DIR / "index.md"
MATRIX_PATH = LIT_DIR / "evidence-matrix.csv"
SOURCES_PARQUET = OUTPUT_DIR / "sources.parquet"
EVIDENCE_PARQUET = OUTPUT_DIR / "source-evidence.parquet"
LINKS_PARQUET = OUTPUT_DIR / "source-claims.parquet"

# A BibTeX key, restricted to what pandoc accepts and a filename tolerates.
# The project's keys run from `avis2016` through `decreto70` to
# `lebovits2025census`, so a year is not part of the shape.
KEY_PATTERN = r"[A-Za-z][A-Za-z0-9_:.+-]*"
CLAIM_ID_PATTERN = r"[a-z][a-z0-9-]*"

EvidenceKind = Literal["verbatim", "paraphrase", "data", "unlocated"]
Status = Literal["queued", "reading", "retained", "superseded", "do-not-use"]
Strength = Literal["high", "medium", "low"]
Verification = Literal["verified_full_text", "verified_secondary", "needs_follow_up"]
# From the annotated review's evidence labels.
EvidenceType = Literal[
    "direct_analogue",
    "method_validation",
    "method_precedent",
    "mechanism_evidence",
    "context",
    "caution",
]
# From the annotated review's allowed `relationship` values.
Relationship = Literal[
    "supports", "qualifies", "contradicts", "method_validates", "context_only"
]
# Rule 5 of the maintenance list: keep these apart, never merge them.
Unit = Literal[
    "building",
    "roof",
    "roof_block",
    "dwelling",
    "household",
    "family",
    "resident",
    "settlement",
    "grid_cell",
    "census_area",
    "jurisdiction",
    "national",
    "not_applicable",
]
# Rule 6: record what a reference population actually is.
ReferenceKind = Literal[
    "census",
    "complete_enumeration",
    "community_estimate",
    "modeled_estimate",
    "administrative_record",
    "undocumented_literature_value",
    "not_applicable",
]
# Who produced the source. From the census-coverage notes' source-card schema.
SourceType = Literal[
    "primary_official",
    "official_documentation",
    "peer_reviewed",
    "preprint",
    "working_paper",
    "independent_research",
    "journalism",
    "dataset",
    "review",
]
# How the source's evidence was produced. The census-coverage notes require
# comparative census cases to be labelled by method, and require direct
# coverage measurement to stay distinct from demographic reconciliation.
Method = Literal[
    "direct_enumeration",
    "post_enumeration_survey",
    "demographic_reconciliation",
    "modeled_population_product",
    "remote_sensing",
    "field_survey",
    "administrative_registry",
    "official_documentation",
    "journalism",
    "independent_analysis",
    "literature_review",
    "not_applicable",
]
# A method that measures coverage directly, as opposed to inferring a total.
DIRECT_COVERAGE = ("direct_enumeration", "post_enumeration_survey", "field_survey")

Origin = Literal[
    "zotero-annotation",
    "annotated-review",
    "litreview-docx",
    "manuscript",
    "audit-notes",
    "manual",
]

# A relationship that asserts more than background needs a locator.
ASSERTIVE = ("supports", "qualifies", "contradicts", "method_validates")

# Markers written at the start of a bib entry's `note` to say the record is
# not trustworthy yet. They are a convention, so the validator enforces them:
# a marked entry must not be cited from the manuscript. Keep them uppercase
# and at the start of the note so they are visible when reading the .bib.
UNTRUSTED_MARKERS = (
    "INCOMPLETE CITATION",
    "UNVERIFIED AND UNLOCATED",
    "YEAR UNVERIFIED",
    "AUTHOR UNCONFIRMED",
    "TITLE PARAPHRASED",
    "DEAD URL",
)


class Evidence(BaseModel):
    """One recorded finding, tied to a location in the source.

    `kind` carries the honesty of the record. `verbatim` is text copied
    exactly from the source. `paraphrase` restates the source, which is
    legitimate but is not the source's own words. `data` is a figure read from
    a table or result. Those three require both the text and a locator.

    `unlocated` is the fourth case and the important one. The finding text is
    recorded, usually from a project document rather than the source itself,
    but nobody has found the page yet. It carries the text and refuses a
    locator, so the debt is visible in the index and in `n_located` instead of
    passing as located evidence.
    """

    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^E[0-9]+$")
    label: str = Field(min_length=3, max_length=200)
    kind: EvidenceKind
    loc: str | None = Field(
        default=None,
        description="Page, section, figure, or table. Required for verbatim, "
        "paraphrase, and data. Forbidden for unlocated.",
    )
    quote: str | None = Field(
        default=None,
        description="The finding, as text. Always required.",
    )
    sample_size: str | None = Field(
        default=None, description="Sample or study extent, as reported."
    )
    reference_kind: ReferenceKind = Field(
        default="not_applicable",
        description="What any reference population in this finding is.",
    )
    origin: Origin = Field(
        default="manual",
        description="Which document this record came from. A project document "
        "means the record is second-hand until located in the source.",
    )
    lang: str | None = Field(default=None, pattern=r"^[a-z]{2}$")

    @model_validator(mode="after")
    def check_quote_and_loc(self) -> Evidence:
        if not (self.quote or "").strip():
            raise ValueError(f"{self.id}: every finding requires a quote")
        if self.kind == "unlocated":
            if (self.loc or "").strip():
                raise ValueError(
                    f"{self.id}: kind 'unlocated' must not carry a loc. Once "
                    "you have the page, change the kind to verbatim, "
                    "paraphrase, or data."
                )
            return self
        if not (self.loc or "").strip():
            raise ValueError(
                f"{self.id}: kind '{self.kind}' requires a loc. Use "
                "'unlocated' if the page is not known yet."
            )
        return self


class ClaimLink(BaseModel):
    """How this source bears on one project claim."""

    model_config = ConfigDict(extra="forbid")

    claim: str = Field(pattern=rf"^{CLAIM_ID_PATTERN}$")
    relationship: Relationship
    evidence: list[str] = Field(min_length=1)
    strength: Strength = "medium"
    note: str | None = None

    @field_validator("evidence")
    @classmethod
    def check_evidence_ids(cls, value: list[str]) -> list[str]:
        for item in value:
            if not re.fullmatch(r"E[0-9]+", item):
                raise ValueError(f"'{item}' is not an evidence ID such as E1")
        if len(set(value)) != len(value):
            raise ValueError("evidence list repeats an ID")
        return value


class SourceNote(BaseModel):
    """The frontmatter of one `literature/sources/<key>.md` file."""

    model_config = ConfigDict(extra="forbid")

    key: str = Field(pattern=rf"^{KEY_PATTERN}$")
    status: Status
    lang: str = Field(pattern=r"^[a-z]{2}$")
    verification: Verification
    strength: Strength
    source_type: SourceType
    method: Method
    evidence_type: list[EvidenceType] = Field(min_length=1)
    unit_of_analysis: list[Unit] = Field(min_length=1)
    geographies: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    cited_in_manuscript: bool = False
    follow_up: str | None = None
    retrieved: dt.date | None = None
    evidence: list[Evidence] = Field(default_factory=list)
    claims: list[ClaimLink] = Field(default_factory=list)
    does_not_establish: list[str] = Field(
        min_length=1,
        description="Mandatory. Maintenance rule 3 of the annotated review.",
    )

    @model_validator(mode="after")
    def check_ids(self) -> SourceNote:
        seen: set[str] = set()
        for item in self.evidence:
            if item.id in seen:
                raise ValueError(f"evidence ID {item.id} appears twice")
            seen.add(item.id)
        for link in self.claims:
            missing = [ref for ref in link.evidence if ref not in seen]
            if missing:
                raise ValueError(
                    f"claim '{link.claim}' cites {', '.join(missing)}, "
                    "which this note does not define"
                )
        pairs = [(link.claim, link.relationship) for link in self.claims]
        if len(set(pairs)) != len(pairs):
            raise ValueError("a claim is linked twice with the same relationship")
        return self


class Claim(BaseModel):
    """The frontmatter of one `literature/claims/<claim-id>.md` file."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=rf"^{CLAIM_ID_PATTERN}$")
    status: Literal["active", "retired"] = "active"
    scope: Literal["international", "argentina", "method"] = "international"
    requires_direct_measurement: bool = Field(
        default=False,
        description="True for a claim about coverage error, where a "
        "demographic reconciliation or a modelled product does not measure "
        "the quantity directly. The census-coverage notes require this "
        "distinction to be kept.",
    )


@dataclass(frozen=True)
class Problem:
    level: Literal["ERROR", "WARN"]
    where: str
    message: str


@dataclass(frozen=True)
class BibEntry:
    key: str
    entry_type: str
    fields: dict[str, str]


def _read_delimited(
    text: str, start: int, open_char: str, close_char: str
) -> tuple[str, int]:
    """Read a brace- or quote-delimited value. Returns the value and the end."""
    depth = 0
    index = start
    while index < len(text):
        char = text[index]
        if char == open_char:
            depth += 1
        elif char == close_char:
            depth -= 1
            if depth == 0:
                return text[start + 1 : index], index + 1
        index += 1
    raise ValueError(f"unterminated {open_char}{close_char} at offset {start}")


def parse_bib(text: str) -> dict[str, BibEntry]:
    """Parse the entry keys and fields this project needs from a .bib file.

    Not a general BibTeX parser. It reads entry types, keys, and top-level
    fields, which is what the registry joins on. It counts braces so a title
    such as `{Buenos Aires}` inside a field does not end the field.
    """
    entries: dict[str, BibEntry] = {}
    for match in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        entry_type = match.group(1).lower()
        key = match.group(2)
        brace_start = text.index("{", match.start())
        body, _ = _read_delimited(text, brace_start, "{", "}")
        fields: dict[str, str] = {}
        for field_match in re.finditer(r"(\w+)\s*=\s*", body):
            name = field_match.group(1).lower()
            cursor = field_match.end()
            if cursor >= len(body):
                continue
            if body[cursor] == "{":
                value, _ = _read_delimited(body, cursor, "{", "}")
            elif body[cursor] == '"':
                end = body.index('"', cursor + 1)
                value = body[cursor + 1 : end]
            else:
                end = body.find(",", cursor)
                value = body[cursor : end if end != -1 else len(body)]
            fields[name] = " ".join(value.split())
        entries[key] = BibEntry(key=key, entry_type=entry_type, fields=fields)
    return entries


FENCE_RE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
COMMENT_RE = re.compile(r"<!--(.*?)-->", re.DOTALL)
YAML_HEADER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
URL_RE = re.compile(r"https?://[^\s)>\]\"'`]+")
CITE_RE = re.compile(rf"(?<![A-Za-z0-9_@])@({KEY_PATTERN})")
ANCHOR_RE = re.compile(rf"ev:\s*({KEY_PATTERN})#(E[0-9]+)")


def strip_noncitable(text: str) -> str:
    """Remove regions where an @ or a URL is not a citation."""
    text = YAML_HEADER_RE.sub("", text)
    text = FENCE_RE.sub("", text)
    text = INLINE_CODE_RE.sub("", text)
    text = COMMENT_RE.sub("", text)
    return URL_RE.sub("", text)


def prose_files() -> list[Path]:
    """Every markdown file that may cite a source, excluding the registry."""
    found = sorted(PAPER_DIR.glob("*.md")) + sorted(DOCS_DIR.rglob("*.md"))
    return [path for path in found if LIT_DIR not in path.parents]


def manuscript_files() -> set[str]:
    return {path.relative_to(ROOT).as_posix() for path in PAPER_DIR.glob("*.md")}


def split_frontmatter(text: str, where: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError(f"{where}: file must start with a YAML frontmatter block")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{where}: frontmatter block is not closed with ---")
    loaded = yaml.safe_load(text[4:end])
    if not isinstance(loaded, dict):
        raise ValueError(f"{where}: frontmatter must be a YAML mapping")
    return loaded, text[end + 5 :]


def summary_of(body: str) -> str:
    return "\n\n".join(
        part.strip() for part in body.strip().split("\n\n") if part.strip()
    )


def load_claims(problems: list[Problem]) -> dict[str, tuple[Claim, str]]:
    claims: dict[str, tuple[Claim, str]] = {}
    for path in sorted(CLAIMS_DIR.glob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        try:
            front, body = split_frontmatter(path.read_text(encoding="utf-8"), rel)
            claim = Claim.model_validate(front)
        except (ValueError, ValidationError) as error:
            problems.append(Problem("ERROR", rel, str(error).splitlines()[0]))
            continue
        if claim.id != path.stem:
            problems.append(
                Problem(
                    "ERROR",
                    rel,
                    f"id '{claim.id}' does not match the filename stem '{path.stem}'",
                )
            )
            continue
        statement = summary_of(body)
        if len(statement) < 40:
            problems.append(
                Problem("ERROR", rel, "the body must state the claim in prose")
            )
        claims[claim.id] = (claim, statement)
    return claims


def load_notes(problems: list[Problem]) -> dict[str, tuple[SourceNote, str]]:
    notes: dict[str, tuple[SourceNote, str]] = {}
    for path in sorted(SOURCES_DIR.glob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        try:
            front, body = split_frontmatter(path.read_text(encoding="utf-8"), rel)
        except ValueError as error:
            problems.append(Problem("ERROR", rel, str(error)))
            continue
        try:
            note = SourceNote.model_validate(front)
        except ValidationError as error:
            for item in error.errors():
                where = ".".join(str(part) for part in item["loc"]) or "frontmatter"
                problems.append(Problem("ERROR", rel, f"{where}: {item['msg']}"))
            continue
        if note.key != path.stem:
            problems.append(
                Problem(
                    "ERROR",
                    rel,
                    f"frontmatter key '{note.key}' does not match the filename "
                    f"stem '{path.stem}'. The filename is the join column.",
                )
            )
            continue
        summary = summary_of(body)
        if len(summary) < 80:
            problems.append(
                Problem("ERROR", rel, "the body must hold a summary of 80+ characters")
            )
        notes[note.key] = (note, summary)
    return notes


def load_pending() -> set[str]:
    """Bib keys registered without a note yet, one per line, # for comments.

    A key listed here reports as a warning instead of an error, so the backlog
    is enumerated in a tracked file and in the index's Open gaps table rather
    than blocking every commit. Remove a key when its note lands. When the
    file is empty the one-note-per-entry rule is strict again.
    """
    if not PENDING_PATH.exists():
        return set()
    return {
        line.strip()
        for line in PENDING_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


def load_allowlist() -> set[str]:
    if not ALLOWLIST_PATH.exists():
        return set()
    return {
        line.strip().rstrip("/")
        for line in ALLOWLIST_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


# Tracking parameters that do not change which document a URL points to.
TRACKING_PARAMS = ("utm_", "fbclid", "gclid", "mc_cid", "mc_eid", "ref_src")


def normalise_url(url: str) -> str:
    """Strip trailing punctuation, tracking parameters, and an archive wrapper."""
    url = url.rstrip(".,;:)»\"'").rstrip("/")
    wrapped = re.search(r"web\.archive\.org/web/\d+(?:id_)?/(https?://.*)", url)
    if wrapped:
        url = wrapped.group(1)
    # A utm parameter records how a link was found, not what it points to.
    if "?" in url:
        base, _, query = url.partition("?")
        kept = [
            part
            for part in query.split("&")
            if part and not part.lower().startswith(TRACKING_PARAMS)
        ]
        url = base + ("?" + "&".join(kept) if kept else "")
    return url.rstrip("/")


def check_registry() -> tuple[list[Problem], dict]:
    problems: list[Problem] = []
    if not BIB_PATH.exists():
        problems.append(Problem("ERROR", str(BIB_PATH), "bibliography is missing"))
        return problems, {}

    bib = parse_bib(BIB_PATH.read_text(encoding="utf-8"))
    claims = load_claims(problems)
    notes = load_notes(problems)
    allowlist = load_allowlist()
    pending = load_pending()

    citations: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    anchors: list[tuple[str, str, str]] = []
    doc_urls: dict[str, list[str]] = defaultdict(list)

    for path in prose_files():
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for match in CITE_RE.finditer(strip_noncitable(text)):
            citations[match.group(1)][rel] += 1
        for comment in COMMENT_RE.finditer(text):
            for match in ANCHOR_RE.finditer(comment.group(1)):
                anchors.append((rel, match.group(1), match.group(2)))
        if path.is_relative_to(DOCS_DIR):
            for match in URL_RE.finditer(text):
                doc_urls[normalise_url(match.group(0))].append(rel)

    # Every URL anywhere in an entry counts as registered, not only the `url`
    # field. Several government documents are mirrored, and the audit notes
    # cite whichever copy resolved. Recording a mirror in `note` keeps one
    # entry per source instead of one per copy.
    bib_urls: dict[str, str] = {}
    for key, entry in bib.items():
        for value in entry.fields.values():
            for match in URL_RE.finditer(value):
                bib_urls.setdefault(normalise_url(match.group(0)), key)
        # A DOI is stored bare in the bib and cited as a resolver URL in
        # prose, so register both forms.
        doi = entry.fields.get("doi", "").strip()
        if doi:
            bib_urls.setdefault(normalise_url(f"https://doi.org/{doi}").lower(), key)
            bib_urls.setdefault(normalise_url(f"https://dx.doi.org/{doi}").lower(), key)

    for key, where in sorted(citations.items()):
        if key not in bib:
            problems.append(
                Problem(
                    "ERROR",
                    ", ".join(sorted(where)),
                    f"citation @{key} has no entry in paper/references.bib. "
                    "Add the item in Zotero, then re-export.",
                )
            )

    for key in sorted(set(bib) - set(notes)):
        problems.append(
            Problem(
                "WARN" if key in pending else "ERROR",
                f"literature/sources/{key}.md",
                f"bib entry @{key} has no source note. Create the file."
                + (
                    ""
                    if key in pending
                    else " Add the key to literature/pending.txt to defer it."
                ),
            )
        )
    # Keep the backlog honest in both directions.
    for key in sorted(pending & set(notes)):
        problems.append(
            Problem(
                "WARN",
                "literature/pending.txt",
                f"@{key} now has a note. Remove it from the pending list.",
            )
        )
    for key in sorted(pending - set(bib)):
        problems.append(
            Problem(
                "ERROR",
                "literature/pending.txt",
                f"@{key} is listed as pending but has no bib entry.",
            )
        )
    for key in sorted(set(notes) - set(bib)):
        problems.append(
            Problem(
                "ERROR",
                f"literature/sources/{key}.md",
                f"note '{key}' has no bib entry. If the key changed, pin it in "
                "Zotero and rename the note to match.",
            )
        )

    for rel, key, ref in anchors:
        if key not in notes:
            problems.append(
                Problem("ERROR", rel, f"anchor ev:{key}#{ref} names an unknown source")
            )
        elif ref not in {item.id for item in notes[key][0].evidence}:
            problems.append(
                Problem(
                    "ERROR",
                    rel,
                    f"anchor ev:{key}#{ref} does not resolve in "
                    f"literature/sources/{key}.md",
                )
            )

    # A record marked untrustworthy must not reach the manuscript. Citing one
    # from docs/ is fine, because the audit notes are where uncertainty gets
    # worked out.
    manuscript = manuscript_files()
    for key, where in sorted(citations.items()):
        entry = bib.get(key)
        if not entry:
            continue
        note = entry.fields.get("note", "")
        marker = next(
            (m for m in UNTRUSTED_MARKERS if note.upper().startswith(m)), None
        )
        if not marker:
            continue
        in_paper = sorted(set(where) & manuscript)
        if in_paper:
            problems.append(
                Problem(
                    "ERROR",
                    ", ".join(in_paper),
                    f"@{key} is marked {marker} in paper/references.bib and "
                    "must not be cited from the manuscript. Fix the record "
                    "first, or cite a source with a complete one.",
                )
            )
        else:
            problems.append(
                Problem(
                    "WARN",
                    "paper/references.bib",
                    f"@{key} is marked {marker} and is cited in "
                    + ", ".join(sorted(where)),
                )
            )

    for key, (note, _) in sorted(notes.items()):
        rel = f"literature/sources/{key}.md"
        in_paper = bool(set(citations.get(key, {})) & manuscript)
        if in_paper and not note.cited_in_manuscript:
            problems.append(
                Problem(
                    "ERROR",
                    rel,
                    "the manuscript cites this source. Set "
                    "cited_in_manuscript to true.",
                )
            )
        if note.cited_in_manuscript and not in_paper:
            problems.append(
                Problem(
                    "WARN",
                    rel,
                    "cited_in_manuscript is true but no file in paper/ cites it",
                )
            )
        if note.status == "do-not-use" and in_paper:
            problems.append(
                Problem(
                    "ERROR",
                    rel,
                    "status is 'do-not-use' but the manuscript cites it",
                )
            )

        located = {item.id for item in note.evidence if (item.loc or "").strip()}
        for link in note.claims:
            if link.claim not in claims:
                problems.append(
                    Problem(
                        "ERROR",
                        rel,
                        f"claim '{link.claim}' has no file in literature/claims/",
                    )
                )
                continue
            if claims[link.claim][0].status == "retired":
                problems.append(
                    Problem(
                        "WARN", rel, f"claim '{link.claim}' is retired but still linked"
                    )
                )
            # Maintenance rules 1 and 10: an assertive claim link needs a
            # located finding. A recorded follow_up turns the failure into
            # tracked debt instead of a blocked commit.
            if link.relationship in ASSERTIVE and not (located & set(link.evidence)):
                level = "WARN" if note.follow_up else "ERROR"
                problems.append(
                    Problem(
                        level,
                        rel,
                        f"claim '{link.claim}' is '{link.relationship}' but none "
                        f"of {', '.join(link.evidence)} carries a loc. Add a page, "
                        "section, figure, or table, or record a follow_up.",
                    )
                )
            # The census-coverage notes require comparative census cases to
            # be labelled by method, and direct coverage measurement to stay
            # distinct from demographic reconciliation. A reconciliation or a
            # modelled product infers a total; it does not measure omission.
            if (
                claims[link.claim][0].requires_direct_measurement
                and link.relationship == "supports"
                and note.method not in DIRECT_COVERAGE
            ):
                problems.append(
                    Problem(
                        "WARN",
                        rel,
                        f"claim '{link.claim}' needs direct coverage "
                        f"measurement, but this source's method is "
                        f"'{note.method}'. Label the comparison by method in "
                        "the claim note, or use 'qualifies'.",
                    )
                )
            # Maintenance rule 7: geographic transfer is a limitation.
            if (
                link.relationship == "supports"
                and link.strength == "high"
                and claims[link.claim][0].scope == "argentina"
                and not any(
                    g.lower() in ("argentina", "brazil", "colombia", "mexico", "chile")
                    for g in note.geographies
                )
            ):
                problems.append(
                    Problem(
                        "WARN",
                        rel,
                        f"claim '{link.claim}' is Argentine in scope but this "
                        "source carries no Argentine or comparable Latin "
                        "American geography. Consider 'qualifies'.",
                    )
                )

    # A publisher URL often embeds the DOI, as sagepub.com/doi/10.1177/...,
    # link.springer.com/article/10.1186/..., or nature.com/articles/s41467-...
    # Treat a URL containing a registered DOI as that source.
    dois = {
        entry.fields["doi"].strip().lower(): key
        for key, entry in bib.items()
        if entry.fields.get("doi")
    }

    def resolves(url: str) -> bool:
        lower = url.lower()
        if url in bib_urls or lower in bib_urls or url in allowlist:
            return True
        return any(doi in lower or doi.partition("/")[2] in lower for doi in dois)

    for url, where in sorted(doc_urls.items()):
        if resolves(url):
            continue
        problems.append(
            Problem(
                "ERROR",
                ", ".join(sorted(set(where))),
                f"URL {url} is cited but not registered. Add it to Zotero and "
                "cite it by key, or list it in literature/url-allowlist.txt.",
            )
        )

    linked = {link.claim for note, _ in notes.values() for link in note.claims}
    for claim_id, (claim, _) in sorted(claims.items()):
        if claim.status == "active" and claim_id not in linked:
            problems.append(
                Problem(
                    "WARN",
                    f"literature/claims/{claim_id}.md",
                    "no source links to this claim",
                )
            )

    # An entry with a note is registered deliberately, so being uncited is a
    # normal state. The project keeps sources it has read and not yet used.
    # Only an entry with neither a note nor a citation is untouched.
    for key in sorted(set(bib) - set(citations) - set(notes)):
        problems.append(
            Problem(
                "WARN",
                "paper/references.bib",
                f"@{key} has neither a note nor a citation",
            )
        )
    for key, (note, _) in sorted(notes.items()):
        gaps = [item.id for item in note.evidence if item.kind == "unlocated"]
        if gaps:
            problems.append(
                Problem(
                    "WARN",
                    f"literature/sources/{key}.md",
                    f"{len(gaps)} finding(s) still need a located quote: "
                    + ", ".join(gaps),
                )
            )
        if note.follow_up:
            problems.append(
                Problem(
                    "WARN",
                    f"literature/sources/{key}.md",
                    f"follow-up: {note.follow_up}",
                )
            )

    return problems, {
        "bib": bib,
        "notes": notes,
        "claims": claims,
        "citations": citations,
    }


def build_rows(state: dict) -> dict[str, list[dict]]:
    bib: dict[str, BibEntry] = state["bib"]
    notes: dict[str, tuple[SourceNote, str]] = state["notes"]
    citations: dict[str, dict[str, int]] = state["citations"]

    source_rows: list[dict] = []
    evidence_rows: list[dict] = []
    link_rows: list[dict] = []

    for key in sorted(notes):
        note, summary = notes[key]
        where = citations.get(key, {})
        entry = bib.get(key)
        fields = entry.fields if entry else {}
        source_rows.append(
            {
                "key": key,
                "status": note.status,
                "lang": note.lang,
                "verification": note.verification,
                "strength": note.strength,
                "source_type": note.source_type,
                "method": note.method,
                "evidence_type": list(note.evidence_type),
                "unit_of_analysis": list(note.unit_of_analysis),
                "geographies": list(note.geographies),
                "tags": list(note.tags),
                "entry_type": entry.entry_type if entry else None,
                "title": fields.get("title"),
                "year": fields.get("year"),
                "doi": fields.get("doi"),
                "url": fields.get("url"),
                "follow_up": note.follow_up,
                "retrieved": note.retrieved.isoformat() if note.retrieved else None,
                "n_evidence": len(note.evidence),
                "n_located": sum(1 for e in note.evidence if (e.loc or "").strip()),
                "n_needs_quote": sum(
                    1 for e in note.evidence if e.kind == "needs-quote"
                ),
                "n_claims": len(note.claims),
                "n_does_not_establish": len(note.does_not_establish),
                "n_citations": sum(where.values()),
                "cited_in": sorted(where),
                "summary": summary,
            }
        )
        for item in note.evidence:
            evidence_rows.append(
                {
                    "key": key,
                    "evidence_id": item.id,
                    "label": item.label,
                    "kind": item.kind,
                    "loc": item.loc,
                    "quote": item.quote,
                    "sample_size": item.sample_size,
                    "reference_kind": item.reference_kind,
                    "origin": item.origin,
                    "lang": item.lang or note.lang,
                }
            )
        by_id = {item.id: item for item in note.evidence}
        for link in note.claims:
            cited = [by_id[ref] for ref in link.evidence]
            link_rows.append(
                {
                    "key": key,
                    "claim": link.claim,
                    "relationship": link.relationship,
                    "strength": link.strength,
                    "evidence": list(link.evidence),
                    "page_or_section": "; ".join(
                        e.loc for e in cited if (e.loc or "").strip()
                    )
                    or None,
                    "located": any((e.loc or "").strip() for e in cited),
                    "direct_result": "; ".join(e.label for e in cited),
                    "note": link.note,
                    "verification": note.verification,
                    "source_type": note.source_type,
                    "method": note.method,
                    "geographies": list(note.geographies),
                    "unit_of_analysis": list(note.unit_of_analysis),
                    "does_not_establish": list(note.does_not_establish),
                    "follow_up": note.follow_up,
                    "doi": fields.get("doi"),
                    "url": fields.get("url"),
                }
            )
    return {"sources": source_rows, "evidence": evidence_rows, "links": link_rows}


def registry_hash(rows: dict[str, list[dict]]) -> str:
    payload = json.dumps(rows, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def cell(value: str | None, width: int = 60) -> str:
    text = " ".join((value or "").split())
    if len(text) > width:
        text = text[: width - 1] + "…"
    return text.replace("|", "\\|")


MATRIX_COLUMNS = [
    "citation_key",
    "claim_id",
    "relationship",
    "evidence_type",
    "source_type",
    "method",
    "geography",
    "unit_of_analysis",
    "sample_size",
    "direct_result",
    "page_or_section",
    "supports",
    "does_not_establish",
    "strength",
    "verification",
    "doi",
    "url",
    "follow_up",
]


def render_matrix(rows: dict[str, list[dict]], state: dict) -> str:
    notes = state["notes"]
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=MATRIX_COLUMNS, lineterminator="\n")
    writer.writeheader()
    for row in rows["links"]:
        note = notes[row["key"]][0]
        by_id = {item.id: item for item in note.evidence}
        sizes = [
            by_id[ref].sample_size for ref in row["evidence"] if by_id[ref].sample_size
        ]
        writer.writerow(
            {
                "citation_key": row["key"],
                "claim_id": row["claim"],
                "relationship": row["relationship"],
                "evidence_type": "|".join(note.evidence_type),
                "source_type": note.source_type,
                "method": note.method,
                "geography": "|".join(row["geographies"]),
                "unit_of_analysis": "|".join(row["unit_of_analysis"]),
                "sample_size": "; ".join(sizes),
                "direct_result": row["direct_result"],
                "page_or_section": row["page_or_section"] or "",
                "supports": row["note"] or "",
                "does_not_establish": " / ".join(row["does_not_establish"]),
                "strength": row["strength"],
                "verification": row["verification"],
                "doi": row["doi"] or "",
                "url": row["url"] or "",
                "follow_up": row["follow_up"] or "",
            }
        )
    return buffer.getvalue()


def render_index(
    rows: dict[str, list[dict]], state: dict, problems: list[Problem]
) -> str:
    sources, evidence, links = rows["sources"], rows["evidence"], rows["links"]
    claims = state["claims"]
    by_claim: dict[str, list[dict]] = defaultdict(list)
    for row in links:
        by_claim[row["claim"]].append(row)

    lines = [
        "<!-- GENERATED by check_sources.py. Do not edit. -->",
        f"<!-- registry-hash: {registry_hash(rows)} -->",
        "",
        "# Source index",
        "",
        f"{len(sources)} sources, {len(evidence)} findings, {len(links)} claim "
        f"links across {len(claims)} claims.",
        "",
        "Regenerate with `pixi run sources-index`. Query "
        "`literature/evidence-matrix.csv` or the parquet tables in `outputs/` "
        "for anything this page does not answer.",
        "",
        "## Claims",
        "",
        "| Claim | Scope | Supports | Qualifies | Contradicts | Method | Context |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for claim_id in sorted(claims):
        group = by_claim.get(claim_id, [])

        def count(kind: str, group: list[dict] = group) -> str:
            hits = [r["key"] for r in group if r["relationship"] == kind]
            return cell(", ".join(sorted(hits)), 34) or "—"

        lines.append(
            f"| `{claim_id}` | {claims[claim_id][0].scope} | {count('supports')} | "
            f"{count('qualifies')} | {count('contradicts')} | "
            f"{count('method_validates')} | {count('context_only')} |"
        )

    lines += [
        "",
        "## Sources",
        "",
        "| Key | Status | Verif. | Str. | Findings | Located | Claims | Limits | Cites |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in sources:
        lines.append(
            f"| `{row['key']}` | {row['status']} | "
            f"{row['verification'].replace('_', ' ')} | {row['strength']} | "
            f"{row['n_evidence']} | {row['n_located']} | {row['n_claims']} | "
            f"{row['n_does_not_establish']} | {row['n_citations']} |"
        )

    lines += ["", "## Claim links", ""]
    lines += [
        "| Key | Claim | Relationship | Str. | Located | Page or section |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in sorted(links, key=lambda r: (r["claim"], r["key"])):
        lines.append(
            f"| `{row['key']}` | `{row['claim']}` | {row['relationship']} | "
            f"{row['strength']} | {'yes' if row['located'] else 'NO'} | "
            f"{cell(row['page_or_section'], 40) or '—'} |"
        )

    gaps = [p for p in problems if p.level == "WARN"]
    lines += ["", "## Open gaps", ""]
    if gaps:
        lines += ["| Where | Note |", "| --- | --- |"]
        for problem in gaps:
            lines.append(f"| `{problem.where}` | {cell(problem.message, 100)} |")
    else:
        lines.append("None recorded.")
    lines.append("")
    return "\n".join(lines)


def write_outputs(
    rows: dict[str, list[dict]], state: dict, problems: list[Problem]
) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(render_index(rows, state, problems), encoding="utf-8")
    MATRIX_PATH.write_text(render_matrix(rows, state), encoding="utf-8")
    for name, path in (
        ("sources", SOURCES_PARQUET),
        ("evidence", EVIDENCE_PARQUET),
        ("links", LINKS_PARQUET),
    ):
        pq.write_table(pa.Table.from_pylist(rows[name]), path)
    SCHEMA_PATH.write_text(
        json.dumps(
            {
                "source_note": SourceNote.model_json_schema(),
                "claim": Claim.model_json_schema(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--write",
        action="store_true",
        help="regenerate the index, the evidence matrix, the parquet tables, "
        "and literature/schema.json",
    )
    parser.add_argument(
        "--quiet", action="store_true", help="print errors only, suppressing warnings"
    )
    args = parser.parse_args()

    problems, state = check_registry()
    errors = [p for p in problems if p.level == "ERROR"]
    warnings = [p for p in problems if p.level == "WARN"]
    empty: dict[str, list[dict]] = {"sources": [], "evidence": [], "links": []}
    rows = build_rows(state) if state else empty

    if args.write:
        write_outputs(rows, state, problems)
        print(
            f"wrote {INDEX_PATH.relative_to(ROOT)}, "
            f"{MATRIX_PATH.relative_to(ROOT)}, three parquet tables, and "
            f"{SCHEMA_PATH.relative_to(ROOT)}"
        )
    elif state and not errors:
        for path, expected in (
            (INDEX_PATH, render_index(rows, state, problems)),
            (MATRIX_PATH, render_matrix(rows, state)),
        ):
            actual = path.read_text(encoding="utf-8") if path.exists() else ""
            if expected != actual:
                errors.append(
                    Problem(
                        "ERROR",
                        path.relative_to(ROOT).as_posix(),
                        "stale. Run `pixi run sources-index`.",
                    )
                )
        # outputs/ is gitignored, so the parquet tables are absent on a fresh
        # clone. That is a build state, not a broken registry.
        for path in (SOURCES_PARQUET, EVIDENCE_PARQUET, LINKS_PARQUET):
            if not path.exists():
                warnings.append(
                    Problem(
                        "WARN",
                        path.relative_to(ROOT).as_posix(),
                        "not built. Run `pixi run sources-index` to query it.",
                    )
                )

    if not args.quiet:
        for problem in warnings:
            print(f"WARN  {problem.where}: {problem.message}")
    for problem in errors:
        print(f"ERROR {problem.where}: {problem.message}", file=sys.stderr)

    counts = f"{len(errors)} error(s), {len(warnings)} warning(s)"
    if state:
        counts += (
            f" across {len(state['notes'])} note(s), {len(state['claims'])} claim(s), "
            f"and {len(state['bib'])} bib entries"
        )
    print(counts)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
