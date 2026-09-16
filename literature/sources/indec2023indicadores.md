---
key: indec2023indicadores
status: retained
lang: es
verification: verified_secondary
strength: high
source_type: primary_official
method: direct_enumeration
evidence_type: [direct_analogue, caution]
unit_of_analysis: [resident, national, jurisdiction]
geographies: [Argentina]
tags: [INDEC, census-2022, definitive, duplication, territorial-coverage, denominator-ambiguity]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Read p. 82 directly and record which denominator the 4.8 percent uses, if
  the publication resolves it at all. Until then neither 2.3 million nor 1.3
  million may be printed as the number of removed records.
evidence:
  - id: E1
    label: "Definitive 2022 total of 45,892,285"
    kind: unlocated
    quote: |
      The definitive total was 45,892,285.
    reference_kind: census
    origin: litreview-docx
  - id: E2
    label: "Duplicate removal of 4.8 percent of persons, stated against digital and paper records together"
    kind: verbatim
    loc: "p. 82; Aspectos metodológicos p. 16"
    quote: |
      respecto del total de registros considerados en conjunto entre digital y
      papel
    lang: es
    reference_kind: census
    origin: audit-notes
  - id: E3
    label: "The table title on the same page restricts the figure to people who completed the online form more than once"
    kind: paraphrase
    loc: "p. 82, table title"
    quote: |
      The table title says persons in private dwellings who completed the
      online form more than once, which contradicts the prose denominator of
      digital and paper records considered together.
    reference_kind: census
    origin: audit-notes
  - id: E4
    label: "The two readings imply 2.3 million or 1.3 million removed records"
    kind: data
    loc: "p. 82"
    quote: |
      2.3 million if the denominator is all records (45.9 million divided by
      0.952); 1.3 million if it is digital records only (about 25.4 million,
      from the 55.6 percent digital share in Análisis Demográfico 39 p. 9).
    reference_kind: census
    origin: audit-notes
  - id: E5
    label: "The provisional publication stated the equivalent rate as 3.6 percent of digital records only"
    kind: verbatim
    loc: "Resultados provisionales p. 63"
    quote: |
      del total de registros del Censo digital
    lang: es
    reference_kind: census
    origin: audit-notes
  - id: E6
    label: "Duplication is highest where the digital share was lowest, so the rate does not scale with digital take-up"
    kind: data
    loc: "Aspectos metodológicos Cuadro 2 p. 16"
    quote: |
      Duplication by province, percent of persons: CABA 3.5, Buenos Aires 4.4,
      Mendoza 4.5, Córdoba 4.8, Santa Fe 4.9, Misiones 5.1, Tucumán 6.2,
      Formosa 6.2, Salta 6.3, Corrientes 6.5, Chaco 6.6, Jujuy 6.6.
      Duplication is highest in the NOA and NEA provinces, where the digital
      share was about 35 percent, and lowest in CABA, where it was about 70
      percent.
    reference_kind: census
    origin: audit-notes
  - id: E7
    label: "Reported territorial coverage of 98.6 percent is the share of predefined segments, not of residents"
    kind: data
    loc: "Aspectos metodológicos Cuadro 3 p. 17"
    quote: |
      98.6% of segments covered on census day. Segment populations vary, so
      this is not the share of residents counted.
    reference_kind: census
    origin: audit-notes
  - id: E8
    label: "Provincial territorial coverage ran from 93.9 percent in San Juan to 97.4 percent in CABA"
    kind: data
    loc: "Aspectos metodológicos Cuadro 3 p. 17"
    quote: |
      San Juan 93.9%, Formosa 96.8%, Mendoza 96.8%, CABA 97.4%. The 1.4
      percent of uncovered segments are not located in any publication.
    reference_kind: census
    origin: audit-notes
claims:
  - claim: territorial-coverage-is-not-population-coverage
    relationship: supports
    strength: high
    evidence: [E7, E8]
    note: >-
      The primary source for the distinction. 98.6 percent counts segments
      completed and says nothing about residents enumerated, and the
      uncovered 1.4 percent is never located.
  - claim: net-accuracy-differs-from-complete-enumeration
    relationship: supports
    strength: high
    evidence: [E2, E3, E4, E5, E6]
    note: >-
      Duplicate removal at this rate is both a risk signal about raw
      duplication and evidence of quality control. Quote the rate, never a
      count. The publication gives two incompatible denominators on one page,
      so 4.8 percent resolves to either 2.3 million or 1.3 million records.
      The provincial pattern argues against the digital-only reading, because
      duplication runs highest where digital take-up was lowest.
does_not_establish:
  - "Territorial coverage cannot be read as the share of people counted, which is the misreading this note exists to prevent."
  - "It does not establish how many records the 4.8 percent represents. The prose denominator on p. 82 and the table title on the same page disagree, and INDEC publishes no reconciliation between them."
  - "Removing a duplicate does not place the surviving record at the right address, so the rate says nothing about whether deduplicated people ended up correctly assigned."
  - "It reports outputs of the census rather than an evaluation of them."
---

INDEC's demographic indicators publication for the 2022 census carries the
definitive total of 45,892,285 along with two figures that are routinely
misread.

Duplicate removal took out 4.8 percent of persons before the definitive count.
The denominator is not settled. The prose on p. 82 says digital and paper
records considered together, while the table title on the same page says
people who completed the online form more than once. That is 2.3 million
records on the first reading and 1.3 million on the second, and INDEC
reconciles the two nowhere.

The provincial breakdown argues against the digital-only reading. Duplication
runs highest in the NOA and NEA provinces, where digital take-up was around 35
percent, and lowest in CABA, where it was around 70 percent. The provisional
publication had stated the equivalent rate as 3.6 percent of digital records
only, so INDEC's own wording moved between releases.

Territorial coverage of 98.6 percent is the share of predefined segments
completed, which differs from the share of residents counted because segment
populations vary. San Juan reached 93.9 percent and CABA 97.4 percent, and the
uncovered 1.4 percent of segments is not located in any publication.
