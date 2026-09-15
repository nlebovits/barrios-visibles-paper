---
key: darin2022
status: retained
lang: en
verification: verified_secondary
strength: medium
source_type: peer_reviewed
method: demographic_reconciliation
evidence_type: [method_precedent]
unit_of_analysis: [census_area, grid_cell]
geographies: [Burkina Faso]
tags: [Burkina-Faso, census-reconstruction, satellite, Bayesian-model]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Verify the full author list and locate the hierarchical Bayesian
  method description on the page.
evidence:
  - id: E1
    label: "Burkina Faso’s 2019 census could not fully enumerate areas affected by insecurity."
    kind: unlocated
    quote: |
      Burkina Faso’s 2019 census could not fully enumerate areas affected by
      insecurity.
    origin: annotated-review
  - id: E2
    label: "Partial enumeration and satellite-derived settlement/building data were incorporated into hierarchical Bayesian estimation and 100 m population grids."
    kind: unlocated
    quote: |
      Partial enumeration and satellite-derived settlement/building data
      were incorporated into hierarchical Bayesian estimation and 100 m
      population grids.
    origin: annotated-review
claims:
  - claim: official-enumeration-omits-areas
    relationship: supports
    strength: medium
    evidence: [E1]
    note: >-
      Burkina Faso's 2019 census could not fully enumerate areas affected by
      insecurity.
  - claim: footprints-contain-population-information
    relationship: method_validates
    strength: medium
    evidence: [E2]
    note: >-
      Partial enumeration plus satellite-derived settlement and building
      data feeding hierarchical Bayesian estimation and 100 metre population
      grids.
does_not_establish:
  - "The omission mechanism was armed-conflict inaccessibility, not informal-urban enumeration."
  - "It does not validate one footprint per dwelling."
---

Darin and colleagues describe how satellite images were used to
complete Burkina Faso's 2019 census where insecurity prevented full
enumeration, combining partial enumeration with satellite-derived
settlement and building data in a hierarchical Bayesian model.

This is a method precedent rather than an undercount measurement. It
matters because a national statistical system treated building
evidence as an acceptable substitute where enumeration failed.
