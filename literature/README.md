# Literature registry

This registry stores the sources, records what each one establishes, and
checks that the two agree. `check_sources.py` implements every rule described
here, and `prek` runs it on any commit that touches `paper/`, `docs/`, or
`literature/`.

## Layers

| Path | Holds | Written by |
|---|---|---|
| `paper/references.bib` | Bibliographic fields only | Zotero, via Better BibTeX |
| `literature/claims/<id>.md` | One project claim per file | Hand |
| `literature/sources/<key>.md` | One note per bib entry | Hand |
| `literature/schema.json` | The frontmatter contract | Generated |
| `literature/index.md` | Human-readable cross-reference | Generated, tracked |
| `literature/evidence-matrix.csv` | The evidence matrix | Generated, tracked |
| `outputs/*.parquet` | Query tables for DuckDB | Generated, gitignored |
| `literature/pending.txt` | Entries awaiting a note | Hand |

The filename stem of a source note is its citation key. That key is the join
column for the whole registry, so it appears in the bib, the note filename,
the note frontmatter, and every `[@key]` in the prose.

## Order of operations

1. Add the item in Zotero. Pin the citation key.
2. Export to `paper/references.bib` with Better BibTeX "Keep updated" on.
3. Create `literature/sources/<key>.md` from the template below.
4. Record findings with locators before writing any claim link.
5. Cite `[@key]` in prose.
6. Run `pixi run sources-index`, then `pixi run sources-check`.

Never hand-edit anything in the generated column. A missing bib entry is
fixed in Zotero, not in the `.bib` file.

The index and the matrix are tracked so a reviewer sees the registry change in
the pull-request diff. The parquet tables are a build product, so `outputs/`
stays gitignored and `sources-index` rebuilds them on demand.

## Template

```yaml
---
key: thomson2021
status: retained            # queued | reading | retained | superseded | do-not-use
lang: en
verification: verified_full_text
strength: high
evidence_type: [direct_analogue, method_precedent]
unit_of_analysis: [settlement, grid_cell]
geographies: [Nigeria, Kenya]
tags: [undercount, gridded-population]
cited_in_manuscript: true
retrieved: 2026-09-15
evidence:
  - id: E1
    label: One-line statement of the finding
    kind: data              # verbatim | paraphrase | data | unlocated
    loc: "pp. 12-14"        # required unless kind is unlocated
    quote: |
      The finding, as text.
    sample_size: 118 settlements
    reference_kind: community_estimate
    origin: annotated-review
claims:
  - claim: informal-population-underrepresentation
    relationship: supports  # supports | qualifies | contradicts
                            # method_validates | context_only
    strength: high
    evidence: [E1]
    note: >-
      Why this source bears on the claim.
does_not_establish:
  - Mandatory. At least one entry, always.
---

The summary prose goes in the body, where Vale and proselint check it.
```

## The rules the validator enforces

The first two come from the annotated literature review's maintenance list.

A quantitative finding needs a page, section, figure, or table. A claim
link whose relationship is `supports`, `qualifies`, `contradicts`, or
`method_validates` must cite at least one located finding. Recording a
`follow_up` on the note turns that failure into a tracked warning, so debt is
visible rather than blocking.

"Does not establish" is mandatory. A note with an empty list fails.

The remaining rules keep the registry consistent:

- A `[@key]` in `paper/` or `docs/` resolves to a bib entry.
- A bib entry has a note, and a note has a bib entry.
- The frontmatter key matches the filename stem.
- A claim link must point to a file in `literature/claims/`.
- An `<!-- ev: key#E1 -->` anchor in prose resolves. Pandoc drops these
  comments from the PDF, so they annotate the source without printing.
- A URL cited in `docs/` belongs to a registered source, or to
  `literature/url-allowlist.txt`.
- A source the manuscript cites has `cited_in_manuscript: true`.
- An entry lacking both a note and a citation is reported. An entry with a
  note but no citation passes, because the project keeps sources it has read
  and not yet used.
- A `do-not-use` source is not cited in the manuscript.
- `literature/index.md` and `literature/evidence-matrix.csv` match a fresh
  regeneration.

## The backlog

`literature/pending.txt` lists bib entries that have no note yet. A key on
that list reports as a warning instead of an error, which is what lets the
registry land before all 151 notes exist.

The list cannot rot. The validator warns when a listed key already has a note,
and errors when a listed key has no bib entry. Once the file lists no keys,
the one-note-per-entry rule is strict again with no code change.

Every key on it is a real source. Sources reached through the audit notes
carry file, sheet, column, and page locators in `docs/`, so their notes will
be better located than the literature notes already written.

A `kind: unlocated` finding carries its text and refuses a locator. That keeps
the text while counting the finding as unlocated in `n_located` and in the
index, which is how second-hand records stay distinguishable from verified
ones.

## Deviations from the handoff spec

`barrios-visibles-annotated-literature-review.md` section X proposes a
structure. This implementation differs in two places, each to remove a second
copy of something.

The spec puts a bibliography at `literature/bibliography/references.bib`. This
project keeps the single file at `paper/references.bib`, because pandoc, the
`pixi` PDF tasks, and the manuscript's own YAML header already read it. The
spec's own follow-up list asks for one BibTeX export rather than two
bibliographies, so one file is the same goal.

The spec describes `evidence-matrix.csv` as a file to maintain. Here it is
generated from the notes, with the columns the spec lists. A hand-maintained
matrix drifts from the notes it summarises, which is the failure this registry
exists to prevent. Edit the notes and regenerate.

## Querying

```sql
-- claim links asserting more than context with no page locator
SELECT claim, key, relationship, strength
FROM 'outputs/source-claims.parquet'
WHERE NOT located AND relationship <> 'context_only'
ORDER BY claim, key;
```

```sql
-- how much of each claim rests on located evidence
SELECT claim, count(*) AS links,
       sum(located::INT) AS located
FROM 'outputs/source-claims.parquet'
GROUP BY claim ORDER BY 3.0/2;
```

## Provenance

The registry draws its content from two reviews, preserved rather than
rewritten.

`barrios-visibles-annotated-literature-review.md` supplies 28 international
sources with findings, limits, and verification labels. Its `origin:
annotated-review` records carry those findings verbatim.

`docs/argentina_census_accuracy_literature_review_final.docx` supplies the
census-accuracy argument and 19 cited sources. Its `origin: litreview-docx`
records carry those.

`origin: manuscript` and `origin: audit-notes` mark records taken from the
project's own writing. Those are second-hand until someone locates the passage
in the source itself.
