---
key: degrande2024
status: retained
lang: es
verification: verified_secondary
strength: high
source_type: peer_reviewed
method: independent_analysis
evidence_type: [mechanism_evidence]
unit_of_analysis: [resident, dwelling, census_area]
geographies: [Argentina]
tags: [duplication, census-2010, microdata, CEPAL]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Locate the record-sequence method and the 312,000 figure in the
  published article.
evidence:
  - id: E1
    label: "Conservative record-sequence analysis finds at least 312,000 people who appear to be replicas of others"
    kind: unlocated
    quote: |
      De Grande's conservative record-sequence analysis finds at least
      312,000 people who appear to be replicas of others in the released
      2010 microdata.
    reference_kind: census
    origin: litreview-docx
  - id: E2
    label: "INDEC's own later review reportedly identified roughly 400,000 unexplained replications"
    kind: unlocated
    quote: |
      INDEC's own later review reportedly identified roughly 400,000
      unexplained replications.
    reference_kind: census
    origin: litreview-docx
  - id: E3
    label: "Some census radios contained extraordinarily high shares of non-original records"
    kind: unlocated
    quote: |
      Some census radios contained extraordinarily high shares of
      non-original records.
    reference_kind: census
    origin: litreview-docx
claims:
  - claim: net-accuracy-differs-from-complete-enumeration
    relationship: supports
    strength: high
    evidence: [E1, E2]
    note: >-
      The Argentine instance of the offsetting problem. At least 312,000
      duplicated people inflate the total while leaving omissions in
      place, so the net figure understates both errors.
  - claim: reconciliation-does-not-repair-small-area-geography
    relationship: supports
    strength: high
    evidence: [E3]
    note: >-
      Radios with extraordinarily high shares of non-original records
      are wrong at the scale the project works at, and no national
      reconciliation touches them.
does_not_establish:
  - "It analyses 2010, not 2022, so it establishes the mechanism rather than a 2022 duplication rate."
  - "Record-sequence replication is an inference from data structure, not a confirmed enumeration error."
  - "The roughly 400,000 figure attributed to INDEC's own review is reported rather than published."
---

De Grande examines the released 2010 census microdata for duplicated
dwellings and finds at least 312,000 people who appear to be replicas of
other records. INDEC's own later review reportedly identified roughly
400,000 unexplained replications.

This is the Argentine case of offsetting error. Duplication inflates the
total while omissions remain, so a small net gap can sit on top of two
large errors pointing in opposite directions. Some radios contain
extraordinarily high shares of non-original records, which is damage at
the scale Barrios Visibles measures.
