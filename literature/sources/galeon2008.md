---
key: galeon2008
status: retained
lang: en
verification: verified_full_text
strength: medium
source_type: peer_reviewed
method: remote_sensing
evidence_type: [method_validation, mechanism_evidence]
unit_of_analysis: [building, roof, resident]
geographies: [Philippines]
tags: [field-validation, QuickBird, verticality, Philippines, structure-detection]
cited_in_manuscript: false
retrieved: 2026-09-15
evidence:
  - id: E1
    label: "QuickBird mapping achieved 95% identification accuracy against stratified field validation."
    kind: data
    loc: "Abstract; §§5.4 and 6.1–6.2"
    quote: |
      QuickBird mapping achieved 95% identification accuracy against
      stratified field validation.
    origin: annotated-review
  - id: E2
    label: "Researchers collected 160 building-level field samples covering roof area, resident count, settlement type, and whether structures were single- or multilevel."
    kind: data
    loc: "Abstract; §§5.4 and 6.1–6.2"
    quote: |
      Researchers collected 160 building-level field samples covering roof
      area, resident count, settlement type, and whether structures were
      single- or multilevel.
    origin: annotated-review
  - id: E3
    label: "Multilevel structures contained many residents despite small visible roof areas and substantially weakened the planar roof-area/population relationship."
    kind: paraphrase
    loc: "Abstract; §§5.4 and 6.1–6.2"
    quote: |
      Multilevel structures contained many residents despite small visible
      roof areas and substantially weakened the planar roof-area/population
      relationship.
    origin: annotated-review
  - id: E4
    label: "The authors excluded multilevel houses before fitting final equations."
    kind: paraphrase
    loc: "Abstract; §§5.4 and 6.1–6.2"
    quote: |
      The authors excluded multilevel houses before fitting final equations.
    origin: annotated-review
  - id: E5
    label: "In a small seven-building validation cluster, one model predicted 71 residents versus 70 observed."
    kind: data
    loc: "Abstract; §§5.4 and 6.1–6.2"
    quote: |
      In a small seven-building validation cluster, one model predicted 71
      residents versus 70 observed.
    origin: annotated-review
claims:
  - claim: footprints-contain-population-information
    relationship: supports
    strength: medium
    evidence: [E1, E2, E5]
    note: >-
      95 percent identification accuracy against stratified field
      validation, with 160 building-level field samples.
  - claim: planar-counts-conservative-when-vertical
    relationship: supports
    strength: high
    evidence: [E3, E4]
    note: >-
      Multilevel structures held many residents behind small roof areas, and
      the authors had to exclude them before fitting final equations.
does_not_establish:
  - "This is one Philippine setting with small validation samples."
  - "It models residents, not households."
  - "The prevalence of multilevel buildings should not be transferred to Argentina."
---

Galeon estimates population in informal settlement communities from
high-resolution satellite imagery in the Philippines, calibrated
against 160 building-level field samples covering roof area, resident
count, settlement type, and number of levels.

The exclusion step is the finding that matters here. Multilevel
structures broke the planar roof-area to population relationship badly
enough that the authors removed them from the model. A two-dimensional
footprint count is conservative wherever informal housing goes
vertical.
