---
key: ibge2023censosummary
status: retained
lang: pt
verification: verified_secondary
strength: high
source_type: official_documentation
method: direct_enumeration
evidence_type: [direct_analogue]
unit_of_analysis: [resident]
geographies: [Brazil]
tags: [Brazil, imputation, census-2022, published-total]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Capture the IBGE passages stating 195.1 million directly enumerated
  residents and roughly 8 million imputed residents.
evidence:
  - id: E1
    label: "Published final census population of 203,080,756"
    kind: unlocated
    quote: |
      Published final Census population: 203,080,756.
    origin: audit-notes
  - id: E2
    label: "About 195.1 million people were directly enumerated"
    kind: unlocated
    quote: |
      Directly enumerated population: approximately 195.1 million.
    origin: audit-notes
  - id: E3
    label: "About 8.0 million of the published total came from imputation for occupied households without completed interviews"
    kind: unlocated
    quote: |
      Difference attributable to population imputation in occupied
      households without completed interviews: approximately 8.0
      million.
    origin: audit-notes
claims:
  - claim: imputation-is-not-enumeration
    relationship: supports
    strength: high
    evidence: [E1, E2, E3]
    note: >-
      The cleanest available demonstration. A published census total of
      203.1 million rests on 195.1 million people actually reached, with
      roughly 8 million assigned statistically.
  - claim: latin-american-omission-range-includes-six-percent
    relationship: qualifies
    strength: medium
    evidence: [E1, E2]
    note: >-
      Labelled by method: these are enumeration and imputation totals,
      not a measured omission rate. The omission figure comes from
      ibge2024ppe.
does_not_establish:
  - "It reports Brazilian totals and establishes nothing about Argentina."
  - "Imputation is not an error. It is a documented procedure, and the point is that it is not equivalent to reaching residents."
  - "The figures are recorded second-hand from the working notes rather than from the IBGE passages themselves."
---

IBGE's summary of the 2022 census gives the published population as
203,080,756. About 195.1 million of those people were directly
enumerated, and roughly 8.0 million were imputed for occupied households
where no interview was completed.

The split is the useful part. Imputation can only work on dwellings the
census system identified, so it cannot recover hidden subdivisions, rear
dwellings, upper-floor households, or buildings absent from the frame.
Those are the mechanisms the Argentine footprint analysis detects
indirectly.
