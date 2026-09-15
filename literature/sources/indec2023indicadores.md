---
key: indec2023indicadores
status: retained
lang: es
verification: verified_secondary
strength: high
source_type: primary_official
method: direct_enumeration
evidence_type: [direct_analogue]
unit_of_analysis: [resident, national, jurisdiction]
geographies: [Argentina]
tags: [INDEC, census-2022, definitive, duplication, territorial-coverage]
cited_in_manuscript: false
retrieved: 2026-09-15
evidence:
  - id: E1
    label: "Definitive 2022 total of 45,892,285"
    kind: unlocated
    quote: |
      The definitive total was 45,892,285.
    reference_kind: census
    origin: litreview-docx
  - id: E2
    label: "Duplicate detection removed 4.8 percent of digital self-enumerated people before the definitive count"
    kind: data
    loc: "pp. 82-87"
    quote: |
      Duplicate detection removed 4.8% of digital self-enumerated people
      before the definitive count.
    reference_kind: census
    origin: litreview-docx
  - id: E3
    label: "Reported territorial coverage of 98.6 percent is the share of predefined segments, not of residents"
    kind: data
    loc: "table 2, pp. 80-81"
    quote: |
      The reported 98.6% territorial coverage is the share of predefined
      segments, not the share of residents counted. Segment populations
      vary.
    reference_kind: census
    origin: litreview-docx
  - id: E4
    label: "Provincial territorial coverage ranged from 93.9 percent in San Juan to 97.4 percent in CABA, with Formosa and Mendoza at 96.8 percent"
    kind: data
    loc: "table 2, pp. 80-81"
    quote: |
      San Juan's rate was 93.9%, CABA's 97.4%, and Formosa and Mendoza's
      96.8%.
    reference_kind: census
    origin: litreview-docx
claims:
  - claim: territorial-coverage-is-not-population-coverage
    relationship: supports
    strength: high
    evidence: [E3, E4]
    note: >-
      The primary source for the distinction. 98.6 percent counts
      segments completed and says nothing about residents enumerated.
  - claim: net-accuracy-differs-from-complete-enumeration
    relationship: supports
    strength: high
    evidence: [E2]
    note: >-
      Removing 4.8 percent of digital self-enumerated records as
      duplicates is both a risk signal about raw duplication and
      evidence of active quality control.
does_not_establish:
  - "Territorial coverage cannot be read as the share of people counted, which is the misreading this note exists to prevent."
  - "The duplicate removal rate applies to digital self-enumeration, not to the whole operation."
  - "It reports outputs of the census rather than an evaluation of them."
---

INDEC's demographic indicators publication for the 2022 census carries
the definitive total of 45,892,285 along with two figures that are
routinely misread.

Duplicate detection removed 4.8 percent of digital self-enumerated
people before the definitive count. That is a large raw duplication rate
and also evidence of quality control working.

Territorial coverage of 98.6 percent is the share of predefined segments
completed, which differs from the share of residents counted because
segment populations vary. San Juan reached 93.9 percent and CABA 97.4 percent.
