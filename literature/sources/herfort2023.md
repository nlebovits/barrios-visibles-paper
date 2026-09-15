---
key: herfort2023
status: retained
lang: en
verification: verified_full_text
strength: high
source_type: peer_reviewed
method: remote_sensing
evidence_type: [caution]
unit_of_analysis: [building, grid_cell]
geographies: []
tags: [OSM, completeness, Latin-America, geographic-bias, priority-caveat]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Locate the completeness figures, particularly the Latin America and
  Caribbean mean, on the page.
evidence:
  - id: E1
    label: "Assesses 13,189 urban centers."
    kind: unlocated
    quote: |
      Assesses 13,189 urban centers.
    origin: annotated-review
  - id: E2
    label: "Only 1,848 exceeded 80% estimated building completeness."
    kind: unlocated
    quote: |
      Only 1,848 exceeded 80% estimated building completeness.
    origin: annotated-review
  - id: E3
    label: "9,163 urban centers—69% of the sample, containing 48% of the studied urban population—had less than 20% estimated completeness."
    kind: unlocated
    quote: |
      9,163 urban centers—69% of the sample, containing 48% of the studied
      urban population—had less than 20% estimated completeness.
    origin: annotated-review
  - id: E4
    label: "Mean estimated completeness for Latin America and the Caribbean was approximately 20%."
    kind: unlocated
    quote: |
      Mean estimated completeness for Latin America and the Caribbean was
      approximately 20%.
    origin: annotated-review
  - id: E5
    label: "Within cities, entire neighborhoods could be absent even where adjacent neighborhoods were relatively complete."
    kind: unlocated
    quote: |
      Within cities, entire neighborhoods could be absent even where
      adjacent neighborhoods were relatively complete.
    origin: annotated-review
claims:
  - claim: no-single-provider-complete
    relationship: supports
    strength: high
    evidence: [E1, E2, E3, E4, E5]
    note: >-
      69 percent of 13,189 urban centres fall below 20 percent estimated OSM
      building completeness. The Latin America and Caribbean mean is about
      20 percent, which bears directly on the Argentine case.
does_not_establish:
  - "Completeness is model-estimated rather than established through a worldwide field census."
  - "Microsoft-derived reference/training data can introduce bias."
  - "The paper does not examine household occupancy or census population."
---

Herfort and colleagues analyse completeness and inequality of global
urban building data in OpenStreetMap across 13,189 urban centres. Only
1,848 exceed 80 percent estimated completeness.

The Latin American figure is the one that matters for this project. A
regional mean near 20 percent means OSM cannot serve as a reference
for Argentine settlements, and it disqualifies any analysis that
treats OSM non-overlap as evidence of another provider's error.
